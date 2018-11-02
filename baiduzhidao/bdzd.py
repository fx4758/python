from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import media, posts
from urllib.parse import quote
from requests_html import HTMLSession
import re
import ssl
from tomorrow import threads

ssl._create_default_https_context = ssl._create_unverified_context

wp = Client('http://127.0.0.1/xmlrpc.php','admin','111')
post = WordPressPost()
post.post_status = 'publish'
post.terms_names ={'category':['西藏旅游问答']}


def htmldown(url):
    html = HTMLSession().get(url).html
    return html

def jiexi(url):
    html = htmldown(url)
    title = html.find('span.ask-title')[0].text

    content = html.find('.content .best-text')[0].html
    content = re.sub('<(d|s|h|/|p|a).*?>','',content)
    content = re.sub('展开全部','',content)
    content = re.sub('\n+([\s\S]*?)','',content)
    content = re.sub('(class|esrc)=".*?"','',content)
    content = re.sub(' +',' ',content)
    content = re.sub('\n','\n\n',content)

    post.title = title
    post.content = content
    post.custom_fields = []
    post.custom_fields.append({
        'key':'via',
        'value':url,
    })

    post.id = wp.call(posts.NewPost(post))
    print(str(title)+'\nhttp://127.0.0.1/?p='+str(post.id)+'\n')

def zhuanma():
    yswords = ['西藏旅游','布达拉宫','林芝']
    zmwords = []
    for ysword in yswords:
        ysword = ysword.encode('GBK','replace')
        ysword = quote(ysword)
        zmwords.append(ysword)
    return zmwords

def run(keyword):
    max_page = 760
    x = 0
    while(x < max_page):
        page_url = ('https://zhidao.baidu.com/search?word=' + str(keyword) + '&ie=gbk&site=-1&sites=0&date=0&pn=' + str(
            x))
        html = htmldown(page_url)
        links = html.find('a.ti')
        for i in links:
            url = i.attrs['href']
            if 'zhidao' in url:
                jiexi(url)
        x = x + 10

for keyword in zhuanma():
    run(keyword)