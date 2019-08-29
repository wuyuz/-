
### 回顾

- 简历模板
    - 如何处理ConectionPool错误： 当爬取速度过快时，爬取数据的后端服务器的连接池用光后会报错
        - 原因：短时间内向网站发起一个高频的请求，可能会被禁用ip。或则连接池（http）中资源被耗尽
        - 解决办法：1、使用代理服务器，做请求转发，ip将会改变
                2、立即将请求断开：在headers中添加 Connection:close，使连接即连即断，释放连接资源

- 下载高清图片
    - 图片懒加载：一般的图片使用的<img src=""/>标签时，浏览器监控可视化区域，只有可见的部分的图片的img标签中的是src，未在可视化框中的img没有src属性，只有src2（这叫伪属性）
        - 

- 数据解析的作用： 为了实现聚焦爬虫
- bs4： 
    - soup.tagName
    - soup.find/find_all('tagName',attrName='value)
    - select('Selector')
        - 空格表示 多个层级 >表示一个层级
    - string/text ：返回的都是文本
    - tag['herf']
    
- xpath:
    - //tagName
    - //tagName[@attrName="value"]
    - //div[1]
    - //text or /text
    - //a/@href
    
- bs4 和 xpath最明显的一个区别是什么？
    - 解析出携带标签的局部内容？
        - bs4相关标签定位的方法或者属性返回值就是携带标签的内容，也就是说bs4定位返回的值包含着标签+标签内容，而xpath返回的是一个对象

#### 代理
- 代理
    - 代理服务器：实现请求转化，从而可以实现更换请求的ip地址
    - 在requests中如何将请求的ip进行更换
    
- 代理的匿名度：
    - 透明：服务器知道你使用了代理并且知道你的真实ip
    - 匿名：服务器知道你使用了代理，但是不知道你的真实ip
    - 高匿：服务器不知道你使用了代理和真实ip

- 代理的类型：
    - http： 该类型的代理只可以转发http协议的请求
    - https: 只可以转发https的协议的请求
    
- 免费的代理ip网站
    - 快代理
    - 西祠代理
    - goubanjia（http://www.goubanjia.com/）
    - 智连代理（http://http.zhiliandaili.cn/）

- 我们通过在智连代理中，购买一天3块钱，然后选择配置，最后通过网址获得代理ip

- 在爬虫中遇到ip被禁掉如何处理？
    - 使用代理
    - 构建一个代理池
    - 拨号服务器


```python
import requests

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

url = 'https://www.baidu.com/s?wd=ip'
# proxies={'http/https':'ip:port'}

# 设置代理ip,使用proxies
page_text = requests.get(url,headers=headers,proxies={'http':'117.191.11.71:80'}).text
with open('./ip.html','w',encoding='utf-8') as f:
    f.write(page_text)
```

### 基于代理ip爬取西祠代理的数据


```python
# 基于代理精灵构建一个ip池，我们通过智连代理获取到IP相应的网址，通过网址取获取ip
from lxml import etree
import requests,re,random

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

# 由于这里我们没有消费代理IP，下面我们将使用goubanjia的ip取构建ip池
# proxy_url = 'http://t.xxxxx'
# proxy_page_text = requests.get(url=proxy_url,headers=headers).text

#基于goubanjia构建ip池, 发现端口是动态生成
# proxy_url = 'http://www.goubanjia.com'
# proxy_page_text = requests.get(url=proxy_url,headers=headers).text


# 简言说明下大致的规则，div/span交替配置文件
#<td class="ip"><p style="display:none;">21</p><span>21</span>
#<p style="display:none;"></p><span></span><div style="display:inline-block;"></div>
#<div style="display: inline-block;"></div><span style="display:inline-block;"></span>
#<span style="display: inline-block;">0.</span><div style="display: inline-block;">2</div>
#<span style="display:inline-block;"></span><span style="display: inline-block;">2</span>
#<p style="display: none;">.5</p><span>.5</span><p style="display:none;">.</p><span>.</span>
#<p style="display: none;">1</p><span>1</span><div style="display: inline-block;">17</div>:<span class="port CFACE">3128</span></td>

# tree = etree.HTML(proxy_page_text)
# proxy_list = tree.xpath('//table[@class="table table-hover"]//tbody/tr')
# for ip in proxy_list:

#     # 下面通过'|'管道符号表示或关系，使用contains(包含属性)进行匹配，然后':'是通过./td[1]/text()可以取得因为没有标签包裹
#     ret = ''.join(ip.xpath('./td[1]/div[contains(@style,"display:inline-block")]//text() | ./td[1]/span[contains(@style,"display:inline-block")]//text() |./td[1]/text()| ./td[1]/span//text()'))
#     last = ip.xpath('./td[1]/span[last()]/text()')
#     print(ret,last)


#最后手动添加免费ip池
all_ips=[
    {'https':'111.231.90.122:8888'},
    {'https':'111.231.92.21:8888'},
]

free_proxies=[]

#爬取西祠代理
url = 'https://www.xicidali.com/nn/%d'
for page in range(1,10):
    new_url = url%page
    #没有使用ip代理可能爬几页就会被禁
    #page_text = requests.get(new_url,headers=headers).text
    
    #使用ip池
    page_text = requests.get(new_url,headers=headers,proxies=random.choice(all_ips)).text

    tree=etree.HTML(page_text)
    tr_list = tree.xpath('//*[@id="ip_list"]//tr')[1:] # 注意：xpath表达式中不可以出现tbody，否则出现不了
    for tr in tr_list:
        ip=tr.xpath('./td[2]/text()')[0]
        port=tr.xpath('./td[3]/text()')[0]
        t_type=tr.xpath('./td[7]/text()')[0]  
        
        dic={
            'ip':ip,
            'port':port,
            'type':t_type
        }
        print(dic)
        free_proxies.append(dic)
    print(f'第{page}爬取完毕')
print(len(free_proxies))
```

### Cookie
- 作用： 保存客户端的相关状态
- 爬取雪球网中的新闻资讯数据

- 在请求中携带cookie，在爬取中如果遇到了cookie的反爬如何处理？
    - 手动处理
        - 在抓包工具中获取cookie，将其封装在headers中
        - 应用场景： cookie没有有效时长且不是动态变化
    - 自动处理：
        - 使用session机制
        - 使用场景：动态变化的cookie
        - session对象： 该对象和requests模块用户几乎一致，如果在请求的过程中产生了cookie，如果该请求使用session发起的，则cookie会被自动存储到session中

### 爬取雪球网

- 使用Session来解决cookie问题


```python
#发现所有的数据都是通过ajax给以下数据发起请求
url='https://xueqiu.com/v4/statuses/public_timeline_by_category.json'

#使用session来保存session
session = requests.Session()

#注意：当用户使用的是ajax发请求的时候，也就是说在加载首页的时候就存了cookie在浏览器中，之后
#通过发请求时下能通过，那么我们需要模拟访问一次首页，才能获得cookie
main_url = 'https://xueqiu.com'
session.get(main_url,headers=headers)

params={
    'since_id': '-1',
    'max_id': '20347175',
    'count': '15',
    'category': '-1',
}

#使用session来发请求
page_text = session.get(url,headers=headers,params=params).json()
# 不能获取数据，要么是ip被禁了，要么就是cookie，因为Headers携带了cookie

```

### 验证登陆
- 相关的线上大码平台识别
    - 打码兔
    - 云打码
    - 超级鹰（http://www.chaojiying.com）
        - 注册，登陆（用户中心身份验证）
        - 充值，创建软件，生成一个软件id，（901284）
        - 下载演示代码，下载粘贴到我们的页面中
        


```python
import requests
from hashlib import md5
class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()



# chaojiying = Chaojiying_Client('wuyuzhu', 'wuyuzhu', '901284')	#用户中心>>软件ID 生成一个替换 96001
# im = open('a.jpg', 'rb').read()#本地图片文件路径 来替换 a.jpg 有时WIN系统须要
# print(chaojiying.PostPic(im, 1902))#1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
```

    {'err_no': 0, 'err_str': 'OK', 'pic_id': '9078521582932500001', 'pic_str': '7261', 'md5': '837d86be3cf1f0567b7a730f9ddd194e'}


 ### 自动登陆古诗文网
 - url:https://so.gushiwen.org/user/login.aspx?from=http://so.gushiwen.org/user/collect.aspx
 - 将古诗文网中的验证码图片进行识别：

 #### 验证码识别


```python
def getCodeImgText(imgPath,img_type):
    chaojiying = Chaojiying_Client('wuyuzhu', 'wuyuzhu', '901284')	#用户中心>>软件ID 生成一个替换 96001
    im = open(imgPath, 'rb').read()#本地图片文件路径 来替换 a.jpg 有时WIN系统须要
    return chaojiying.PostPic(im, img_type)['pic_str']  #1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
```


```python
url = 'https://so.gushiwen.org/user/login.aspx?from=http://so.gushiwen.org/user/collect.aspx'
page_text = requests.get(url,headers=headers).text
tree = etree.HTML(page_text)
img_src ='https://so.gushiwen.org' + tree.xpath('//*[@id="imgCode"]/@src')[0]
img_code_data = requests.get(img_src,headers=headers).content

with open('./gushiwen.jpg','wb') as f:
    f.write(img_code_data)
    
img_text = getCodeImgText('./gushiwen.jpg',1004)
# print(img_text)
```

    teer
    None


#### 为什么在爬虫中需要实现模拟登陆
- 有的数据是必须经过登陆后才可以显示出来的
- 额外注意一些post中出现的未见过的参数，可能时动态生成的，我们叫做动态请求参数


- 涉及到的反爬：
    - 验证码
    - 动态请求参数，每次请求对应的请求参数都是动态变化的

        - 动态捕获： 通常情况下，动态的请求参数都会隐藏在前台页面的源码中，通过全局搜索出对应的动态参数

     - cookie: 找到那个请求获得请求，其实时在验证码请求时获得的cookie
       
        

### 对古诗文模拟登陆


```python
def getCodeImgText(imgPath,img_type):
    chaojiying = Chaojiying_Client('wuyuzhu', 'wuyuzhu', '901284')
    im = open(imgPath, 'rb').read()
    return chaojiying.PostPic(im, img_type)['pic_str'] 

# 使用session捕获cookie
s = requests.Session()

first_url = 'https://so.gushiwen.org/user/login.aspx?from=https://so.gushiwen.org/user/collect.aspx'
s.get(first_url,headers=headers)

url = 'https://so.gushiwen.org/user/login.aspx?from=http://so.gushiwen.org/user/collect.aspx'
page_text = s.get(url,headers=headers).text
tree = etree.HTML(page_text)
img_src ='https://so.gushiwen.org' + tree.xpath('//*[@id="imgCode"]/@src')[0]

# 在此将获得cookie
img_code_data = s.get(img_src,headers=headers).content

with open('./gushiwen.jpg','wb') as f:
    f.write(img_code_data)

# 识别验证码
img_text = getCodeImgText('./gushiwen.jpg',1004)

# 获取动态请求参数
__VIEWSTATE = tree.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
__VIEWSTATEGENERATOR = tree.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]

# 点击登陆按钮后发起请求的url，通过抓包工具捕获，登陆时带有输入数据的url接口
login_url = 'https://so.gushiwen.org/user/login.aspx?from=https://so.gushiwen.org/user/collect.aspx'

print(img_text,__VIEWSTATE,__VIEWSTATEGENERATOR)

data = {
    '__VIEWSTATE': __VIEWSTATE,
    '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
    'from': 'https://so.gushiwen.org/user/collect.aspx',
    'email': '18997207634',
    'pwd': '18997207634',
    'code': img_text,
    'denglu': '登录',
}


main_page_text = s.post(login_url,headers=headers,data=data).text
with open('./main.html','w',encoding='utf-8') as f:
    f.write(main_page_text)
    

# 验证码正确但是仍然不能获取正确的数据，注意我们的data出现了两个未见多的参数，那么我们就
# 可能猜测，他就是一种csrftoken的存在数据，也就是说在某个请求中获得了服务器端的token值，必须
# 加这个值才能合理的提交数据
```

    lcsy lHpFNj2fB0ebewhzeAY5tI4hHBfQFUsMnl5W1CLEO2WuQxkkKqfYc/+ucGQohG+q/B5iuAfTfYUanZecvF12Bf61Jl0Hxn5Bx9ncYO6YgSg6ry+9mMOQiXFup0U= C93BE1AE

#### 基于线程池的异步爬取

```python
url = 'https://www.qiushibaike.com/text/page/%d/'
urls = []
for page in range(1,11):
    new_url = format(url%page)
    urls.append(new_url)
    
def get_request(url): #必须有一个参数
    return requests.get(url,headers=headers).text

from multiprocessing.dummy import Pool
pool = Pool(10)
response_text_list = pool.map(get_request,urls) #使用自定义的函数func异步的处理urls列表中的每一个列表元素
# print(response_text_list)
```



#### 理论知识回顾

##### Cookie 和 Session

- 无状态的http协议：

  ![1567008327376](C:\Users\wanglixing\AppData\Roaming\Typora\typora-user-images\1567008327376.png)

  ​     如上图所示，HTTP协议 是无状态的协议，用户浏览服务器上的内容，只需要发送页面请求，服务器返回内容。对于服务器来说，并不关心，也并不知道是哪个用户的请求。对于一般浏览性的网页来说，没有任何问题。
    - 但是，现在很多的网站，是需要用户登录的。以淘宝为例：比如说某个用户想购买一个产品，当点击 “ 购买按钮 ” 时，由于HTTP协议 是无状态的，那对于淘宝来说，就不知道是哪个用户操作的。
    - 为了实现这种用户标记，服务器就采用了cookie这种机制来识别具体是哪一个用户的访问。

- **了解Cookie**

  ![1567008418871](C:\Users\wanglixing\AppData\Roaming\Typora\typora-user-images\1567008418871.png)

  - ​     如图，为了实现用户标记，在Http无状态请求的基础之上，我们需要在请求中携带一些用户信息（比如用户名之类，这些信息是服务器发送到本地浏览器的，但是服务器并不存储这些信息），这就是cookie机制。

    ​      需要注意的是：cookie信息是保存在本地浏览器里面的，服务器上并不存储相关的信息。 在发送请求时，cookie的这些内容是放在 Http协议中的header 字段中进行传输的。几乎现在所有的网站都会发送一些 cookie信息过来，当用户请求中携带了cookie信息，服务器就可以知道是哪个用户的访问了，从而不需要再使用账户和密码登录。但是，刚才也提到了，cookie信息是直接放在Http协议的header中进行传输的，看得出来，这是个隐患！一旦别人获取到你的cookie信息（截获请求，或者使用你的电脑），那么他很容易从cookie中分析出你的用户名和密码。为了解决这个隐患，所以有了session机制。



- **了解session**

  刚才提到了cookie不安全，所以有了session机制。简单来说（每个框架都不一样，这只是举一个通用的实现策略），整过过程是这样： 
    - 服务器根据用户名和密码，生成一个session ID，存储到服务器的数据库中。
    - 用户登录访问时，服务器会将对应的session ID发送给用户（本地浏览器）。

  -  浏览器会将这个session ID存储到cookie中，作为一个键值项。

  - 以后，浏览器每次请求，就会将含有session ID的cookie信息，一起发送给服务器。

  - 服务器收到请求之后，通过cookie中的session ID，到数据库中去查询，解析出对应的用户名，就知道是哪个用户的请求了。



#### 爬取梨视频的视频信息，并计算其爬取数据的耗时

- 普通爬取

  ```python
  import requests
  import random
  from lxml import etree
  import re
  from fake_useragent import UserAgent
  #安装fake-useragent库:pip install fake-useragent
  url = 'http://www.pearvideo.com/category_1'
  #随机产生UA,如果报错则可以添加如下参数：
  #ua = UserAgent(verify_ssl=False,use_cache_server=False).random
  #禁用服务器缓存：
  #ua = UserAgent(use_cache_server=False)
  #不缓存数据：
  #ua = UserAgent(cache=False)
  #忽略ssl验证：
  #ua = UserAgent(verify_ssl=False)
  
  ua = UserAgent().random
  headers = {
      'User-Agent':ua
  }
  #获取首页页面数据
  page_text = requests.get(url=url,headers=headers).text
  #对获取的首页页面数据中的相关视频详情链接进行解析
  tree = etree.HTML(page_text)
  li_list = tree.xpath('//div[@id="listvideoList"]/ul/li')
  detail_urls = []
  for li in li_list:
      detail_url = 'http://www.pearvideo.com/'+li.xpath('./div/a/@href')[0]
      title = li.xpath('.//div[@class="vervideo-title"]/text()')[0]
      detail_urls.append(detail_url)
  for url in detail_urls:
      page_text = requests.get(url=url,headers=headers).text
      vedio_url = re.findall('srcUrl="(.*?)"',page_text,re.S)[0]
      
      data = requests.get(url=vedio_url,headers=headers).content
      fileName = str(random.randint(1,10000))+'.mp4' #随机生成视频文件名称
      with open(fileName,'wb') as fp:
          fp.write(data)
          print(fileName+' is over')
  ```

- 基于线程池的爬取

  ```python
  import requests
  import random
  from lxml import etree
  import re
  from fake_useragent import UserAgent
  #安装fake-useragent库:pip install fake-useragent
  #导入线程池模块
  from multiprocessing.dummy import Pool
  #实例化线程池对象
  pool = Pool()
  url = 'http://www.pearvideo.com/category_1'
  #随机产生UA
  ua = UserAgent().random
  headers = {
      'User-Agent':ua
  }
  #获取首页页面数据
  page_text = requests.get(url=url,headers=headers).text
  #对获取的首页页面数据中的相关视频详情链接进行解析
  tree = etree.HTML(page_text)
  li_list = tree.xpath('//div[@id="listvideoList"]/ul/li')
  
  detail_urls = []#存储二级页面的url
  for li in li_list:
      detail_url = 'http://www.pearvideo.com/'+li.xpath('./div/a/@href')[0]
      title = li.xpath('.//div[@class="vervideo-title"]/text()')[0]
      detail_urls.append(detail_url)
      
  vedio_urls = []#存储视频的url
  for url in detail_urls:
      page_text = requests.get(url=url,headers=headers).text
      vedio_url = re.findall('srcUrl="(.*?)"',page_text,re.S)[0]
      vedio_urls.append(vedio_url) 
  #使用线程池进行视频数据下载    
  func_request = lambda link:requests.get(url=link,headers=headers).content
  video_data_list = pool.map(func_request,vedio_urls)
  #使用线程池进行视频数据保存
  func_saveData = lambda data:save(data)
  pool.map(func_saveData,video_data_list)
  def save(data):
      fileName = str(random.randint(1,10000))+'.mp4'
      with open(fileName,'wb') as fp:
          fp.write(data)
          print(fileName+'已存储')
          
  pool.close()
  pool.join()
  
  ```

  