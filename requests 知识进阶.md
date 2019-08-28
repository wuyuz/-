## requests 知识进阶

### 1、模块说明

requests是使用Apache2 licensed 许可证的HTTP库。用python编写。比urllib2模块更简洁。

Request支持HTTP连接保持和连接池，支持使用cookie保持会话，支持文件上传，支持自动响应内容的编码，支持国际化的URL和POST数据自动编码。

在python内置模块的基础上进行了高度的封装，从而使得python进行网络请求时，变得人性化，使用Requests可以轻而易举的完成浏览器可有的任何操作。现代，国际化，友好。requests会自动实现持久连接keep-alive

### **2、基础入门**

1）导入模块

```
import requests
```

2）发送请求的简洁

　　示例代码：获取一个网页（个人`github`）

```python
import requests
  
r = requests.get('https://github.com/Ranxf')       # 最基本的不带参数的get请求
r1 = requests.get(url='http://dict.baidu.com/s', params={'wd': 'python'})      # 带参数的get请求   
```

我们就可以使用该方式使用以下各种方法

```python
requests.get(‘https://github.com/timeline.json’)    # GET请求
requests.post(“http://httpbin.org/post”)            # POST请求
requests.put(“http://httpbin.org/put”)              # PUT请求
requests.delete(“http://httpbin.org/delete”)        # DELETE请求
requests.head(“http://httpbin.org/get”)             # HEAD请求
requests.options(“http://httpbin.org/get” )         # OPTIONS请求
```

3）为url传递参数

```python
>>> url_params = {'key':'value'}     # 字典传递参数，如果值为None的键不会被添加到url中
>>> r = requests.get('your url',params = url_params) # get方式使用params传参
>>> print(r.url)
...your url?key=value
```

4）响应的内容

```python
r.encoding                       #获取当前的编码
r.encoding = 'utf-8'             #设置编码
r.text                           #以encoding解析返回内容。字符串方式的响应体，会自动根据响应头部的字符编码进行解码。

r.content                        #以字节形式（二进制）返回。字节方式的响应体，会自动为你解码 gzip 和 deflate 压缩。返回byte类型，可以直接保存音频/图片等

r.headers                        #以字典对象存储服务器响应头，但是这个字典比较特殊，字典键不区分大小写，若键不存在则返回None

r.status_code                     #响应状态码
r.raw                             #返回原始响应体，也就是 urllib 的 response 对象，使用 r.raw.read()   

r.ok                              # 查看r.ok的布尔值便可以知道是否登陆成功

 #*特殊方法*#
r.json()                         #Requests中内置的JSON解码器，以json形式返回,前提返回的内容确保是json格式的，不然解析出错会抛异常，将返回的json对象反序列化
r.raise_for_status()             #失败请求(非200响应)抛出异常
```

post发送json请求：

```python
import requests
import json
  
r = requests.post('https://api.github.com/some/endpoint', data=json.dumps({'some': 'data'}))
print(r.json())
```

5）定制头和cookie信息

```python
header = {'user-agent': 'my-app/0.0.1''}
cookie = {'key':'value'}
r = requests.get/post('your url',headers=header,cookies=cookie) 
```

```python
import requests
import json
 
data = {'some': 'data'}
headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
 
r = requests.post('https://api.github.com/some/endpoint', data=data, headers=headers)
print(r.text)
```

6）响应状态码

使用requests方法后，会返回一个response对象，其存储了服务器响应的内容，如上实例中已经提到的 r.text、r.status_code……
获取文本方式的响应体实例：当你访问 r.text 之时，会使用其响应的文本编码进行解码，并且你可以修改其编码让 r.text 使用自定义的编码进行解码。

```python
r = requests.get('http://www.itwhy.org')
print(r.text, '\n{}\n'.format('*'*79), r.encoding)
r.encoding = 'GBK'
print(r.text, '\n{}\n'.format('*'*79), r.encoding)
```

