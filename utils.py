# -*- coding: utf-8 -*-
import requests
import os
import magic
import tempfile
import re
import urllib2
import mimetypes


def ip_address(ip):
    ret_dict = {}
    response = urllib2.urlopen("http://ip.cn/index.php?ip=" + ip).read()
    address = re.findall(r'</code>(.*?)</p>', response)[0]
    ret_dict['address'] = address[6:]
    geoip = re.findall(r'(GeoIP:.*?)</p>',response)[0]
    ret_dict['geoip'] = geoip

    return  ret_dict


def fix_extension(file_path):
    type = magic.from_file(file_path, mime=True).decode("utf-8")
    extension = str(mimetypes.guess_extension(type, strict=False))
    if extension is not None:
        # I hate to have to use this s***, f*** jpe
        if '.jpe' in extension:
            extension = extension.replace('jpe', 'jpg')
        os.rename(file_path, file_path + extension)
        return file_path + extension
    else:
        return file_path

def download(url, type=None, params=None, headers=None):
    try:
        jstr = requests.get(url, params=params, headers=headers, stream=True)
        ext = os.path.splitext(url)[1]
        f = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        for chunk in jstr.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    except IOError as e:
        return None
    f.seek(0)
    if not ext:
        f.name = fix_extension(f.name)
    elif type == 'qr':
        f.name = fix_extension(f.name)
    file = open(f.name, 'rb')
    return file
