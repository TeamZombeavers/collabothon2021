from bokeh.embed import components
from bokeh.resources import INLINE
from flask import Flask, render_template

from load_map import load_google_map

app = Flask(__name__)

@app.route('/')
def bokeh():

    center_map_lat, center_map_lng = (51.834070, 19.355114) #TODO: change this as first value of dataset or something
    fig = load_google_map(center_map_lat, center_map_lng)
    
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