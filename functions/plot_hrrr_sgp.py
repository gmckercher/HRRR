# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 08:32:23 2014

@author: mattjohnson
"""


from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
from mpl_toolkits.basemap import Basemap
import os

def plot_hrrr_sgp(filename,parameter,directory = os.getcwd(),hinp = '', scaling = 1, final_unit = '', margin = 10, vmax = None, vmin = None):

    """
    Plots an hrrr file focused on the SGP site for a given hrrr filename, parameter and height in hPa. 
    Labels the SGP site.  
     
    Leaving the height blank will cause it to plot the maximum values of the file.  The margin defines half the length of 
    the plot area in degrees latitude and longitude.  Scaling and final_unit can be used to tweak the data in order to 
    make it more visible on the graph.  vmax and vmin function the same as in pcolormesh from Basemap.  
    """
    wkdir = os.getcwd()
    os.chdir(directory)
    
    if hinp != '':
        [data,parameterlist,units] = read_hrrr(filename,[parameter])
    else:
        [data,parameterlist,units] = read_hrrr(filename,[parameter],directory = directory,max=True)
        
    if hinp !='':
        datah = HRRR_PS.tolist()
        hindex = datah.index(hinp)
        
    if final_unit == '':
        final_unit = units[0]
        

    f = plt.figure(figsize=[12,10])
    m = Basemap(llcrnrlon = -97.485-margin,llcrnrlat = 36.605-margin, urcrnrlon = -97.485+margin,
                   urcrnrlat = 36.605+margin, projection = 'mill', area_thresh =10000 ,
                   resolution='l')
        
    latlonsgp = [-97.485,36.605]
    cities = ['Lamont,OK']
    sgpx,sgpy = m(latlonsgp[0],latlonsgp[1])
    m.plot(sgpx,sgpy,'bo')
    #plt.text(sgpx+50000,sgpy+50000,'SGP site')
        
    x, y = m(HRRR_DATALOC[1],HRRR_DATALOC[0])
    data = np.array(data)
    
    
    if hinp != '':
        newdata = data[0][hindex][:][:]
    else:
        newdata = data[0]
        
    my_mesh = m.pcolor(x, y, newdata, vmax = .05, norm = colors.LogNorm())
#    my_coast = m.drawcoastlines(linewidth=1.25)
#    my_states = m.drawstates()
#    my_p = m.drawparallels(np.arange(20,80,4),labels=[1,1,0,0])
#    my_m = m.drawmeridians(np.arange(-140,-60,4),labels=[0,0,0,1])
        
    plt.colorbar(label=parameter+' '+final_unit)
    plt.show()
    
    os.chdir(wkdir)
    return