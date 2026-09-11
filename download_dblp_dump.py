# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 2026

@author: Markus Borg

Downloads a monthly DBLP XML dump snapshot and the DTD it references from Dagstuhl DROPS
(https://drops.dagstuhl.de/entities/collection/10.4230/dblp.xml) into dblp_dump/.

Usage: python download_dblp_dump.py [YYYY-MM]   (defaults to the current month)
"""

import gzip
import hashlib
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date

DROPS_URL = "https://drops.dagstuhl.de/storage/artifacts/dblp/xml/"
DUMP_DIR = "dblp_dump"
USER_AGENT = "SWE-SE-SCI/1.0 (+https://github.com/mrksbrg/SE-Achievements)"
BLOCK_SIZE = 1024 * 1024


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(request, timeout=60)


def md5_of(path):
    digest = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(BLOCK_SIZE), b""):
            digest.update(block)
    return digest.hexdigest()


def download_verified(url, path):
    """ Download url to path, verified against the published .md5, unless it is already there. """
    with fetch(url + ".md5") as response:
        expected_md5 = response.read().decode().split()[0]
    if os.path.isfile(path) and md5_of(path) == expected_md5:
        print("Already downloaded: " + path)
        return
    print("Downloading " + url)
    tmp_path = path + ".part"
    with fetch(url) as response, open(tmp_path, "wb") as f:
        for block in iter(lambda: response.read(BLOCK_SIZE), b""):
            f.write(block)
    if md5_of(tmp_path) != expected_md5:
        os.remove(tmp_path)
        raise RuntimeError("MD5 mismatch for " + url)
    os.replace(tmp_path, path)
    print("Saved " + path)


def main():
    month = sys.argv[1] if len(sys.argv) > 1 else date.today().strftime("%Y-%m")
    if not re.fullmatch(r"\d{4}-\d{2}", month):
        sys.exit("Usage: python download_dblp_dump.py [YYYY-MM]")
    os.makedirs(DUMP_DIR, exist_ok=True)

    dump_name = "dblp-" + month + "-01.xml.gz"
    dump_path = os.path.join(DUMP_DIR, dump_name)
    try:
        download_verified(DROPS_URL + month[:4] + "/" + dump_name, dump_path)
    except urllib.error.HTTPError as e:
        sys.exit("Could not download " + dump_name + " (HTTP " + str(e.code) + "). "
                 "Snapshots appear early each month; try the previous month.")

    # The dump's DOCTYPE names the DTD it needs, e.g., dblp-2023-06-28.dtd
    with gzip.open(dump_path, "rt", encoding="iso-8859-1") as f:
        doctype = re.search(r'SYSTEM "(dblp-(\d{4})-\d{2}-\d{2}\.dtd)"', f.read(1000))
    if doctype is None:
        sys.exit("Could not find the DTD reference in " + dump_path)
    dtd_name, dtd_year = doctype.group(1), doctype.group(2)
    download_verified(DROPS_URL + dtd_year + "/" + dtd_name, os.path.join(DUMP_DIR, dtd_name))


if __name__ == "__main__":
    main()
