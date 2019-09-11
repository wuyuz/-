## Fiddler的介绍和使用



**Fiddler基础知识**

- Fiddler是强大的抓包工具，它的原理是以web代理服务器的形式进行工作的，使用的代理地址是：127.0.0.1，端口默认为8888，我们也可以通过设置进行修改。
- 代理就是在客户端和服务器之间设置一道关卡，客户端先将请求数据发送出去后，代理服务器会将数据包进行拦截，代理服务器再冒充客户端发送数据到服务器；同理，服务器将响应数据返回，代理服务器也会将数据拦截，再返回给客户端。
- Fiddler可以抓取支持http代理的任意程序的数据包，如果要抓取https会话，要先安装证书。



**HTTP协议**

- 要分析Fiddler抓取的数据包，我们首先要熟悉HTTP协议。HTTP即超文本传输协议，是一个基于请求与响应模式的、无状态的、应用层的协议，绝大多数的Web开发，都是构建在HTTP协议之上的Web应用。
- HTTP的工作过程：当我们请求一个超链接时，HTTP就开始工作了，客户端先发送一个请求到服务器，请求内容包括：协议版本号、请求地址、请求方式、请求头和请求参数；服务器收到请求后做相应的处理，并将响应数据返回到客户端，响应内容包括：协议版本号、状态码和响应数据。前端根据响应数据做相应的处理，就是最终我们看到的内容。这些过程是HTTP自动完成的，我们只是输入或点击请求地址，然后查看前端给我们展示的内容。更多关于HTTP协议的介绍请参考：http://www.cnblogs.com/li0803/archive/2008/11/03/1324746.html
- 请求方式常用的有：GET、PUT、POST、DELETE。
- HTTP状态码主要分为5类：以1开头的代表请求已被接受，需要继续处理；以2开头的代表请求已成功被服务器接收、理解、并接受；以3开头的代表需要客户端采取进一步的操作才能完成请求；以4开头的代表了客户端看起来可能发生了错误，妨碍了服务器的处理；以5开头的代表了服务器在处理请求的过程中有错误或者异常状态发生，也有可能是服务器意识到以当前的软硬件资源无法完成对请求的处理。
- 常见的主要有：200：服务器成功处理了请求；404：未找到资源；500：内部服务器错误；503：服务器目前无法为请求提供服务；302：请求的URL已临时转移；304：客户端的缓存资源是最新的，要客户端使用缓存。
- 每个状态码的详细介绍请参考：https://baike.baidu.com/item/HTTP%E7%8A%B6%E6%80%81%E7%A0%81/5053660?fr=aladdin



**Fiddler的使用**

- Fiddler是一个很好用的抓包工具，可以将网络传输发送与接收的数据包进行截获、重发、编辑等操作。也可以用来检测流量。

- Fiddler安装后，设置的端口默认为8888，当Fiddler启动后，默认将IE的代理设为了127.0.0.1:8888，而其他如火狐浏览器需要手动设置代理后才可以抓包。设置内容如图：

  ![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805123401850-157864315.png) 



#### 使用讲解

- 要使用Fiddler进行抓包，首先需要确保Capture Traffic是开启的（安装后是默认开启的），勾选File->Capture Traffic，也可以直接点击Fiddler界面左下角的图标开启和关闭抓包。

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805112019053-1967751343.png)



- 所以基本上不需要做什么配置，安装后就可以进行抓包了。那么我们怎么分析抓到的这些数据包呢？如图所示的区域为数据包列表，要分析这些数据包，首先要了解各字段的含义。

  ```python
  #：顺序号，按照抓包的顺序从1递增
  
  Result：HTTP状态码　　　　　　
  
  Protocol：请求使用的协议，如HTTP/HTTPS/FTP等
  
  HOST：请求地址的主机名或域名
  
  URL：请求资源的位置
  
  Body：请求大小
  
  Caching：请求的缓存过期时间或者缓存控制值
  
  Content-Type：请求响应的类型
  
  Process：发送此请求的进程ID
  
  Comments：备注 
  
  Custom：自定义值
  ```

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805112443537-1867996529.png)





- 每个Fiddler抓取到的数据包都会在该列表中展示，点击具体的一条数据包可以在右侧菜单点击Inspect查看检查详细内容。主要分为请求（即客户端发出的数据）和响应（服务器返回的数据）两部分。

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805113441147-1748009750.png)



-  HTTP Request Header：以百度为例，查看请求百度主页这条数据包的请求数据，从上面的Headers中可以看到如下内容：

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805123838850-1680235418.png)

