## Scrapy 运用与总结



#### 介绍：

​	Scrapy是一个为了爬取网站数据，提取结构性数据而编写的应用框架。 可以应用在包括数据挖掘，信息处理或存储历史数据等一系列的程序中。所谓的框架就是一个已经被集成了各种功能（高性能异步下载，队列，分布式，解析，持久化等）的具有很强通用性的项目模板。对于框架的学习，重点是要学习其框架的特性、各个功能的用法即可。

![1567493148727](C:\Users\wanglixing\Desktop\知识点复习\爬虫笔记\assets\1567493148727.png)



#### Scrapy主要包含了以下几个组件：

- **引擎(Scrapy)**：用来处理整个系统的数据流，触发事务（框架核心）。
- **调度器(Scheduler)**：用来接受引擎发过来的请求, 压入队列中, 并在引擎再次请求的时候返回. 可以想像成一个URL(抓取网页的网址或者说是链接)的优先队列, 它来决定下一个要抓取的网址是什么, 同时去除重复的网址
- **下载器(Downloader)**：用于下载网页内容,并将网页内容返回给蜘蛛(Scrapy下载器是建立在twisted这个高效的异步模型上的)
- **爬虫(Spiders)**：爬虫是主要干活的, 用于从特定的网页中提取自己需要的信息, 即所谓的实体(Item)。用户也可以从中提取出链接,让Scrapy继续抓取下一个页面
- **项目管道(Pipeline)**：负责处理爬虫从网页中抽取的实体，主要的功能是持久化实体、验证实体的有效性、清除不需要的信息。当页面被爬虫解析后，将被发送到项目管道，并经过几个特定的次序处理数据。
- **下载器中间件(Downloader Middlewares)**：位于Scrapy引擎和下载器之间的框架，主要是处理Scrapy引擎与下载器之间的请求及响应。
- **爬虫中间件(Spider Middlewares)**：介于Scrapy引擎和爬虫之间的框架，主要工作是处理蜘蛛的响应输入和请求输出。
- **调度中间件(Scheduler Middlewares)**：介于Scrapy引擎和调度之间的中间件，从Scrapy引擎发送到调度的请求和响应。




#### Scrapy运行流程大概如下：

- 引擎从调度器中取出一个链接(URL)用于接下来的抓取
- 引擎把URL封装成一个请求(Request)传给下载器
- 下载器把资源下载下来，并封装成应答包(Response)
- 爬虫解析Response
- 解析出实体（Item）,则交给实体管道进行进一步的处理
- 解析出的是链接（URL）,则把URL交给调度器等待抓取
  

#### 安装Scrapy命令：

```
Linux：
      pip3 install scrapy

Windows：
      a. pip3 install wheel
      b. 下载twisted http://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted
      c. 进入下载目录，执行 pip3 install Twisted‑17.1.0‑cp35‑cp35m‑win_amd64.whl
      d. pip3 install pywin32
      e. pip3 install scrapy
```



#### 第一个Scrapy爬虫项目：

- 进入终端创建项目：

  ```python
  1、cd进一个文件夹中，输入scrapy，查看环境是否搭建完成
  2、创建第一个project：scrapy startproject firstBlood(项目名)
  
  创建的目录结构：
      project_name/
         scrapy.cfg  #项目的主配置信息。（真正爬虫相关的配置信息在settings.py文件中）
         project_name/
             __init__.py
             items.py     #设置数据存储模板，用于结构化数据，如：Django的Model
             pipelines.py #数据持久化处理模块
             settings.py  #配置文件，如：递归的层数、并发数，延迟下载等
             spiders/     # 爬虫目录，如：创建文件，编写爬虫解析规则
                 __init__.py
              
  3、在创建爬虫应用程序：（不能用pycharm工具创建py文件，必须cd到项目中，执行下列命令：
     >cd project_name（进入项目目录）
     >scrapy genspider 应用名称 爬取网页的起始url （例如：scrapy genspider qiubai www.qiushibaike.com）,其实url可以修改在生成后
  
  4、编写爬虫文件:在步骤2执行完毕后，会在项目的spiders中生成一个应用名的py爬虫文件，文件源码如下：
      
  import scrapy
  class FirstSpider(scrapy.Spider):  #这个类型前半部分是我们写的项目名，后面是它拼接的Spider
      name = 'first'   #应用名称，唯一标识，则spider文件夹中是可以创建多个爬虫文件
      allowed_domains = ['www.xxx.com'] #允许爬取的域名（如果遇到非该域名的url则爬取不到数据），通常不需要，注释
      start_urls =  ['https://www.baidu.com/','https://www.sogou.com/'] #起始爬取的url，列表中存放的url会被scrapy自动的进行请求发送
  	
       #访问起始URL并获取结果后的回调函数，该函数的response参数就是向起始的url发送请求后，获取的响应对象.该函数返回值必须为可迭代对象或者NUll 
      def parse(self, response):
          print(response.text) #获取字符串类型的响应内容
          print(response.body) #获取字节类型的相应内容
          pass
  
  5、设置修改settings.py配置文件相关配置:
    修改内容及其结果如下：
  	19行：USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' #伪装请求载体身份
  
  	22行：ROBOTSTXT_OBEY = False  #可以忽略或者不遵守robots协议  
      23行：LOG_LEVEL ='ERROR'  #设置日志报错等级
      
  6、小试牛刀,爬取下百度和搜狐的首页：（需要注释掉域名列表，并且要在项目目录下执行）
  	 scrapy crawl 爬虫名称 ：该种执行形式会显示执行的日志信息
       scrapy crawl 爬虫名称 --nolog：该种执行形式不会显示执行的日志信息
       如：\scrapy学习\firstBlood>scrapy crawl first
  
  ```

  - 实例：将糗百中的内容和标题进行爬取

    ```python
    # -*- coding: utf-8 -*-
    import scrapy
    
    class QiubaiSpider(scrapy.Spider):
        name = 'qiubai'
        allowed_domains = ['https://www.qiushibaike.com/']
        start_urls = ['https://www.qiushibaike.com/']
    
        def parse(self, response):
            #xpath为response中的方法，可以将xpath表达式直接作用于该函数中
            odiv = response.xpath('//div[@id="content-left"]/div')
            content_list = [] #用于存储解析到的数据
            for div in odiv:
                #xpath函数返回的为列表，列表中存放的数据为Selector类型的数据。我们解析到的内容被封装在了Selector对象中，需要调用extract()函数将解析的内容从Selecor中取出。
                author = div.xpath('.//div[@class="author clearfix"]/a/h2/text()')[0].extract()#等价于extract_first()
                #如果是列表，,extract()函数作用与每个元素
                content=div.xpath('.//div[@class="content"]/span//text()').extract()
    
                #将解析到的内容封装到字典中
                dic={
                    '作者':author,
                    '内容':content 
                }
                #将数据存储到content_list这个列表中
                content_list.append(dic)
    
            return content_list
    ```

    

#### Scrapy 的持久化存储

- ##### 基于终端指令

  - 特性: 只可以将parse方法的返回值存到本地磁盘文件中，保证爬虫文件的parse方法中有可迭代类型对象（通常为列表or字典）的返回，该返回值可以通过终端指令的形式写入指定格式的文件中进行持久化操作。

  - 指令：

    ```python
    执行输出指定格式进行存储：将爬取到的数据写入不同格式的文件中进行存储，没有txt文件格式
        scrapy crawl 爬虫名称 -o xxx.json
        scrapy crawl 爬虫名称 -o xxx.xml
        scrapy crawl 爬虫名称 -o xxx.csv    
    ```

    

