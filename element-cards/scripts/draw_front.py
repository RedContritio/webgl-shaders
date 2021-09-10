#!/usr/bin/python
# -*- coding: UTF-8 -*-

from PIL import Image, ImageFont, ImageDraw
import os
import math
import numpy as np
import utils
import config

paths = config.paths

foldl = utils.foldl

title_font_path = paths["assets"] + "Alegreya-VariableFont_wght.ttf"
number_font_path = paths["assets"] + "CrimsonText-Regular.ttf"

card_names = [
    filename[:-5] for filename in os.listdir(paths["cards"]) if filename.startswith("0")
]
card_names.sort()

if not os.path.exists(paths["front_test"]):
    os.mkdir(paths["front_test"])


def drawTitle(image, title):
    im = image.copy()
    draw = ImageDraw.Draw(im)

    title_msg = title.upper()

    title_color = (0, 0, 0)

    title_font_size = math.floor(22.0 * im.size[0] / 448)
    title_font_big_size = math.floor(1.4 * title_font_size)
    title_small_font = ImageFont.truetype(title_font_path, size=title_font_size)
    title_big_font = ImageFont.truetype(title_font_path, size=title_font_big_size)

    textsizes = []
    words = title_msg.split()
    for word in words:
        if len(textsizes) > 0:
            textsizes.append(draw.textsize(' ', font=title_small_font))
        textsizes.append(draw.textsize(word[0], font=title_big_font))
        textsizes.append(draw.textsize(word[1:], font=title_small_font))

    height = max([sz[1] for sz in textsizes])
    height_small = min([sz[1] for sz in textsizes])
    title_position_x = 0.5 * im.size[0] - 0.5 * foldl(lambda s, sz: s + sz[0], 0, textsizes)
    title_position_y = 0.895 * im.size[1] - 0.5 * height

    height_offset = 0.6
    i = 0
    j = 0
    while i < len(textsizes):
        word = words[j]
        if j > 0:
            draw.text((title_position_x, title_position_y + height_offset * (height - height_small)), ' ', title_color, font=title_small_font)
            title_position_x = title_position_x + textsizes[i][0]
            i = i + 1
        draw.text((title_position_x, title_position_y), word[0], title_color, font=title_big_font)
        title_position_x = title_position_x + textsizes[i][0]
        i = i + 1
        draw.text((title_position_x, title_position_y + height_offset * (height - height_small)), word[1:], title_color, font=title_small_font)
        title_position_x = title_position_x + textsizes[i][0]
        i = i + 1
        j = j + 1

    return im


def drawNumber(image, number):
    im = image.copy()
    draw = ImageDraw.Draw(im)

    number_font_size = math.floor(30.0 * im.size[0] / 448)
    number_font = ImageFont.truetype(number_font_path, size=number_font_size)
    w, h = draw.textsize(number, font=number_font)
    number_image = Image.new("1", im.size)
    number_mask = ImageDraw.Draw(number_image)
    number_position = (0.5 * (im.size[0] - w), 0.093 * im.size[1] - 0.5 * h)
    number_mask.text(number_position, number, 1, font=number_font)
    # number_image.save('number_mask.png')

    return utils.InvertRGBA(im, number_image)


if __name__ == "__main__":
    for card_name in card_names:
        image_path = paths["front"] + card_name + ".png"
        source_path = paths["cards"] + card_name + ".frag"
        # read the code
        with open(source_path, "r") as f:
            codes = f.readlines()

        meta = utils.getMetaFromFrag(card_name, codes)

        print(card_name)
        [print(key, ":", value) for key, value in meta.items()]  # line by line print

        # read the image
        im = Image.open(image_path)

        im = drawTitle(im, meta["title"])
        if "number" in meta:
            im = drawNumber(im, "- {} -".format(meta["number"]))

        im.save(paths["front_test"] + card_name + ".png")
        # break
