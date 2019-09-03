## Scrapy 运用与总结



#### 介绍：

​	Scrapy是一个为了爬取网站数据，提取结构性数据而编写的应用框架。 可以应用在包括数据挖掘，信息处理或存储历史数据等一系列的程序中。所谓的框架就是一个已经被集成了各种功能（高性能异步下载，队列，分布式，解析，持久化等）的具有很强通用性的项目模板。对于框架的学习，重点是要学习其框架的特性、各个功能的用法即可。

​	

![1567417350117](C:\Users\wanglixing\AppData\Roaming\Typora\typora-user-images\1567417350117.png)



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

  ![1567441302414](C:\Users\wanglixing\Desktop\知识点复习\爬虫笔记\1567441302414.png)



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

  