from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import media, posts
from urllib.parse import quote
from requests_html import HTMLSession
import re
import ssl
from langconv import *

ssl._create_default_https_context = ssl._create_unverified_context

#网页下载
def htmldown(url):
    html = HTMLSession().get(url).html
    return html

#简体转换为繁体
def jt_to_ft(line):
    line = Converter('zh-hant').convert(line)
    line.encode('utf-8')
    return line


wp = Client('https://tibetdreamtravel.wordpress.com/xmlrpc.php','aimlokr','910409hbHS')  #办公室111
post = WordPressPost()
post.post_status = 'publish'
post.terms_names ={'category':['西藏旅游问答']}

#页面单页解析
def jiexi(url):
    try:
        print('开始采集：'+str(url))
        html = htmldown(url)
        title = html.find('span.ask-title')[0].text
        title = jt_to_ft(title)

        content = html.find('.content .best-text')[0].html
        content = re.sub('<(d|s|h|/|p|a|li|ol|ul).*?>','',content)
        content = re.sub('展开全部','',content)
        content = re.sub('\n+([\s\S]*?)','',content)
        content = re.sub('(class|esrc)=".*?"','',content)
        content = re.sub(' +',' ',content)
        content = re.sub('<b[\s\S]*?>','\n\n',content)
        content = re.sub('(<img[\s\S]*?>)','\n\n\g<1>\n\n',content)
        content = jt_to_ft(content)

        pic_list = re.findall('src="(.*?)"',content)
        for pic in pic_list:
            date = {
                'name':str(hash(pic))+'.jpeg',
                'type':'image/jpeg',
            }
            date['bits'] = HTMLSession().get(pic).content
            repson = wp.call(media.UploadFile(date))
            content = re.sub(pic,repson['url'],content)
            pic_id = []
            pic_id.append(repson['id'])
            print(repson['url'])

        field = []
        field.append({
            'key':'via',
            'value':url,
        })

        post.title = title
        post.content = content
        post.custom_fields = field

        post.id = wp.call(posts.NewPost(post))
        print(str(title) + '\nhttps://tibetdreamtravel.wordpress.com/?p=' + str(post.id) + '\n')

    except:
        print('出现异常，跳过。\n\n')

#关键词转码为GBK编码，并生成转码后的列表
def zhuanma():
    yswords = ['西藏旅游','布达拉宫','林芝','拉萨','西藏','入藏函','外国人到西藏','台湾人到西藏旅游','香港人到西藏','华人到西藏','入藏证','西藏边防证']
    zmwords = []
    for ysword in yswords:
        ysword = ysword.encode('GBK','replace')
        ysword = quote(ysword)
        zmwords.append(ysword)
    return zmwords

#生成列表页，从列表页中获取单页
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

#从转码后的列表中获取单独关键词，进行采集发布
for keyword in zhuanma():
    run(keyword)