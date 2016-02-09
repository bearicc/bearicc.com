import os
import sys
import logging
import re
import traceback
import copy
import random

import requests
from lxml import etree
from urllib.parse import urlsplit

from setting import ROOT_DIR

def get_logger():
    logger = logging.getLogger('bearicc')
    if not logger.handlers:
        hdlr = logging.FileHandler(os.path.join(ROOT_DIR, 'bearicc.log'))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        hdlr.setLevel(logging.INFO)
        logger.addHandler(hdlr)
        logger.setLevel(logging.DEBUG)
    return logger

def resolve_http_redirect(url):
    try:
        response = requests.head(url, timeout=4, allow_redirects=True)
        return response.url
    except:
        logger.exception('')
        return url

def strip_link(link):
    key_link = urlsplit(link)
    key_link = key_link.netloc+key_link.path+key_link.query
    return key_link

# Get page using proxies
g_proxies_bak = []
g_proxies = copy.deepcopy(g_proxies_bak)
def get_page_response(url, timeout=5, stream=False):
    global g_proxies
    try:
        proxy = random.choice(g_proxies)
        response = requests.get(url, proxies={'http': proxy, 'https': proxy}, timeout=timeout, stream=stream)
    except Exception:
        g_proxies.remove(proxy)
        if g_proxies:
            logger.warning('HTTPError')
            return get_page_response(url, timeout=timeout, stream=stream)
        else:
            logger.warning('Failed to get page response: %s' % url)
            g_proxies = copy.deepcopy(g_proxies_bak)
            return None
    return response

def get_tree(url):
    htmlparser = etree.HTMLParser()
    if g_proxies:
        response = get_page_response(url, stream=True)
    else:
        response = requests.get(url, stream=True)
    response.raw.decode_content = True
    tree = etree.parse(response.raw, htmlparser)
    return tree

def get_element_text(e, sep=',', include=[], skip=[]):
    if not include and not skip:
        return ','.join(filter(None, map(str.strip, e.itertext())))
    else:
        return get_element_text2(e, sep, include, skip)

def get_element_text2(e, sep=',', include=[], skip=[]):
    text = []
    children = e.getchildren()
    for child in children:
        if include and type(child) == etree._Comment and 'comment' not in include:
            continue
        if include and type(child) != etree._Comment and child.tag.lower() not in include:
            continue
        if type(child) == etree._Comment and 'comment' in skip:
            continue
        if type(child) != etree._Comment and child.tag.lower() in skip:
            continue
        buf = get_element_text2(child, sep=sep, include=include, skip=skip)
        if buf:
            text.append(buf)
    if e.text:
        text.insert(0, e.text)
    if e.tail:
        text.append(e.tail)
    return sep.join(filter(None, map(str.strip, text)))

def get_bootstrap_version():
    v = ''
    url = 'http://getbootstrap.com/'
    tree = get_tree(url)
    buf = tree.xpath('//p[@class="version"]')
    if buf:
        buf = buf[0].text
        v = re.search('[0-9.]+',buf).group()
    return v

logger = get_logger()

if __name__ == '__main__':
    v = get_bootstrap_version()
    print(v)
    url = 'http://getbootstrap.com/'
    tree = get_tree(url)
    head = tree.xpath('//head')[0]
    print(get_element_text(head, skip=['comment', 'script']))
