# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 2026

@author: Markus Borg

Reads scholar data from a local DBLP XML dump instead of the DBLP web API, which is behind a bot check.
The newest monthly snapshot (dblp-YYYY-MM-01.xml.gz) and the DTD it references are downloaded from Dagstuhl DROPS:
https://drops.dagstuhl.de/entities/collection/10.4230/dblp.xml
"""

import glob
import gzip
import hashlib
import os
import pyexpat
import re
import urllib.error
import urllib.request
from datetime import date, timedelta
from xml.sax.xmlreader import AttributesImpl

DEFAULT_DUMP_DIR = "dblp_dump"
DROPS_URL = "https://drops.dagstuhl.de/storage/artifacts/dblp/xml/"
USER_AGENT = "SWE-SE-SCI/1.0 (+https://github.com/mrksbrg/SE-Achievements)"
HOMEPAGE_PREFIX = "homepages/"
PERSON_TAGS = ("author", "editor")
CHUNK_SIZE = 1024 * 1024

# Buffered SAX events
START, CHARS, END = 0, 1, 2


def ensure_latest_dump(dump_dir=DEFAULT_DUMP_DIR, today=None):
    """ Return the newest monthly DBLP dump, downloading it (and removing older ones) unless it is already there. """
    if os.environ.get("DBLP_DUMP"):
        return os.environ["DBLP_DUMP"]
    first_of_month = (today or date.today()).replace(day=1)
    previous_month = (first_of_month - timedelta(days=1)).replace(day=1)
    for month in (first_of_month, previous_month):
        name = "dblp-" + month.isoformat() + ".xml.gz"
        path = os.path.join(dump_dir, name)
        try:
            if not os.path.isfile(path):
                os.makedirs(dump_dir, exist_ok=True)
                download_verified(DROPS_URL + str(month.year) + "/" + name, path)
                remove_other_dumps(dump_dir, name)
            ensure_dtd(path)
            return path
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue  # snapshots are published a few days into the month
            print("Could not download " + name + ": " + str(e))
            break
        except urllib.error.URLError as e:
            print("Could not download " + name + ": " + str(e))
            break
    print("Falling back to the most recent local DBLP dump")
    return default_dump_path(dump_dir)


def default_dump_path(dump_dir=DEFAULT_DUMP_DIR):
    """ Return $DBLP_DUMP if set, otherwise the most recent dump in dump_dir. """
    env_path = os.environ.get("DBLP_DUMP")
    if env_path:
        return env_path
    dumps = sorted(glob.glob(os.path.join(dump_dir, "dblp-*.xml.gz")))
    if not dumps:
        raise FileNotFoundError("No DBLP dump found in " + dump_dir + "/")
    return dumps[-1]


def download_verified(url, path):
    """ Download url to path, verified against the published .md5 file. """
    with _fetch(url + ".md5") as response:
        expected_md5 = response.read().decode().split()[0]
    tmp_path = path + ".part"
    with _fetch(url) as response, open(tmp_path, "wb") as f:
        total = int(response.headers.get("Content-Length", 0))
        done = 0
        for block in iter(lambda: response.read(CHUNK_SIZE), b""):
            f.write(block)
            done += len(block)
            if total:
                print("\rDownloading " + url + ": " + str(100 * done // total) + "%", end="")
    print()
    if _md5_of(tmp_path) != expected_md5:
        os.remove(tmp_path)
        raise RuntimeError("MD5 mismatch for " + url)
    os.replace(tmp_path, path)


def ensure_dtd(dump_path):
    """ Download the DTD named in the dump's DOCTYPE (e.g., dblp-2023-06-28.dtd) unless it is next to the dump. """
    with gzip.open(dump_path, "rt", encoding="iso-8859-1") as f:
        doctype = re.search(r'SYSTEM "(dblp-(\d{4})-\d{2}-\d{2}\.dtd)"', f.read(1000))
    if doctype:
        dtd_path = os.path.join(os.path.dirname(dump_path), doctype.group(1))
        if not os.path.isfile(dtd_path):
            download_verified(DROPS_URL + doctype.group(2) + "/" + doctype.group(1), dtd_path)


def remove_other_dumps(dump_dir, keep_name):
    for path in glob.glob(os.path.join(dump_dir, "dblp-*.xml.gz*")):
        if os.path.basename(path) != keep_name:
            os.remove(path)
            print("Removed old DBLP dump file: " + path)


def _fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(request, timeout=60)


def _md5_of(path):
    digest = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(CHUNK_SIZE), b""):
            digest.update(block)
    return digest.hexdigest()


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
            raise FileNotFoundError("DBLP dump not found: " + path)
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
            raise FileNotFoundError("The DBLP dump needs its DTD next to it: " + dtd_path)
        with open(dtd_path, "rb") as f:
            parser.ExternalEntityParserCreate(context).ParseFile(f)
        return 1
