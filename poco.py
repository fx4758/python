import sys
sys.path.append("/usr/local/lib/python3.6/site-packages")

from requests_html import HTMLSession
import datetime
from tomorrow import threads
import re

def down_html(url):
    html = HTMLSession().get(url).html
    return html

@threads(10)
def down_photo(url):
    photo_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'_'+str(hash(url))
    photo_name = re.sub('-','',photo_name)
    try:
        photo_content = HTMLSession().get(url).content
    except:
        pass
    else:
        file = open('E:/poco/'+str(photo_name)+'.jpg','wb')
        file.write(photo_content)
        file.close()

url = input('输入poco页面地址：')
html = down_html(url)
img_list = html.find('img')
for i in img_list:
    if 'data-src' in i.html:
        if i.attrs['data-src'].strip() != '':
            url = i.attrs['data-src']
            url = 'http:'+str(url)
            print(url)
            down_photo(url)