​    示例代码：

```python
import requests
 
r = requests.get('https://github.com/Ranxf')       # 最基本的不带参数的get请求
print(r.status_code)                               # 获取返回状态
r1 = requests.get(url='http://dict.baidu.com/s', params={'wd': 'python'})      # 带参数的get请求
print(r1.url)
print(r1.text)        # 打印解码后的返回数据
```

 运行结果：

```python
/usr/bin/python3.5 /home/rxf/python3_1000/1000/python3_server/python3_requests/demo1.py
200
http://dict.baidu.com/s?wd=python
…………

Process finished with exit code 0
```

```python
 r.status_code                      #如果不是200，可以使用 r.raise_for_status() 抛出异常
```

7）响应

```python
r.headers                                  #返回字典类型,头信息
r.requests.headers                         #返回发送到服务器的头信息
r.cookies                                  #返回cookie
r.history                                  #返回重定向信息,当然可以在请求是加上allow_redirects = false 阻止重定向
```

8）超时

```python
r = requests.get('url',timeout=1)           #设置秒数超时，仅对于连接有效
```

9)会话对象，能够跨请求保持某些参数

```python
s = requests.Session()
s.auth = ('auth','passwd')
s.headers = {'key':'value'}
r = s.get('url')
r1 = s.get('url1') 
```

10）代理

```python
proxies = {'http':'ip1','https':'ip2' }
requests.get('url',proxies=proxies)
```

 汇总：

```python
# HTTP请求类型
# get类型
r = requests.get('https://github.com/timeline.json')
# post类型
r = requests.post("http://m.ctrip.com/post")
# put类型
r = requests.put("http://m.ctrip.com/put")
# delete类型
r = requests.delete("http://m.ctrip.com/delete")
# head类型
r = requests.head("http://m.ctrip.com/head")
# options类型
r = requests.options("http://m.ctrip.com/get")

# 获取响应内容
print(r.content) #以字节的方式去显示，中文显示为字符
print(r.text) #以文本的方式去显示

#URL传递参数
payload = {'keyword': '香港', 'salecityid': '2'}
r = requests.get("http://m.ctrip.com/webapp/tourvisa/visa_list", params=payload) 
print（r.url） #示例为http://m.ctrip.com/webapp/tourvisa/visa_list?salecityid=2&keyword=香港

#获取/修改网页编码
r = requests.get('https://github.com/timeline.json')
print （r.encoding）


#json处理
r = requests.get('https://github.com/timeline.json')
print（r.json()） # 需要先import json    

# 定制请求头
url = 'http://m.ctrip.com'
headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
r = requests.post(url, headers=headers)
print （r.request.headers)

#复杂post请求
url = 'http://m.ctrip.com'
payload = {'some': 'data'}
r = requests.post(url, data=json.dumps(payload)) #如果传递的payload是string而不是dict，需要先调用dumps方法格式化一下

# post多部分编码文件
url = 'http://m.ctrip.com'
files = {'file': open('report.xls', 'rb')}
r = requests.post(url, files=files)

# 响应状态码
r = requests.get('http://m.ctrip.com')
print(r.status_code)
    
# 响应头
r = requests.get('http://m.ctrip.com')
print (r.headers)
print (r.headers['Content-Type'])
print (r.headers.get('content-type')) #访问响应头部分内容的两种方式
    
# Cookies
url = 'http://example.com/some/cookie/setting/url'
r = requests.get(url)
r.cookies['example_cookie_name']    #读取cookies
    
url = 'http://m.ctrip.com/cookies'
cookies = dict(cookies_are='working')
r = requests.get(url, cookies=cookies) #发送cookies

#设置超时时间
r = requests.get('http://m.ctrip.com', timeout=0.001)

#设置访问代理
proxies = {
           "http": "http://10.10.1.10:3128",
           "https": "http://10.10.1.100:4444",
          }
r = requests.get('http://m.ctrip.com', proxies=proxies)


#如果代理需要用户名和密码，则需要这样：
proxies = {
    "http": "http://user:pass@10.10.1.10:3128/",
}
```

