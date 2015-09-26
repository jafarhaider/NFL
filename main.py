

### file to import with all programs

## libraries
import urllib3
import datetime
import copy

import csv as csv
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt
from scipy.stats.mstats import zscore
from copy import deepcopy

import matplotlib.font_manager as fm
import locale
import os
from  more_itertools import unique_everseen

# from ggplot import *
# from bokeh.plotting import *
# from bokeh.charts import *
# from bokeh.models import Range1d, HoverTool, DataRange1d
# from bokeh.palettes import (Blues9, BrBG9, BuGn9, BuPu9, GnBu9, Greens9,
#                             Greys9, OrRd9, Oranges9, PRGn9, PiYG9, PuBu9,
#                             PuBuGn9, PuOr9, PuRd9, Purples9, RdBu9, RdGy9,
#                             RdPu9, RdYlBu9, RdYlGn9, Reds9, Spectral9, YlGn9,
#                             YlGnBu9, YlOrBr9, YlOrRd9)

## declare global variables

# declare years to search
firstYear = 1998 # Peyton Manning's rookie year
lastYear = datetime.datetime.now().year # currently 2015, so that it will search up to 2014

# folders for output
output_prefix = "/Users/python/Dropbox/Python/NFL/Output/PFR/"
data_prefix = "/Users/python/Dropbox/Python/NFL/Data/PFR/"
test_csv = "%stest.csv" % (output_prefix)
test2_csv = "%stest2.csv" % (output_prefix)
playoffs_csv = "%splayoffs.csv" % (data_prefix)
dfout = '%sdf.csv' % data_prefix
dfout2 = '%sdf2.csv' % data_prefix
cumAvgDF_csv = '%scumAvgDF.csv' % (data_prefix)


# output display width
pd.options.display.width = 115

