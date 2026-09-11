# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 2026

@author: Markus Borg
"""

import gzip
import pytest
from xml.sax.handler import ContentHandler
from swesesci.dblp_dump import DblpDump, replay_person

DTD = '<!ENTITY ouml "&#246;">\n'
DUMP = '''<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE dblp SYSTEM "test.dtd">
<dblp>
<article key="a1"><author>Bjorn Test</author><author>Ada Other</author><title>Old.</title><year>2001</year></article>
<www key="homepages/3/4"><crossref>homepages/1/2</crossref></www>
<www key="homepages/1/2"><author>Bj&ouml;rn Test</author><author>Bjorn Test</author><title>Home Page</title></www>
<inproceedings key="i1"><author>Ada Other</author><author>Bj&ouml;rn Test</author><title>New.</title><year>2020</year></inproceedings>
<proceedings key="p1"><editor>Bj&ouml;rn Test</editor><title>Proc.</title><year>2010</year></proceedings>
<article key="a2"><author>Ada Other</author><title>Unrelated.</title><year>2015</year></article>
</dblp>
'''
NAMES = ["Björn Test", "Bjorn Test"]


class Recorder(ContentHandler):

    def __init__(self):
        super().__init__()
        self.starts = []
        self.person = None
        self.text = ""

    def startElement(self, tag, attributes):
        self.starts.append(tag)
        if tag == "dblpperson":
            self.person = dict(attributes)

    def characters(self, content):
        self.text += content


@pytest.fixture
def dump(tmp_path):
    (tmp_path / "test.dtd").write_text(DTD)
    with gzip.open(tmp_path / "dblp.xml.gz", "wb") as f:
        f.write(DUMP.encode("iso-8859-1"))
    return DblpDump(str(tmp_path / "dblp.xml.gz"))


class TestClass_DblpDump:

    def test_name_variants_with_entities(self, dump):
        # TC1: Name variants come from the Home Page record, with entities resolved via the DTD
        assert dump.find_person_names(["1/2", "9/9"]) == {"1/2": NAMES}

    def test_merged_profile(self, dump):
        # TC2: An old pid of a merged profile resolves to the names of the profile it points to
        assert dump.find_person_names(["3/4"]) == {"3/4": NAMES}

    def test_records_by_any_name_variant(self, dump):
        # TC3: Records authored or edited under any name variant, but not the Home Page record
        records = dump.collect_person_records({"1/2": NAMES, "3/4": NAMES})
        assert [events[0][2]["key"] for events, persons in records["1/2"]] == ["a1", "i1", "p1"]
        assert records["3/4"] == records["1/2"]

    def test_replay_as_dblpperson(self, dump):
        # TC4: Replay yields the per-person XML shape: entry count, newest records first, co-authors
        recorder = Recorder()
        replay_person(recorder, "1/2", NAMES, dump.collect_person_records({"1/2": NAMES})["1/2"])
        assert recorder.person == {"name": "Björn Test", "pid": "1/2", "n": "3"}
        assert [tag for tag in recorder.starts if tag in ("article", "inproceedings", "proceedings")] == \
               ["inproceedings", "proceedings", "article"]
        assert recorder.starts.count("na") == 1
        assert recorder.text.endswith("Ada Other")

    def test_missing_dtd(self, dump, tmp_path):
        # TC5: A clear error when the DTD is not next to the dump
        (tmp_path / "test.dtd").unlink()
        with pytest.raises(FileNotFoundError):
            dump.find_person_names(["1/2"])

    def test_missing_dump(self, tmp_path):
        # TC6: A clear error when the dump does not exist
        with pytest.raises(FileNotFoundError):
            DblpDump(str(tmp_path / "missing.xml.gz"))
