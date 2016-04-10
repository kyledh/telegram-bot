#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re


class domain(object):
    def ip_address(self, ip):

        ret_dict = {}
        response = urllib2.urlopen("http://ip.cn/index.php?ip=" + ip).read()

        ret_dict['address'] = re.findall(r'</code>(.*?)</p>', response)
        ret_dict['geoip'] = re.findall(r'(GeoIP:.*?)</p>',response)

        return  ret_dict