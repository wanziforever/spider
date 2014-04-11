#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from media import Media
from utils import *

common_re = re.compile(r"http://(.+).douban.com.*")
no_media_page_re = re.compile(r"<title>页面不存在</title>")
class Book(Media):
    mytype = "book"
    #author1_re_try_list = [re.compile(r'''<span>[\n\r\s]*<span class="pl"> 作者</span>:[\n\r\s]*(.*)[\n\r\s]*</span>''', re.MULTILINE)]
    author1_re_try_list = [re.compile(r'''<span class="pl">[\n\r\s]*作者</span>:[\n\r\s]*((?:[\n\r\s]*.*[\n\r\s]*)+?)</span>''', re.MULTILINE)]
    author2_re_try_list = [re.compile(r'''<a class="" href=".+?">(.+?)\</a>''')]
    publisher_re_try_list = [re.compile(r'''<span class="pl">出版社:</span>(.+)<br/>''')]
    pubdate_re_try_list = [re.compile(r'''<span class="pl">出版年:</span>(.+)<br/>''')]
    length_re_try_list = [re.compile(r'''<span class="pl">页数:</span>(.+)<br/>''')]
    #summary_re_try_list = [re.compile(r'''<div class="intro">[\n\r\s]*(.*?)<p>(?:<a(?:.*?)</a>)*</p></div>''', re.MULTILINE)]
    summary_re_try_list = [re.compile(r'''<div class="intro">[\n\r\s]*(.*?)(?:<p><a(?:.*?)</a></p>)*</div>''', re.MULTILINE),
                           re.compile(r'''<div class="indent" id="dir_(.*)_full" style="display:none">((?:[\n\r\s]*.*[\n\r\s]*)+?)</div>''')]

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

def getMediaType(url):
    m = common_re.match(url)
    if not m:
        return 'other'
    return m.groups()[0]

def genMedia(id, url, source):
    media = None
    mytype = getMediaType(url)
    print "mytype", mytype
    if mytype == Book.mytype:
        media = Book(id)
    elif mytype == Movie.mytype:
        media = Movie(id)
    elif mytype == Music.mytype:
        media = Music(id)
    else:
        return None

    no_media = no_media_page_re.findall(source)
    if len(no_media) >= 1:
        print "no media found"
        return None

    title = ''
    count = 0
    for try_re in Media.title_re_try_list:
        m = try_re.search(source)
        if m:
            title = m.group(1)
            break
    
    if title == '':
        print "no title found for id", id
        return None
    media.setTitle(title)

    return media

if __name__ == "__main__":
    import httplib2
    myid = 1025032
    url = "http://book.douban.com/subject/{0}/".format(myid)
    hdr = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
       #'Accept-Encoding':'gzip,deflate,sdch',
       'Accept-Language':'zh-CN,zh;q=0.8',
       'Cache-Control':'max-age=0',
       'Connection':'keep-alive',
       'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36',
       'Cookie': "bid=\"E11cH5Legjk\"; ll=\"108302\"; viewed=\"1007772_3071264_5367515\"; ct=y; dbcl2=\"43826175:/xpuV6WQbyc\"; ck=\"HCIT\"; push_noty_num=0; push_doumail_num=4; __utma=30149280.421945324.1388474197.1393763318.1393807114.61; __utmb=30149280.9.10.1393807114; __utmc=30149280; __utmz=30149280.1393742261.57.30.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=30149280.4382; __utma=81379588.707195876.1388474197.1393763318.1393807114.19; __utmb=81379588.2.10.1393807114; __utmc=81379588; __utmz=81379588.1391234397.5.5.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/43826175/"}
    req = httplib2.Http()
    resp, content = req.request(url, headers=hdr)
    status = int(resp['status'])
    print "[ %s ]"%url
    if status >= 400:
        print "fail response with status", status
        exit(1)
    #from spider import genMedia
    media = genMedia(myid, url, content)
    if media is None:
        "fail to gen media"
    media.setParameters(content)
    print repr(media)
    
