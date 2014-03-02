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

from media import Media
from movie import Movie
from book import Book
from music import Music

book_re = re.compile(r"http://book.douban.com.*")
movie_re = re.compile(r"http://movie.douban.com.*")
music_re = re.compile(r"http://music.douban.com.*")

common_re = re.compile(r"http://(.+).douban.com.*")
no_media_page_re = re.compile(r"<title>页面不存在</title>")

dump_file = "urlmgt"
douban_tv = "http://movie.douban.com/subject/{0}/"

start = 1000001
end = 2000000

#hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#       'Accept-Encoding': 'none',
#       'Accept-Language': 'en-US,en;q=0.8',
#       'Connection': 'keep-alive'}
#hdr = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
hdr = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
       #'Accept-Encoding':'gzip,deflate,sdch',
       'Accept-Language':'zh-CN,zh;q=0.8',
       'Cache-Control':'max-age=0',
       'Connection':'keep-alive',
       'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'}


class UrlManager(object):
    def __init__(self):
        self.failed_url_pool = {}
        self.ok_url_pool = {}
        self.redirect_url_pool = {}
        self.other_url_pool = {}
        self.last_access_time = datetime.now()
        self.magic = 0
        self.type_count = {}
    def url_used(self, url):
        return self.failed_url_pool.has_key(url) or \
               self.ok_url_pool.has_key(url) or \
               self.redirect_url_pool.has_key(url) or \
               self.other_url_pool.has_key(url)
            
    def get_pool_by_status(self, status):
        if status < 300 and status >= 200:
            return self.ok_url_pool
        elif status < 400 and status >= 300:
            return self.redirect_url_pool
        elif status < 500 and status > 400:
            return self.failed_url_pool
        else:
            return self.other_url_poll

    def get_pool_by_url(self, url):
        if self.ok_url_pool.has_key(url):
            return self.ok_url_pool
        elif self.failed_url_pool.has_key(url):
            return self.failed_url_poll
        elif self.redirect_url_pool.has_key(url):
            return redirect_url_pool
        elif self.other_url_pool.has_key(url):
            return other_url_pool
        else:
            return None

    def get_media(self, url):
        pool = get_pool_by_url(url)
        return pool[url] if pool is not None else None

    def addTypeCount(self, type, step=1):
        if self.type_count.has_key(type):
            self.type_count[type] += step
        else:
            self.type_count[type] = step

    def decTypeCount(self, type, step=1):
        if not self.type_count.has_key(type):
            return
        if self.type_count[type] < step:
            self.type_count.pop(type)
        else:
            self.type_count[type] -= step
            
        
    def append_media(self, url, status, media):
        if status == 403:
            return
        pool = self.get_pool_by_url(url)
        if pool is not None:
            m = pool[url]
            if m is None and media is None:
                return
            if m is not None and \
                (media is None or m.mytype != media.mytype):
                self.decTypeCount(m.mytype)
            pool.pop(url)
            
        pool = self.get_pool_by_status(status)
        pool[url] = media
        if media is not None:
            self.addTypeCount(media.mytype)
        self.last_access_time = datetime.now()

    def show_medias(self):
        '''only search from the ok pool'''
        print "show all medias:"
        for m in self.ok_url_pool:
            print repr(self.ok_url_pool[m])

    def __repr__(self):
        ok = len(self.ok_url_pool)
        failed = len(self.failed_url_pool)
        redirect = len(self.redirect_url_pool)
        other = len(self.other_url_pool)
        total = ok + failed + redirect + other
        s = "total %s of url accessed\n"%total
        s += "OK       : %s\n"%ok
        s += "FAILED   : %s\n"%failed
        s += "REDIRECT : %s\n"%redirect
        s += "OTHER    : %s\n"%other
        s += "last access time : %s\n"%self.last_access_time.strftime("%Y-%m-%d %H:%M:%S")

        s += "following %s types of media found:\n"%len(self.type_count.keys())
        s += "\n".join(["%s :\t%s"%(t, self.type_count[t]) for t in self.type_count.keys()])
        
        return s

def getMediaType(url):
    m = common_re.match(url)
    if not m:
        return 'other'
    return m.groups()[0]

def genMedia(id, url, source):
    media = None
    mytype = getMediaType(url)
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
        titles = try_re.findall(source)
        if len(titles) == 0:
            continue
        title = titles[0]
        break
    
    if title == '':
        print "no title found for id", id
        return None
    media.setTitle(title)

    return media

def writeResult():
    f = open("./movies", "a")
    #f.write([t.encode("utf-8") for t in titles])
    f.write("\n".join(titles))
    f.close()

def flushData():
    global titles
    writeResult()
    del titles
    gc.collect()
    titles = []

def dumpUrlmgt(dumpf):
    global urlmgt
    with open(dumpf, "wb") as f:
        pickle.dump(urlmgt, f, pickle.HIGHEST_PROTOCOL)

def loadUrlmgt(dumpf):
    try:
        with open(dumpf, "rb") as f:
            urlmgt = pickle.load(f)
    except Exception, e :
        return None
    return urlmgt

def validate_response(content, status):
    status = int(status)
    if status == 403:
        print "url forbidden"
        return False
    return True

def usage():
    print "%s <start> <end>"%(sys.argv[0])

if __name__ == "__main__":
    #start = 1000001
    #end = 7999999


    if len(sys.argv) != 3:
        usage()
        exit(1)

    start = int(sys.argv[1])
    end = int(sys.argv[2])

    print "spider start from %s to %s ..."%(start, end)
    time.sleep(2)

    urlmgt = loadUrlmgt(dump_file)
    if urlmgt is None:
        urlmgt = UrlManager()

    print "current url manager status"
    print repr(urlmgt)

    #while count < end:
    id_collection = [random.randrange(start, end+1) for n in xrange(start, end)]
    #print id_collection
    count = 0
    
    for myid in id_collection:
        url = douban_tv.format(myid)
        #print "\n[ %s ]"%url,
        if urlmgt.url_used(url):
            print "[already accessed]"
            continue
        print ''
        req = urllib2.Request(url, headers=hdr)
        status = 200
        real_url = None
        content = ''
        try:
            page = urllib2.urlopen(req)
            content = page.read()
            status = page.getcode()
            real_url = page.geturl()
            page.close()
        except urllib2.HTTPError, e:
            #print e.reason
            status = e.code
            real_url = url

        print "[ %s ]"%real_url
        if not validate_response(content, status):
            continue
        media = genMedia(myid, real_url, content)
        if real_url != url:
            #print "real url is %s, but access to is %s"%(real_url, url)
            urlmgt.append_media(real_url, status, None)

        urlmgt.append_media(real_url, status, media)
        if media is None:
            print "media is None for ", myid
            continue
            
        media.setParameters(content)

        print repr(media)
        
        
        #content = req.read()
        count += 1
        if (count % 20) == 0:
            print "\n----------- %s links processed -----------\n"%count
            dumpUrlmgt(dump_file)
        sleep_timer = random.uniform(0.3, 2.2)
        #print "sleep_timer", sleep_timer
        time.sleep(sleep_timer)

        #print content
    print repr(urlmgt)
    
    dumpUrlmgt(dump_file)

    urlmgt.show_medias()
    
