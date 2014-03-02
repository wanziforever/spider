#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import os
import sys
import gc
import pickle
from  datetime import datetime
import time
import random
from spider import dump_file, UrlManager

from media import Media
from movie import Movie
from book import Book
from music import Music

book_re = re.compile(r"http://book.douban.com.*")
movie_re = re.compile(r"http://movie.douban.com.*")
music_re = re.compile(r"http://music.douban.com.*")

common_re = re.compile(r"http://(.+).douban.com.*")
no_media_page_re = re.compile(r"<title>页面不存在</title>")

urlmgt = None

def loadUrlmgt(dumpf):
    try:
        with open(dumpf, "rb") as f:
            urlmgt = pickle.load(f)
    except Exception, e :
        return None
    return urlmgt


def call_query():
    global urlmgt
    urlmgt = loadUrlmgt(dump_file)
    if urlmgt is None:
        print "fail to read data file ", dump_file
        exit(1)
    print repr(urlmgt)

if __name__ == "__main__":
    call_query()
