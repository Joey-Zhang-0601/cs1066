from trends_scraper import get_driver, scrape_interest_data
import csv


def build_url(query):
    """Build the Google Trends URL for a query and US geography."""
    date_range = "now%207-d"
    geo = "US"
    site = "https://trends.google.com/trends/explore"
    return f"{site}?date={date_range}&geo={geo}&q={query}&hl=en"


def main():
    query = "vibe coding"
    url = build_url(query)

    driver = get_driver()
    if driver is None:
        print("Unable to initialize Chrome driver.")
        return

    try:
        interest_data = scrape_interest_data(driver, url)
    finally:
        driver.quit()

    if not interest_data:
        print("No interest data retrieved.")
        return

    with open("scraped_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["region", "interest"])

        for region, interest in interest_data.items():
            writer.writerow([region, interest])

    print(f"Saved {len(interest_data)} rows to scraped_data.csv")


if __name__ == "__main__":
    main()