- **基于管道**：主要用于数据解析

  scrapy框架中已经为我们专门集成好了高效、便捷的持久化操作功能，我们直接使用即可。要想使用scrapy的持久化操作功能，我们首先来认识如下两个文件：

  ```
  items.py：数据结构模板文件。定义数据属性。
  pipelines.py：管道文件。接收数据（items），进行持久化操作。
  ```

  ##### 持久化流程：

  ```
  	1.爬虫文件爬取到数据后(parse函数解析的数据），需要将数据封装到items对象中。（item对象就是item.py文件中对应的类的对象）
  	2.在item类中定义相应的属性，用来存储我们解析的数据，在parse函数中调用item对象，并赋值
      3.使用yield关键字将items对象提交给pipelines管道进行持久化操作。将item数据提交给管道 
      4.在管道文件中的process_item方法中接收爬虫文件提交过来的item对象，然后编写持久化存储的代码将item对象中存储的数据进行持久化存储
      5.settings.py配置文件中开启管道：在settings中打开ITEM_PIPELINES，LOG_LEVEL = 'ERROR'
  LOG_FILE = './log.txt'，以及USER_AGENT
  ```
  - 代码演示：将糗百的文字数据存储

    ```python
     #item.py文件中，对解析完的数据进行封装处理
    import scrapy
    class FirstbloodItem(scrapy.Item):
        #Field可以将其理解成一个万能的数据类型，可以存任意数据类型，Field不能写死，只能用万能的
        author = scrapy.Field()
        content = scrapy.Field()
    
    --------------------------------------------------------------
     #parse函数对相应数据先交给item、后交给pipeline
    import scrapy
    from firstBlood.items import FirstbloodItem
    
    class SencondSpider(scrapy.Spider):
        name = 'sencond'
        # allowed_domains = ['www.xxx.com']
        start_urls = ['https://www.qiushibaike.com/text/']
    
    
        def parse(self, response):
            div_list = response.xpath('//*[@id="content-left"]/div')
            for div in div_list:
                author = div.xpath('./div[1]/a[2]/h2/text()').extract_first()
                content = div.xpath('./a/div/span//text()').extract()
    
                # 每次循环的数据都要实例化一个item类
                item = FirstbloodItem()
                # 类似于字典，item已经封装好了，将各字段封装成字典
                item['author'] = author
                item['content'] = ''.join(content)
    			# 交给管道，一定提交给优先级高的管道类
                yield item
    
    ------------------------------------------------------------
     #管道，用于数据的持久化储存
    class FirstbloodPipeline(object):
        #设置全局变量，否则无效
        fp = None
    
        #重写父类的方法
        def open_spider(self,spider):
            print('开始爬虫')
            # 只打开一次文件就行了，不用反复打开，开始爬虫时就会执行
            self.fp = open('qiushibaike.txt','w',encoding='utf-8')
    
        # 用于接收爬虫文件提交过来的item，然后将其进行任意形式的持久化存储，
        #参数item：就是接收到的item对象,一次接受一个item
        #该方法每接受一个item就会调用一次
        def process_item(self, item, spider):
            author = item['author']
            content = item['content']
            self.fp.write(author+":"+content+'\n')
            return item
    
        # 重写父类方法，当爬虫结束后执行
        def close_spider(self,spider):
            print('爬虫结束')
            self.fp.close()
    
    -----------------------------------------------------------
     # settings.py文件
    ITEM_PIPELINES = {
       'firstBlood.pipelines.FirstbloodPipeline': 300, #300表示管道优先级，意思是可以开启多个管道
    }
    ```

    ![1567425897312](C:\Users\wanglixing\AppData\Roaming\Typora\typora-user-images\1567425897312.png)



- 将同一份数据持久化到不同的平台中

  - 分析：

    - 管道文件中的一个管道类负责数据的一种形式的持久化存储

    - 爬虫文件向管道提交item只会提交给优先级最高的那一个管道类（值越小越大）

    - 在管道类的process_item中的return item表示的时将当前管道接受的 item提交给下一个即将执行的管道类（优先级低次的）

      ```mysql
      首先需要创建一个表：
      mysql> create database s1 charset 'utf8';
      Query OK, 1 row affected (0.01 sec)
      
      mysql> use s1;
      mysql> create table qiubai (author varchar(100),content varchar(5000));
      Query OK, 0 rows affected (0.03 sec)
      mysql> desc qiubai;
      +---------+---------------+------+-----+---------+-------+
      | Field   | Type          | Null | Key | Default | Extra |
      +---------+---------------+------+-----+---------+-------+
      | author  | varchar(100)  | YES  |     | NULL    |       |
      | content | varchar(5000) | YES  |     | NULL    |       |
      +---------+---------------+------+-----+---------+-------+
      mysql> commit;
      ```

  - 代码实现: sencond.py 爬虫文件不需要改变，每次依旧返回item， 主要还是针对管道类return item来实现多管道存储

    ```python
    import pymysql
    from redis import Redis
    
    class FirstbloodPipeline(object):
        #设置全局变量，否则无效
        fp = None
    
        #重写父类的方法
        def open_spider(self,spider):
            print('开始爬虫')
            # 只打开一次文件就行了，不用反复打开，开始爬虫时就会执行
            self.fp = open('qiushibaike.txt','w',encoding='utf-8')
    
        # 用于接收爬虫文件提交过来的item，然后将其进行任意形式的持久化存储，
        #参数item：就是接收到的item对象,一次接受一个item
        #该方法每接受一个item就会调用一次
        def process_item(self, item, spider):
            author = item['author']
            content = item['content']
            self.fp.write(author+":"+content+'\n')
    
            # 注意pipeline类中写了return item，表示会交给紧接这该类的优先级的管道类处理
            return item
    
        # 重写父类方法，当爬虫结束后执行
        def close_spider(self,spider):
            print('爬虫结束')
            self.fp.close()
    
    
    # 自定义存储类，用于数据存储到mysql中
    class MysqlPL(object):
        conn = None   #数据库连接
        cursor = None  # 执行sql语句
        def open_spider(self,spider):
            self.conn = pymysql.Connect(host='127.0.0.1',port=3306,user='root',password='123',db='s1',charset='utf8')
    
        def process_item(self,item,spider):
            author = item['author']
            content = item['content']
    
            sql = "insert into qiubai values ('%s','%s')"%(author,content)
            self.cursor = self.conn.cursor()  #创建游标
    
            try:
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(e)
                self.conn.rollback()  #回滚
    
            #仍然返回给下一个管道，当然可以不写
            return item
    
        def close_spider(self,spider):
            self.cursor.close()
            self.conn.close()
    
    #重点:首先如果你的settings中的ITEM_PIPELINE写了第一种类的优先级最高，但是你在这把那个类删除了，意味着后面的类都拿不到item了
    class RedisPL(object):
        conn = None
        def open_spider(self,spider):
            self.conn = Redis(host='127.0.0.1',port=6379)
            print(self.conn)
    
        def process_item(self,item,spider):
            # 注意我们之前说的item是一个类似与字典的数据结构，相对有序字典
            self.conn.lpush('all_data',item)  #每次将item添加到 all_data的列表中
    
            
    ------------------------------------------------------------
     #settings.py文件
    ITEM_PIPELINES = {
       # 这里的优先级越高，数值越小，也就是说第一个大于第二个优先级
       'firstBlood.pipelines.FirstbloodPipeline': 300, #300表示管道优先级，意思是可以开启多个管道
       'firstBlood.pipelines.MysqlPL':301 , #yield item 选择优先级高的管道类
       'firstBlood.pipelines.RedisPL':302
    }  #同时向三个管道中输入问及那存储
    ```

    - 注意：将字典输入到redis的时候报错

      ```python
       Invalid input of type: 'FirstbloodItem'. Convert to a byte, string or number first.
      
       #解决办法：降低redis版本>>pip install -U redis==2.10.6
      ```

