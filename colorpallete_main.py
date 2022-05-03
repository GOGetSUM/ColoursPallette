from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from PIL import Image
import numpy as np
from numpy import asarray
from colorthief import ColorThief
from webcolors import CSS3_HEX_TO_NAMES, hex_to_rgb, rgb_to_name

#--------------SetUp App----------------------------------------------------------------

app = Flask(__name__)
Bootstrap(app)

#-------------Index Home-----------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')

#-------------Functions-----------------------------------------------------------------------
@app.route('/top_five', methods=["GET", "POST"])
def top_ten():
    fp_ = request.form['filepath'] #from user file path of image
    color_thief = ColorThief(fp_)
    palette = color_thief.get_palette(color_count=5)
    hex = []
    colours_act = []
    colours_cls = []
    for color in palette:
        def rgb_to_hex(r, g, b):
            return ('{:X}{:X}{:X}').format(r, g, b)
        a = rgb_to_hex(color[0],color[1],color[2])
        hex.append(a)

        def closest_colour(requested_colour):
            min_colours = {}
            for key, name in CSS3_HEX_TO_NAMES.items():
                r_c, g_c, b_c = hex_to_rgb(key)
                rd = (r_c - requested_colour[0]) ** 2
                gd = (g_c - requested_colour[1]) ** 2
                bd = (b_c - requested_colour[2]) ** 2
                min_colours[(rd + gd + bd)] = name
            return min_colours[min(min_colours.keys())]

        def get_colour_name(requested_colour):
            try:
                closest_name = actual_name = rgb_to_name(requested_colour)
            except ValueError:
                closest_name = closest_colour(requested_colour)
                actual_name = None
            return actual_name, closest_name

        requested_colour = (color[0],color[1],color[2])
        actual_name, closest_name = get_colour_name(requested_colour)
        colours_act.append(actual_name)
        colours_cls.append(closest_name)
    print(hex)
    print(colours_act)
    print(colours_cls)


    return render_template('top_list.html', rgb=palette, hex=hex,act=colours_act, clst=colours_cls )

#---------Run App---------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)