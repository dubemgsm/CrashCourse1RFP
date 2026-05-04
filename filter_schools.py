import csv
from collections import defaultdict

# 1. Identify LGAs with violence events
violence_file = 'Nigeria_HRP_political_violence.csv'
lga_violence = defaultdict(int)

print(f"Reading violence data from {violence_file}...")
with open(violence_file, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        lga = row['Admin2']
        events = int(row['Events']) if row['Events'] else 0
        if events > 0:
            lga_violence[lga] += events

print(f"Found {len(lga_violence)} LGAs with violence events.")

# 2. Filter schools in those LGAs
schools_file = 'North_East_schools.csv'
output_file = 'at_risk_schools.csv'
at_risk_schools = []

print(f"Filtering schools from {schools_file}...")
with open(schools_file, mode='r', encoding='latin-1') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        lga = row['LGA Name']
        if lga in lga_violence:
            # Add violence info to the row
            row['Total Violence Events in LGA'] = lga_violence[lga]
            at_risk_schools.append(row)

# 3. Save the result
if 'Total Violence Events in LGA' not in fieldnames:
    fieldnames.append('Total Violence Events in LGA')

print(f"Saving {len(at_risk_schools)} at-risk schools to {output_file}...")
with open(output_file, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(at_risk_schools)

print("Done.")
