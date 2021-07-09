from bokeh.models import ColumnDataSource, GMapOptions, HoverTool, ColorBar
from bokeh.plotting import gmap

from bokeh.transform import linear_cmap
from bokeh.palettes import Plasma256 as palette
from google.cloud import bigquery


api_key = 'AIzaSyCCKJAMQRcfWjlXJMQhzsVA22FbAGqEDZM'
GCP_PROJECT = 'collabothon21-team-a'
DATASET_NAME = 'testlodz'
TABLE_NAME = 'trees'

QUERY = (
    f'SELECT X, Y, Height, Radius '
    f'FROM `{GCP_PROJECT}.{DATASET_NAME}.{TABLE_NAME}`'
)

with open('static/map_style.txt', 'r') as style:
    map_style = style.read()


def load_google_map(lat, lng, zoom=14, map_type='roadmap'):
    client = bigquery.Client()
    gmap_options = GMapOptions(
        lat=lat, lng=lng, map_type=map_type, zoom=zoom, styles=map_style
    )

    hover = HoverTool(
        tooltips=[

            ('height of tree [m]', '@Height'),
            ('upper branches of a tree width [m]', '@Radius'),

        ]
    )

    gmap_obj = gmap(api_key, gmap_options, title='Trees density',
                    width=850, height=550, tools=[hover, 'reset', 'wheel_zoom', 'pan'])
    source = ColumnDataSource(client.query(QUERY).to_dataframe())

    mapper = linear_cmap('Height', palette, 1., 40.)

    gmap_obj.circle(
        'X', 'Y', alpha=0.5, color=mapper, radius='Radius', source=source,
    )

    color_bar = ColorBar(
        color_mapper=mapper['transform'],
        label_standoff=14,
        location=(0, 0),
        title="Tree height [m]"
    )
    gmap_obj.add_layout(color_bar, 'right')

    return gmap_obj
