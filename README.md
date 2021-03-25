pynsee package
=======

**Work in progress**

<br> 

 [![Build Status](https://github.com/hadrilec/pynsee/actions/workflows/pynsee-test.yml/badge.svg)](https://github.com/hadrilec/pynsee/actions) 
[![Codecov test coverage](https://codecov.io/gh/hadrilec/pynsee/branch/master/graph/badge.svg)](https://codecov.io/gh/hadrilec/pynsee?branch=master) 
 [![Documentation Status](https://readthedocs.org/projects/py-insee-macrodata/badge/?version=latest)](https://py-insee-macrodata.readthedocs.io/en/latest/?badge=latest)
<br> 

# Overview

The pynsee package contains tools to easily download data and metadata from INSEE API.
Using the API or the SDMX queries, get the data of more than 150 000 INSEE series.
Have a look at the detailed API page with the following [link](https://api.insee.fr/catalogue/).
This package is a contribution to reproducible research and public data transparency.

## Installation & Loading

```python
# Get the development version from GitHub
pip install git+https://github.com/hadrilec/pynsee.git#egg=pynsee

# Subscribe to api.insee.fr and get your credentials!
# Beware : any change to the keys should be tested after having cleared the cache
# Please use : pynsee.utils.clear_all_cache to do so
import os
os.environ['insee_key'] = "my_key"
os.environ['insee_secret'] = "my_secret_key"
```
## French GDP growth rate

![](examples/pictures/example_gdp_picture.png)

```python
from pynsee import * 
import plotly.express as px
from plotly.offline import plot

# Subscribe to api.insee.fr and get your credentials!
# Beware : any change to the keys should be tested after having cleared the cache
# Please use : pynsee.utils.clear_all_cache to do so
import os
os.environ['insee_key'] = "my_insee_key"
os.environ['insee_secret'] = "my_insee_secret"

# get series key (idbank), for Gross domestic product balance
id = get_idbank_list("CNT-2014-PIB-EQB-RF")

id = id.loc[(id.FREQ == "T") &
            (id.OPERATION == "PIB") &
            (id.NATURE == "TAUX") &
            (id.CORRECTION == "CVS-CJO")]

data = get_insee_idbank(id.idbank)

# plot with plotly
fig = px.bar(data, x = data.index, y = "OBS_VALUE",
             facet_col = "TITLE_EN", facet_col_wrap=5)
fig.update_yaxes(matches=None)
plot(fig)
```
## Population Map

![](examples/pictures/example_pop_map.png)

```python
from pynsee.local import get_map
from pynsee.macro import *
import geopandas as gpd
import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import descartes

map_file = get_map('departements')
map = gpd.read_file(map_file)

dataset_list = get_dataset_list()

id = get_idbank_list("TCRED-ESTIMATIONS-POPULATION") 

id = id.loc[(id.AGE == "00-") &
            (id.SEXE == "0") &
            (id.REF_AREA.str.match("^D"))]

data = get_insee_idbank(id.idbank, lastNObservations=1)
data = data[['REF_AREA', 'OBS_VALUE']]

map['REF_AREA'] = 'D' + map['code']

map = map.to_crs(epsg=3035)
map["area"] = map['geometry'].area/ 10**6
map = map.to_crs(epsg=4326)

map = map.merge(data, how = 'left', on = 'REF_AREA')
map['density'] = map['OBS_VALUE'] / map["area"]

map.loc[map.density < 40, 'range'] = "< 40"
map.loc[map.density >= 20000, 'range'] = "> 20 000"

density_ranges = [40, 50, 70, 100, 120, 160, 200, 240, 260, 410, 600, 1000, 5000, 20000]
list_ranges = []
list_ranges.append( "< 40")

for i in range(len(density_ranges)-1):
    min = density_ranges[i]
    max = density_ranges[i+1]
    range_string = "[{}, {}[".format(min, max)
    map.loc[(map.density >= min) & (map.density < max), 'range'] = range_string
    list_ranges.append(range_string)

list_ranges.append("> 20 000")

map['range'] = map['range'].astype( CategoricalDtype(categories=list_ranges, ordered=True))

fig, ax = plt.subplots(1,1,figsize=[10,10])
map.plot(column='range', cmap=cm.viridis, 
    legend=True, ax=ax,
    legend_kwds={'bbox_to_anchor': (1.1, 0.8),
                 'title':'density per km2'})
ax.set_axis_off()
ax.set(title='Distribution of population in metropolitan France')
plt.show()
```
## Poverty in Paris urban area

![](examples/pictures/example_poverty_paris_uu.png)

```python

from pynsee.local import *

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import descartes

# get a list all data available : datasets and variables
metadata = get_local_metadata()

# geographic metadata
nivgeo = get_nivgeo_list()

# get geographic area list
area = get_area_list()

# get all communes in Paris urban area
areaParis = get_insee_area('unitesUrbaines2020', ['00851'])

# get selected communes identifiers
code_com_paris = areaParis.code.to_list()

# get numeric values from INSEE database 
dataParis = get_insee_local(dataset='GEO2020FILO2017',
                       variables =  'INDICS_FILO_DISP_DET',
                       geo = 'COM',
                       geocodes = code_com_paris)

#select poverty rate data
data_plot = dataParis.loc[dataParis.UNIT=='TP60']

#get communes limits
map = get_map('communes')

# merge values and geographic limits
mapparis = map.merge(data_plot, how = 'right',
                     left_on = 'code', right_on = 'CODEGEO')

#plot
fig, ax = plt.subplots(1,1,figsize=[15,15])
mapparis.plot(column='OBS_VALUE', cmap=cm.viridis, 
    legend=True, ax=ax, legend_kwds={'shrink': 0.3})
ax.set_axis_off()
ax.set(title='Poverty rate in Paris urban area in 2017')
plt.show()
fig.savefig('poverty_paris_urban_area.png')
```

## How to avoid proxy issues ?

```python
import os 
os.environ['http_proxy'] = 'http://my_proxy_server:port'
os.environ['https_proxy'] = 'http://my_proxy_server:port'
```

## Support
Feel free to contact me with any question about this package using this [e-mail address](mailto:hadrien.leclerc@insee.fr?subject=[pynsee]).
