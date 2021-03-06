#!/usr/bin/env python
"""
This is being used to form quicktile approximation to text location with 
the goal of having another markup language as input (TODO)

This is a variant of add_text, in which we also add text effects to it, 
we'll leave the layer grouping etc to be manual work(?)

./add_bubble_text.py poster.xcf "hello world" 2
"""

BORDERWIDTH = 3

# padding in percentile around the border
PADDING = 0.0825

# based on Quicktile approximations
# tuple is (x in perc, y in perc, x perc adj, y perc adj)
LOCATION_MAPPING = {
    "7": (0.0, 0.0, PADDING, PADDING),  # top left
    "8": (0.0, 0.5, PADDING, -PADDING),  # top middle
    "9": (0.0, 1.0, PADDING, -PADDING * 2),  # top right
    "4": (0.5, 0.0, -PADDING, PADDING),  # middle left
    "5": (0.5, 0.5, -PADDING, -PADDING),  # middle middle
    "6": (0.5, 1.0, -PADDING, -PADDING * 2),  # middle right
    "1": (1.0, 0.0, -PADDING * 2, PADDING),  # bottom left
    "2": (1.0, 0.5, -PADDING * 2, -PADDING),  # bottom middle
    "3": (1.0, 1.0, -PADDING * 2, -PADDING * 2),  # bottom right
}


def invert_tt(color):
    return (255 - color[0], 255 - color[1], 255 - color[2])


def exchange_color():
    bg = pdb.gimp_context_get_background()
    fg = pdb.gimp_context_get_foreground()
    pdb.gimp_context_set_foreground(bg)
    pdb.gimp_context_set_background(fg)


def add_bubble_text_quick(fname, text, location):
    """
    Adds some text based on quicktile approximation
    """
    img = pdb.gimp_file_load(fname, fname)

    width = pdb.gimp_image_width(img)
    height = pdb.gimp_image_height(img)

    location_mapper = LOCATION_MAPPING[location]
    loc_y = int((location_mapper[0] + location_mapper[2]) * height)
    loc_x = int((location_mapper[1] + location_mapper[3]) * width)

    # add invert text
    exchange_color()
    text_layer = pdb.gimp_text_fontname(
        img, None, loc_x, loc_y, text, 0, True, 27, 1, "Intuitive Semi-Bold"
    )
    exchange_color()

    # select + grow, create new layer below and fill
    pdb.gimp_selection_none(img)
    pdb.gimp_image_select_item(img, CHANNEL_OP_REPLACE, text_layer)
    pdb.gimp_selection_grow(img, BORDERWIDTH)

    shadow_layer = pdb.gimp_layer_new_from_visible(img, img, "shadow")
    pdb.gimp_image_insert_layer(img, shadow_layer, None, 1)
    pdb.gimp_edit_fill(shadow_layer, FOREGROUND_FILL)

    pdb.gimp_xcf_save(0, img, text_layer, fname, fname)
    pdb.gimp_image_delete(img)


# GIMP auto-execution stub
if __name__ == "__main__":
    import os, sys, subprocess

    scrdir = os.path.dirname(os.path.realpath(__file__))
    scrname = os.path.splitext(os.path.basename(__file__))[0]
    args = str(tuple(sys.argv[1:]))
    shcode_template = "import sys;sys.path.insert(0, '{scrdir}'); import {scrname}; {scrname}.{scrname}{args}".format(
        scrdir=scrdir, scrname=scrname, args=args
    )
    shcode = 'gimp-console -i --batch-interpreter python-fu-eval -b "{}" -b "pdb.gimp_quit(1)"'.format(
        shcode_template
    )
    print("Running command:\n{}\n".format(shcode))
    sys.exit(subprocess.call(shcode, shell=True))
else:
    from gimpfu import *
