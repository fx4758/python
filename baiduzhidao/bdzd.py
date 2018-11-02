from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import media, posts
from urllib.parse import quote
from requests_html import HTMLSession
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

#网页下载
def htmldown(url):
    html = HTMLSession().get(url).html
    return html

#发布到wordpress模块，支持标题，内容，自定义字段
def post_to_wp(title,content,field):
    wp = Client('http://127.0.0.1/xmlrpc.php','admin','199011')  #办公室111
    post = WordPressPost()
    post.post_status = 'publish'
    post.terms_names ={'category':['西藏旅游问答']}

    post.title = title
    post.content = content
    post.custom_fields = field

    post.id = wp.call(posts.NewPost(post))
    print(str(title) + '\nhttp://127.0.0.1/?p=' + str(post.id) + '\n')

#页面单页解析
def jiexi(url):
    print('开始采集：'+str(url))
    html = htmldown(url)
    try:
        title = html.find('span.ask-title')[0].text

        content = html.find('.content .best-text')[0].html
        content = re.sub('<(d|s|h|/|p|a|li|ol|ul).*?>','',content)
        content = re.sub('展开全部','',content)
        content = re.sub('\n+([\s\S]*?)','',content)
        content = re.sub('(class|esrc)=".*?"','',content)
        content = re.sub(' +',' ',content)
        content = re.sub('<b[\s\S]*?>','\n\n',content)
        content = re.sub('(<img[\s\S]*?>)','\n\n\g<1>\n\n',content)

        field = []
        field.append({
            'key':'via',
            'value':url,
        })

        post_to_wp(title,content,field)

    except:
        print('出现异常，跳过。\n\n')

#关键词转码为GBK编码，并生成转码后的列表
def zhuanma():
    yswords = ['西藏旅游','布达拉宫','林芝','拉萨','西藏','入藏函','外国人到西藏']
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