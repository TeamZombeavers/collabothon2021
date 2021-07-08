from bokeh.models import ColumnDataSource, GMapOptions, HoverTool, ColorBar
from bokeh.plotting import gmap
from bokeh.io import show
import pandas as pd

from bokeh.transform import linear_cmap
from bokeh.palettes import Plasma256 as palette


api_key = 'AIzaSyCCKJAMQRcfWjlXJMQhzsVA22FbAGqEDZM'


trees_df = pd.read_csv('drzewa.csv')


def load_google_map(lat, lng, zoom=17, map_type='roadmap'):
    gmap_options = GMapOptions(lat=lat, lng=lng,
                               map_type=map_type, zoom=zoom)

    hover = HoverTool(
        tooltips=[

            ('height of tree [m]', '@Height'),
            ('upper branches of a tree width [m]', '@Radius'),

        ]
    )

    gmap_obj = gmap(api_key, gmap_options, title='Trees density',
                    width=550, height=450, tools=[hover, 'reset', 'wheel_zoom', 'pan'])
    source = ColumnDataSource(trees_df)

    mapper = linear_cmap('Height', palette, 1., 40.)

    center = gmap_obj.circle('X', 'Y', alpha=0.5,
                             color=mapper, radius='Radius', source=source)

    color_bar = ColorBar(color_mapper=mapper['transform'], label_standoff=14,
                         location=(0, 0), title="Tree height [m]")
    gmap_obj.add_layout(color_bar, 'right')

    return gmap_obj
