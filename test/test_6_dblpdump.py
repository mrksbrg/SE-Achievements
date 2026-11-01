# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 2026

@author: Markus Borg
"""

import gzip
import io
import urllib.error
from datetime import date
import pytest
from xml.sax.handler import ContentHandler
from swesesci import dblp_dump
from swesesci.dblp_dump import DblpDump, DROPS_URL, StaleDumpError, ensure_latest_dump, replay_person

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
        monkeypatch.delenv("DBLP_ALLOW_STALE_DUMP", raising=False)

    @staticmethod
    def published(monkeypatch, snapshot):
        monkeypatch.setattr(dblp_dump, "latest_published_snapshot", lambda: snapshot)

    @staticmethod
    def offline(monkeypatch):
        def no_network(*args):
            raise urllib.error.URLError("offline")
        monkeypatch.setattr(dblp_dump, "latest_published_snapshot", no_network)
        monkeypatch.setattr(dblp_dump, "download_verified", no_network)

    def test_existing_dump_needs_no_download(self, tmp_path, monkeypatch):
        # TC7: This month's dump and its DTD are already there, so nothing is downloaded
        def unexpected_download(url, path):
            raise AssertionError("Unexpected download: " + url)
        monkeypatch.setattr(dblp_dump, "download_verified", unexpected_download)
        self.published(monkeypatch, date(2026, 9, 1))
        write_dump(tmp_path / "dblp-2026-09-01.xml.gz")
        (tmp_path / DTD_NAME).write_text(DTD)
        assert ensure_latest_dump(str(tmp_path), date(2026, 9, 11)) == str(tmp_path / "dblp-2026-09-01.xml.gz")

    def test_snapshot_published_after_the_first(self, tmp_path, monkeypatch):
        # TC8: The snapshot named on the collection page is downloaded, whatever its day, and older dumps removed
        urls = []

        def fake_download(url, path):
            urls.append(url)
            if url.endswith(".dtd"):
                (tmp_path / DTD_NAME).write_text(DTD)
            else:
                write_dump(path)
        monkeypatch.setattr(dblp_dump, "download_verified", fake_download)
        self.published(monkeypatch, date(2026, 10, 3))
        write_dump(tmp_path / "dblp-2026-09-01.xml.gz")

        path = ensure_latest_dump(str(tmp_path), date(2026, 10, 5))
        assert path == str(tmp_path / "dblp-2026-10-03.xml.gz")
        assert urls == [DROPS_URL + "2026/dblp-2026-10-03.xml.gz", DROPS_URL + "2023/" + DTD_NAME]
        assert not (tmp_path / "dblp-2026-09-01.xml.gz").exists()
        assert DblpDump(path).find_person_names(["1/2"]) == {"1/2": NAMES}

    def test_stops_before_this_months_release(self, tmp_path, monkeypatch):
        # TC9: On the first of the month the newest snapshot is last month's, so nothing is downloaded or mined
        def unexpected_download(url, path):
            raise AssertionError("Unexpected download: " + url)
        monkeypatch.setattr(dblp_dump, "download_verified", unexpected_download)
        self.published(monkeypatch, date(2026, 10, 3))
        with pytest.raises(StaleDumpError, match="2026-10-03"):
            ensure_latest_dump(str(tmp_path), date(2026, 11, 1))

    def test_stale_dump_on_request(self, tmp_path, monkeypatch):
        # TC10: With DBLP_ALLOW_STALE_DUMP set, last month's snapshot is mined anyway
        monkeypatch.setenv("DBLP_ALLOW_STALE_DUMP", "1")
        self.published(monkeypatch, date(2026, 10, 3))
        write_dump(tmp_path / "dblp-2026-10-03.xml.gz")
        (tmp_path / DTD_NAME).write_text(DTD)
        assert ensure_latest_dump(str(tmp_path), date(2026, 11, 1)) == str(tmp_path / "dblp-2026-10-03.xml.gz")

    def test_offline_uses_current_local_dump(self, tmp_path, monkeypatch):
        # TC11: Without network access, a local dump from this month is used
        self.offline(monkeypatch)
        write_dump(tmp_path / "dblp-2026-09-01.xml.gz")
        assert ensure_latest_dump(str(tmp_path), date(2026, 9, 11)) == str(tmp_path / "dblp-2026-09-01.xml.gz")

    def test_offline_stops_on_old_local_dump(self, tmp_path, monkeypatch):
        # TC12: Without network access, a local dump from an earlier month is not mined
        self.offline(monkeypatch)
        write_dump(tmp_path / "dblp-2026-09-01.xml.gz")
        with pytest.raises(StaleDumpError, match="2026-09-01"):
            ensure_latest_dump(str(tmp_path), date(2026, 11, 1))

    def test_newest_snapshot_on_collection_page(self, monkeypatch):
        # TC13: The newest snapshot is read off the collection page, also when it is not from the first
        page = (b'<a href="https://doi.org/10.4230/dblp.xml.2026-08-01">x</a>'
                b'<a href="https://doi.org/10.4230/dblp.xml.2026-10-03">x</a>'
                b'<a href="https://doi.org/10.4230/dblp.xml.2026-09-01">x</a>')
        monkeypatch.setattr(dblp_dump, "_fetch", lambda url: io.BytesIO(page))
        assert dblp_dump.latest_published_snapshot() == date(2026, 10, 3)
