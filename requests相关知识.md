
### HTTP 和 HTTPS

- http:
    - 概念： Clinet和Server进行数据交互的某种形式

- 常用的头信息：
    - User-Agent: 请求载体的身份标识，请求载体可以时浏览器/requests模块等
    - Connection: keep-alive 长连接， close 短链接
    - Content-Type: 响应格式

- https:
    - 概念： 安全的http协议
        - 证书
            - 证书密钥加密
            - 非对称密钥加密
            - 对称密钥加密



### 爬虫相关概述

- 爬虫概念：
    - 通过编写程序模拟浏览器上网，然后让其去互联网上爬取/抓取数据的过程
        - 模拟： 浏览器就是一款纯天然的原始的爬虫工具
    
- 爬虫分类：
     - 通用爬虫：爬取一整张页面中的数据，爬去数据（爬虫程序）
     - 聚焦爬虫： 爬取页面中局部的数据。一定是建立在通用爬虫的基础之上
     - 增量式爬虫： 用来检测网站数据更新的情况，以便爬取到网站最新更新出来的数据
     
- 风险分析：
    - 合理的使用
    - 爬虫风险的体现：
        - 爬虫干扰了被访问网站的正常运营
        - 爬虫爬取了受到了法律保护的特定类型的数据和信息
    - 避免风险：
        - 严格遵守网站设置robots协议；
        - 在规避反爬虫措施的同时， 需要优化自己的代码，避免干扰被访问网站的正常运行；
        - 在使用、传播抓取到的信息时，应审查所爬取的内容，如发现属于用户的个人信息、隐私或他人商务机密时，应及停止并删除
    
- 反爬机制
- 反反爬策略

- robots.txt协议： 文本协议，在文本中指定了可爬和不可爬数据的说明



### reqeust模块

- 概念： 一个基于网络请求的模块，作用就是用来模拟浏览器发起请求。requests模块是python中原生的基于网络请求的模块，其主要作用是用来模拟浏览器发起请求。功能强大，用法简洁高效。在爬虫领域中占据着半壁江山的地位。

- 编码流程：
  - 指定url
  - 进行请求的发送
  - 获取相应数据(爬取到的数据)
  - 持久化存储

- 环境安装

  - pip install reqeusts

  

#### requests模块和urllib模块

- requests和urllib模块对比

  ```
  因为在使用urllib模块的时候，会有诸多不便之处，总结如下：
  	1、手动处理url编码
  	2、手动处理post请求参数
  	3、处理cookie和代理操作繁琐
  	......
  	
  使用requests模块：
  	1、自动处理url编码
  	2、自动处理post请求参数
  	3、简化cookie和代理操作
  	......
  ```



### 爬取搜狗首页对应的页面源码数据


```python
import requests
#step_1
url = 'https://www.sogou.com'

#setp_2, shift+tab 打开提示, 返回值是一个响应对象
response = requests.get(url=url)

#step_3: text 返回的是字符串形式的响应数据
page_text = response.text

#step_4：持久化保存
with open('./sogou.html','w',encoding='utf-8') as f:
    f.write(page_text)
```

### 基于搜狗编写一个简易的网页采集器


```python
#想要将url携带的参数自行设定
wd = input('enter a key: ')
url = 'https://www.sogou.com/web'

#存储的就是动态的请求参数
params = {
    'query':wd
}

# 一定需要将params作用到请求中
# params参数表示的是对请求url参数的封装
requests.get(url=url, params=params)

#手动修改响应数据的编码，设置响应体以什么编码，
response.encoding = 'utf-8'

page_text = response.text

fileName = wd + '.html'
with open(fileName,'w',encoding='utf-8') as f:
    f.write(page_text)
    
print(wd,'下载成功')
```

    enter a key: 邓紫棋
    邓紫棋 下载成功


- 上述程序出现的问题
    - 问题1：中文乱码？
        - 手动修改响应数据的编码，设置响应体以什么编码
             response.encoding = 'utf-8' 
        
    - 问题2：遇到UA反爬机制？
        - 添加headers，用来实现UA伪装

### 反爬机制
- 反爬机制： UA检测，某些门户网站会对访问该网站的请求中的User-Agent进行捕获和判断，如果该请求的UA为爬虫程序，则拒绝向该请求提供数据。

  ```
  User-Agent：请求载体身份标识，通过浏览器发起的请求，请求载体为浏览器，则该请求的User-Agent为浏览器的身份标识，使用爬虫程序发起的请求，则该请求的载体为爬虫程序，则该请求的User-Agent为爬虫程序的身份标识。可以通过判断该值来获知该请求的载体究竟是基于哪款浏览器还是基于爬虫程序。
  ```

  

- 反反爬机制: UA伪装，将爬虫程序的UA伪装成某一款浏览器的身份标识。


```python
#想要将url携带的参数自行设定
wd = input('enter a key: ')
url = 'https://www.sogou.com/web'

#存储的就是动态的请求参数
params = {
    'query':wd
}

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

# 一定需要将params作用到请求中
# params参数表示的是对请求url参数的封装
requests.get(url=url, params=params,headers=headers)

#手动修改响应数据的编码，设置响应体以什么编码，
response.encoding = 'utf-8'

page_text = response.text

fileName = wd + '.html'
with open(fileName,'w',encoding='utf-8') as f:
    f.write(page_text)
    
print(wd,'下载成功')
```

    enter a key: 周杰伦
    周杰伦 下载成功



 ### 爬取豆瓣电影信息

 - 爬取电影的排行榜：
     https://movie.douban.com/typerank?type_name=%E5%96%9C%E5%89%A7&type=24&interval_id=100:90&action=
     
 - 爬取豆瓣电影的电影详情数据电影
     - 分析： 当滚轮滑动到底部的时候， 发起一个ajax请求，且该请求请求到一组数据，也就是说网站并没有变化，当我们打开浏览器的Network抓包工具，选中XHR时（用来检测ajax请求的），可以查看变化
     
 - 动态加载的数据： 就是通过另一个额外的请求请求到的数据
     - ajax 生成动态加载的数据
     - js 生成动态的数据


