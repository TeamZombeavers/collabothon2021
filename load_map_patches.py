from bokeh.io import show
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool
from bokeh.plotting import gmap
import pandas as pd
from bokeh.transform import linear_cmap
from bokeh.palettes import Plasma256 as palette

trees_df_poly = pd.read_csv('trees.csv')


def get_coordinates():
    wkt_list = list(trees_df_poly['WKT'])
    wkt_s = [w[16:-3] for w in wkt_list]
    wkt_s = [w.split(',') for w in wkt_s]
    xs = [[float(w.split()[1]) for w in ws] for ws in wkt_s]
    ys = [[float(w.split()[0]) for w in ws] for ws in wkt_s]
    return xs, ys


def load_map_with_patches(lat, lng):
    lats, lons = get_coordinates()
    map_options = GMapOptions(lat=lat, lng=lng, map_type="roadmap", zoom=15)

    hover = HoverTool(
        tooltips=[

            ('temperature [C]', '@temperature'),
            ('percentage of tree coverage [%]', '@tree_perc'),

        ]
    )

    map_plot = gmap(google_api_key='AIzaSyCCKJAMQRcfWjlXJMQhzsVA22FbAGqEDZM', map_options=map_options, title="Patches",
             width=550, height=450, tools=['reset', 'wheel_zoom', 'pan', hover])

    pnts = ColumnDataSource(
        data=dict(
            lats=lats,
            lons=lons,
            temperature=trees_df_poly['TEMPERATURA'],
            tree_perc=trees_df_poly['DRZEWA_POW_PROC']
        )
    )

    mapper = linear_cmap('temperature', palette, 1., 40.)

    map_plot.patches(xs="lons", ys="lats", fill_alpha=0.2, source=pnts, color=mapper)

    return map_plot


