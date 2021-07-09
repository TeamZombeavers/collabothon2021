from bokeh.io import show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Plasma256 as palette
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from google.cloud import bigquery

api_key = 'AIzaSyCCKJAMQRcfWjlXJMQhzsVA22FbAGqEDZM'
GCP_PROJECT = 'collabothon21-team-a'
DATASET_NAME = 'testlodz'
TABLE_NAME = 'tree_patches'

QUERY = (
    f'SELECT avg(TEMPERATURA) as avg_temp, round(DRZEWA_POW_PROC, 2) as trees '
    f'FROM `{GCP_PROJECT}.{DATASET_NAME}.{TABLE_NAME}`'
    f'GROUP BY trees'
)


def load_scatter():
    client = bigquery.Client()
    data = client.query(QUERY).to_dataframe()

    data.sort_values(by=["avg_temp"], inplace=True)

    pnts = ColumnDataSource(
        data=dict(
            x=data['trees'],
            y=data['avg_temp']
        )
    )

    mapper = linear_cmap('y', palette, 15., 40.)

    scatter_plot = figure(plot_width=750, plot_height=500)

    scatter_plot.circle('x', 'y', line_width=2, color=mapper, source=pnts)

    return scatter_plot
