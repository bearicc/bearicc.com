import requests
from lxml import etree
import re

def getTree(url):
    htmlparser = etree.HTMLParser()
    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    tree = etree.parse(response.raw, htmlparser)

    return tree

def getBootstrapVesrion():
    v = ''
    url = 'http://getbootstrap.com/'
    tree = getTree(url)
    buf = tree.xpath('//p[@class="version"]')
    if buf:
        buf = buf[0].text
        v = re.search('[0-9.]+',buf).group()
    return v

if __name__ == '__main__':
    print(getBootstrapVesrion())
