import json
from difflib import get_close_matches
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import requests


HOST = "localhost"
PORT = 8000
EDGAR_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
EDGAR_COMPANIES_URL = "https://www.sec.gov/files/company_tickers.json"
EDGAR_HEADERS = {"User-Agent": "UniversityStudent your.email@university.edu"}


HTML = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Ten-Year Financial Lens</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
    <style>
        :root { --ink: #183642; --muted: #5d7479; --paper: #f7f4ed; --accent: #d45d3e; --line: #d9ded5; }
        * { box-sizing: border-box; }
        body { margin: 0; color: var(--ink); background: linear-gradient(135deg, #dbe8e1, var(--paper) 45%, #f0d5bd); font-family: Georgia, "Times New Roman", serif; }
        main { width: min(1100px, 100%); margin: 0 auto; padding: 3rem 1.25rem 4rem; }
        header { display: flex; justify-content: space-between; gap: 2rem; align-items: end; margin-bottom: 2rem; }
        .kicker { margin: 0 0 .6rem; color: var(--accent); font: 700 .75rem/1.2 system-ui, sans-serif; letter-spacing: .14em; text-transform: uppercase; }
        h1 { margin: 0; max-width: 620px; font-size: clamp(2.5rem, 7vw, 5.5rem); line-height: .92; }
        header p { max-width: 270px; margin: 0; color: var(--muted); font: 1rem/1.5 system-ui, sans-serif; }
        form { display: flex; flex-wrap: wrap; gap: .7rem; align-items: end; padding: 1rem 0; }
        .search-row { border-bottom: 1px solid var(--line); }
        label { display: grid; gap: .35rem; color: var(--muted); font: 700 .78rem system-ui, sans-serif; letter-spacing: .05em; text-transform: uppercase; }
        input, button { min-height: 2.8rem; padding: .65rem .85rem; border: 1px solid var(--line); font: 1rem system-ui, sans-serif; }
        input { width: 220px; color: var(--ink); background: #fffdf8; }
        button { color: #fffdf8; background: var(--accent); border-color: var(--accent); cursor: pointer; font-weight: 700; }
        button:hover { background: #b84730; }
        button:focus-visible, input:focus-visible { outline: 3px solid #183642; outline-offset: 3px; }
        #status { min-height: 1.6rem; margin: 1rem 0; color: var(--muted); font: .95rem system-ui, sans-serif; }
        #status.error { color: #a5342c; }
        .identity { display: flex; justify-content: space-between; gap: 1rem; align-items: baseline; margin: 1.5rem 0 .8rem; }
        h2 { margin: 0; font-size: clamp(1.5rem, 3vw, 2.4rem); }
        .identity span { color: var(--muted); font: .9rem system-ui, sans-serif; }
        .charts { display: grid; gap: 1rem; }
        .chart-panel { min-height: 270px; padding: 1rem; background: #fffdf8cc; border: 1px solid var(--line); }
        .chart-panel h3 { margin: 0 0 .5rem; font: 700 .95rem system-ui, sans-serif; letter-spacing: .04em; text-transform: uppercase; }
        .chart-wrap { position: relative; height: 230px; }
        @media (max-width: 650px) { header { display: block; } header p { margin-top: 1rem; } .identity { display: block; } .identity span { display: block; margin-top: .35rem; } }
    </style>
</head>
<body>
<main>
    <header>
        <div><p class="kicker">EDGAR / annual filings</p><h1>Ten-Year Financial Lens</h1></div>
        <p>Enter a CIK to trace a company’s revenue, net income, and assets across its latest ten fiscal years.</p>
    </header>
    <form id="company-form" class="search-row">
        <label for="company-query">Company name <input id="company-query" name="company" placeholder="e.g. Apple" required></label>
        <button type="submit">Find company</button>
    </form>
    <div id="company-match" hidden></div>
    <form id="lookup-form">
        <label for="cik">Company CIK <input id="cik" name="cik" inputmode="numeric" pattern="[0-9]{1,10}" placeholder="e.g. 320193" required></label>
        <button type="submit">Load financials</button>
    </form>
    <div id="status" role="status" aria-live="polite"></div>
    <section id="results" hidden>
        <div class="identity"><h2 id="company-name"></h2><span id="company-cik"></span></div>
        <div class="charts">
            <article class="chart-panel"><h3>Annual revenue</h3><div class="chart-wrap"><canvas id="revenue-chart"></canvas></div></article>
            <article class="chart-panel"><h3>Net income</h3><div class="chart-wrap"><canvas id="income-chart"></canvas></div></article>
            <article class="chart-panel"><h3>Total assets</h3><div class="chart-wrap"><canvas id="assets-chart"></canvas></div></article>
        </div>
    </section>
</main>
<script>
    const charts = {};
    const companyForm = document.querySelector("#company-form");
    const form = document.querySelector("#lookup-form");
    const status = document.querySelector("#status");
    const results = document.querySelector("#results");
    const companyMatch = document.querySelector("#company-match");

    companyForm.addEventListener("submit", async event => {
        event.preventDefault();
        status.className = "";
        status.textContent = "Searching SEC company records...";
        companyMatch.hidden = true;
        try {
            const name = document.querySelector("#company-query").value.trim();
            const response = await fetch(`/api/company?name=${encodeURIComponent(name)}`);
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || "No matching company was found.");
            document.querySelector("#cik").value = data.cik;
            companyMatch.textContent = `Official company: ${data.company} | CIK ${data.cik}`;
            companyMatch.hidden = false;
            status.textContent = "Company found. Load its financials below.";
        } catch (error) {
            status.className = "error";
            status.textContent = error.message;
        }
    });

    function drawChart(id, label, values, color) {
        if (charts[id]) charts[id].destroy();
        charts[id] = new Chart(document.querySelector(`#${id}`), {
            type: "line",
            data: { labels: values.map(point => point.year), datasets: [{ label, data: values.map(point => point.value), borderColor: color, backgroundColor: `${color}22`, fill: true, tension: .25, pointRadius: 4 }] },
            options: { maintainAspectRatio: false, responsive: true, scales: { y: { ticks: { callback: value => new Intl.NumberFormat("en-US", { notation: "compact", maximumFractionDigits: 1 }).format(value) } } }, plugins: { legend: { display: false }, tooltip: { callbacks: { label: context => new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 }).format(context.raw) } } } }
        });
    }

    form.addEventListener("submit", async event => {
        event.preventDefault();
        const cik = document.querySelector("#cik").value.trim();
        status.className = "";
        status.textContent = "Retrieving annual filings from EDGAR...";
        results.hidden = true;
        try {
            const response = await fetch(`/api/financials?cik=${encodeURIComponent(cik)}`);
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || "EDGAR could not provide this company’s facts.");
            document.querySelector("#company-name").textContent = data.company;
            document.querySelector("#company-cik").textContent = `CIK ${data.cik}`;
            drawChart("revenue-chart", "Revenue", data.revenue, "#d45d3e");
            drawChart("income-chart", "Net income", data.net_income, "#2d7b78");
            drawChart("assets-chart", "Total assets", data.assets, "#d18a32");
            results.hidden = false;
            status.textContent = `Showing ${data.years} fiscal years from annual 10-K filings.`;
        } catch (error) {
            status.className = "error";
            status.textContent = error.message;
        }
    });
</script>
</body>
</html>"""


def normalized_cik(value: str) -> str:
    digits = "".join(character for character in value if character.isdigit())
    if not digits or len(digits) > 10:
        raise ValueError("Enter a CIK number with up to ten digits.")
    return digits.zfill(10)


def find_company(name: str) -> dict:
    query = " ".join(name.split()).casefold()
    if not query:
        raise ValueError("Enter a company name.")
    response = requests.get(EDGAR_COMPANIES_URL, headers=EDGAR_HEADERS, timeout=20)
    response.raise_for_status()
    companies = response.json().values()
    records = [{"company": item["title"], "cik": str(item["cik_str"])} for item in companies]
    exact = [item for item in records if item["company"].casefold() == query]
    if exact:
        return exact[0]
    matching = [item for item in records if query in item["company"].casefold()]
    if matching:
        return matching[0]
    closest = get_close_matches(query, [item["company"].casefold() for item in records], n=1, cutoff=.65)
    if closest:
        return next(item for item in records if item["company"].casefold() == closest[0])
    raise ValueError(f"No SEC company record matched '{name}'.")


def fact_series(facts: dict, tags: tuple[str, ...], cutoff: int = 10) -> list[dict]:
    available_tags = [tag for tag in tags if facts.get("us-gaap", {}).get(tag)]
    if not available_tags:
        raise ValueError(f"EDGAR does not report the requested fact ({tags[0]}).")

    by_year = {}
    for tag in available_tags:
        units = facts["us-gaap"][tag].get("units", {})
        unit_values = units.get("USD") or next(iter(units.values()), [])
        for item in unit_values:
            if item.get("form") != "10-K" or item.get("fp") != "FY" or not item.get("fy"):
                continue
            year = int(item["fy"])
            previous = by_year.get(year)
            if previous is None or (previous["tag"] not in tags[:tags.index(tag)] and item.get("filed", "") > previous["item"].get("filed", "")):
                by_year[year] = {"item": item, "tag": tag}
    return [{"year": year, "value": by_year[year]["item"]["val"]} for year in sorted(by_year)[-cutoff:]]


def fetch_financials(cik: str) -> dict:
    response = requests.get(EDGAR_FACTS_URL.format(cik=cik), headers=EDGAR_HEADERS, timeout=20)
    response.raise_for_status()
    payload = response.json()
    facts = payload.get("facts", {})
    return {
        "company": payload.get("entityName", f"CIK {cik}"),
        "cik": str(int(cik)),
        "revenue": fact_series(facts, ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet")),
        "net_income": fact_series(facts, ("ProfitLoss", "NetIncomeLoss")),
        "assets": fact_series(facts, ("Assets",)),
    }


class FinancialRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.send_content(HTML.encode("utf-8"), "text/html; charset=utf-8")
            return
        if parsed.path == "/api/financials":
            try:
                cik = normalized_cik(parse_qs(parsed.query).get("cik", [""])[0])
                self.send_content(json.dumps(fetch_financials(cik)).encode("utf-8"), "application/json")
            except (ValueError, requests.RequestException, KeyError) as error:
                self.send_content(json.dumps({"error": f"Could not load financials: {error}"}).encode("utf-8"), "application/json", 400)
            return
        if parsed.path == "/api/company":
            try:
                name = parse_qs(parsed.query).get("name", [""])[0]
                self.send_content(json.dumps(find_company(name)).encode("utf-8"), "application/json")
            except (ValueError, requests.RequestException, KeyError) as error:
                self.send_content(json.dumps({"error": f"Could not find company: {error}"}).encode("utf-8"), "application/json", 400)
            return
        self.send_error(404)

    def send_content(self, content: bytes, content_type: str, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format_string, *args):
        print(f"{self.address_string()} - {format_string % args}")


def main():
    server = ThreadingHTTPServer((HOST, PORT), FinancialRequestHandler)
    print(f"Ten-Year Financial Lens running at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping financial dashboard.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()