# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 08:27:12 2022

@author: regie
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import griddata


## ===== 1 ARC SECOND ===== ##

# ---Uploading all the files and make one table---#
data1old = pd.read_csv("cahuita_points_modifs2.txt",
                       sep=';', usecols=[4, 5, 6], dtype=float)
# rearrange the columns order for the first dataset
data1 = pd.DataFrame()
data1['lon'] = data1old['lon']
data1['lat'] = data1old['lat']
data1['ele'] = data1old['ele']

# the other dataset imports
data2 = pd.read_csv("Bati_Cahuita_Imares.txt", delim_whitespace=True,
                    dtype=float, names=['lon', 'lat', 'ele'])
data3 = pd.read_csv("cahui10XYZ.txt", delim_whitespace=True,
                    names=['lon', 'lat', 'ele'])
data4 = pd.read_csv("Malla_5m_Bati.txt", delim_whitespace=True, names=[
                    'lon', 'lat', 'ele'])
data5 = pd.read_csv("Malla_20m_Bati.txt",
                    delim_whitespace=True, names=['lon', 'lat', 'ele'])
data6 = pd.read_csv("Malla_40m_Bati.txt",
                    delim_whitespace=True, names=['lon', 'lat', 'ele'])
data7 = pd.read_csv("coastline.txt", sep=';', usecols=[2, 3, 4], dtype=float)

# concatenate all the DataFrame in one
data = pd.concat([data1, data2, data3, data4, data5,
                 data6, data7], axis=0, ignore_index=True)

for k in range(len(data.ele)):
    print(data.ele[k])
    if data.ele[k] < 0:
        data.ele[k] = 0
        print(data.ele[k])


# ---Create a global grid to interpolate field data at 1 arcsecond resolution---#
# grid x & y
xx = np.arange(np.min(data.lon), np.max(data.lon), 1/3600)
yy = np.arange(np.min(data.lat), np.max(data.lat), 1/3600)

# interpolation with griddata / linear
[x, y] = np.meshgrid(xx, yy)
z = griddata((data.lon, data.lat), data.ele, (x, y), method='linear')
x = np.matrix.flatten(x)  # Gridded longitude
y = np.matrix.flatten(y)  # Gridded latitude
z = np.matrix.flatten(z)  # Gridded elevation


# ---Create the grid 4---#
# Put all the results in a DataFrame
results = pd.DataFrame()
results['XX'] = x
results['YY'] = y
results['ZZ'] = z

# Mask (cut) the data to have only the geographical area we want
data_test = results.mask(results['YY'] > 9.778)  # LARGER
data_lat = data_test.mask(data_test['YY'] < 9.648)  # TINIER
data_lat = data_lat.dropna()

data_test = data_lat.mask(data_lat['XX'] < -82.89)  # TINIER
data_1arc = data_test.mask(data_test['XX'] > -82.78)  # LARGER
data_1arc = data_1arc.dropna()

data_1arc = data_1arc.mask(data_1arc['ZZ'] == 0)
data_1arc = data_1arc.dropna()

# to avoid some gaps on this grids, we delete the first and last row of the map
# ind_min=np.max(np.where(data_1arc['YY']==np.min(data_1arc['YY'])))+1
# ind_max=np.min(np.where(data_1arc['YY']==np.max(data_1arc['YY'])))

# data_1arc=data_1arc[ind_min:ind_max]


file_test = open("land.txt", "w")
file_test.write(data_1arc.to_csv(sep=';', index=False))
file_test.close

# test de la carte
plt.figure()
plt.scatter(data_1arc['XX'], data_1arc['YY'],
            1, data_1arc['ZZ'], cmap='rainbow')
plt.colorbar(label='Elevation [m]')
plt.xlabel('Longitude [°]')
plt.ylabel('Latitude [°]')
plt.title("Test Cahuita 1arcsecond")

"""
### écriture du fichier de sortie
x=np.array(data_1arc['XX'])
y=np.array(data_1arc['YY'])
z=np.array(data_1arc['ZZ'])

file = open("grid4_Cahuita.txt","w")
file.write("# Elevation grid with 1arcs resolution for Cahuita region (Costa Rica, Caribbean Coast) \n# elevation (m) ; longitude (decimal degrees) ; latitude (decimal degrees)\n")
for k in range(len(z)):
    file.write(f"{z[k]};{x[k]};{y[k]}\n")
file.close
"""
