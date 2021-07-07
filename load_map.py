from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap
from bokeh.io import show
import pandas as pd

from bokeh.transform import linear_cmap
from bokeh.palettes import Plasma256 as palette

api_key = 'AIzaSyCCKJAMQRcfWjlXJMQhzsVA22FbAGqEDZM'
center_map_lat, center_map_lng = (51.834070, 19.355114) # center point for starting map TODO: change to first values from table

trees_df = pd.read_csv('drzewa.csv')

def load_google_map(lat, lng, zoom=17, map_type='roadmap'):
    gmap_options = GMapOptions(lat=lat, lng=lng,
                               map_type=map_type, zoom=zoom)
    gmap_obj = gmap(api_key, gmap_options, title='Trees density',
             width=550, height=450)
    source = ColumnDataSource(trees_df)

    mapper = linear_cmap('Height', palette, 2000.,8000.)

    center = gmap_obj.circle('X', 'Y', size=4, alpha=0.5, color=mapper, radius='Radius', source=source)          
    show(gmap_obj)
    return gmap_obj


load_google_map(center_map_lat, center_map_lng)