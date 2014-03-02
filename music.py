#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from media import Media
from utils import *

class Music(Media):
    mytype = "music"
    #director_re = re.compile(r'''<span><span class='pl'>导演</span>: (?:<a href=".+" rel="v:directedBy">(.+)</a>)+</span>''')
    player1_re_try_list = [re.compile(r'''<span class="pl">[\n\r\s]*表演者:[\n\r\s]*((?:[\n\r\s]*.*[\n\r\s]*)+?)</span>''', re.MULTILINE)]
    #player1_re_try_list = [re.compile(r'''<span class="pl">[\n\r\s]* 表演者:[\n\r\s]*(.*)[\n\r\s]*</span>''', re.MULTILINE)]
    player2_re_try_list = [re.compile(r'''<a href=".+?">(.+?)\</a>''')]
    publisher_re_try_list = [re.compile(r'''<span class="pl">[\n\r\s]* 出版者:[\n\r\s]*<a href="(?:.*)">(.*)</a>[\n\r\s]*</span>''', re.MULTILINE)]
    length_re_try_list = [re.compile(r'''<span class="pl">唱片数:</span>(.*)[\n\r\s]*<br />''')]
    pubdate_re_try_list = [re.compile(r'''<span class="pl">发行时间:</span>(.*)[\n\r\s]*<br /''')]
    summary_re_try_list = [re.compile(r'''<span property="v:summary">(.*)</span>''', re.MULTILINE)]

    def __init__(self, id):
        super(Music, self).__init__(id, 'music')
        self.player = []
        self.pulisher = ""
        self.pubdate = ""
        self.length = ""
        self.summary = ""

    def setParameters(self, content):
        self.players = two_steps_capture(Music.player1_re_try_list,
                                         Music.player2_re_try_list, content)
        self.publisher = one_step_capture(Music.publisher_re_try_list, content)
        self.pubdate = one_step_capture(Music.pubdate_re_try_list, content)
        self.length = one_step_capture(Music.length_re_try_list, content)
        self.summary = one_step_capture(Music.summary_re_try_list, content)

        self.wrap_properties()

    def wrap_properties(self):
        self.players = wrap_html_special_words(self.players)
        self.pubdate = wrap_html_special_words(self.pubdate)
        self.length = wrap_html_special_words(self.length)
        self.summary = wrap_html_special_words(self.summary)

    def __repr__(self):
        s = super(Music, self).__repr__() + "\n"
        s += "players: %s\n"%(", ".join(self.players))
        s += "publisher: %s\n"%(self.publisher)
        s += "pubdate: %s\n"%(self.pubdate)
        s += "length: %s\n"%(self.length)
        s += "summary: %s\n"%(self.summary)
        return s
    