- 面试题：如果最终需要将爬取到的数据值一份存储到磁盘文件，一份存储到数据库中，则应该如何操作scrapy？　

  ```python
  管道文件中的代码为
  
  #该类为管道类，该类中的process_item方法是用来实现持久化存储操作的。
  class DoublekillPipeline(object):
      def process_item(self, item, spider):
          #持久化操作代码 （方式1：写入磁盘文件）
          return item
  
  #如果想实现另一种形式的持久化操作，则可以再定制一个管道类：
  class DoublekillPipeline_db(object):
      def process_item(self, item, spider):
          #持久化操作代码 （方式1：写入数据库）
          return item
  
  在settings.py开启管道操作代码为：
  
  #下列结构为字典，字典中的键值表示的是即将被启用执行的管道文件和其执行的优先级。
  ITEM_PIPELINES = {
     'doublekill.pipelines.DoublekillPipeline': 300,
     'doublekill.pipelines.DoublekillPipeline_db': 200,
  }
  
  #上述代码中，字典中的两组键值分别表示会执行管道文件中对应的两个管道类中的process_item方法，实现两种不同形式的持久化操作
  ```

  

#### Scrapy手动请求发送

​	场景：将多个页码对应的数据进行爬取和解析的操作，原始方法：将多个页码的url 放进start_url列表中，但是要是url过多怎么办

- 使用场景：爬取多个页码对应的页面源码数据

- yield scrapy.Request(new_url, callback=self.parse) 执行回调，形成递归，模板url

- 实例：将糗事百科所有页码的作者和段子内容数据进行爬取切持久化存储，分析：每一个页面对应一个url，则scrapy工程需要对每一个页码对应的url依次发起请求，然后通过对应的解析方法进行作者和段子内容的解析。

  ```python
  import scrapy
  from firstBlood.items import FirstbloodItem
  
  class SencondSpider(scrapy.Spider):
      name = 'sencond'
      # allowed_domains = ['www.xxx.com']
      start_urls = ['https://www.qiushibaike.com/text/']
  
      # 将多个页码对应的数据进行爬取和解析的操作
      url = 'https://www.qiushibaike.com/text/page/%d/'   #先制定一个通用的url模板
      #page 第一次调用表示的是用来解析第一页对应页面中的段子内容和作者
      pageNum = 1
      def parse(self, response):
          div_list = response.xpath('//*[@id="content-left"]/div')
          for div in div_list:
              author = div.xpath('./div[1]/a[2]/h2/text()').extract_first()
              content = div.xpath('./a/div/span//text()').extract()
  
              # 每次循环的数据都要实例化一个item类
              item = FirstbloodItem()
              # 类似于字典，item已经封装好了，将各字段封装成字典
              item['author'] = author
              item['content'] = ''.join(content)
  
              #将item提交给管道
              yield item #item一定是提交给了优先级最高的管道类
  
          # 递归条件
          if self.pageNum <= 5:
              self.pageNum += 1
              new_url = self.url%self.pageNum
              #手动请求发送,发起get请求, 使整个函数进行递归，必须要yield，否则响应发送不成功
              yield scrapy.Request(new_url,callback=self.parse)
  ```

- 自动重写start_request方法，自动访问网页

  ```python
  class SencondSpider(scrapy.Spider):
      name = 'sencond'
      # allowed_domains = ['www.xxx.com']
      start_urls = ['https://www.qiushibaike.com/text/','https://www.qiushibaike.com/text/page/2/','https://www.qiushibaike.com/text/page/3/']
  
      #重写start_requests方法循环自动爬取页面
      def start_requests(self):
          for url in self.start_urls:
              yield  scrapy.Request(url,callback=self.parse)
  
      pageNum = 1
      def parse(self, response):
          div_list = response.xpath('//*[@id="content-left"]/div')
          for div in div_list:
              author = div.xpath('./div[1]/a[2]/h2/text()').extract_first()
              content = div.xpath('./a/div/span//text()').extract()
  
              # 每次循环的数据都要实例化一个item类
              item = FirstbloodItem()
              # 类似于字典，item已经封装好了，将各字段封装成字典
              item['author'] = author
              item['content'] = ''.join(content)
  
              #将item提交给管道
              yield item #item一定是提交给了优先级最高的管道类
  ```

  

#### Scrapy发post请求

​	问题：在之前代码中，我们从来没有手动的对start_urls列表中存储的起始url进行过请求的发送，但是起始url的确是进行了请求的发送，那这是如何实现的呢？

-  解答：其实是因为爬虫文件中的爬虫类继承到了Spider父类中的start_requests（self）这个方法，该方法就可以对start_urls列表中的url发起请求

  ```python
      def start_requests(self):
          cls = self.__class__
          if method_is_overridden(cls, Spider, 'make_requests_from_url'):
  			...
              for url in self.start_urls:
                  yield self.make_requests_from_url(url)
          else:
              for url in self.start_urls:
                  yield Request(url, dont_filter=True)
  
      def make_requests_from_url(self, url):
          """ This method is deprecated. """
          return Request(url, dont_filter=True)  #Request中默认的method=GET
  ```

  该方法默认的实现，是对起始的url发起get请求，如果想发起post请求，则需要子类重写该方法。

  ```python
   #方法： 重写start_requests方法，让其发起post请求
   
  def start_requests(self):
          #请求的url
          post_url = 'http://fanyi.baidu.com/sug'
          # post请求参数
          formdata = {
              'kw': 'wolf',
          }
          # 发送post请求
          yield scrapy.FormRequest(url=post_url, formdata=formdata, callback=self.parse)
  ```

  ![1567493123576](C:\Users\wanglixing\Desktop\知识点复习\爬虫笔记\assets\1567493123576.png)



#### 如何基于Scrapy进行图片数据的爬取

- 实例：爬取笑话网的图片，url：<http://www.521609.com/daxuemeinv/>

  ```python
                            #pipeline.py文件
  #原有的，不用
  # class ImgproPipeline(object):
  #     def process_item(self, item, spider):
  #         return item
  
  from scrapy.pipelines.images import ImagesPipeline
  import scrapy
  
  #注意这个类名如果更改，用自己的mingz，相应的配置文件也要改变，所以这里我直接使用它原名
  class ImgproPipeline(ImagesPipeline):
  
      #重写继承类的方法,对某一个媒体资源进行请求发送
      #item就是接受到的spider提交过来的item
      def get_media_requests(self, item, info):
          yield scrapy.Request(item['src'])
  
  
       # 制定媒体数据存储的名称，在settings.py中配置IMAGEs_STORE
      def file_path(self, request, response=None, info=None):
          name = request.url.split('/')[-1]
          print(name)
          return name
  
      # 在图片储存好后，交给下一个待执行的管道了，return item
      def item_completed(self, results, item, info):
          return item
      
  -----------------------------------------------------------
   #items.py
  import scrapy
  
  class ImgproItem(scrapy.Item):
      # define the fields for your item here like:
      src = scrapy.Field()
      pass
  
  -----------------------------------------------------------
   #img.py文件
  import scrapy
  from imgPro.items import ImgproItem
  
  class ImgSpider(scrapy.Spider):
      name = 'img'
      # allowed_domains = ['www.xxx.com']
      #分析url的页码是有规律的，从81开始
      start_urls = ['http://www.521609.com/daxuemeinv/']
  
      #url模板
      url = 'http://www.521609.com/daxuemeinv/list8%d.html'
      pageNum = 1
      def parse(self, response):
          li_list = response.xpath('//*[@id="content"]/div[2]/div[2]/ul/li')
          for li in li_list:
              img_src = 'http://www.521609.com'+li.xpath('./a[1]/img/@src').extract_first()
              # scrapy已经为我们建立好了imgpipeline类
  
              item= ImgproItem()
              item['src'] = img_src
              # 将图片的地址传给管道，当然我们可以自己使用response.body来接受byte类型，然后给item
              yield item
  
          if self.pageNum <=3:
              self.pageNum += 1
              new_url = self.url%self.pageNum
  
              yield  scrapy.Request(new_url,callback=self.parse)
  
   ----------------------------------------------------------------
   #settings.py文件
  ITEM_PIPELINES = {
     'imgPro.pipelines.ImgproPipeline': 300,
  }
  
  ROBOTSTXT_OBEY = False
  LOG_LEVEL = 'ERROR'
  LOG_FILE = './log.txt'
  IMAGES_STORE = './imgsLib'
  ```

