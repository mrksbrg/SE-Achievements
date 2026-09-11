# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 2026

@author: Markus Borg

Reads scholar data from a local DBLP XML dump instead of the DBLP web API, which is behind a bot check.
Monthly snapshots (dblp-YYYY-MM-DD.xml.gz) and the DTD they reference are published on Dagstuhl DROPS:
https://drops.dagstuhl.de/entities/collection/10.4230/dblp.xml -- run download_dblp_dump.py to fetch them.
"""

import glob
import gzip
import os
import pyexpat
from xml.sax.xmlreader import AttributesImpl

DEFAULT_DUMP_DIR = "dblp_dump"
HOMEPAGE_PREFIX = "homepages/"
PERSON_TAGS = ("author", "editor")
CHUNK_SIZE = 1024 * 1024

# Buffered SAX events
START, CHARS, END = 0, 1, 2


def default_dump_path():
    """ Return $DBLP_DUMP if set, otherwise the most recent dump in dblp_dump/. """
    env_path = os.environ.get("DBLP_DUMP")
    if env_path:
        return env_path
    dumps = sorted(glob.glob(os.path.join(DEFAULT_DUMP_DIR, "dblp-*.xml.gz")))
    if not dumps:
        raise FileNotFoundError("No DBLP dump found in " + DEFAULT_DUMP_DIR + "/. Run: python download_dblp_dump.py")
    return dumps[-1]


def replay_person(handler, pid, names, records):
    """ Feed a person's records to a SAX ContentHandler, shaped like DBLP's per-person XML (dblpperson). """
    handler.startElement("dblpperson", AttributesImpl({"name": names[0], "pid": pid, "n": str(len(records))}))
    coauthors = {}
    # The per-person XML lists the newest records first
    for events, persons in sorted(records, key=lambda record: _record_year(record[0]), reverse=True):
        for event in events:
            if event[0] == START:
                handler.startElement(event[1], AttributesImpl(event[2]))
            elif event[0] == CHARS:
                handler.characters(event[1])
            else:
                handler.endElement(event[1])
        for person in persons:
            if person not in names:
                coauthors[person] = True
    for coauthor in coauthors:
        handler.startElement("na", AttributesImpl({}))
        handler.characters(coauthor)
        handler.endElement("na")
    handler.endElement("dblpperson")


def _record_year(events):
    for i, event in enumerate(events[:-1]):
        if event[0] == START and event[1] == "year" and events[i + 1][0] == CHARS:
            return events[i + 1][1]
    return ""


class _HomepageHandler:
    """ Collects the name variants of the requested pids from their Home Page (www) records. """

    def __init__(self, pids):
        self.pid_by_key = {HOMEPAGE_PREFIX + pid: pid for pid in pids}
        self.names_by_pid = {}
        # Merged profiles keep their old key with a crossref to the new one
        self.redirects = {}
        self.current_pid = None
        self.current_text = None

    def start(self, tag, attrs):
        if tag == "www":
            self.current_pid = self.pid_by_key.get(attrs.get("key"))
        elif tag in ("author", "crossref") and self.current_pid is not None:
            self.current_text = []

    def characters(self, data):
        if self.current_text is not None:
            self.current_text.append(data)

    def end(self, tag):
        if tag in ("author", "crossref") and self.current_text is not None:
            text = "".join(self.current_text)
            if tag == "author":
                self.names_by_pid.setdefault(self.current_pid, []).append(text)
            elif text.startswith(HOMEPAGE_PREFIX):
                self.redirects[self.current_pid] = text[len(HOMEPAGE_PREFIX):]
            self.current_text = None
        elif tag == "www":
            self.current_pid = None


class _RecordHandler:
    """ Buffers the events of each record and keeps the records authored or edited by the requested persons. """

    def __init__(self, names_by_pid):
        self.pids_by_name = {}
        for pid, names in names_by_pid.items():
            for name in names:
                self.pids_by_name.setdefault(name, []).append(pid)
        self.records_by_pid = {}
        self.depth = 0
        self.events = None
        self.persons = None
        self.current_text = None

    def start(self, tag, attrs):
        self.depth += 1
        if self.depth == 2:  # a record directly below <dblp>
            self.events = []
            self.persons = []
        if self.depth >= 2:
            self.events.append((START, tag, attrs))
            if tag in PERSON_TAGS:
                self.current_text = []

    def characters(self, data):
        if self.depth >= 2:
            self.events.append((CHARS, data))
            if self.current_text is not None:
                self.current_text.append(data)

    def end(self, tag):
        if self.depth >= 2:
            self.events.append((END, tag))
            if tag in PERSON_TAGS and self.current_text is not None:
                self.persons.append("".join(self.current_text))
                self.current_text = None
            # Home Page records describe persons, they are not publications
            if self.depth == 2 and tag != "www":
                self.keep_record()
        self.depth -= 1

    def keep_record(self):
        pids = dict.fromkeys(pid for person in self.persons for pid in self.pids_by_name.get(person, ()))
        for pid in pids:
            self.records_by_pid.setdefault(pid, []).append((self.events, self.persons))


class DblpDump:

    def __init__(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError("DBLP dump not found: " + path + ". Run: python download_dblp_dump.py")
        self.path = path

    def find_person_names(self, pids, progress=None):
        """ Return {pid: [name, alias, ...]} for the pids that have a Home Page record, following merged profiles. """
        handler = _HomepageHandler(pids)
        self.parse(handler, progress)
        names_by_pid = handler.names_by_pid
        if handler.redirects:
            print("Merged DBLP profiles (update input_scholars.csv to skip an extra pass): " +
                  ", ".join(pid + " -> " + target for pid, target in handler.redirects.items()))
            targets = [target for target in handler.redirects.values() if target not in names_by_pid]
            if targets:
                names_by_pid.update(self.find_person_names(targets, progress))
            for pid, target in handler.redirects.items():
                if target in names_by_pid:
                    names_by_pid[pid] = names_by_pid[target]
        return {pid: names_by_pid[pid] for pid in pids if pid in names_by_pid}

    def collect_person_records(self, names_by_pid, progress=None):
        """ Return {pid: [(events, persons), ...]} with all records by each person. """
        handler = _RecordHandler(names_by_pid)
        self.parse(handler, progress)
        return handler.records_by_pid

    def parse(self, handler, progress=None):
        parser = pyexpat.ParserCreate()
        parser.buffer_text = True
        # dblp.xml uses named entities (e.g., &ouml;) declared in its external DTD
        parser.SetParamEntityParsing(pyexpat.XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE)
        parser.ExternalEntityRefHandler = lambda context, base, system_id, public_id: \
            self.parse_dtd(parser, context, system_id)
        parser.StartElementHandler = handler.start
        parser.EndElementHandler = handler.end
        parser.CharacterDataHandler = handler.characters

        total = os.path.getsize(self.path)
        last_percent = -1
        with open(self.path, "rb") as raw:
            stream = gzip.GzipFile(fileobj=raw) if self.path.endswith(".gz") else raw
            chunk = stream.read(CHUNK_SIZE)
            while chunk:
                parser.Parse(chunk, False)
                percent = 100 * raw.tell() // total
                if progress and percent != last_percent:
                    progress(percent, 100)
                    last_percent = percent
                chunk = stream.read(CHUNK_SIZE)
            parser.Parse(b"", True)

    def parse_dtd(self, parser, context, system_id):
        dtd_path = os.path.join(os.path.dirname(os.path.abspath(self.path)), system_id)
        if not os.path.isfile(dtd_path):
            raise FileNotFoundError("The DBLP dump needs its DTD next to it: " + dtd_path +
                                    ". Run: python download_dblp_dump.py")
        with open(dtd_path, "rb") as f:
            parser.ExternalEntityParserCreate(context).ParseFile(f)
        return 1
