#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
from media import Media
from utils import *

class Movie(Media):
    mytype = "movie"
    director1_re_try_list = [re.compile(r'''<span class=['"]pl['"]>[\n\r\s]*导演</span>:(.*)</span>''', re.MULTILINE)]
    director2_re_try_list = [re.compile(r'''<a href=".+?" rel=".+?">(.+?)</a>''')]
    writer1_re_try_list = [re.compile(r'''<span><span class='pl'>编剧</span>: (.+)</span>''')]
    writer2_re_try_list = [re.compile(r'''<a href=".+?">(.+?)\</a>''')]
    actor1_re_try_list = [re.compile(r'''<span><span class='pl'>主演</span>: (.+)</span>''')]
    actor2_re_try_list = [re.compile(r'''<a href=".+?" rel=".+?">(.+?)</a>''')]
    type1_re_try_list = [re.compile(r'''<span class="pl">类型:</span> (.+)<br/>''')]
    type2_re_try_list = [re.compile(r'''<span property="v:genre">(.*?)</span>''')]
    region_re_try_list = [re.compile(r'''<span class="pl">制片国家/地区:</span>(.+)<br/>''')]
    language_re_try_list = [re.compile(r'''<span class="pl">语言:</span>(.+)<br/>''')]
    pubdate_re_try_list = [re.compile(r'''<span class="pl">上映日期:</span> <span property="(?:.+?)" content="(?:.+)">(.+)</span><br/>''')]
    length_re_try_list = [re.compile(r'''<span class="pl">片长:</span> <span property="v:runtime" content="(?:.*?)">(.+)</span><br/>''')]
    #summary_re_try_list = [re.compile(r'''<span property="v:summary" class="">\s*[\n\r]*\s*(.+)[\n\r]*\s*</span>''', re.MULTILINE)]
    summary_re_try_list = [re.compile(r'''<span property="v:summary" class="">(([\n\r\s]*.*[\n\r\s]*)+?)</span>''', re.MULTILINE)]
    def __init__(self, id):
        super(Movie, self).__init__(id, 'movie')
        self.stars = []
        self.directors = []
        self.writers = []
        self.region = ""
        self.genres = []
        self.language = ""
        self.pubdate = ""
        self.length = ""
        self.summary = ""
        self.plays = []

    def setParameters(self, content):
        self.directors = two_steps_capture(Movie.director1_re_try_list,
                                           Movie.director2_re_try_list, content)
        self.writers = two_steps_capture(Movie.writer1_re_try_list,
                                         Movie.writer2_re_try_list, content)
        self.stars = two_steps_capture(Movie.actor1_re_try_list,
                                       Movie.actor2_re_try_list, content)
        self.genres = two_steps_capture(Movie.type1_re_try_list,
                                        Movie.type2_re_try_list, content)
        self.region = one_step_capture(Movie.region_re_try_list, content)
        self.language = one_step_capture(Movie.language_re_try_list, content)
        self.pubdate = one_step_capture(Movie.pubdate_re_try_list, content)
        self.length = one_step_capture(Movie.length_re_try_list, content)
        self.summary = one_step_capture(Movie.summary_re_try_list, content)

        self.wrap_properties()

    def wrap_properties(self):
        self.directors = wrap_html_special_words(self.directors)
        self.writers = wrap_html_special_words(self.writers)
        self.stars = wrap_html_special_words(self.stars)
        self.genres = wrap_html_special_words(self.genres)
        self.region = wrap_html_special_words(self.region)
        self.language = wrap_html_special_words(self.language)
        self.length = wrap_html_special_words(self.length)
        self.summary = wrap_html_special_words(self.summary)
        
    def __repr__(self):
        s = super(Movie, self).__repr__() + "\n"
        s += "directors: %s\n"%(", ".join(self.directors))
        s += "wirters: %s\n"%(", ".join(self.writers))
        s += "stars: %s\n"%(", ".join(self.stars))
        s += "genres: %s\n"%(", ".join(self.genres))
        s += "region: %s\n"%(self.region)
        s += "languange: %s\n"%(self.language)
        s += "pubdate: %s\n"%(self.pubdate)
        s += "length: %s\n"%(self.length)
        s += "summary: %s"%(self.summary)
        return s
    
if __name__ == "__main__":
    import urllib2
    myid = 1307011
    url = "http://movie.douban.com/subject/{0}/".format(myid)
    hdr = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
       #'Accept-Encoding':'gzip,deflate,sdch',
       'Accept-Language':'zh-CN,zh;q=0.8',
       'Cache-Control':'max-age=0',
       'Connection':'keep-alive',
       'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'}
    req = urllib2.Request(url, headers=hdr)
    page = urllib2.urlopen(req)
    content = page.read()
    from spider import genMedia
    media = genMedia(myid, url, content)
    media.setParameters(content)
    print "[ %s ]"%url
    print repr(media)
    
