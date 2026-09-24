import json

# Load the JSON data
with open('amd_data.json', 'r') as f:
    data = json.load(f)

# Extract Revenue data
revenue_data = data['facts']['us-gaap']['Revenues']['units']['USD']

# Dictionary to store yearly revenue values
yearly_revenue = {}

# Process each entry
for entry in revenue_data:
    # Only include full-year (FY) entries
    if entry.get('fp') == 'FY':
        year = entry.get('fy')
        value = entry.get('val')
        
        # Store the value (keeping the most recent entry for each year)
        if year not in yearly_revenue:
            yearly_revenue[year] = value

# Sort by year and print
print("AMD Revenue by Year (in USD)")
print("-" * 40)
print(f"{'Year':<10} {'Revenue':>20}")
print("-" * 40)

for year in sorted(yearly_revenue.keys()):
    value = yearly_revenue[year]
    print(f"{year:<10} ${value:>18,}")
