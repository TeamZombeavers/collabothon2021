from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable,  DateFormatter, TableColumn
from bokeh.io import output_file, show
from google.cloud import bigquery

api_key = 'AIzaSyCCKJAMQRcfWjlXJMQhzsVA22FbAGqEDZM'
GCP_PROJECT = 'collabothon21-team-a'
DATASET_NAME = 'testlodz'
TABLE_NAME = 'tree_patches'

QUERY = (
    f'SELECT NDVI, TEMPERATURA, DRZEWA_POW, DRZEWA_POW_PROC '
    f'FROM {GCP_PROJECT}.{DATASET_NAME}.{TABLE_NAME}'
)




def load_preview_data():
    client = bigquery.Client()
    data = client.query(QUERY).to_dataframe()
    source = ColumnDataSource(data)
    columns = [
        TableColumn(field="NDVI", title="NDVI"),
        TableColumn(field="TEMPERATURA", title="TEMPERATURA"),
        TableColumn(field="DRZEWA_POW", title="DRZEWA_POW"),
        TableColumn(field="DRZEWA_POW_PROC", title="DRZEWA_POW_PROC"),

    ]
    data_table = DataTable(source=source, columns =columns,width=400, height=280)
    return data_table