- 原始方法:

  ```python
  import scrapy
  from xiaohua.items import XiaohuaItem
  class XiahuaSpider(scrapy.Spider):
      name = 'xiaohua'
      allowed_domains = ['www.521609.com']
      start_urls = ['http://www.521609.com/daxuemeinv/']
  
      pageNum = 1
      url = 'http://www.521609.com/daxuemeinv/list8%d.html'
  
      def parse(self, response):
          li_list = response.xpath('//div[@class="index_img list_center"]/ul/li')
          for li in li_list:
              school = li.xpath('./a/img/@alt').extract_first()
              img_url = li.xpath('./a/img/@src').extract_first()
  
              item = XiaohuaItem()
              item['school'] = school
              item['img_url'] = 'http://www.521609.com' + img_url
  
              yield item
  
          if self.pageNum < 10:
              self.pageNum += 1
              url = format(self.url % self.pageNum)
              #print(url)
              yield scrapy.Request(url=url,callback=self.parse)
  
  
  -------------------------------------------------------
   #item.py文件
  import scrapy
  
  
  class XiaohuaItem(scrapy.Item):
      # define the fields for your item here like:
      # name = scrapy.Field()
      school=scrapy.Field()
      img_url=scrapy.Field()
  
  ----------------------------------------------------------
   #pipeline.py文件
  import json
  import os
  import urllib.request
  class XiaohuaPipeline(object):
      def __init__(self):
          self.fp = None
  
      def open_spider(self,spider):
          print('开始爬虫')
          self.fp = open('./xiaohua.txt','w')
  
      def download_img(self,item):
          url = item['img_url']
          fileName = item['school']+'.jpg'
          if not os.path.exists('./xiaohualib'):
              os.mkdir('./xiaohualib')
          filepath = os.path.join('./xiaohualib',fileName)
          urllib.request.urlretrieve(url,filepath)
          print(fileName+"下载成功")
  
      def process_item(self, item, spider):
          obj = dict(item)
          json_str = json.dumps(obj,ensure_ascii=False)
          self.fp.write(json_str+'\n')
  
          #下载图片
          self.download_img(item)
          return item
  
      def close_spider(self,spider):
          print('结束爬虫')
          self.fp.close()
  
  配置文件：
  
  USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
  ROBOTSTXT_OBEY = False
  CONCURRENT_REQUESTS = 100
  COOKIES_ENABLED = False
  LOG_LEVEL = 'ERROR'
  RETRY_ENABLED = False
  DOWNLOAD_TIMEOUT = 3
  DOWNLOAD_DELAY = 3
  ```

  

#### Scrapy实现请求传参

- 实现深度爬取：爬取多个层级对应的页面数据

- 使用场景： 爬取的数据没有在同一张页面中，例如: 我们爬取一个电影网站，电影的名称，评分在一级页面，而要爬取的其他电影详情在其二级子页面中。这时我们就需要用到请求传参。

- 案例展示：爬取<https://www.4567tv.tv/frim/index1.html>电影网，将一级页面中的电影名称，类型，评分一级二级页面中的上映时间，导演，片长进行爬取。

  ```python
   #items.py文件
  import scrapy
  
  class MovieItem(scrapy.Item):
      # define the fields for your item here like:
      title = scrapy.Field()
      desc = scrapy.Field()
      
  ------------------------------------------------------------
   #movies.py 文件
  import scrapy
  from movie.items import MovieItem
  
  class MoviesSpider(scrapy.Spider):
      name = 'movies'
      # allowed_domains = ['www.xxx.com']
      start_urls = ['https://www.4567tv.tv/frim/index1.html']
  
      def parse(self, response):
          li_list = response.xpath('/html/body/div[1]/div/div/div/div[2]/ul/li')
          for li in li_list:
              title = li.xpath('./div[1]/a/@title').extract_first()
              detail_url ='https://www.4567tv.tv' + li.xpath('./div[1]/a/@href').extract_first()
  
              # 此时我们可以拿到item了，但是我们不能在这就直接item赋值了额，因为我们还要获取详情页的数据
              item = MovieItem()
              item['title'] = title
  
              #进行请求传参，将item进行传递,因为是将item放在请求中传递，所以叫请求传参,meta参数是一个字典，该字典
              #可以传递给callback指定的回调函数
              yield scrapy.Request(detail_url,callback=self.parse_detail,meta={'item':item})
  
      def parse_detail(self,response):
          # item接受的就是我们传递过来的item
          item = response.meta['item']
          desc = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[5]/span[2]/text()').extract_first()
          item['desc'] = desc
          yield item
          
  ----------------------------------------------------------------
   #pipelines.py文件
  class MoviePipeline(object):
      def process_item(self, item, spider):
          print(item)
          return item
      
  ---------------------------------------------------------------
  ROBOTSTXT_OBEY = False
  LOG_LEVEL ='ERROR'
   #settings.py文件
  ITEM_PIPELINES = {
     'movie.pipelines.MoviePipeline': 300,
  }
  
  ROBOTSTXT_OBEY = False
  LOG_LEVEL ='ERROR'
  ```

  - 原始版本代码演示

    ```PYTHON
     # 爬虫文件中
    import scrapy
    from moviePro.items import MovieproItem
    
    class MovieSpider(scrapy.Spider):
        name = 'movie'
        allowed_domains = ['www.id97.com']
        start_urls = ['http://www.id97.com/']
    
        def parse(self, response):
            div_list = response.xpath('//div[@class="col-xs-1-5 movie-item"]')
    
            for div in div_list:
                item = MovieproItem()
                item['name'] = div.xpath('.//h1/a/text()').extract_first()
                item['score'] = div.xpath('.//h1/em/text()').extract_first()
                #xpath(string(.))表示提取当前节点下所有子节点中的数据值（.）表示当前节点
                item['kind'] = div.xpath('.//div[@class="otherinfo"]').xpath('string(.)').extract_first()
                item['detail_url'] = div.xpath('./div/a/@href').extract_first()
                #请求二级详情页面，解析二级页面中的相应内容,通过meta参数进行Request的数据传递
                yield scrapy.Request(url=item['detail_url'],callback=self.parse_detail,meta={'item':item})
    
        def parse_detail(self,response):
            #通过response获取item
            item = response.meta['item']
            item['actor'] = response.xpath('//div[@class="row"]//table/tr[1]/a/text()').extract_first()
            item['time'] = response.xpath('//div[@class="row"]//table/tr[7]/td[2]/text()').extract_first()
            item['long'] = response.xpath('//div[@class="row"]//table/tr[8]/td[2]/text()').extract_first()
            #提交item到管道
            yield item
    
    ---------------------------------------------------------------------
    　#items文件：
    import scrapy
    
    class MovieproItem(scrapy.Item):
        # define the fields for your item here like:
        name = scrapy.Field()
        score = scrapy.Field()
        time = scrapy.Field()
        long = scrapy.Field()
        actor = scrapy.Field()
        kind = scrapy.Field()
        detail_url = scrapy.Field()
    
    --------------------------------------------------------------------
     #管道文件：
    import json
    class MovieproPipeline(object):
        def __init__(self):
            self.fp = open('data.txt','w')
        def process_item(self, item, spider):
            dic = dict(item)
            print(dic)
            json.dump(dic,self.fp,ensure_ascii=False)
            return item
        def close_spider(self,spider):
            self.fp.close()
    ```

