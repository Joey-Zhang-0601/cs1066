### m05/extract_net_income_rehearsal.py
# Generated on 20260812 using Auto model (Claude Haiku 4.5)
# PROMPT: In the directory `m05`, write a Python program to extract Net Income from the file `amd_data.json` and print the yearly values.
import json

# Load the JSON data
with open('amd_data.json', 'r') as f:
    data = json.load(f)

# Extract Net Income data
net_income_data = data['facts']['us-gaap']['NetIncomeLoss']['units']['USD']

# Dictionary to store yearly net income values
yearly_net_income = {}

# Process each entry
for entry in net_income_data:
    # Only include full-year (FY) entries
    if entry.get('fp') == 'FY':
        year = entry.get('fy')
        value = entry.get('val')
        
        # Store the value (keeping the most recent entry for each year)
        if year not in yearly_net_income:
            yearly_net_income[year] = value

# Sort by year and print
print("AMD Net Income by Year (in USD)")
print("-" * 40)
print(f"{'Year':<10} {'Net Income':>20}")
print("-" * 40)

for year in sorted(yearly_net_income.keys()):
    value = yearly_net_income[year]
    print(f"{year:<10} ${value:>18,}")
