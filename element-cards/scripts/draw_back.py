#!/usr/bin/python
# -*- coding: UTF-8 -*-

from PIL import Image, ImageFont, ImageDraw
import os
import math
import re
import numpy as np
import utils
import config

paths = config.paths

foldl = utils.foldl

card_names = [
    filename[:-5] for filename in os.listdir(paths["cards"]) if filename.startswith("0")
]
card_names.sort()

tex_template_path = paths["assets"] + "tarot-back-normalized.png"

id_font_path = paths["assets"] + "Rokkitt-VariableFont_wght.ttf"

code_font_path = paths["assets"] + "FiraMono-Regular.ttf"

if not os.path.exists(paths["back_test"]):
    os.mkdir(paths["back_test"])


def DrawId(image, id_str):
    text_canvas = Image.new("1", image.size)
    draw = ImageDraw.Draw(text_canvas)

    id_msg = "{}".format(id_str)

    id_font_size = math.floor(22.0 * text_canvas.size[0] / 448)
    id_font = ImageFont.truetype(id_font_path, size=id_font_size)

    id_color = (226, 226, 226, 255)

    w, h = draw.textsize(id_msg, font=id_font)
    title_position = (
        0.141 * text_canvas.size[0] - 0.5 * w,
        0.090 * text_canvas.size[1] - 0.5 * h,
    )

    draw.text(title_position, id_msg, 1, font=id_font)

    text_array = np.array(text_canvas)
    image_array = np.array(image)

    for i in range(image_array.shape[0]):
        ri = text_array.shape[0] - 1 - i
        for j in range(image_array.shape[1]):
            rj = text_array.shape[1] - 1 - j
            # 中心对称的两个数字
            if text_array[i, j] or text_array[ri, rj]:
                image_array[i, j] = id_color

    return Image.fromarray(image_array)


def DrawCode(image, content):
    im = image.copy()
    draw = ImageDraw.Draw(im)

    code_font_size = math.floor(11.0 * im.size[0] / 448)
    code_font = ImageFont.truetype(code_font_path, size=code_font_size)

    textsizes = [draw.textsize(code, font=code_font) for code in content]
    space_size = 2
    code_position_x = 0.112 * im.size[0]
    code_position_y = 0.5 * im.size[1] - 0.5 * (
        foldl(lambda s, sz: s + sz[1], 0, textsizes) + (len(textsizes) - 1) * space_size
    )

    normal_color = (255, 255, 255)
    keyword_color = (0xB1, 0x9F, 0x5F)
    for i in range(len(content)):
        words = [word for word in re.split("(\W)", content[i]) if word and len(word) > 0]
        cur_x = code_position_x
        for word in words:
            draw.text(
                (cur_x, code_position_y),
                word,
                (keyword_color if utils.isKeyWord(word) else normal_color),
                font = code_font,
            )
            cur_x += draw.textsize(word, font=code_font)[0]
        code_position_y += space_size + textsizes[i][1]

    return im


if __name__ == "__main__":
    tex_template = Image.open(tex_template_path)
    tex_template = tex_template.resize([4 * v for v in tex_template.size])

    # card_names = ["046-the_world"]
    for card_name in card_names:
        source_path = paths["cards"] + card_name + ".frag"
        # read the code
        with open(source_path, "r") as f:
            codelines = f.readlines()

        meta = utils.getMetaFromFrag(card_name, codelines)

        print("\n" + card_name)
        [print(key, ":", value) for key, value in meta.items()]  # line by line print
        # [print(code, end='') for code in meta['codes']]  # print code line by line

        # clone the image
        im = tex_template.copy()

        im = DrawId(im, card_name[1:3])

        content = meta['codes']
        if len(meta['deps']) > 0:
            content = ["// Deps  {}".format(" ".join(meta["deps"]))] + content
        # print(content)

        im = DrawCode(im, content)

        im.save(paths["back_test"] + card_name + ".png")
        # break