- 以上案例只能爬取单页，当我们需要爬取多页时，可以使用CrawlSpider,这里我们先使用收到请求多页的方式爬取

  ```python
  import scrapy
  from movie.items import MovieItem
  
  #多页爬取,之后我们会学习CrawlSpider可以全栈爬取
  class MoviesSpider(scrapy.Spider):
      name = 'movies'
      # allowed_domains = ['www.xxx.com']
      start_urls = ['https://www.4567tv.tv/frim/index1.html']
      url = 'https://www.4567tv.tv/frim/index1-%d.html'
      pageNum = 1
  
      def parse(self, response):
          li_list = response.xpath('/html/body/div[1]/div/div/div/div[2]/ul/li')
          for li in li_list:
              title = li.xpath('./div[1]/a/@title').extract_first()
              detail_url ='https://www.4567tv.tv' + li.xpath('./div[1]/a/@href').extract_first()
  
              # 此时我们可以拿到item了，但是我们不能在这就直接item赋值了额，因为我们还要获取详情页的数据
              item = MovieItem()
              item['title'] = title
  
              #进行请求传参，将item进行传递,因为是将item放在请求中传递，所以叫请求传参,meta参数是一个字典，该字典
              #可以传递给callback指定的回调函数
              yield scrapy.Request(detail_url,callback=self.parse_detail,meta={'item':item})
  
          if self.pageNum < 5:
              self.pageNum += 1
              new_url = self.url % self.pageNum
  
              # 递归，对其他页面进行爬取
              yield  scrapy.Request(new_url, callback=self.parse)
  
  
      def parse_detail(self,response):
          # item接受的就是我们传递过来的item
          item = response.meta['item']
          desc = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[5]/span[2]/text()').extract_first()
          item['desc'] = desc
          yield item
  ```

- 总结：

  ```
  1、在手动请求的时候传递item：yield scrapy.Request(url,callback=,meta={'item':item})
     将meta这个字典传递给callback，在callback中接收meta：item = response.meta['item']
        
  ```

  



#### Scrapy中的中间件的应用

- **爬虫中间件(Spider Middlewares)**：介于Scrapy引擎和爬虫之间的框架，主要工作是处理蜘蛛的响应输入和请求输出。

- **下载器中间件(Downloader Middlewares)**：位于Scrapy引擎和下载器之间的框架，主要是处理Scrapy引擎与下载器之间的请求及响应。

  - 作用：批量拦截请求和响应

    - 引擎将请求传递给下载器过程中， 下载中间件可以对请求进行一系列处理。比如设置请求的 User-Agent，设置代理等
    - 在下载器完成将Response传递给引擎中，下载中间件可以对响应进行一系列处理。比如进行gzip解压等。

    我们主要使用下载中间件处理请求，一般会对请求设置随机的User-Agent ，设置随机的代理。目的在于防止爬取网站的反爬虫策略。

- ##### 下载中间件的应用：

  - 拦截请求：
    - UA伪装
    - 代理操作
  - 拦截响应：

- 打开middlewares.py文件后，可以看见两个类，分别代表着爬虫中间件/下载中间件，这里我们以下载中间件为例

  ```python
  class MovieDownloaderMiddleware(object):
      # Not all methods need to be defined. If a method is not defined,
      # scrapy acts as if the downloader middleware does not modify the
      # passed objects.
  
      @classmethod
      def from_crawler(cls, crawler):
          # This method is used by Scrapy to create your spiders.
          s = cls()
          crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
          return s
      
  	#拦截正常请求，参数request就是拦截到的请求对象
      def process_request(self, request, spider):
          # Called for each request that goes through the downloader
          # middleware.
  
          # Must either:
          # - return None: continue processing this request
          # - or return a Response object
          # - or return a Request object
          # - or raise IgnoreRequest: process_exception() methods of
          #   installed downloader middleware will be called
          return None
  	
      #拦截异常响应：参数response就是拦截到的响应
      def process_response(self, request, response, spider):
          # Called with the response returned from the downloader.
  
          # Must either;
          # - return a Response object
          # - return a Request object
          # - or raise IgnoreRequest
          return response
  	
      #拦截发生异常的请求
      def process_exception(self, request, exception, spider):
          #拦截到的异常请求然后对其进行修正，然后重新进行请求发送
          # Called when a download handler or a process_request()
          # (from other downloader middleware) raises an exception.
  
          # Must either:
          # - return None: continue processing this exception
          # - return a Response object: stops process_exception() chain
          # - return a Request object: stops process_exception() chain
          pass
  	
      def spider_opened(self, spider):
          #打印日志
          spider.logger.info('Spider opened: %s' % spider.name)
  ```


- （拦截请求）UA伪装和代理池的设置：将所有的请求尽可能多的设定成不同请求载体身份标识（通过UA池）

  - 我们不是在配置文件中配置了USER_AGENT? 有必要在中间件中再次进行UA伪装,在配置文件中的UA伪装，将所有的请求都使用同一套伪装，而通过中间件，我们可以为每一个请求进行UA伪装。有的网站会检测同一个User_Agent的高频访问，从而禁止。

    ```python
    import random
    #可被选用的代理IP
    PROXY_http = [
        '153.180.102.104:80',
        '195.208.131.189:56055',
    ]
    PROXY_https = [
        '120.83.49.90:9000',
        '95.189.112.214:35508',
    ]
    
    #UA池
    user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
            "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
           ....
            "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
            "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    
    class MovieDownloaderMiddleware(object):
    
        def process_request(self, request, spider):
            # 实现：将拦截到的请求尽可能多的设定成不同的请求载体身份标识
            # UA池
            request.headers['User-Agent'] = random.choice(user_agent_list)
    
            #代理IP池
            if request.url.split(':')[0] =='http':
                request.meta['proxy'] = 'http://' + random.choice(PROXY_http)
            else:
                request.meta['proxy'] = 'https://' + random.choice(PROXY_https)
            return None
        
        def process_response(self, request, response, spider):
    
            return response
    
        def process_exception(self, request, exception, spider):
            # 做相关修正操作，如有些网站请求失败后会返回错误页面，也就是说可以访问但是返回的页面是错误的，这时候我们就可以进行修正
            # 代理IP池
            if request.url.split(':')[0] == 'http':
                request.meta['proxy'] = 'http://' + random.choice(PROXY_http)
            else:
                request.meta['proxy'] = 'https://' + random.choice(PROXY_https)
    
            #重新发送，将修正之后的请求进行重新发送
            return request
    
        def spider_opened(self, spider):
            spider.logger.info('Spider opened: %s' % spider.name)
    ```

