import csv

# Open the earthquake data file.
filename = './significant_month.csv'

# Create empty lists for the latitudes and longitudes.
lats, lons = [], []

# Read through the entire file, skip the first line,
#  and pull out just the lats and lons.
with open(filename) as f:
    # Create a csv reader object.
    reader = csv.reader(f)

    # Ignore the header row.
    next(reader)

    # Store the latitudes and longitudes in the appropriate lists.
    for row in reader:
        lats.append(float(row[1]))
        lons.append(float(row[2]))

# Display the first 5 lats and lons.
print('lats', lats[0:5])
print('lons', lons[0:5])