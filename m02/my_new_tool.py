"""Enhanced tool: scrape, plot, and produce a short AI explanation when a clear leader exists.

Behavior:
- Prompts for a search term.
- Scrapes interest-by-region data (uses `trends_scraper`).
- Plots and saves a PNG (same naming scheme as `my_tool.py`).
- If the top region's interest is > 1.5 * second region's interest, produce a short
  explanation paragraph (<=500 words) and save it to `<safe_query>_explanation.md`.
- The explanation is requested from OpenAI if `OPENAI_API_KEY` is set and the
  `openai` package is available; otherwise a clear fallback paragraph is written.
"""
from urllib.parse import quote_plus
import re
import os
import textwrap
import pandas as pd
import matplotlib.pyplot as plt

from trends_scraper import get_driver, scrape_interest_data


def parse_interest(value_text):
    if value_text is None:
        return 0.0
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


def generate_explanation_openai(query, top_region, top_val, second_region, second_val):
    try:
        import openai
    except Exception:
        return None

    key = os.environ.get('OPENAI_API_KEY')
    if not key:
        return None

    openai.api_key = key
    prompt = (
        f"Write a concise (<=500 words) explanatory paragraph for why the region '{top_region}' "
        f"might show significantly higher Google Trends interest ({top_val:.1f}) for the search term "
        f"'{query}' compared with the next region '{second_region}' ({second_val:.1f}). "
        "Be factual, avoid invented specifics, suggest plausible high-level reasons (local events, "
        "cultural relevance, media coverage) and keep the tone neutral and short."
    )

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini" if hasattr(openai, 'ChatCompletion') else "gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
        )
        # ChatCompletion responses may vary in shape; extract text defensively
        text = None
        if isinstance(resp, dict):
            choices = resp.get('choices') or []
            if choices:
                text = choices[0].get('message', {}).get('content') or choices[0].get('text')
        if not text:
            text = str(resp)
        return textwrap.shorten(text.strip(), width=4000, placeholder='')
    except Exception:
        return None


def generate_fallback(query, top_region, top_val, second_region, second_val, ratio):
    lines = []
    lines.append(f"Search term: {query}")
    lines.append("")
    lines.append(
        f"The region '{top_region}' shows markedly higher interest ({top_val:.1f}) compared to "
        f"the next region '{second_region}' ({second_val:.1f}), a ratio of {ratio:.2f}x."
    )
    lines.append("")
    lines.append(
        "Possible explanations include local events or news that temporarily boosted interest, "
        "stronger regional relevance or language/cultural affinity for the topic, or localized "
        "promotion and media coverage. To confirm the true cause, check local news sources, "
        "social media, or official announcements for the dates reflected in the Trends data."
    )
    return "\n\n".join(lines)


def write_md(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


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

    rows = []
    for region, raw in interest_data.items():
        num = parse_interest(raw)
        rows.append((region, num))

    df = pd.DataFrame(rows, columns=['Region', 'Interest'])
    df = df.sort_values(by='Interest', ascending=False)

    safe = re.sub(r"[^0-9A-Za-z_-]", "_", query).strip('_')[:60]
    plot_file = f"interest_{safe or 'query'}.png"
    make_plot(df, plot_file)
    print(f"Saved plot to {plot_file}")

    # Decide significant leader
    if len(df) >= 2:
        top_region = df.iloc[0]['Region']
        top_val = float(df.iloc[0]['Interest'])
        second_region = df.iloc[1]['Region']
        second_val = float(df.iloc[1]['Interest'])
        ratio = (top_val / second_val) if second_val != 0 else float('inf')
    else:
        top_region = df.iloc[0]['Region']
        top_val = float(df.iloc[0]['Interest'])
        second_region = ''
        second_val = 0.0
        ratio = float('inf')

    md_name = f"{safe or 'query'}_explanation.md"

    if ratio > 1.5 and second_region:
        print(f"Significant leader detected: {top_region} ({ratio:.2f}x)")
        # Try OpenAI first
        explanation = generate_explanation_openai(query, top_region, top_val, second_region, second_val)
        if not explanation:
            explanation = generate_fallback(query, top_region, top_val, second_region, second_val, ratio)
        # Ensure not too long (<=500 words)
        words = explanation.split()
        if len(words) > 500:
            explanation = ' '.join(words[:500])
        header = f"# Explanation for '{query}' — top region: {top_region}\n\n"
        write_md(md_name, header + explanation)
        print(f"Wrote explanation to {md_name}")
    else:
        print("No significant leader detected.")
        content = f"Search term: {query}\n\nNo outstanding result detected: no region exceeds 1.5x the second place in interest."
        write_md(md_name, content)
        print(f"Wrote report to {md_name}")


if __name__ == '__main__':
    main()
