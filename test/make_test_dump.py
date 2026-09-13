# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 2026

@author: Markus Borg

Creates test/dblp_test_dump.xml.gz, a small subset of a DBLP XML dump with the scholars used in the tests.

Usage: python test/make_test_dump.py dblp_dump/dblp-YYYY-MM-DD.xml.gz
"""

import csv
import gzip
import os
import sys
from xml.sax.saxutils import escape, quoteattr

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from swesesci.dblp_dump import DblpDump, START, CHARS
from swesesci.scholar_reader import string_splitter

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_CSVS = ["test_2_onescholar.csv", "test_3_twoscholars.csv", "test_4_nonasciititles.csv", "test_5_runningnumber.csv"]
OUTPUT_PATH = os.path.join(TEST_DIR, "dblp_test_dump.xml.gz")


def test_pids():
    pids = []
    for name in TEST_CSVS:
        with open(os.path.join(TEST_DIR, name), newline="", encoding="utf-8") as f:
            pids += [string_splitter(row)[3] for row in csv.reader(f)]
    return pids


def events_to_xml(events):
    xml = []
    for event in events:
        if event[0] == START:
            attributes = "".join(" " + name + "=" + quoteattr(value) for name, value in event[2].items())
            xml.append("<" + event[1] + attributes + ">")
        elif event[0] == CHARS:
            xml.append(escape(event[1]))
        else:
            xml.append("</" + event[1] + ">")
    return "".join(xml)


def write_test_dump(names_by_pid, records_by_pid, path=OUTPUT_PATH):
    # Entities are already resolved, so the subset is plain UTF-8 without a DTD
    xml = ['<?xml version="1.0" encoding="UTF-8"?>\n<dblp>\n']
    for pid, names in names_by_pid.items():
        authors = "".join("<author>" + escape(name) + "</author>" for name in names)
        xml.append("<www key=" + quoteattr("homepages/" + pid) + ">" + authors + "<title>Home Page</title></www>\n")
    written_keys = set()
    for records in records_by_pid.values():
        for events, persons in records:
            key = events[0][2].get("key")
            if key not in written_keys:  # co-authored records are shared between scholars
                written_keys.add(key)
                xml.append(events_to_xml(events) + "\n")
    xml.append("</dblp>\n")
    with open(path, "wb") as f, gzip.GzipFile(filename="", mode="wb", fileobj=f, mtime=0) as gz:
        gz.write("".join(xml).encode("utf-8"))
    print("Wrote " + path + " with " + str(len(written_keys)) + " records")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python test/make_test_dump.py dblp_dump/dblp-YYYY-MM-DD.xml.gz")
    dump = DblpDump(sys.argv[1])
    names = dump.find_person_names(test_pids())
    write_test_dump(names, dump.collect_person_records(names))