```
请求方式：GET
协议： HTTP/1.1

Client 头域：

    Accept: text/html, application/xhtml+xml, image/jxr, */*      -浏览器端可以接受的媒体类型
    Accept-Encoding: gzip, deflate    压缩方法
    Accept-Language: zh-CN   语言类型
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393         -客户端使用的操作系统和浏览器的名称和版本

COOKIE头域：将cookie值发送给服务器
Transport 头域：
	Connection：当网页打开完成后，客户端和服务器之间用于传输HTTP数据的TCP连接是否关闭。keep-alive表示不会关闭，客户端再次访问这个服务器上的网页，会继续使用这一条已经建立的连接；close表示关闭，客户端再次访问这个服务器上的网页，需要重新建立连接。

HOST：主机名或域名，若没有指定端口，表示使用默认端口80.
```



- HTTP Response Header：继续以百度为例，如图所示：


![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805125323225-627073311.png)

```
协议：HTTP/1.1

状态码：200

Cache头域：
Cache-Control: private                                               ---------此响应消息不能被共享缓存处理，对于其他用户的请求无效

Date: Sat, 05 Aug 2017 04:37:43 GMT                      ---------生成消息的具体时间和日期

Expires: Sat, 05 Aug 2017 04:37:42 GMT                  ---------浏览器会在指定过期时间内使用本地缓存

Cookie/Login 头域：

Set-Cookie: BDSVRTM=264; path=/                           ---------把cookie发送到客户端
Set-Cookie: BD_HOME=1; path=/
Set-Cookie: H_PS_PSSID=1425_21097_22157; path=/; domain=.baidu.com

Entity头域
Content-Length: 202740                                              ---------正文长度
Content-Type: text/html;charset=utf-8                         ---------告知客户端服务器本身响应的对象的类型和字符集

Miscellaneous 头域：
Bdpagetype: 2

Bdqid: 0x99791efd00036253

Bduserid: 2577220064
Server: BWS/1.1                                                          ---------指明HTTP服务器的软件信息

X-Ua-Compatible: IE=Edge,chrome=1
Security头域：
Strict-Transport-Security: max-age=172800                ---------基于安全考虑而需要发送的参数，关于这个参数的解释，请参考：http://www.freebuf.com/articles/web/66827.html

Transport头域：

Connection: Keep-Alive
```



- TextView：显示请求或响应的数据。

- WebForms：请求部分以表单形式显示所有的请求参数和参数值；响应部分与TextView内容是一样的。


- Auth：显示认证信息，如Authorization


- Cookies：显示所有cookies


- Raw：显示Headers和Body数据


- JSON：若请求或响应数据是json格式，以json形式显示请求或响应内容


- XML：若请求或响应数据是xml格式，以xml形式显示请求或响应内容




​	上面是以百度主页为例，百度主页采用的是GET请求，在TextView中没有请求body，我们再以无忧行网站登录接口为例，它是一个POST请求，除了请求头外，在TextView中多了请求数据。这也是GET请求和POST请求的一个区别。*GET请求是将请求参数放在url中，而POST请求一般是将请求参数放在请求body中*。

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805133646022-1557077459.png)

 

 ![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805133817162-375948978.png)

​	总结：通过Fiddler可以抓取请求和响应参数，通过对参数进行分析，可以定位是前端还是后台问题。例如我们在测试登录接口时，输入了正确的手机号和密码，但前端提示“请输入正确的用户名和密码”；仅仅通过界面提示我们只能描述bug表象，但不能分析出问题原因。假设通过抓包我们发现是由于前端参数名错误或参数值为空，从而导致后台报错。这个时候我们将bug指向前端开发人员，并将参数数据和接口文档中对应的报文数据作为附件上传，是不是可以提高bug的解决效率呢？Fiddler在实际的功能测试中有很大的作用，一方面帮助我们更好的了解某个业务中客户端和服务器端是通过哪些接口进行请求的，从而更好的了解代码逻辑；另一方面，我们还可以通过响应数据判断哪里出现了问题，例如可能服务器程序挂了，导致前端报“服务器故障”，这时我们通过抓包发现响应数据返回502，这时我们可以手动去重启服务或是联系运维重启服务，从而提高问题的解决效率。



**Andriod配置方法：**

- 确保手机和Fiddler所在主机在同一个局域网中(电脑开启wifi)

- 获取Fiddler所在主机的ip地址，通过cmd命令进入命令编辑器，输入ipconfig -all，找到IPv4地址，记下该地址


![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805140357069-1183095335.png)

 

- 对手机所连接的无线网络进行设置，点击WLAN，长按与Fiddler所在主机在同一个局域网的wifi，长按点击【修改网络】，选中【显示高级选项】，代理设置为手动，输入代理服务器的主机名和端口后保存。代理服务器的主机名即2）中的IPv4地址，端口为Fiddler上配置的端口（默认为8888），可以到Fiddler菜单栏中【Tool】-【Fiddler Option】的【Connections】中查看。（手机和电脑处于同一局域网，如果使用电脑的wifi是不行的）

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805142454319-914046820.png)

 

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805140523444-1538531634.png)

