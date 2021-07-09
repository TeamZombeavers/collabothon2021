from bokeh.models import ColumnDataSource, GMapOptions, HoverTool
from bokeh.plotting import gmap
from bokeh.transform import linear_cmap
from bokeh.palettes import Plasma256 as palette
from google.cloud import bigquery


GCP_PROJECT = 'collabothon21-team-a'
DATASET_NAME = 'testlodz'
TABLE_NAME = 'tree_patches'
QUERY = (
    f'SELECT WKT, TEMPERATURA, DRZEWA_POW_PROC '
    f'FROM `{GCP_PROJECT}.{DATASET_NAME}.{TABLE_NAME}`'
)


def get_coordinates(trees_df_poly):
    wkt_list = list(trees_df_poly['WKT'])
    wkt_s = [w[16:-3] for w in wkt_list]
    wkt_s = [w.split(',') for w in wkt_s]
    xs = [[float(w.split()[1]) for w in ws] for ws in wkt_s]
    ys = [[float(w.split()[0]) for w in ws] for ws in wkt_s]
    return xs, ys


def load_map_with_patches(lat, lng):
    client = bigquery.Client()
    trees_df_poly = client.query(QUERY).to_dataframe()
    lats, lons = get_coordinates(trees_df_poly)
    map_options = GMapOptions(lat=lat, lng=lng, map_type="roadmap", zoom=14)

    hover = HoverTool(
        tooltips=[

            ('temperature [C]', '@temperature'),
            ('percentage of tree coverage [%]', '@tree_perc'),

        ]
    )

    map_plot = gmap(google_api_key='AIzaSyCCKJAMQRcfWjlXJMQhzsVA22FbAGqEDZM', map_options=map_options, title="Patches",
                    width=750, height=500, tools=['reset', 'wheel_zoom', 'pan', hover])

    pnts = ColumnDataSource(
        data=dict(
            lats=lats,
            lons=lons,
            temperature=trees_df_poly['TEMPERATURA'],
            tree_perc=trees_df_poly['DRZEWA_POW_PROC']
        )
    )

    mapper = linear_cmap('temperature', palette, 1., 40.)

    map_plot.patches(xs="lons", ys="lats", fill_alpha=0.2,
                     source=pnts, color=mapper)

    return map_plot
