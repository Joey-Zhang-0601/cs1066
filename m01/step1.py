#!/usr/bin/env python3
"""Fetch AMD company facts from the SEC EDGAR API and save the JSON locally."""

import json
from pathlib import Path
from urllib.request import Request, urlopen


CIK = "0000002488"
URL = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json"
USER_AGENT = "cs1066-class@example.com"
OUTPUT_FILE = Path(__file__).with_name("amd_data.json")


def main():
    request = Request(URL, headers={"User-Agent": USER_AGENT})

    with urlopen(request, timeout=30) as response:
        data = json.load(response)

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:
        json.dump(data, output, indent=2)

    print(f"Saved SEC EDGAR company facts to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