- 在手机浏览器上输入：http://IPv4地址:端口（例如：http://192.168.11.29:8888），点击【FiddlerRoot certificate】下载安装Fiddler证书。


![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805142547334-219557589.png)

 	若在浏览器上无法打开该地址，需要做两项检查：

```
一、确保在浏览器、wifi中配置的代理与Fiddler所在主机地址和Fiddler中配置的端口，三者保持一致；
二、确保在Fiddler-【Tools】-【Fiddler Option]-[Connection]中【Allow remote computers to connect】已经勾选上，若没有勾选，则需要勾选后保存并重启Fiddler。
三、手机和电脑处于同一网段
```

 ![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805142629084-590036877.png)

- 这时我们打开手机上的浏览器或APP，可以在Fiddler上看到手机上的数据包了。


![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805142853584-463948636.png)

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805143017787-295366381.png)



 **IOS配置方法：**

1）基本与andriod的配置方法一致，除了安装证书方式与andriod略有不同，另外ios在下载证书后，需要手动信任证书。设置方法：打开【设置】-【通用】-【关于本机】-【证书信任证书】，找到对应的证书，启用即可。

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805144208162-718533077.png)



**HTTPS抓包**

上面都是针对HTTP协议进行抓包的设置，那么HTTPS需要进行什么配置呢？

1）打开Fiddler-【Tools】-【Fiddler Option】，切换到HTTPS选项卡，勾选【Capture HTTPS CONNECTs】和【Decrypt HTTPS traffic】，然后点击【Actions】-【Trust Root Certificate】，然后按照提示一路yes，直到弹框提示“Trust Cert success”点击确定后，重启Fiddler就可以抓取HTTPS协议的数据包了。

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805144650897-516128605.png)

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805155328256-418313473.png)

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805155422334-36027677.png)



![img](file:///C:/Users/mian/AppData/Local/YNote/data/miantest@163.com/53cf8809503c4fc3a5a0d9a4b476b629/clipboard.png)

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805144923350-139684438.png)



**Fiddler过滤会话**

​	我们在使用Fiddler进行抓包时，发现只要是使用了Fiddler代理服务器的所有HTTP/HTTPS数据包都会在Fiddler数据列表中显示出来，但有时我们只关注从某个或某些服务器发出的请求，不想要看到其他服务器的数据包，应该怎么进行设置呢？我们都知道Fiddler是一款强大的抓包工具，我们可以通过设置来过滤只筛选出我们想要的数据包。

1）在右侧菜单中，找到Fittlers选项，共有9个部分进行设置

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805151229194-790393457.png)

 

2）Use Filters：勾选则表示使用过滤，不勾选则表示不进行过滤

3）Actions：有四个选项，Run Filterset now：立即运行过滤设置；Load Filterset：加载保存的过滤设置；Save Filterset：保存过滤设置；help：帮助

4）Hosts：该设置项有两个选项

- 第一个下拉框是只显示内网或者外网选项
- ![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805150028319-1575722844.png)
- 第二个下拉框是根据主机名信息显示或者隐藏或者标记指定请求
- ![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805150047397-1919434052.png)

5）Client Process：有三个选项，Show only traffic from：根据进程信息进行过滤，选择后，将只显示由该进程发出的请求；Show only Internet Explorer traffic：只关心由IE浏览器发出的请求；Hide traffic from Service Host：隐藏来自service host（即由svchost.exe进程发出）的请求

6）Request Headers：有五个选项，Show only if URL contains：可以通过正则表达式过滤请求地址中包含或不包含的内容，例如REGEX:\.(js|css|js\?.*|css\?.*)$（隐藏所有js和css请求）；Hide if URL contains：与Show only if URL contains相反，一个是显示，一个是隐藏；Flags requests with headers：支持指定某个http请求头名称，如果在web session列表中存在该请求头，会加粗显示该session；Delete requests headers：与Flags requests with headers类似，这里是如果包含该请求头，则删除该请求头；Set request header：将HTTP请求头更新为所输入的值。

7）Breakpoints：断点设置，有四个选项。Break request on POST：对POST请求设置断点；Break request on GET with query string：会为所有方法为GET且URL中包含了给定查询条件的请求设置断点；Break on XMLHttpRequest：对所有能够确定是通过XMLHTTPRequest对象发送的请求设置断点；Break response on Content-Type：会为所有响应头Content-Type中包含了指定文本的响应设置响应断点。

8）Response Status Code：根据响应状态码设置断点。

