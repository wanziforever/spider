#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def two_steps_capture(myres1, myres2, content):
    for r1 in myres1:
        m = r1.search(content)
        if m:
            for r2 in myres2:
                l = r2.findall(m.group(1))
                if len(l) == 0:
                    continue
                return l
    return []

def one_step_capture(myres, content):
    for r in myres:
        m = r.search(content)
        if m:
            return m.group(1)
    return ""

def wrap_html_special_words(s):
    if isinstance(s, str):
        return re.sub("&nbsp;", "", s.strip())
    if isinstance(s, (list, tuple)):
        new = []
        for i in s:
            new.append(wrap_html_special_words(i))
        return new
