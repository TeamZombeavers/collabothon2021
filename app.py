from bokeh.embed import components
from bokeh.layouts import column, row
from bokeh.resources import INLINE
from flask import Flask, render_template

from load_map import load_google_map
from load_map_patches import load_map_with_patches

app = Flask(__name__)


@app.route('/')
def bokeh():

    # TODO: change this as first value of dataset or something
    center_map_lat, center_map_lng = (51.75502945945417, 19.436975611786895)
    trees_map = load_google_map(center_map_lat, center_map_lng)
    polygon_map = load_map_with_patches(center_map_lat, center_map_lng)

    fig = column(
        row(trees_map),
        row(polygon_map),
    )

    script, div = components(fig)

    return render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    ).encode(encoding='UTF-8')


if __name__ == '__main__':
    app.run(debug=True)
