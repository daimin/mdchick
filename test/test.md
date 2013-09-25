今天将原来的博客的博文全部移植到了 [codecos](codecos.com) 上面，其实blogjava.net里面有功能的，它是导出为xml，可是我看导出后的xml，解析起来，还要比直接解析html麻烦些，所以还是用python写了一个抓取的脚本。

脚本的功能用到了多线程、urllib2进行GET请求，urllib2、urllib1、cookielib进行POST请求，BeautifulSoup对html数据进行分析。

1. 从我原来的博客 [http://www.blogjava.net/vagasnail](http://www.blogjava.net/vagasnail)中抓取数据，用的urllib2：

        req = urllib2.Request(self.url)
        response = urllib2.urlopen(req)
        the_page = response.read()

2. 由于开始使用单线程，很慢啊，基本上不能运行成功，不得已使用了多行程的方式，每一个url的抓取、解析数据和向目标博客POST数据都会启动一个新的线程。

        ### 建立线程类从threading.Thread继承
        class FetchThread(threading.Thread):
            def run(self):
                # 这个函数是必须实现的，其实和JAVA中的Thread类是如此的像
                # 线程实际运行就是这个函数
                pass

3. 用的解析库是BeautifulSoup，这个非常好用啊。

        soup = BeautifulSoup(data)
        #拿到所有的链接
        alinks =  soup.find_all('a')
        #正则表达式，因为不是所有的链接都有用的
        pattern1 = re.compile(r'^http://www.blogjava.net/vagasnail/articles/[0-9]+\.html$')
        pattern2 = re.compile(r'^http://www.blogjava.net/vagasnail/archive/[0-9]{4}/[0-9]{2}/[0-9]{2}/[0-9]+\.html$')
        pattern3 = re.compile(r'^http://www.blogjava.net/vagasnail/category/[0-9]+\.html$')
        pattern4 = re.compile(r'^http://www.blogjava.net/vagasnail/archive/[0-9]{4}/[0-9]{2}\.html$')
        #拿到标题，标题是ID标识的
        title = soup.find_all(id="viewpost1_TitleUrl")
        #只要文本数据就行了
        art['title'] = title[0].get_text()
        #拿到内容
        content = soup.find_all('div', class_="postbody")
        #内容应该所有HTML字符
        art['content'] = str(content[0])
        #发布日期是直接作为普通的文本节点在里面的，没办法只能用正则了
        re.M表示多行模式
        pattern_date = re.compile(r'([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2})',re.M)
        #必须要用findall它会查询字符串中匹配模式的所有子字符串
        pdates = pattern_date.findall(str_postfoot) 

4. 就是POST到[目标博客](codecos.com)了

        #引入要用的库
        import urllib,urllib2,cookielib
         
        cj = cookielib.CookieJar()
        #处理POST数据的URL
        b_url ='http://codecos.com/****'
        art['tag'] = ",".join(art['tag'])
        #art是列表这里把它转成元组
        body = art.items()
        #设置cookie
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        #模拟浏览器请求
        opener.addheaders = [('User-agent',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]
        urllib2.install_opener(opener)
        #发送请求
        req = urllib2.Request(b_url, urllib.urlencode(body))
        u = urllib2.urlopen(req)
        u.read()

> 所以[我的博客](codecos.com)现在的已经有很多文章了，不过有些还是样式有些问题，只能手动调整了。
> 还有这些不是用[markdown](http://wowubuntu.com/markdown/)写的，改起来很麻烦啊，所有还是[markdown](http://wowubuntu.com/markdown/)舒服啊。
    