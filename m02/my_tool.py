"""Combine scraping and plotting in-memory for CS1066 PSet1.

This script prompts for a search term, scrapes Google Trends via
`trends_scraper.scrape_interest_data`, builds a pandas DataFrame in memory,
and writes a plot PNG. It does NOT save or read a CSV file.
"""
from urllib.parse import quote_plus
import re
import pandas as pd
import matplotlib.pyplot as plt

from trends_scraper import get_driver, scrape_interest_data


def parse_interest(value_text):
    """Convert a scraped interest string to a float.

    Examples of accepted inputs: '23', '23%', '23.5', 'n/a'.
    If parsing fails return 0.0
    """
    if value_text is None:
        return 0.0
    # Find first numeric substring
    m = re.search(r"[0-9]+(?:\.[0-9]+)?", str(value_text))
    if not m:
        return 0.0
    try:
        return float(m.group(0))
    except Exception:
        return 0.0


def make_plot(df, output_file):
    plt.figure(figsize=(12, 6))
    plt.bar(df['Region'], df['Interest'], color='skyblue')
    plt.xlabel('Region')
    plt.ylabel('Interest')
    plt.title('Google Trends Interest by Region')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


def main():
    date_range = "now%207-d"
    geo = "US"

    query = input("Enter a term or a phrase to search (e.g. 'vibe coding'): ").strip()
    if not query:
        query = "vibe coding"

    encoded = quote_plus(query)
    site = "https://trends.google.com/trends/explore"
    url = f"{site}?date={date_range}&geo={geo}&q={encoded}&hl=en"

    print(f"Scraping trends for: {query}")
    driver = get_driver()
    if driver is None:
        print("Error: could not initialize web driver. Aborting.")
        return

    interest_data = scrape_interest_data(driver, url)
    driver.quit()

    if not interest_data:
        print("No interest data retrieved.")
        return

    # Convert to DataFrame and normalize numeric values
    rows = []
    for region, raw in interest_data.items():
        num = parse_interest(raw)
        rows.append((region, num))

    df = pd.DataFrame(rows, columns=['Region', 'Interest'])

    # Sort descending by interest for a nicer plot
    df = df.sort_values(by='Interest', ascending=False)

    # Sanitize filename
    safe = re.sub(r"[^0-9A-Za-z_-]", "_", query).strip('_')[:60]
    output_file = f"interest_{safe or 'query'}.png"

    make_plot(df, output_file)
    print(f"Saved plot to {output_file}")


if __name__ == '__main__':
    main()