```python
# 我们打开每次滚动后加载的XHR的ajax请求，看看每次ajax访问的是什么网址，发现都是对一个接口进行发送数据，如下
url = 'https://movie.douban.com/j/chart/top_list'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

start = input('enter a start: ')

limit = input('enter a limit: ')

#处理请求参数,参考具体的请求头数据，进行整合我们的参数
params = {
    'type':'5',
    'interval_id':'100:90',
    'action':'',
    'start':start,
    'limit':limit
}

response = requests.get(url=url, params=params,headers=headers)

#返回的是序列化好的对象
data_list = response.json()

with open('douban.txt','w', encoding='utf-8') as f:
    for dict in data_list:
        name = dict['title']
        score = dict['score']
        f.write(name+':'+ score+'\n')
        print(name,'爬取成功')
```

    enter a start: 1
    enter a limit: 1



### 如何判定一张也页面中是否存在动态加载的数据

**什么是动态加载数据？**
    - 访问一个网址，即发起一个请求，得到一个响应，但是当有些页面数据没有在返回的response中的时候，此时就是在加载页面的时候又其他respose中返回出的数据，可能是ajax、也可能是js返回的数据

- 爬取企业详细信息： http://125.35.6.84:81/xk/

- 抓包工具进行局部搜索： 在response中ctrl+f搜索，没有搜到表示数据不是来自响应，而是动态加载
- 如果判定出页面中又动态加载的数据如何进行数据定位？
    - 使用抓包工具进行全局搜索，有个放大镜
    
- 具体操作：
    - 我们访问上面的网址，发现每一个数据都是动态加载，再点击任意一个数据进入后，没有数据也是动态加载，也是就说里面的数据有些是局部搜不到的，表示是动态加载的，只能通过全局搜索
    
    - 我们取出每个企业页面的一条数据，进行全局搜索，我们找到生成数据的是一个xvasfdaf=dfafdaf(可能是一个ajax/js),我们点击它的 Header查看，发现是ajax(post)得到的，请求对应的url='http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById'
    
    - 该请求携带了一个参数：id:xxxx
    - 发现规律：所有的企业都是针对上一个网址，拼接对应的id，获得的数据，那么我们只要知道对应的id，就可以得到响应的数据
    
    - 获取每一家企业的id值：
        - 思路： 每一家企业的id值应该存储再首页对应的相关响应的数据中，只需要获得企业id即可
        - 我们打开首页，发现数据都是通过ajax的post方式请求的，且url='http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList'
        - 我们可以通过提交相应的数据给这个url，从而获得id
        


```python
# 获取每家企业的对应id
url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

data={
   'on':'true',
    'page':'1',
    'pageSize':'15',
    'productName':'',
    'conditionType':'1',
    'applyname':'',
    'applysn':'',
}

fp = open('./company_detail.txt','w',encoding='utf-8')

# 该json() 的返回值中就有每一家企业的id
data_dic = requests.post(url=url,data=data,headers=headers).json()
for dic in data_dic['list']:
    _id = dic['ID']
    print(_id)
    
    #对每一个id对应的企业详情数据进行捕获（发起请求）
    post_url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById'
    post_data = {
        'id':_id
    }
    
    # json返回值是某一家企业的详情信息
    detail_dic = requests.post(url=post_url,data=post_data,headers=headers).json()
    company_title = detail_dic['epsName']
    address = detail_dic['epsProductAddress'] 
    fp.write(company_title+': '+address+'\n')
    print(company_title,'爬取成功')

fp.close()
```



#### 爬取国家药品监督管理总局中基于中华人民共和国化妆品生产许可证相关数据

```python
import requests
from fake_useragent import UserAgent

ua = UserAgent(use_cache_server=False,verify_ssl=False).random
headers = {
    'User-Agent':ua
}

url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList'
pageNum = 3
for page in range(3,5):
    data = {
        'on': 'true',
        'page': str(page),
        'pageSize': '15',
        'productName':'',
        'conditionType': '1',
        'applyname':'',
        'applysn':''
    }
    
    json_text = requests.post(url=url,data=data,headers=headers).json()
    all_id_list = []
    for dict in json_text['list']:
        id = dict['ID']#用于二级页面数据获取
        #下列详情信息可以在二级页面中获取
        # name = dict['EPS_NAME']
        # product = dict['PRODUCT_SN']
        # man_name = dict['QF_MANAGER_NAME']
        # d1 = dict['XC_DATE']
        # d2 = dict['XK_DATE']
        all_id_list.append(id)
    #该url是一个ajax的post请求
    post_url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById'
    for id in  all_id_list:
        post_data = {
            'id':id
        }
        response = requests.post(url=post_url,data=post_data,headers=headers)
        #该请求响应回来的数据有两个，一个是基于text，一个是基于json的，所以可以根据content-type,来获取指定的响应数据
        if response.headers['Content-Type'] == 'application/json;charset=UTF-8':
            #print(response.json())
            #进行json解析
            json_text = response.json()
            print(json_text['businessPerson'])
```