### 3、示例代码

### GET请求

```python
# 1、无参数实例  
import requests   
ret = requests.get('https://github.com/timeline.json')
print(ret.url)
print(ret.text)
   
  
# 2、有参数实例 
import requests  
payload = {'key1': 'value1', 'key2': 'value2'}
ret = requests.get("http://httpbin.org/get", params=payload)   
print(ret.url)
print(ret.text)
```



### POST请求

```python
# 1、基本POST实例
import requests 
payload = {'key1': 'value1', 'key2': 'value2'}
ret = requests.post("http://httpbin.org/post", data=payload) #上传data数据
print(ret.text) 
  
# 2、发送请求头和数据实例 
import requests
import json 
url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}
headers = {'content-type': 'application/json'}  
ret = requests.post(url, data=json.dumps(payload), headers=headers)
  
print(ret.text)
print(ret.cookies)
```



#### request的各种应用场景

```python
 #请求网址
def param_method_url():
    requests.request(method='get', url='http://127.0.0.1:8000/test/')
    requests.request(method='post', url='http://127.0.0.1:8000/test/')
    pass

 #params用于get方式传递参数
def param_param():       
	 #可以是字典
    requests.request(method='get',
    url='http://127.0.0.1:8000/test/',
    params={'k1': 'v1', 'k2': '水电费'})
	
    # 可以是字符串
    requests.request(method='get',
    url='http://127.0.0.1:8000/test/',
    params="k1=v1&k2=水电费&k3=v3&k3=vv3")
	
    # 可以是字节（ascii编码以内）
    requests.request(method='get',
    url='http://127.0.0.1:8000/test/',
    params=bytes("k1=v1&k2=k2&k3=v3&k3=vv3", encoding='utf8'))

    # 错误
    # requests.request(method='get',
    # url='http://127.0.0.1:8000/test/',
    # params=bytes("k1=v1&k2=水电费&k3=v3&k3=vv3", encoding='utf8'))
    pass


def param_data():
    
    
    
    # 可以是文件对象
	# 可以是字典
    requests.request(method='POST',
    url='http://127.0.0.1:8000/test/',
    data={'k1': 'v1', 'k2': '水电费'})
    
	# 可以是字符串
    requests.request(method='POST',
    url='http://127.0.0.1:8000/test/',
    data="k1=v1; k2=v2; k3=v3; k3=v4"
    )
	
    # 可以是字节
    requests.request(method='POST',
    url='http://127.0.0.1:8000/test/',
    data="k1=v1;k2=v2;k3=v3;k3=v4",
    headers={'Content-Type': 'application/x-www-form-urlencoded'}#设置请求体的格式
    )

    requests.request(method='POST',
    url='http://127.0.0.1:8000/test/',
    data=open('data_file.py', mode='r', encoding='utf-8'), # 文件内容是：k1=v1;k2=v2;k3=v3;k3=v4
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
     )
    pass


def param_json():
    # 将json中对应的数据进行序列化成一个字符串，json.dumps(...)
    # 然后发送到服务器端的body中，并且Content-Type是 {'Content-Type': 'application/json'}
    requests.request(method='POST',
                     url='http://127.0.0.1:8000/test/',
                     json={'k1': 'v1', 'k2': '水电费'})


def param_headers():
    # 发送请求头到服务器端
    requests.request(method='POST',
                     url='http://127.0.0.1:8000/test/',
                     json={'k1': 'v1', 'k2': '水电费'},
                     headers={'Content-Type': 'application/x-www-form-urlencoded'}
                     )


def param_cookies():
    # 发送Cookie到服务器端
    requests.request(method='POST',
                     url='http://127.0.0.1:8000/test/',
                     data={'k1': 'v1', 'k2': 'v2'},
                     cookies={'cook1': 'value1'},
                     )
    # 也可以使用CookieJar（字典形式就是在此基础上封装）
    from http.cookiejar import CookieJar
    from http.cookiejar import Cookie

    obj = CookieJar()
    obj.set_cookie(Cookie(version=0, name='c1', value='v1', port=None, domain='', path='/', secure=False, expires=None,
                          discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False,
                          port_specified=False, domain_specified=False, domain_initial_dot=False, path_specified=False)
                   )
    requests.request(method='POST',
                     url='http://127.0.0.1:8000/test/',
                     data={'k1': 'v1', 'k2': 'v2'},
                     cookies=obj)


def param_files():
    # 发送文件
    file_dict = {
    'f1': open('readme', 'rb')
   }
    requests.request(method='POST',
    url='http://127.0.0.1:8000/test/',
    files=file_dict)

    # 发送文件，定制文件名
    file_dict = {
   	'f1': ('test.txt', open('readme', 'rb'))
    }
    requests.request(method='POST',
    url='http://127.0.0.1:8000/test/',
   files=file_dict)

    # 发送文件，定制文件名
    file_dict = {
    'f1': ('test.txt', "hahsfaksfa9kasdjflaksdjf")
    }
    
    requests.request(method='POST',
    url='http://127.0.0.1:8000/test/',
    files=file_dict)

    # 发送文件，定制文件名
    file_dict = {
        'f1': ('test.txt', "hahsfaksfa9kasdjflaksdjf", 'application/text', {'k1': '0'})
    }
    requests.request(method='POST',
                     url='http://127.0.0.1:8000/test/',
                     files=file_dict)

    pass


def param_auth():
    #导入认证模块
    from requests.auth import HTTPBasicAuth, HTTPDigestAuth

    ret = requests.get('https://api.github.com/user', auth=HTTPBasicAuth('wupeiqi', 'sdfasdfasdf'))
    print(ret.text)

    ret = requests.get('http://192.168.1.1',
    auth=HTTPBasicAuth('admin', 'admin'))
    ret.encoding = 'gbk'
    print(ret.text)

    ret = requests.get('http://httpbin.org/digest-auth/auth/user/pass', auth=HTTPDigestAuth('user', 'pass'))
    print(ret)
    


def param_timeout():
    ret = requests.get('http://google.com/', timeout=1)
    print(ret)

    ret = requests.get('http://google.com/', timeout=(5, 1))
    print(ret)
    pass


def param_allow_redirects():
    ret = requests.get('http://127.0.0.1:8000/test/', allow_redirects=False)
    print(ret.text)


def param_proxies():
    proxies = {
    "http": "61.172.249.96:80",
    "https": "http://61.185.219.126:3128",
    }

    proxies = {'http://10.20.1.128': 'http://10.10.1.10:5323'}

    ret = requests.get("http://www.proxy360.cn/Proxy", proxies=proxies)
    print(ret.headers)


    from requests.auth import HTTPProxyAuth
    
    proxyDict = {
    'http': '77.75.105.165',
    'https': '77.75.105.165'
     }
    auth = HTTPProxyAuth('username', 'mypassword')
   
    r = requests.get("http://www.google.com", proxies=proxyDict, auth=auth)
    print(r.text)

    pass


def param_stream():
    ret = requests.get('http://127.0.0.1:8000/test/', stream=True)
    print(ret.content)
    ret.close()

    # from contextlib import closing
    # with closing(requests.get('http://httpbin.org/get', stream=True)) as r:
    # # 在此处理响应。
    # for i in r.iter_content():
    # print(i)


def requests_session():
    import requests

    session = requests.Session()

    # 1、首先登陆任何页面，获取cookie

    i1 = session.get(url="http://dig.chouti.com/help/service")

    # 2、用户登陆，携带上一次的cookie，后台对cookie中的 gpsd 进行授权
    i2 = session.post(
        url="http://dig.chouti.com/login",
        data={
            'phone': "8615131255089",
            'password': "xxxxxx",
            'oneMonth': ""
        }
    )

    i3 = session.post(
        url="http://dig.chouti.com/link/vote?linksId=8589623",
    )
    print(i3.text)
```

