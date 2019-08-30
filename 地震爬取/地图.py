import csv
# Open the earthquake data file.
# filename = './significant_month.csv'
filename = './all_month.csv'

# Create empty lists for the data we are interested in.
lats, lons = [], []
magnitudes = []


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
        try:
            magnitudes.append(float(row[4]))
        except:
            lats.pop()
            lons.pop()
            continue


# ---------------build map -----------------
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

def get_marker_color(magnitude):
    # Returns green for small earthquakes, yellow for moderate
    #  earthquakes, and red for significant earthquakes.
    if magnitude < 4.0:
        return ('go')
    elif magnitude < 5.0:
        return ('yo')
    else:
        return ('ro')

# make sure the value of resolution is a lowercase L,
#  for 'low', not a numeral 1
my_map = Basemap(projection='robin', lat_0=39, lon_0=115,#lat是纬度
                 resolution='l', area_thresh=1000.0,
                 # llcrnrlon 纬度，llcrnrlat经度
                 llcrnrlon =70 , llcrnrlat = 17,  # 左下角
                 urcrnrlon =138, urcrnrlat = 54,  # 右上角
                 )

my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color = 'gray')
my_map.drawmapboundary()

my_map.drawmeridians(np.arange(0, 360, 30))
my_map.drawparallels(np.arange(-90, 90, 30))

min_marker_size = 1.5
for lon, lat, mag in zip(lons, lats, magnitudes):
    x,y = my_map(lon, lat)
    msize = mag * min_marker_size
    marker_string = get_marker_color(mag)
    my_map.plot(x, y, marker_string, markersize=msize)


plt.show()