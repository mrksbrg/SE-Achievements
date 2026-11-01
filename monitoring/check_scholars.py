#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Swe-SE-SCI Scholar Monitoring Script
=====================================
Checks whether scholars in input_scholars.csv are still at their listed
affiliations, and scans institution staff pages for potential new scholars.

Two complementary checks are run:
  1. DBLP XML  – fetches each scholar's DBLP record and reads any
                  <note type="affiliation"> elements. A mismatch with the
                  listed affiliation is flagged for manual review.
  2. Staff page – fetches each institution's department page from
                  monitoring_institutions.csv and checks whether each
                  known scholar's name still appears on that page.
                  Names that are absent are flagged.

Scholars are prioritised by last_checked date (oldest / never-checked first)
so that running the script in small batches gradually covers everyone.

Outputs
-------
  monitoring_log.csv   – updated after every run; one row per scholar
  monitoring_report.txt – human-readable summary of flags and coverage

Usage
-----
  python check_scholars.py [--batch N] [--delay S] [--skip-dblp] [--skip-pages]

  --batch N    scholars to DBLP-check per run (default 20)
  --delay S    seconds between HTTP requests   (default 1.5)
  --skip-dblp  skip DBLP XML checks entirely
  --skip-pages skip institution staff-page checks entirely

Author: generated for mrksbrg/SE-Achievements
"""

import argparse
import csv
import os
import re
import time
import unicodedata
from datetime import date, datetime

import xml.etree.ElementTree as ET

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependencies. Run:  pip install requests beautifulsoup4")
    raise

# ---------------------------------------------------------------------------
# File paths (relative to the script's directory)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)   # one level up → project root

INPUT_SCHOLARS_CSV      = os.path.join(ROOT_DIR, "input_scholars.csv")
MONITORING_INSTITUTIONS = os.path.join(BASE_DIR, "monitoring_institutions.csv")
MONITORING_LOG_CSV      = os.path.join(BASE_DIR, "monitoring_log.csv")
REPORT_FILE             = os.path.join(BASE_DIR, "monitoring_report.txt")

LOG_FIELDS = ["pid", "name", "affiliation", "last_checked",
              "dblp_status", "page_status", "profile_url", "notes"]


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def load_scholars(csv_file: str) -> dict:
    """Return dict keyed by DBLP PID with scholar metadata."""
    scholars = {}
    with open(csv_file, newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) < 4:
                continue
            affiliation, name, disambig, url = row[0], row[1], row[2], row[3]
            try:
                pid = url.split("pid/")[1].split(".xml")[0]
            except IndexError:
                print(f"  [WARN] Could not parse PID from URL for {name} – skipping")
                continue
            scholars[pid] = {
                "name":        name,
                "affiliation": affiliation,
                "disambig":    disambig,
                "dblp_url":    url,
                "pid":         pid,
            }
    return scholars


def load_log(log_file: str) -> dict:
    """Return existing monitoring log keyed by PID, or empty dict."""
    log = {}
    if not os.path.exists(log_file):
        return log
    with open(log_file, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            log[row["pid"]] = dict(row)
    return log


def save_log(log: dict, log_file: str) -> None:
    """Write monitoring log to CSV."""
    with open(log_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        writer.writeheader()
        for entry in log.values():
            writer.writerow({k: entry.get(k, "") for k in LOG_FIELDS})


def load_institutions(inst_file: str) -> list:
    """Return list of institution dicts from monitoring_institutions.csv."""
    institutions = []
    if not os.path.exists(inst_file):
        print(f"  [WARN] {inst_file} not found – skipping institution page checks")
        return institutions
    with open(inst_file, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("url"):
                institutions.append(row)
    return institutions


# ---------------------------------------------------------------------------
# Prioritisation
# ---------------------------------------------------------------------------

def prioritize_scholars(scholars: dict, log: dict) -> list:
    """
    Return PID list ordered by last_checked ascending.
    Never-checked scholars sort first (date.min).
    """
    def sort_key(pid):
        entry = log.get(pid)
        if not entry or not entry.get("last_checked"):
            return date.min          # never checked → highest priority
        if entry.get("dblp_status") == "error":
            return date.min          # previous error → retry first
        try:
            return datetime.strptime(entry["last_checked"], "%Y-%m-%d").date()
        except ValueError:
            return date.min

    return sorted(scholars.keys(), key=sort_key)


# ---------------------------------------------------------------------------
# DBLP check
# ---------------------------------------------------------------------------

def check_dblp(scholar: dict, session: requests.Session) -> dict:
    """
    Fetch the scholar's DBLP XML and extract <note type="affiliation"> elements.

    Returns dict:
      found        bool   – whether the URL was reachable
      affiliations list   – affiliation strings found in DBLP
      dblp_status  str    – 'ok' | 'mismatch' | 'no_affiliation' | 'error'
      notes        str    – human-readable detail
    """
    result = {"found": False, "affiliations": [], "dblp_status": "error", "notes": ""}
    try:
        # Retry up to 3 times with backoff on 503 / timeout
        for attempt in range(3):
            try:
                resp = session.get(scholar["dblp_url"], timeout=15)
                if resp.status_code == 503:
                    wait = 10 * (attempt + 1)
                    print(f"(503 – waiting {wait}s) ", end="", flush=True)
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                break
            except requests.Timeout:
                if attempt < 2:
                    print(f"(timeout – retrying) ", end="", flush=True)
                    time.sleep(5)
                else:
                    raise
        else:
            result["notes"] = "DBLP returned 503 after 3 attempts – try again later"
            return result
        result["found"] = True

        root = ET.fromstring(resp.content)
        aff_notes = root.iter("note")
        affiliations = [
            n.text.strip() for n in aff_notes
            if n.get("type") == "affiliation" and n.text and n.text.strip()
        ]
        result["affiliations"] = affiliations

        if not affiliations:
            result["dblp_status"] = "no_affiliation"
            result["notes"] = "No affiliation recorded in DBLP"
            return result

        # Loose match: check if the listed affiliation overlaps with any DBLP entry
        listed = scholar["affiliation"].lower()
        matched = any(
            _affiliation_overlap(listed, a.lower()) for a in affiliations
        )
        if matched:
            result["dblp_status"] = "ok"
            result["notes"] = f"DBLP: {'; '.join(affiliations)}"
        else:
            result["dblp_status"] = "mismatch"
            result["notes"] = (
                f"Listed: {scholar['affiliation']} | "
                f"DBLP: {'; '.join(affiliations)}"
            )

    except requests.RequestException as exc:
        result["notes"] = f"Request error: {exc}"

    return result


def _affiliation_overlap(listed: str, dblp: str) -> bool:
    """
    Return True if there is meaningful word overlap between the listed
    affiliation string and a DBLP affiliation string.
    Uses the longest word in the listed name as the key signal
    (e.g. 'chalmers', 'blekinge', 'mälardalen').
    """
    # Strip accents for robust comparison
    listed_norm = _strip_accents(listed)
    dblp_norm   = _strip_accents(dblp)

    listed_words = set(re.findall(r"[a-z]{4,}", listed_norm))
    dblp_words   = set(re.findall(r"[a-z]{4,}", dblp_norm))
    return bool(listed_words & dblp_words)


def _strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


# ---------------------------------------------------------------------------
# Institution staff-page check
# ---------------------------------------------------------------------------

def check_institution_page(institution: dict,
                            scholars_here: list,
                            session: requests.Session) -> dict:
    """
    Fetch the institution staff page and check which scholars appear on it.

    Returns dict:
      status          str         – 'ok' | 'error'
      error           str         – error message if status=='error'
      missing         list[str]   – scholars NOT found on the page
      confirmed       list[str]   – scholars confirmed on the page
      page_text_len   int         – length of page text (sanity check)
    """
    result = {
        "status": "error", "error": "",
        "missing": [], "confirmed": [], "page_text_len": 0
    }
    url = institution["url"]

    try:
        resp = session.get(url, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as exc:
        result["error"] = str(exc)
        return result

    soup = BeautifulSoup(resp.text, "html.parser")
    page_text = _strip_accents(soup.get_text(" ", strip=True).lower())
    result["page_text_len"] = len(page_text)
    result["status"] = "ok"

    for scholar in scholars_here:
        if _name_on_page(scholar["name"], page_text):
            result["confirmed"].append(scholar["name"])
        else:
            result["missing"].append(scholar["name"])

    return result


def _name_on_page(name: str, page_text: str) -> bool:
    """
    Return True if both the first and last name tokens appear in the page text.
    Falls back to last-name-only match if the name has only one part.
    Accent-normalised comparison.
    """
    parts = _strip_accents(name.lower()).split()
    if len(parts) == 0:
        return False
    if len(parts) == 1:
        return parts[0] in page_text

    first = parts[0]
    last  = parts[-1]

    # Both first and last present anywhere on page
    if first in page_text and last in page_text:
        return True

    # Last name alone is a strong signal on small department pages
    # (reduce false negatives for people with uncommon surnames)
    if len(last) >= 6 and last in page_text:
        return True

    return False


# ---------------------------------------------------------------------------
# Individual profile page check
# ---------------------------------------------------------------------------

def check_profile_page(scholar: dict, session: requests.Session) -> dict:
    """
    Fetch a scholar's individual staff profile page and check whether
    their listed affiliation still appears on it.

    Returns dict:
      status          str  – 'confirmed' | 'mismatch' | 'error'
      notes           str  – human-readable detail
      page_text_len   int  – sanity-check length of fetched page text
    """
    url = scholar.get("profile_url", "").strip()
    result = {"status": "error", "notes": "", "page_text_len": 0}

    if not url:
        result["notes"] = "No profile URL set"
        return result

    try:
        resp = session.get(url, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as exc:
        result["notes"] = f"Request error: {exc}"
        return result

    soup = BeautifulSoup(resp.text, "html.parser")
    page_text = _strip_accents(soup.get_text(" ", strip=True).lower())
    result["page_text_len"] = len(page_text)

    if _affiliation_overlap(scholar["affiliation"].lower(), page_text):
        result["status"] = "confirmed"
        result["notes"]  = f"Affiliation found on profile page ({url})"
    else:
        result["status"] = "mismatch"
        result["notes"]  = (
            f"Listed affiliation '{scholar['affiliation']}' NOT found "
            f"on profile page ({url}) — possible move or page layout issue"
        )

    return result


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(today: str,
                    dblp_flags: list,
                    page_flags: dict,
                    page_errors: dict,
                    page_confirmed: dict,
                    log: dict,
                    output_file: str) -> str:
    """Write and return a human-readable monitoring report."""
    lines = [
        f"Swe-SE-SCI Monitoring Report  –  {today}",
        "=" * 60,
        "",
    ]

    # ── DBLP flags ────────────────────────────────────────────────
    lines.append("## 1. DBLP affiliation mismatches")
    if dblp_flags:
        for f in dblp_flags:
            lines.append(f"  🚩 {f['name']}  ({f['affiliation']})")
            lines.append(f"     {f['notes']}")
    else:
        lines.append("  None detected in this batch.")
    lines.append("")

    # ── Staff-page flags ──────────────────────────────────────────
    lines.append("## 2. Scholars not found on institution staff pages")
    any_missing = False
    for inst_name, missing in page_flags.items():
        if missing:
            any_missing = True
            confirmed = page_confirmed.get(inst_name, [])
            lines.append(f"\n  {inst_name}  "
                         f"(confirmed {len(confirmed)}, missing {len(missing)}):")
            for name in missing:
                lines.append(f"    🚩 {name}")
    if not any_missing:
        lines.append("  All checked scholars found on their pages.")
    lines.append("")

    # ── Page fetch errors ─────────────────────────────────────────
    if page_errors:
        lines.append("## 3. Institution pages that could not be fetched")
        for inst_name, errs in page_errors.items():
            for group, err in errs:
                lines.append(f"  ⚠️  {inst_name} [{group}]: {err}")
        lines.append("")

    # ── Coverage summary ──────────────────────────────────────────
    checked_today = [e for e in log.values() if e.get("last_checked") == today]
    total = len(log)
    never = sum(1 for e in log.values() if not e.get("last_checked"))
    lines.append("## 4. Coverage")
    lines.append(f"  Checked today : {len(checked_today)}")
    lines.append(f"  Total in log  : {total}")
    lines.append(f"  Never checked : {never}")
    lines.append("")
    lines.append("Run the script again to check the next batch.")

    report = "\n".join(lines)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    return report


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Swe-SE-SCI scholar monitor")
    parser.add_argument("--batch",      type=int,   default=20,
                        help="Number of scholars to DBLP-check per run (default 20)")
    parser.add_argument("--delay",      type=float, default=3.0,
                        help="Seconds between HTTP requests (default 3.0)")
    parser.add_argument("--skip-dblp",  action="store_true",
                        help="Skip DBLP XML checks")
    parser.add_argument("--skip-pages", action="store_true",
                        help="Skip institution staff-page checks")
    args = parser.parse_args()

    today = date.today().isoformat()
    print(f"\n=== Swe-SE-SCI Scholar Monitor  –  {today} ===\n")

    # Load data
    scholars     = load_scholars(INPUT_SCHOLARS_CSV)
    log          = load_log(MONITORING_LOG_CSV)
    institutions = load_institutions(MONITORING_INSTITUTIONS)
    print(f"Scholars in roster : {len(scholars)}")
    print(f"Entries in log     : {len(log)}")
    print(f"Institutions       : {len(institutions)}")

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Swe-SE-SCI-monitor/1.0 (academic research; github.com/mrksbrg)"
    })

    dblp_flags = []

    # ── DBLP checks ───────────────────────────────────────────────
    if not args.skip_dblp:
        ordered = prioritize_scholars(scholars, log)
        batch   = ordered[:args.batch]
        print(f"\n[DBLP] Checking batch of {len(batch)} scholars "
              f"(oldest-checked first) …")

        for pid in batch:
            scholar = scholars[pid]
            print(f"  {scholar['name']} … ", end="", flush=True)

            result = check_dblp(scholar, session)

            # Initialise or update log entry
            entry = log.get(pid, {
                "pid":        pid,
                "name":       scholar["name"],
                "affiliation": scholar["affiliation"],
                "page_status": "",
            })
            entry["last_checked"] = today
            entry["dblp_status"]  = result["dblp_status"]
            entry["notes"]        = result["notes"]
            log[pid] = entry

            status_icon = {"ok": "✅", "mismatch": "🚩",
                           "no_affiliation": "–", "error": "⚠️"
                           }.get(result["dblp_status"], "?")
            print(status_icon)

            if result["dblp_status"] == "mismatch":
                dblp_flags.append({
                    "name":        scholar["name"],
                    "affiliation": scholar["affiliation"],
                    "notes":       result["notes"],
                })

            time.sleep(args.delay)
    else:
        print("\n[DBLP] Skipped (--skip-dblp)")

    # ── Institution page checks ───────────────────────────────────
    # Multiple pages can exist per institution (one per research group).
    # A scholar is confirmed if found on ANY page; only flagged missing
    # if absent from ALL pages for their institution.

    page_flags     = {}   # inst_name → list of missing scholar names
    page_confirmed = {}   # inst_name → list of confirmed names
    page_errors    = {}   # inst_name → list of (group, error) tuples

    if not args.skip_pages:
        # Group pages by institution name
        from collections import defaultdict
        pages_by_inst = defaultdict(list)
        for inst in institutions:
            inst_name = inst.get("institution", "Unknown")
            pages_by_inst[inst_name].append(inst)

        print(f"\n[Pages] Checking pages for {len(pages_by_inst)} institutions "
              f"({len(institutions)} URLs total) …")

        for inst_name, pages in pages_by_inst.items():
            scholars_here = [s for s in scholars.values()
                             if s["affiliation"] == inst_name]
            if not scholars_here:
                print(f"  {inst_name}: no scholars listed – skipping")
                continue

            print(f"  {inst_name} ({len(scholars_here)} scholars, "
                  f"{len(pages)} page(s)):")

            # Accumulate which scholars are confirmed across all pages
            confirmed_names = set()
            inst_errors = []

            for page in pages:
                group = page.get("group", page.get("url", ""))
                print(f"    [{group}] … ", end="", flush=True)
                result = check_institution_page(page, scholars_here, session)

                if result["status"] == "error":
                    print(f"⚠️  {result['error']}")
                    inst_errors.append((group, result["error"]))
                else:
                    newly_confirmed = set(result["confirmed"])
                    confirmed_names |= newly_confirmed
                    print(f"found {len(newly_confirmed)} scholar(s)  "
                          f"(page: {result['page_text_len']} chars)")
                time.sleep(args.delay)

            if inst_errors:
                page_errors[inst_name] = inst_errors

            # Only missing if absent from every page (and at least one page worked)
            pages_ok = len(inst_errors) < len(pages)
            if pages_ok:
                missing = [s["name"] for s in scholars_here
                           if s["name"] not in confirmed_names]
                confirmed = list(confirmed_names)
                page_flags[inst_name]     = missing
                page_confirmed[inst_name] = confirmed

                # Update log
                for scholar in scholars_here:
                    pid = scholar["pid"]
                    if pid not in log:
                        log[pid] = {k: "" for k in LOG_FIELDS}
                        log[pid]["pid"]         = pid
                        log[pid]["name"]        = scholar["name"]
                        log[pid]["affiliation"] = scholar["affiliation"]
                    log[pid]["page_status"] = (
                        "confirmed" if scholar["name"] in confirmed_names
                        else "missing"
                    )

                flag_str = f"🚩 {len(missing)} missing" if missing else "✅ all found"
                print(f"    → {flag_str} across all pages")
            else:
                print(f"    → ⚠️  all pages failed, skipping log update")

    else:
        print("\n[Pages] Skipped (--skip-pages)")

    # ── Individual profile page checks ───────────────────────────
    # Runs for any scholar who has a profile_url in the log,
    # regardless of whether institution page checks were skipped.
    scholars_with_profile = [
        s for s in scholars.values()
        if log.get(s["pid"], {}).get("profile_url", "").strip()
    ]
    if scholars_with_profile:
        print(f"\n[Profiles] Checking {len(scholars_with_profile)} "
              f"individual profile page(s) …")
        profile_flags = []
        for scholar in scholars_with_profile:
            pid = scholar["pid"]
            scholar_with_url = {**scholar,
                                "profile_url": log[pid]["profile_url"]}
            print(f"  {scholar['name']} … ", end="", flush=True)
            result = check_profile_page(scholar_with_url, session)

            icon = {"confirmed": "✅", "mismatch": "🚩", "error": "⚠️"
                    }.get(result["status"], "?")
            print(icon)

            log[pid]["page_status"] = result["status"]
            log[pid]["notes"]       = result["notes"]

            if result["status"] == "mismatch":
                profile_flags.append({
                    "name":        scholar["name"],
                    "affiliation": scholar["affiliation"],
                    "notes":       result["notes"],
                })
            time.sleep(args.delay)

        # Merge profile flags into page_flags for reporting
        if profile_flags:
            page_flags.setdefault("(profile pages)", [])
            for f in profile_flags:
                page_flags["(profile pages)"].append(f["name"])
                page_confirmed.setdefault("(profile pages)", [])

    # ── Save & report ─────────────────────────────────────────────
    save_log(log, MONITORING_LOG_CSV)
    report = generate_report(today, dblp_flags, page_flags, page_errors,
                             page_confirmed, log, REPORT_FILE)

    print("\n" + "─" * 60)
    print(report)
    print("─" * 60)
    print(f"\nLog    → {MONITORING_LOG_CSV}")
    print(f"Report → {REPORT_FILE}\n")


if __name__ == "__main__":
    main()