- （拦截响应）：篡改响应数据或者直接替换响应对象，对返回的响应数据进行判定是否是我们想要的
  - 实例：爬取网易新闻的国内、国际、军事、航空、无人机板块下的新闻数据 url：<https://news.163.com/>

  - 分析：当点击国内超链进入国内对应的页面时，会发现当前页面展示的新闻数据是被动态加载出来的，如果直接通过程序对url进行请求，是获取不到动态加载出的新闻数据的。则就需要我们使用selenium实例化一个浏览器对象，在该对象中进行url的请求，获取动态加载的新闻数据。

    ```python
     #items.py文件
    import scrapy
    class WangyiproItem(scrapy.Item):
        # define the fields for your item here like:
        title = scrapy.Field()
        content = scrapy.Field()
        
    ---------------------------------------------------------------
     #pipelines.py文件
    class WangyiproPipeline(object):
        def process_item(self, item, spider):
            print(item)
            return item
    --------------------------------------------------------------
     #middlewares.py文件中的下载中间件
    from scrapy import signals
    from scrapy.http import HtmlResponse
    import time
    class WangyiproDownloaderMiddleware(object):
    
        def process_request(self, request, spider):
            return None
    
        #进行响应对象进行拦截,这里的spider就是爬虫文件爬虫类实例化的对象，也就是WangyiSpider类的对象，我们
        # 可以通过spider点出类的属性
        def process_response(self, request, response, spider):
            #1、将所有的响应中的那五个不满足要求的response进行截获，先不return它，进行修正后再返回，
            #因为这五个response（模板）是动态加载的，也就是说我们拿到的页面不是先要的
                # 1、每个响应对象对应唯一一个请求对象
                # 2、如果我们可以定位到五个响应对象的请求对象后，就可以通过该请求对象定位到指定的响应对象
                # 3、可以通过五个板块的url定位请求对象
                # 总结： url --> request --> response
    
    
            #2、将找到的五个不满足需求的响应对象进行修正
            #spider.five_model_urls : 通过spider点出五个模块对应的url
            bro = spider.bro
            if request.url in spider.five_model_urls:
                # 如果if条件成立则该response就是五个板块对应的响应对象
                # 这里的response就是HtmlResponse类对象
                bro.get(request.url)
                time.sleep(1)
                page_text = bro.page_source # 包含了动态加载
                new_response = HtmlResponse(
                    url=request.url,  # 响应对象对应的请求对象
                    body=page_text,  #将selenums 获得的页面数据传入
                    encoding='utf-8',
                    request=request  #五个模板对应的请求对象
                )
    
                # 返回新的响应对象，包含着动态加载的新闻数据
                return new_response
            return response
        
    ----------------------------------------------------------------
     #爬虫文件，wangyi.py文件
    import scrapy
    from selenium import webdriver
    from wangyiPro.items import WangyiproItem
    
    class WangyiSpider(scrapy.Spider):
        name = 'wangyi'
        # allowed_domains = ['wwww.xxx.com']
        start_urls = ['https://news.163.com/']
        five_model_urls = []
        # 创建浏览器对象
        bro = webdriver.Chrome(executable_path=r'D:\21期\爬虫 + 数据分析\tools\chromedriver.exe')
    
        # 用来解析五个板块对应的url，然后对其进行手动发送发送
        def parse(self, response):
            # 找出所需模块对应的li标签索引
            model_index = [3,4,6,7,8]
            li_list = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
            for index in model_index:
                # 五个板块的li标签,取出url
                li = li_list[index]
                model_url = li.xpath('./a/@href').extract_first()
    
                self.five_model_urls.append(model_url)
                # 对每一个板块的url进行手动请求发送
                yield scrapy.Request(model_url,callback=self.parse_model)
    
        # 解析每个板块页面中的新闻标题和新闻详情页的url
        # 问题：response中并没有包含每个板块中动态加载出的新闻数据，也就是说这个response是不满足需求的响应
        # 解决： 在中间件中，对不满足要求的response进行重新修正或重新加载
        def parse_model(self,response):
            # 通过中间件中使用selenium处理后每个板块已经获得了动态加载的页面数据后
            div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div/div/ul/li/div/div')
            for div in div_list:
                title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
                detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()
    
                item = WangyiproItem()
                item['title'] = title
    
                # 对详情页发起请求解析出新闻内容,再定义一个回调函数提取新闻内容,将item传递给下一个需要的解析函数
                yield scrapy.Request(detail_url,callback=self.parse_new_content,meta={'item':item})
    
    
        #解析新闻内容
        def parse_new_content(self,response):
            content = response.xpath('//*[@id="endText"]//text()').extract()
            content = ''.join(content)
    
            item = response.meta['item']
            
            item['content'] = content
    
            yield item
    
        #重写父类的关闭函数，所有操作的最后执行
        def closed(self,spider):
            self.bro.quit()
            
    ------------------------------------------------------------------
     # settings.py文件
    DOWNLOADER_MIDDLEWARES = {
       'wangyiPro.middlewares.WangyiproDownloaderMiddleware': 543,
    }
    ITEM_PIPELINES = {
       'wangyiPro.pipelines.WangyiproPipeline': 300,
    }
    
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    ROBOTSTXT_OBEY = False
    LOG_LEVEL = 'ERROR'
    ```

- selenium在scrapy中的应用

  - 实例化浏览器对象： 写在爬虫类的构造方法中
  - 关闭浏览器：爬虫类中的closed(self,spider) 关闭浏览器
  - 在中间件中执行浏览器自动化操作

 

#### 百度AI识别新闻关键字

- 需求：爬取网易新闻的国内，国际，军事，航空，无人机五个板块下的新闻标题和新闻内容，然后基于百度AI将新闻类型和关键字进行提取，然后将其四个字段写入mysql数据库进行存储！

  ```python
  from aip import AipNlp  #数据上列中已经获取，只需要修改pipeline文件，注意要修改settings中的pipelines文件。
  #pip install baidu-aip
  import pymysql
  import time
  
  APP_ID = '17170467'
  API_KEY = 'I9gTHCwucpgxwPUjepnLrpsG'
  SECRET_KEY = '7BouOaHfzde2rv7XD7QPWl40gRB0j7GE'
  class MysqlPL(object):
      client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
      conn = None
      cursor = None
  
      def open_spider(self, spider):
          # 提前在数据库中创建news数据库和new表，包含四个字段
          self.conn = pymysql.Connect(host='127.0.0.1', port=3306, user="root", password='123', db='news',)
  
      def process_item(self, item, spider):
          title = item["title"]
          content = item['content']
          tag = self.client.keyword(title,content)  # 标签
          first_tag = tag.get('items')[0].get('tag')
  
          time.sleep(1)
          types = self.client.topic(title,content)  # 类型
          content_type = types.get('item').get('lv1_tag_list')[0].get('tag')
          sql = 'insert into new values ("%s","%s","%s","%s")' % (title, content, content_type, first_tag)
          self.cursor = self.conn.cursor()
          try:
              self.cursor.execute(sql)
          except Exception as e:
              self.conn.rollback()
  
      def close_spider(self, spider):
          self.cursor.close()
          self.conn.close()
  ```

  

#### 基于CrawlSpider的全栈数据爬取

提问：如果想要通过爬虫程序去爬取”糗百“全站数据新闻数据的话，有几种实现方法？

方法一：基于Scrapy框架中的Spider的递归爬取进行实现（Request模块递归回调parse方法）。

方法二：基于CrawlSpider的自动爬取进行实现（更加简洁和高效）。



- **CrawlSpider介绍：**CrawlSpider其实是Spider的一个子类，除了继承到Spider的特性和功能外，还派生除了其自己独有的更加强大的特性和功能。其中最显著的功能就是”LinkExtractors链接提取器“、” Rule : 规则解析器“。Spider是所有爬虫的基类，其设计原则只是为了爬取start_url列表中网页，而从爬取到的网页中提取出的url进行继续的爬取工作使用CrawlSpider更合适。