#### 上传文件

使用request模块，也可以上传文件，文件的类型会自动进行处理：

```python
import requests
 
url = 'http://127.0.0.1:8080/upload'
files = {'file': open('/home/rxf/test.jpg', 'rb')}
#files = {'file': ('report.jpg', open('/home/lyb/sjzl.mpg', 'rb'))}     #显式的设置文件名
 
r = requests.post(url, files=files)
print(r.text)
```



#### 使用requests模块自动登陆

- 自动登陆github

  ```python
  import requests
  from bs4 import BeautifulSoup
  
  def login_github():
       """
       通过requests模块模拟浏览器登陆GitHub
       :return: 
       """
       # 获取csrf_token
       r1 = requests.get('https://github.com/login')   # 获得get请求的对象
       s1 = BeautifulSoup(r1.text, 'html.parser')      # 使用bs4解析HTML对象
       token = s1.find('input', attrs={'name': 'authenticity_token'}).get('value')     # 获取登陆授权码，即csrf_token
       get_cookies = r1.cookies.get_dict()     # 获取get请求的cookies，post请求时必须携带
       
       # 发送post登陆请求
       '''
       post登陆参数
       commit    Sign+in
       utf8    ✓
       authenticity_token    E961jQMIyC9NPwL54YPj70gv2hbXWJ…fTUd+e4lT5RAizKbfzQo4eRHsfg==
       login    JackUpDown（用户名）
       password    **********（密码）
       '''
       r2 = requests.post(
           'https://github.com/session',
           data={
               'commit': 'Sign+in',
               'utf8': '✓',
               'authenticity_token': token,
               'login': 'JackUpDown',
               'password': '**********'
           },
           cookies=get_cookies     # 携带get请求的cookies
                          )
       login_cookies = r2.cookies.get_dict()   # 获得登陆成功的cookies，携带此cookies就可以访问任意GitHub页面
   
       # 携带post cookies跳转任意页面
       r3 = requests.get('https://github.com/settings/emails', cookies=login_cookies)
       print(r3.text)
  ```

