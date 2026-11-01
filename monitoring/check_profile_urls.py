#!/usr/bin/env python3
"""
check_profile_urls.py
---------------------
Reads monitoring/monitoring_log.csv and HTTP-checks every profile_url.
Prints a summary of broken (non-200) URLs so you can fix or remove them.

Usage:
    python check_profile_urls.py

Requirements:
    pip install requests
"""

import csv
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Missing dependency: run  pip install requests")

CSV_PATH = Path(__file__).parent / "monitoring_log.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

TIMEOUT = 10      # seconds per request
DELAY   = 0.3     # seconds between requests (be polite)


def check_url(url: str) -> tuple:
    """Return (status_code, error_message). status_code is None on exception."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT,
                         allow_redirects=True)
        return r.status_code, ""
    except requests.exceptions.ConnectionError as e:
        return None, f"ConnectionError: {e}"
    except requests.exceptions.Timeout:
        return None, "Timeout"
    except Exception as e:
        return None, str(e)


def main():
    if not CSV_PATH.exists():
        sys.exit(f"CSV not found: {CSV_PATH}")

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    to_check = [(r["name"], r["affiliation"], r["profile_url"])
                for r in rows if r.get("profile_url", "").strip()]

    print(f"Checking {len(to_check)} profile URLs …\n")

    broken = []
    ok_count = 0

    for i, (name, affiliation, url) in enumerate(to_check, 1):
        status, err = check_url(url)
        label = f"[{i:>3}/{len(to_check)}]"

        if status == 200:
            print(f"{label} OK       {url}")
            ok_count += 1
        else:
            reason = err if err else f"HTTP {status}"
            print(f"{label} BROKEN   {url}  ({reason})")
            broken.append((name, affiliation, url, reason))

        time.sleep(DELAY)

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print(f"Results: {ok_count} OK  |  {len(broken)} broken\n")

    if broken:
        print("BROKEN URLs:")
        print(f"{'Name':<35} {'Affiliation':<30} Reason")
        print("-" * 100)
        for name, aff, url, reason in broken:
            print(f"{name:<35} {aff:<30} {reason}")
            print(f"  {url}")
        print()
        print("To clear broken URLs from the CSV, run:")
        print("  python check_profile_urls.py --fix")
    else:
        print("All URLs are healthy!")

    # ── Optional --fix mode ──────────────────────────────────────────────────
    if "--fix" in sys.argv and broken:
        broken_urls = {url for _, _, url, _ in broken}
        fixed = 0
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows_out = list(reader)

        for r in rows_out:
            if r.get("profile_url", "").strip() in broken_urls:
                r["profile_url"] = ""
                fixed += 1

        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows_out)

        print(f"\n--fix: cleared {fixed} broken URL(s) from {CSV_PATH.name}")


if __name__ == "__main__":
    main()