- 使用流程：

  - 创建一个基于CrawlSpider的爬虫文件：

    ```python
    1.创建scrapy工程：scrapy startproject projectName
    2.创建爬虫文件：scrapy genspider -t crawl spiderName www.xxx.com
    　　　　--此指令对比以前的指令多了 "-t crawl"，表示创建的爬虫文件是基于CrawlSpider这个类的，而不再是Spider这个基类。
    
    3.观察生成的爬虫文件
    import scrapy
    from scrapy.linkextractors import LinkExtractor #连接提取器
    from scrapy.spiders import CrawlSpider, Rule  #规则解析器
    
    class SunSpider(CrawlSpider):
        name = 'sun'
        allowed_domains = ['www.xxx.com']
        start_urls = ['http://www.xxx.com/']
    	link = LinkExtractor(allow=r'Items/'),
        rules = (
            # 实例化一个Rule（规则解析器）的对象
            Rule(link, callback='parse_item', follow=True),
        )
    
        def parse_item(self, response):
            item = {}
            #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
            #item['name'] = response.xpath('//div[@id="name"]').get()
            #item['description'] = response.xpath('//div[@id="description"]').get()
            return item
    ```

  - 构造连接提取器和规则解析器：CrawlSpider类和Spider类的最大不同是CrawlSpider多了一个rules属性，其作用是定义”提取动作“。在rules中可以包含一个或多个Rule对象，在Rule对象中包含了LinkExtractor对象

    **连接提取器**：可以根据指定的规则进行指定连接的提取。

    ```python
    LinkExtractor：顾名思义，链接提取器。
    LinkExtractor(
    　　　　　　　   allow=r'Items/'，#满足括号中“正则表达式”的值会被提取，如果为空则全部匹配。
    　　　　　　　　 deny=xxx,  #满足正则表达式的则不会被提取。
    
    　　　　　　　　 restrict_xpaths=xxx, # 满足xpath表达式的值会被提取
    
    　　　　　　　　 restrict_css=xxx, # 满足css表达式的值会被提取
    
    　　　　　　　　 deny_domains=xxx, # 不会被提取的链接的domains。　
    　　  )
    ```

    规则解析器：根据链接提取器中提取到的链接，根据指定规则提取解析器链接网页中的内容。

    ```python
     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True)
     参数介绍：
    　　　参数1：指定链接提取器
    　　　参数2：指定规则解析器解析数据的规则（回调函数）
    　　　参数3：是否将链接提取器继续作用到链接提取器提取出的链接网页中。当callback为None,参数3的默认值为true。
    ```

    rules=( ): 指定不同规则解析器。一个Rule对象表示一种提取规则

- ##### CrawlSpider整体爬取流程

  - 爬虫文件首先根据起始url，获取该url的网页内容a

  - 链接提取器会根据指定提取规则将步骤a中网页内容中的链接进行提取

  - 规则解析器会根据指定解析规则将链接提取器中提取到的链接中的网页内容根据指定的规则进行解析

  - 将解析数据封装到item中，然后提交给管道进行持久化存储

    案例演示：爬取阳光网投诉信息：url： <http://wz.sun0769.com/index.php/question/questionType?type=4&page=>

    解析出每一页的页码url: follow=True 将连接提取器 继续作用到 连接提取器提取到的页码连接所对应的页面中

    ```python
    import scrapy
    from scrapy.linkextractors import LinkExtractor
    from scrapy.spiders import CrawlSpider, Rule
    
    class SunSpider(CrawlSpider):
        name = 'sun'
        # allowed_domains = ['www.xxx.com']
        start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=']
    
        #连接提取器：http://wz.sun0769.com/index.php/question/report?page=，但是这个规则写的时候太多符号需要转义，所以我们想简化哈
        #简化版本：r'report\?page=\d+', 即提取规则，allow表示提取规则
        link = LinkExtractor(allow=r'type=4&page=\d+')
    
        #规则解析器
        #作用：获取连接提取器取到的连接，然后对其进行请求发送，根据指定规则对请求到的页面源码数据进行数据解析
        rules = (
            #实例化一个Rule对象
            Rule(link, callback='parse_item', follow=True),
        )
    
        def parse_item(self, response):
            print(response)
    
    #结果：
    <200 http://wz.sun0769.com/index.php/question/questionType?type=4&page=111630>
     ....
    
    ------------------------------------------------------------------
    获得更多数据
    
    class SunSpider(CrawlSpider):
        name = 'sun'
        # allowed_domains = ['www.xxx.com']
        start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=']
    
        #连接提取器：http://wz.sun0769.com/index.php/question/report?page=，但是这个规则写的时候太多符号需要转义，所以我们想简化哈
        #简化版本：r'report\?page=\d+', 即提取规则
        link = LinkExtractor(allow=r'type=4&page=\d+')
    
        #规则解析器
        #作用：获取连接提取器取到的连接，然后对其进行请求发送，根据指定规则对请求到的页面源码数据进行数据解析
        rules = (
            #实例化一个Rule对象, 这里的follow如果是False，那么只加载起始页的下方的页码连接，如果是True则可以获取每一页的下方的页码url
            #且可自动去重，也就是说所有的页码都会获取到
            Rule(link, callback='parse_item', follow=True),
        )
    
        def parse_item(self, response):
            tr_list = response.xpath('//*[@id="morelist"]/div/table[2]//tr/td/table//tr')
            for tr in tr_list:
                title = tr.xpath('./td[2]/a[2]/@title').extract_first()
                status = tr.xpath('./td[3]/span/text()').extract_first()
                print(title, status)
    ```

    

#### 基于CrawlSpider深度爬取