- 知乎自动登陆

  ```python
  import time
  
  import requests
  from bs4 import BeautifulSoup
  
  session = requests.Session()
  
  i1 = session.get(
      url='https://www.zhihu.com/#signin',
      headers={
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
      }
  )
  
  soup1 = BeautifulSoup(i1.text, 'lxml')
  xsrf_tag = soup1.find(name='input', attrs={'name': '_xsrf'})
  xsrf = xsrf_tag.get('value')
  
  current_time = time.time()
  i2 = session.get(
      url='https://www.zhihu.com/captcha.gif',
      params={'r': current_time, 'type': 'login'},
      headers={
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
      })
  
  with open('zhihu.gif', 'wb') as f:
      f.write(i2.content)
  
  captcha = input('请打开zhihu.gif文件，查看并输入验证码：')
  form_data = {
      "_xsrf": xsrf,
      'password': 'xxooxxoo',
      "captcha": 'captcha',
      'email': '424662508@qq.com'
  }
  i3 = session.post(
      url='https://www.zhihu.com/login/email',
      data=form_data,
      headers={
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
      }
  )
  
  i4 = session.get(
      url='https://www.zhihu.com/settings/profile',
      headers={
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
      }
  )
  
  soup4 = BeautifulSoup(i4.text, 'lxml')
  tag = soup4.find(id='rename-section')
  nick_name = tag.find('span',class_='name').string
  print(nick_name)
  ```

  

