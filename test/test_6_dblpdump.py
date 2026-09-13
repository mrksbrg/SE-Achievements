# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 2026

@author: Markus Borg
"""

import gzip
import urllib.error
from datetime import date
import pytest
from xml.sax.handler import ContentHandler
from swesesci import dblp_dump
from swesesci.dblp_dump import DblpDump, DROPS_URL, ensure_latest_dump, replay_person

DTD_NAME = "dblp-2023-06-28.dtd"
DTD = '<!ENTITY ouml "&#246;">\n'
DUMP = '''<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE dblp SYSTEM "dblp-2023-06-28.dtd">
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


def write_dump(path):
    with gzip.open(path, "wb") as f:
        f.write(DUMP.encode("iso-8859-1"))


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
    (tmp_path / DTD_NAME).write_text(DTD)
    write_dump(tmp_path / "dblp.xml.gz")
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
        (tmp_path / DTD_NAME).unlink()
        with pytest.raises(FileNotFoundError):
            dump.find_person_names(["1/2"])

    def test_missing_dump(self, tmp_path):
        # TC6: A clear error when the dump does not exist
        with pytest.raises(FileNotFoundError):
            DblpDump(str(tmp_path / "missing.xml.gz"))


class TestClass_DumpDownload:

    @pytest.fixture(autouse=True)
    def no_env_override(self, monkeypatch):
        monkeypatch.delenv("DBLP_DUMP", raising=False)

    def test_existing_dump_needs_no_download(self, tmp_path, monkeypatch):
        # TC7: This month's dump and its DTD are already there, so nothing is downloaded
        def unexpected_download(url, path):
            raise AssertionError("Unexpected download: " + url)
        monkeypatch.setattr(dblp_dump, "download_verified", unexpected_download)
        write_dump(tmp_path / "dblp-2026-09-01.xml.gz")
        (tmp_path / DTD_NAME).write_text(DTD)
        assert ensure_latest_dump(str(tmp_path), date(2026, 9, 11)) == str(tmp_path / "dblp-2026-09-01.xml.gz")

    def test_previous_month_before_release(self, tmp_path, monkeypatch):
        # TC8: This month's snapshot is not published yet, so last month's is downloaded and older dumps removed
        urls = []

        def fake_download(url, path):
            urls.append(url)
            if "2026-09-01" in url:
                raise urllib.error.HTTPError(url, 404, "Not Found", None, None)
            if url.endswith(".dtd"):
                (tmp_path / DTD_NAME).write_text(DTD)
            else:
                write_dump(path)
        monkeypatch.setattr(dblp_dump, "download_verified", fake_download)
        write_dump(tmp_path / "dblp-2026-07-01.xml.gz")

        path = ensure_latest_dump(str(tmp_path), date(2026, 9, 1))
        assert path == str(tmp_path / "dblp-2026-08-01.xml.gz")
        assert urls == [DROPS_URL + "2026/dblp-2026-09-01.xml.gz", DROPS_URL + "2026/dblp-2026-08-01.xml.gz",
                        DROPS_URL + "2023/" + DTD_NAME]
        assert not (tmp_path / "dblp-2026-07-01.xml.gz").exists()
        assert DblpDump(path).find_person_names(["1/2"]) == {"1/2": NAMES}

    def test_offline_uses_local_dump(self, tmp_path, monkeypatch):
        # TC9: Without network access, the most recent local dump is used
        def offline(url, path):
            raise urllib.error.URLError("offline")
        monkeypatch.setattr(dblp_dump, "download_verified", offline)
        write_dump(tmp_path / "dblp-2026-07-01.xml.gz")
        assert ensure_latest_dump(str(tmp_path), date(2026, 9, 11)) == str(tmp_path / "dblp-2026-07-01.xml.gz")