- 深度爬取：就是爬取多层级页面数据，有些数据爬取的时候不能像之前通过scrapy.Request()函数通过定制元信息meta，进行请求传参，因为这里我们使用的使Rule()规则解析器，所以我们不能进行深度爬取，将一组数据保存在一个item中，这里我们可以使用多个item包装数据，最后通过一个唯一码进行绑定（编号），最好存入数据库。

  ```python
   #item.py文件
  import scrapy
  #创建两个item类
  class SunproItem(scrapy.Item):
      content = scrapy.Field()
      num = scrapy.Field()
  
  class SunproItem_second(scrapy.Item):
      title = scrapy.Field()
      status = scrapy.Field()
      num = scrapy.Field()
    
  -----------------------------------------------------------------
   # pipelines.py文件
  class SunproPipeline(object):
      def process_item(self, item, spider):
          if item.__class__.__name__ == 'SunproItem':
              content = item['content']
              # 执行sql语句，但是发现不能同时存入content以及对应的title、status，我们可以用num标识
              #我们通过编号进行唯一码标识
              num = item['num']
              print(content,num)
  
          else:
              title = item['title']
              status = item['status']
              num = item['num']
              print(num,title)
  
          return item
  
  -----------------------------------------------------------------
   #sun.py文件
  import scrapy
  from scrapy.linkextractors import LinkExtractor
  from scrapy.spiders import CrawlSpider, Rule
  
  from sunPro.items import SunproItem,SunproItem_second
  
  #实现深度爬取
  class SunSpider(CrawlSpider):
      name = 'sun'
      # allowed_domains = ['www.xxx.com']
      start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=']
  
      #连接提取器：http://wz.sun0769.com/index.php/question/report?page=，但是这个规则写的时候太多符号需要转义，所以我们想简化哈
      #简化版本：r'report\?page=\d+', 即提取规则
      link = LinkExtractor(allow=r'type=4&page=\d+')   # 提取页码连接
  
      #详情页：http://wz.sun0769.com/html/question/201909/427019.shtml
      #简化版本：r'question/\d+/\d+\.shtml'
      link_detail = LinkExtractor(allow=r'question/\d+/\d+\.shtml')  #提取详情页url
  
      #规则解析器
      #作用：获取连接提取器取到的连接，然后对其进行请求发送，根据指定规则对请求到的页面源码数据进行数据解析
      rules = (
          #实例化一个Rule对象, 这里的follow如果是False，那么只加载起始页的下方的页码连接，如果是True则可以获取每一页的下方的页码url
          #且可自动去重，也就是说所有的页码都会获取到
          Rule(link, callback='parse_item', follow=True),  # 匹配到每一页url并获得response后，调用parse_item解析函数，获得每个tr
  
          #匹配每一tr对应的response，然后调用回调函数解析正文内容
          Rule(link_detail,callback='parse_detail',follow=False)  # 不需要检测每个详情页的页码，但是一般页匹配不到提取规则
      )
  
      def parse_item(self, response):
          tr_list = response.xpath('//*[@id="morelist"]/div/table[2]//tr/td/table//tr')
          for tr in tr_list:
              title = tr.xpath('./td[2]/a[2]/@title').extract_first()
              status = tr.xpath('./td[3]/span/text()').extract_first()
              num = tr.xpath('./td[1]/text()').extract_first()
  
              # 使用item 记录每个二级页面的新闻标签
              item = SunproItem_second()
              item['title'] = title
              item['status'] = status
              item['num'] = num
              yield  item
  
  
      # 注意：之前我们做深度爬取的时候，通过meta传递item，可以使每条跨页面数据共用一个item，但是现在由于Rule规则
      #作用，是我们不能使用meta传递参数，因为之前使scrap.Request类中的回调和meta元数据，但这里的Rule显然没有那种功能，
  
      #解决办法：各自存储一个item，同过唯一键进行连接绑定存储
      def parse_detail(self,response):
          # 不能出现tbody，不然匹配不到content数据
          content = response.xpath('/html/body/div[9]/table[2]//tr[1]//text()').extract()
          content = ''.join(content)
          num = response.xpath('/html/body/div[9]/table[1]//tr/td[2]/span[2]/text()').extract_first()
          if num:
              num = num.split(':')[-1]
              # 使用item，记录正文
              item = SunproItem()
              item['num'] = num
              item['content'] = content
              yield  item
              
  -------------------------------------------------------------
   #settings.py文件
  ITEM_PIPELINES = {
     'sunPro.pipelines.SunproPipeline': 300,
  }
  ROBOTSTXT_OBEY = False
  LOG_LEVEL = 'ERROR'
  BOT_NAME = 'sunPro'
  
  SPIDER_MODULES = ['sunPro.spiders']
  NEWSPIDER_MODULE = 'sunPro.spiders'
  
  USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
  ```

  

#### 分布式爬虫

**什么是分布式爬虫？：**基于多台电脑组件一个分布式机群，然后让机群中的每一台电脑执行同一组程序，然后让它们对同一个网站的数据进行分布爬取(各自爬各自的，爬过的就不会再爬了)

**为什么要使用分布式爬虫**：提升爬取数据的效率

**如何实现分布式爬虫：**

- 基于scrapy+redis的形式实现分布式：scrapy结合着scrapy-redis组件实现分布式

- 原生的scrapy框架是无法实现分布式的！

  ```
  scrapy框架是否可以自己实现分布式？不可以。原因有二。
  　　其一：因为多台机器上部署的scrapy会各自拥有各自的调度器，这样就使得多台机器无法分配start_urls列表中的url。（多台机器无法共享同一个调度器）
  　　其二：多台机器爬取到的数据无法通过同一个管道对数据进行统一的数据持久出存储。（多台机器无法共享同一个管道）
  ```

  ![1567528181079](C:\Users\wanglixing\Desktop\知识点复习\爬虫笔记\assets\1567528181079.png)



- 环境安装

  ```
  1、下载redis
  2、pip install  scrapy-redis
  ```

  

#### 基于scrapy-redis组件的分布式爬虫

- scrapy-redis组件中为我们封装好了可以被多台机器共享的调度器和管道，我们可以直接使用并实现分布式数据爬取。
  - 实现方式：

  ​            1.基于该组件的RedisSpider类

  ​            2.基于该组件的RedisCrawlSpider类

- 实现流程：

  - 创建一个工程

  - 创建一个爬虫文件：基于CrawlSpider的爬虫文件

    ```shell
    1、\scrapy学习>  scrapy startproject fbsPro
    2、\scrapy学习\fbsPro>  scrapy genspider -t crawl fbs www.xxx.com
    ```

  - 修改爬虫文件

    - 导包：from scrapy_redis.spiders import RedisCrawlSpider

    - 将当亲爬虫类的父类修改继承为RedisCrawlSpider，当然也可以继承RedisSpider，我们这就以CrawlSpider为例

    - 将start_urls替换成redis_key

      ```
      为什么要将start_url替换成redis_key?
        答：首先我们知道redis_key是一个队列，是一个分配任务的队列，我们之前的项目中爬虫对象spider一开始就从start_url中提取到主页中额页码url，然后将每个页码url封装成请求对象，到调度器中过滤等，再分布式中我们使用的是一个调度器，如果每台机器都从start_url中获取url然后发给调度器，这样调度器的压力就很大，我们其实只需要机群中的任意一台机器发起start_url请求就可以得到所有的页码对象了，这样调度器就没有过多压力再去重问题上，换句话说其他的机器就只需要守着redis_key队列，争抢任务就是了
      ```

    - 编写爬虫类爬取数据的操作

    - 在配置文件中进行相关配置，开启使用scrapy-redis组件中封装好的管道   

      ```
      ITEM_PIPELINES = {
          'scrapy_redis.pipelines.RedisPipeline': 400
      }
      ```

      ![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)在配置文件中进行相关配置，开启使用scrapy-redis组件中封装好的调度器

      ```
      # 使用scrapy-redis组件的去重队列
      DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
      # 使用scrapy-redis组件自己的调度器
      SCHEDULER = "scrapy_redis.scheduler.Scheduler"
      # 是否允许暂停
      SCHEDULER_PERSIST = True
      ```

       在配置文件中进行爬虫程序链接redis的配置：

      ```
      REDIS_HOST = 'redis服务的ip地址'
      REDIS_PORT = 6379
      REDIS_ENCODING = ‘utf-8’
      REDIS_PARAMS = {‘password’:’123456’}
      ```

    - 开启redis服务器：redis-server 配置文件

      ```
      打开redis.winds.conf文件
      	1、注释掉：bind 127.0.0.1 否则其他人无法访问
      	2、protected-mode no
      
      重启redis服务：
      	在cmd中：执行i> ./redis-server redis.windows.conf
      ```

    - 开启redis客户端：redis-cli

    - 运行爬虫文件：scrapy runspider SpiderFile

    - 向调度器队列中扔入一个起始url（在redis客户端中操作）：lpush redis_key属性值 起始url

      ```
      可设置CONCURRENT_REQUESTS =2 放慢爬取速度
      ```

    - 向调度器中仍入一个其实url：程序执行一段后会夯住，需要我们给以个url

      - 队列在哪？ 答：队列在redis中

        ```shell
        redis客户端 > lpush fbsQueue www.xxx.com  #这样就向队列中放入了起始页，返回数据后，parse会解析出其余的页码url
        
        lpush + 队列名 + 起始页url
        ```

        

  - 爬取阳光热线：爬取所有页码对应的页面标题