9）Response Type and Size：有几种类型，一类是根据响应数据的类型显示或隐藏；一类是根据响应数据的大小显示或隐藏；一类是根据响应所需要的时间设置背景颜色；一类是根据文件类型进行限制。

- type有以下几种类型：
- ![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170805153756178-2093225681.png)
- Time HeatMap复选框会基于服务器返回给定响应所需要的时间为每个session设置背景颜色。

10）Response Headers：与Request Headers不同的是，这块区域是针对响应数据的头部进行过滤。

这么多设置项，比较常用的就是1.2.3部分。通过过滤设置，可以快速的帮助我们找到我们需要抓包分析的数据包，从而提高效率，避免过多的数据包信息干扰我们找到正确的数据包。

我们知道Fiddler是位于客户端和服务器之间的代理，它能够记录客户端和服务器之间的所有 HTTP请求，可以针对特定的HTTP请求，分析请求数据、设置断点、调试web应用、修改请求的数据，甚至可以修改服务器返回的数据，功能非常强大，是web调试的利器。前面我们介绍了如何使用Fiddler进行抓包和分析，以及如何抓取APP上的数据包。这里我们介绍下如何修改请求和响应数据，也就是设置断点。



**对request设置断点**

1）通过菜单选项或快捷键F11进行设置，如图

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806131927459-583396411.png)

当我们设置断点后，进行HTTP请求，数据包顺序列会有中断的标记，单击该数据包可以看到在右侧会增加一行操作栏。这个时候我们在前端是没有正常加载网页的，点击【Run to Completion】后可以返回响应数据。

 ![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806132337522-1932518895.png)

接下来为了看我们的断点设置是否生效，我们以登录为例子进行测试。登录无忧行网站，输入正确的用户名和密码，点击登录。我们断点规则设置为before request，然后将密码清空，看看服务器给我们返回了什么响应数据。

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806133702412-821730526.png)

 

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806133705178-1720852233.png)

 

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806133812537-931454580.png)

继续以登录为例子，这次我们将手机号改成非移动账号进行登录。

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806134113725-846616690.png)

 

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806134032694-126591576.png)

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806134227725-1475342505.png)

 

 由此可见，我们的断点已经设置成功，并且成功修改了HTTP的请求数据。

 2）通过菜单选项或快捷键进行设置时，会将所有的HTTP请求都设置断点，但有时我们只想针对某个服务器发出的请求设置断点，应该怎么操作呢？Fiddler是支持命令操作的，我们可以通过“bpu 服务器地址”命令来对特定的请求设置断点。

在下图所示的位置输入命令，然后回车运行。

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806134818459-756901470.png)

这个时候从该服务器发出的所有请求都会被中断，而从其他服务器发出的请求可以正常响应。

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806135110162-692784586.png)

如果要清除原来的断点，可以在命令行输入“bpu”，就会清除所有的断点。

**对response设置断点**

1）同样的也可以通过菜单选项或快捷键alt+F11进行设置

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806135708506-1465420089.png)

2）通过命令“bpafter 服务器地址”

我们也用一个实例来验证通过设置断点修改响应数据。以百度主页为例，我们拦截到响应数据中的title值为”百度一下，你就知道“，我们将响应数据中的title改成”test百度一下，你就知道“，然后在前端看看最终展示的是什么数据。

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806142021350-1195559610.png)

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806142204912-1760085694.png)

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806142219194-1500079151.png)

通过几个实例，更好的帮助我们理解断点的含义，也巩固了Fiddler作为代理服务器的概念。接下来我们再来说说，Fiddler另一个很实用的功能：Fiddler的编码和解码。

 **Fiddler的编码和解码**

1）响应body解码

有时候我们在Fiddler上看到响应数据是几个乱码字符，首先我们可以点击，上方黄色提示区域直接进行解码。如下面的两个图所示。

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806142515694-708674643.png)

 

 ![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806142526709-1905127094.png)

2）请求和响应数据解码

有的时候，基于安全性考虑，开发人员会将请求和响应的body根据一定规则进行解码。如果是普通的编码规则，我们可以直接通过Fiddler操作进行解码。例如在登录百度网站的时候，有个参数的值是一个url地址，这个url经过urlEncode进行转码了。我们就可以将该参数通过urlDecode进行解码。

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806143300209-427783913.png)

首先，找到这个参数，选中后右键选择【send to TextWizard】

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806143435756-379901753.png)

然后，在【transform】中找到【URLDecode】，字段值就被成功解码，我们就可以很清楚的看到里面有哪些参数以及参数的值是什么了。

![img](https://images2017.cnblogs.com/blog/1213812/201708/1213812-20170806143538850-889026353.png)

上面都是解码的例子，编码在实际运用中很少，就不介绍了。另外里面还有很多其他的编码/解码方法，就不一一举例啦~~

