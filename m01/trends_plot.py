import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_scraped_data(csv_path):
    """Load the scraped Google Trends data from scraped_data.csv."""
    regions = []
    interests = []

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            regions.append(row["region"])
            interests.append(int(row["interest"]))

    return regions, interests


def main():
    regions, interests = load_scraped_data("scraped_data.csv")

    plt.figure(figsize=(12, 8))
    plt.bar(regions, interests, color="steelblue")
    plt.title("Interest in 'vibe coding' by Region")
    plt.xlabel("Region")
    plt.ylabel("Interest")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("interest_trends.png")
    plt.close()

    print("Saved bar chart to interest_trends.png")


if __name__ == "__main__":
    main()
