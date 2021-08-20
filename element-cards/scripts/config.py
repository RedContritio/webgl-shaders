#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

paths = {
    "root": "..{}".format(os.sep),
    "front": "..{}front{}".format(os.sep, os.sep),
    "cards": "..{}cards{}".format(os.sep, os.sep),
    "assets": "..{}assets{}".format(os.sep, os.sep),
    "front_test": "cached_front{}".format(os.sep),
    "back_test": "cached_back{}".format(os.sep),
}
