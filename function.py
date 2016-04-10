#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re


class domain(object):

    def ip_address(self, ip):

        ret_dict = {}
        response = urllib2.urlopen("http://ip.cn/index.php?ip=" + ip).read()
        address = re.findall(r'</code>(.*?)</p>', response)[0]
        ret_dict['address'] = address[6:]
        geoip = re.findall(r'(GeoIP:.*?)</p>',response)[0]
        ret_dict['geoip'] = geoip

        return  ret_dict