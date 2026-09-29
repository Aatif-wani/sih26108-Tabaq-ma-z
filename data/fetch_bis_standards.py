"""
Look up Indian Standards on the official BIS Standards Portal (standards.bis.gov.in)
and print the current (non-withdrawn) edition's number, title and official URL.

Used to collect Batch 2 (File 08). Only factual metadata is fetched; write
scope/keywords yourself in your own words (see File 03 copyright note).

Usage:
    pip install requests
    python fetch_bis_standards.py "IS 383" "IS 1489 (Part 1)" > found.csv
"""

import csv
import re
import sys
import urllib.parse

import requests

API = "https://standardsadmin.bis.gov.in/review-service/searchKnowStandards"
HEADERS = {"User-Agent": "Mozilla/5.0", "Origin": "https://standards.bis.gov.in",
           "Referer": "https://standards.bis.gov.in/"}


def base_number(s):
    """'IS 1489 (Part 1)  : 2015' -> 'is1489(part1)'"""
    return re.sub(r"\s+", "", s).lower().split(":")[0]


def current_edition(is_number):
    rows = requests.post(API, json={"searchText": is_number}, headers=HEADERS,
                         timeout=60).json().get("data") or []
    current = [r for r in rows
               if base_number(r["standardNumber"]) == base_number(is_number)
               and r.get("withdrawStatus") == 0]
    if not current:
        return None
    # Several editions can be current during a transition; keep the newest.
    return max(current, key=lambda r: r["standardNumber"].split(":")[-1])


def main():
    out = csv.writer(sys.stdout)
    out.writerow(["query", "standard_id", "title", "year", "official_url"])
    for q in sys.argv[1:]:
        r = current_edition(q)
        if r is None:
            print(f"# not found / withdrawn: {q}", file=sys.stderr)
            continue
        std = re.sub(r"\s*:\s*", ":", r["standardNumber"].strip())
        url = ("https://standards.bis.gov.in/website/standard-details?encryptedId="
               + r["standardEncId"] + "&standardNumber=" + urllib.parse.quote(std, safe=":()/"))
        out.writerow([q, std, re.sub(r"\s+", " ", r["standardName"]).strip(), std[-4:], url])


if __name__ == "__main__":
    main()
