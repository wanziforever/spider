#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class Media(object):
    title_re_try_list = [re.compile(r"<span property=\"v:itemreviewed\">(.+)</span>"),
                         re.compile(r"^\s*<title>[\n\r]*\s*(.*)\s+\(豆瓣\)[\n\r]*</title>", re.MULTILINE)]
    #title_re_try_list = [re.compile(r"<span property=\"v:itemreviewed\">(.+)</span>")]

    
    def __init__(self, id, t):
        self.id = id
        self.title=""
        self.mytype = t
        self.year=""

    def setTitle(self, t):
        if not isinstance(t, str):
            self.title = t.encode('utf-8')
        else:
            self.title = t
    def setParameters(self, content):
        pass
        
    def __repr__(self):
        s = 'Media: %s, ID: %s, Title: %s'%(self.mytype, self.id, self.title)
        return s
    
