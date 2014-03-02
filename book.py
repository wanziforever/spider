#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from media import Media
from utils import *

class Book(Media):
    mytype = "book"
    #author1_re_try_list = [re.compile(r'''<span>[\n\r\s]*<span class="pl"> 作者</span>:[\n\r\s]*(.*)[\n\r\s]*</span>''', re.MULTILINE)]
    author1_re_try_list = [re.compile(r'''<span class="pl">[\n\r\s]*作者</span>:[\n\r\s]*((?:[\n\r\s]*.*[\n\r\s]*)+?)</span>''', re.MULTILINE)]
    author2_re_try_list = [re.compile(r'''<a class="" href=".+?">(.+?)\</a>''')]
    publisher_re_try_list = [re.compile(r'''<span class="pl">出版社:</span>(.+)<br/>''')]
    pubdate_re_try_list = [re.compile(r'''<span class="pl">出版年:</span>(.+)<br/>''')]
    length_re_try_list = [re.compile(r'''<span class="pl">页数:</span>(.+)<br/>''')]
    #summary_re_try_list = [re.compile(r'''<div class="intro">[\n\r\s]*(.*?)<p>(?:<a(?:.*?)</a>)*</p></div>''', re.MULTILINE)]
    summary_re_try_list = [re.compile(r'''<div class="intro">[\n\r\s]*(.*?)(?:<p><a(?:.*?)</a></p>)*</div>''', re.MULTILINE)]

    def __init__(self, id):
        super(Book, self).__init__(id, 'book')
        self.authors = []
        self.publisher = ""
        self.pubdate = ""
        self.length = ""
        self.summary = ""
        
    def setParameters(self, content):
        self.authors = two_steps_capture(Book.author1_re_try_list,
                                         Book.author2_re_try_list, content)
        self.publisher = one_step_capture(Book.publisher_re_try_list, content)
        self.pubdate = one_step_capture(Book.pubdate_re_try_list, content)
        self.length = one_step_capture(Book.length_re_try_list, content)
        self.summary = one_step_capture(Book.summary_re_try_list, content)

        self.wrap_properties()

    def wrap_properties(self):
        self.authors = wrap_html_special_words(self.authors)
        self.publisher = wrap_html_special_words(self.publisher)
        self.pubdate = wrap_html_special_words(self.pubdate)
        self.length = wrap_html_special_words(self.length)
        self.summary = wrap_html_special_words(self.summary)

    def __repr__(self):
        s = super(Book, self).__repr__() + "\n"
        s += "authors: %s\n"%(", ".join(self.authors))
        s += "publisher: %s\n"%(self.publisher)
        s += "pubdate: %s\n"%(self.pubdate)
        s += "length: %s\n"%(self.length)
        s += "summary: %s\n"%(self.summary)
        return s
        
if __name__ == "__main__":
    import urllib2
    myid = 1957586
    url = "http://book.douban.com/subject/{0}/".format(myid)
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
    
