#!/usr/bin/env python
# -.- coding: utf-8 -.-

"""
twbulo
======
get tribes data from `臺灣原住民族資訊資源網 <http://www.tipp.org.tw/formosan/tribe/tribe.jspx>`__

Usage
=====
$ twbulo - parse tribe name only
$ twbulo kml - get kml

Requirements
============
* Python 2.6.x
* BeautifulSoup 3.2.0

Author
======
Suhen Lee <moogoo78 at gmail.com>

ChangeLog
=========
* 2011-11-10 created
"""

import urllib2, re, os, os.path, sys
from BeautifulSoup import BeautifulSoup

BASE_URL = 'http://www.tipp.org.tw/'
START_URL = 'http://www.tipp.org.tw/formosan/tribe/tribe.jspx'
KML_DIR = 'get_kml'


def get_soup(url):
    print "scrapping...\n%s" % url
    res = urllib2.urlopen(url)
    html = res.read()

    return BeautifulSoup(''.join(html))

def save_file(fname, data):
    if os.path.exists(KML_DIR) == 0:
        os.mkdir(KML_DIR)
    f = open(os.path.join(KML_DIR, fname), 'w')
    f.write(data)
    f.close()

def get_kml(kml_url, gname, n_kml):
    kml_url = kml_url + '&output=kml'
    #soup4 = get_soup(kml_url, True)
    res = urllib2.urlopen(kml_url)
    html = res.read()
    soup4 = BeautifulSoup(''.join(html))
    if soup4.find('name'):
        n_kml += 1
        fname = "%s_%s.kml" % (gname, soup4.find('name').text)
        save_file(fname, html)
    else:
        print 'unknown map'

    return n_kml

def get_tribes(flag_kml=False):
    num = 0
    num_have_map = 0
    num_have_gmap = 0
    num_have_kml = 0

    # 首頁 > 認識原住民 > 部落介紹 > 依族群選擇
    soup = get_soup(START_URL)
    tribe_groups = soup.findAll(name='a',
                                attrs={'href':re.compile('tribe_detail1\.jspx')})
    # 部落列表
    for g in tribe_groups:
        print "%s\n============" % g.text
        soup2 = get_soup(BASE_URL + g.attrs[0][1])
        tribes = soup2.findAll(name='a',
                               attrs={'href':re.compile('tribe_detail3\.jspx')})
        for t in tribes:
            num += 1
            print "%s" % t.text
            soup3 = get_soup(BASE_URL + t.attrs[0][1])
            emap = soup3.find(lambda tag: (tag.text) == u'部落電子地圖')
            if emap: 
                num_have_map += 1
                if re.search('maps.google.com.tw', emap.attrs[0][1]):
                    num_have_gmap += 1
                    if flag_kml:
                        num_have_kml = get_kml(emap.attrs[0][1], g.text, num_have_kml)
                else:
                    print "no map"

    print '------------------------------'
    print 'total tribes: %d' % num
    print 'tribes have map: %d' % num_have_map
    print 'tribes have google maps: %d' % num_have_gmap
    print 'tribes have kml: %d' % num_have_kml


if __name__ == '__main__':
    if len(sys.argv) > 1:
        get_tribes(sys.argv[1])
    else:
        get_tribes()
