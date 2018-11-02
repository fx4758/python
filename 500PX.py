from requests_html import HTMLSession
from requests_html import HTML
import datetime
from selenium import webdriver
import re

def down_html(url):

    chrome_options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)

    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.maximize_window()
    browser.get(url)
    html = HTML(html=browser.page_source)
    browser.quit()
    return html

def down_img(url):
    name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'_'+str(hash(url))
    name = re.sub('-','',name)
    try:
        bit = HTMLSession().get(url).content
    except:
        pass
    else:
        f = open('E:/500px/'+str(name)+'.jpeg','wb')
        f.write(bit)
        f.close()
        print('E:/500px/'+str(name)+'.jpeg')

url = input('input:')
html = down_html(url)
img = html.find('.photo',first=True)
img = img.attrs['src']
down_img(img)