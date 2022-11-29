# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 08:27:12 2022

@author: Neraliel
regien.m28@gmail.com

This code is aimed to construct xyz.txt grids with topographic and bathymetric data

Input files : 
    => Only lon lat ele tables in csv or txt type.
In this code you will find 3 examples with :
    - file with blankspaces
    - columns reorganization
    - columns selection
    

Output files :
    => xyz.txt file with the grid
    => map of the grid
      
"""

# ===== LIBRAIRIES ===== #

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import griddata

# ===== GRID BUILDING ===== #

#---Uploading all the files and make one table---#

# example : reorganize the columns 
data1old=pd.read_csv("cahuita_points_modifs2.txt",sep=';',usecols=[4,5,6],dtype=float)
data1=pd.DataFrame()
data1['lon']=data1old['lon']
data1['lat']=data1old['lat']
data1['ele']=data1old['ele']

# example : files with blankspaces
data2=pd.read_csv("Bati_Cahuita_Imares.txt",delim_whitespace=True, dtype=float, names=['lon','lat','ele'])
data3=pd.read_csv("cahui10XYZ.txt",delim_whitespace=True,names=['lon','lat','ele'])
data4=pd.read_csv("Malla_5m_Bati.txt",delim_whitespace=True,names=['lon','lat','ele'])
data5=pd.read_csv("Malla_20m_Bati.txt",delim_whitespace=True,names=['lon','lat','ele'])
data6=pd.read_csv("Malla_40m_Bati.txt",delim_whitespace=True,names=['lon','lat','ele'])

# example : columns selection
data7=pd.read_csv("coastline.txt",sep=';',usecols=[2,3,4],dtype=float)

### concatenate all the DataFrame in one
data_all=pd.concat([data1,data2,data3,data4,data5,data6,data7],axis=0,ignore_index=True)

### if you need to add land correction
data_all=data_all.mask(data_all['ele']>0.1) # we delete all elevation upper than 0.1 meters
data_all=data_all.dropna()

data8=pd.read_csv("land_corrected.txt",sep=';',usecols=[1,2,3],dtype=float)
data=pd.concat([data_all,data8],axis=0,ignore_index=True)

#---Create a global grid to interpolate field data at 1 arcsecond resolution---#
### grid x & y
xx=np.arange(np.min(data.lon),np.max(data.lon),1/3600) # you can replace by 4, 12, 20...
yy=np.arange(np.min(data.lat),np.max(data.lat),1/3600)

### interpolation with griddata / linear
[x,y]=np.meshgrid(xx,yy)
z = griddata((data.lon, data.lat), data.ele, (x, y), method='linear')
x = np.matrix.flatten(x) #Gridded longitude
y = np.matrix.flatten(y) #Gridded latitude
z = np.matrix.flatten(z) #Gridded elevation


### Put all the results in a DataFrame
results=pd.DataFrame()
results['XX']=x
results['YY']=y
results['ZZ']=z

### Mask (cut) the data to have only the geographical area we want
# Lat and Lon in 180° base decimal degrees
data_test=results.mask(results['YY']>9.778) #LARGER LATITUDE
data_lat=data_test.mask(data_test['YY']<9.648) #TINIER LATITUDE
data_lat=data_lat.dropna()

data_test=data_lat.mask(data_lat['XX']<-82.89) #TINIER LONGITUDE
data_1arc=data_test.mask(data_test['XX']>-82.78) #LARGER LONGITUDE
data_1arc=data_1arc.dropna()

### Writing of the file
file_test=open("grid.txt","w") # here you can name the output file
file_test.write(data_1arc.to_csv(sep=';',index=False))
file_test.close

### Map creation
plt.figure()
plt.scatter(data_1arc['XX'],data_1arc['YY'],1,data_1arc['ZZ'],cmap='rainbow')
plt.colorbar(label='Elevation [m]')
plt.xlabel('Longitude [°]')
plt.ylabel('Latitude [°]')
plt.title("Map") # here you can name the map