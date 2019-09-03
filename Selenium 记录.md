## Selenium 记录



#### 设置浏览器大小

- maximize_window()：设置浏览器大小为全屏

- set_window_size(500,500)：设置浏览器分辨率为：500×500

  ```python
  from selenium import webdriver
  import time  
  
  browser = webdriver.Chrome()
  browser.maximize_window()   #设置浏览器大小：全屏
  browser.get('https://www.baidu.com')  
  time.sleep(2)
  
  browser.set_window_size(500,500)  # 分辨率 1280*800  
  time.sleep(2)
  
  browser.set_window_size(1024,768)  # 分辨率 1024*768  
  time.sleep(2)
  ```

  

#### 刷新浏览器页面

- refresh()方法：刷新浏览器页面

  ```python
  from selenium import webdriver
  import time  
  
  browser = webdriver.Chrome()
  browser.maximize_window()   #设置浏览器大小：全屏
  browser.get('https://www.baidu.com')  
  time.sleep(1)
  
  try:
      browser.refresh()  #刷新页面
      print('刷新页面')
  except Exception as e:
      print('test fail')
  
  #输出内容：刷新页面
  ```

  

#### 浏览器后退和前进

- back()：后退

- forward()：前进

  ```python
  from selenium import webdriver
  import time  
  
  browser = webdriver.Chrome()
  browser.maximize_window()   #设置浏览器大小：全屏
  browser.get('https://www.baidu.com')  
  
  #点击打开百度新闻页面
  browser.find_element_by_link_text('新闻').click()
  time.sleep(2)
  
  browser.back()  #后退：回到百度首页
  time.sleep(2)
  
  browser.forward()  #前进：前进到百度新闻页面
  time.sleep(2)
  ```

  

本篇文字主要学习selenium定位页面元素的集中方法，以百度首页为例子。

#### 元素定位方法主要有：

- id定位：find_element_by_id(' ')
- name定位：find_element_by_name(' ')
- class定位：find_element_by_class_name(' ')
- tag定位：find_element_by_tag_name(' ')
- link定位：find_element_by_link_text(' ')
- partial link定位：find_element_by_partial_link_text(' ')
- xpath定位：find_element_by_xpath(' ')
- CSS定位：find_element_by_css_selector(' ')
- By定位

#### 利用ID定位元素

- 简单示例

  ```python
  from selenium import webdriver
  # 设置浏览器
  browser = webdriver.Chrome()
  #设置浏览器大小：全屏
  browser.maximize_window()
  #打开百度首页
  browser.get('https://www.baidu.com/')
  #定位百度搜索输入框之前，先分析下它的html结构
  #<input type="text" class="s_ipt nobg_s_fm_hover" name="wd" id="kw" maxlength="100" autocomplete="off">
  #发现它的 id="kw" ，接下来我们就通过id进行定位
  try:
      browser.find_element_by_id('kw').send_keys('哈哈')
      print('test post：id')
  except Exception as e:
      print('test fail')
  
  #输出内容：test post：id
  ```

  

#### 利用name定位元素

- 简单示例

  ```python
  from selenium import webdriver
  browser = webdriver.Chrome()
  browser.maximize_window()
  
  #打开百度首页
  browser.get('https://www.baidu.com/')
  #搜索框的html结构：<input type="text" class="s_ipt nobg_s_fm_hover" name="wd" id="kw" maxlength="100" autocomplete="off">
  # 根据name属性定位
  try:
      browser.find_element_by_name('wd').send_keys('哈哈')
      print('test post：name')
  except Exception as e:
      print('test fail')
  
  #输出内容：test post：name
  ```

  

#### 利用class定位元素

- 简单示例

  ```python
  from selenium import webdriver
  browser = webdriver.Chrome()
  browser.maximize_window()
  
  #打开百度首页
  browser.get('https://www.baidu.com/')
  #搜索框的html结构：<input type="text" class="s_ipt nobg_s_fm_hover" name="wd" id="kw" maxlength="100" autocomplete="off">
  # 根据class_name属性定位
  try:
      browser.find_element_by_class_name('s_ipt').send_keys('哈哈')
      print('test post：class_name')
  except Exception as e:
      print('test fail')
  
  #输出内容：test post：class_name
  ```

  

#### 利用tag_name定位元素

- 简单示例

  ```python
  from selenium import webdriver
  browser = webdriver.Chrome()
  browser.maximize_window()
  
  #打开百度首页
  browser.get('https://www.baidu.com/')
  #搜索框的html结构：<input type="text" class="s_ipt nobg_s_fm_hover" name="wd" id="kw" maxlength="100" autocomplete="off">
  # 根据tag_name属性定位
  try:
      browser.find_element_by_tag_name('form')
      print('test post：tag_name')
  except Exception as e:
      print('test fail')
  
  #输出内容：test post：tag_name
  ```

  

#### 利用link_text定位元素

- link_text：根据跳转链接上面的文字来定位元素。

  ```python
  from selenium import webdriver
  browser = webdriver.Chrome()
  browser.maximize_window()
  
  #打开百度首页
  browser.get('https://www.baidu.com/')
  # 根据link_text属性定位元素“新闻”，然后点击按钮
  try:
      browser.find_element_by_link_text('新闻').click()
      print('test post：tag_name')
  except Exception as e:
      print('test fail')
  
  #输出内容：test post：link_text
  ```

  

#### 利用partial_link_text定位元素

- 和link_text定位元素差不多，partial_link_text是通过文字信息中的部分字段来定位元素。

  ```python
  from selenium import webdriver
  browser = webdriver.Chrome()
  browser.maximize_window()
  
  #打开百度首页
  browser.get('https://www.baidu.com/')
  # 根据partial_link_text属性定位元素“新闻”，然后点击按钮
  try:
      browser.find_element_by_partial_link_text('闻').click()
      print('test post：tag_name')
  except Exception as e:
      print('test fail')
  
  #输出内容：test post：partial_link_text
  ```

  

#### 利用xpath定位元素

- 简单示例

  ```python
  from selenium import webdriver
  browser = webdriver.Chrome()
  browser.maximize_window()
  
  #打开百度首页
  browser.get('https://www.baidu.com/')
  # 根据xpath定位元素
  try:
      browser.find_element_by_xpath('//*[@id="kw"]').send_keys('哈哈')
      print('test post：xpath')
  except Exception as e:
      print('test fail')
  
  #输出内容：test post：xpath
  ```

  

#### 利用CSS定位页面元素

- 简单示例

  ```python
  from selenium import webdriver
  browser = webdriver.Chrome()
  browser.maximize_window()
  
  #打开百度首页
  browser.get('https://www.baidu.com/')
  # 根据css_selector定位元素
  try:
      browser.find_element_by_css_selector('#kw').send_keys('哈哈')
      print('test post：xpath')
  except Exception as e:
      print('test fail')
  
  #输出内容：test post：css_selector
  ```

  

#### By定位

- 除了使用上面的方法外，还可以利用find_element()方法，通过By来定位元素。

- 使用之前需要导入By类：

  ```python
  #导入By类
  from selenium.webdriver.common.by import By
  ```

  

- 那么上面的方法还可以改写为：

  ```python
  browser.find_element(By.ID,'kw')
  browser.find_element(By.NAME,'wd')
  browser.find_element(By.CLASS_NAME,'s_ipt')
  browser.find_element(By.TAG_NAME,'form')
  browser.find_element(By.LINK_TEXT,'新闻')
  browser.find_element(By.PARTIAL_LINK_TEXT,'闻')
  browser.find_element(By.XPATH,'//*[@id="kw"]')
  browser.find_element(By.CSS_SELECTOR,'#kw')
  ```

  

#### 输入内容

- send_keys('valve')：输入内容valve

  ```python
  #定位输入框
  input_box = browser.find_element_by_id('kw')
  try:
      #输入内容：selenium
      input_box.send_keys('selenium')
      print('搜索关键词：selenium')
  except Exception as e:
      print('fail')
  
  #输出内容：搜索关键词：selenium
  ```

  

#### 点击按钮

- click():点击按钮

  ```python
  #定位搜索按钮
  button = browser.find_element_by_id('su')
  try:
      #点击搜索按钮
      button.click()
      print('成功搜索')
  except Exception as e:
      print('fail搜索')
  #输出内容：成功搜索
  ```

  

#### 清空输入框

- clear()：清空输入框

  ```python
  #clear()：清空输入框
  try:
      input_box.clear()
      print('成功清空输入框')
  except Exception as e:
      print('fail清空输入框')
  #输出内容：成功清空输入框
  ```

  

#### 输入内容、点击按钮、清空输入完整实例

- 简单示例

  ```python
  from selenium import webdriver
  import time  
  
  browser = webdriver.Chrome()
  browser.maximize_window()   #设置浏览器大小：全屏
  browser.get('https://www.baidu.com')  
  
  #定位输入框
  input_box = browser.find_element_by_id('kw')
  try:
      #输入内容：selenium
      input_box.send_keys('selenium')
      print('搜索关键词：selenium')
  except Exception as e:
      print('fail')
  #输出内容：搜索关键词：selenium
  
  #定位搜索按钮
  button = browser.find_element_by_id('su')
  try:
      #点击搜索按钮
      button.click()
      print('成功搜索')
  except Exception as e:
      print('fail搜索')
  #输出内容：成功搜索
  
  #clear()：清空输入框
  try:
      input_box.clear()
      print('成功清空输入框')
  except Exception as e:
      print('fail清空输入框')
  #输出内容：成功清空输入框
  ```

  

#### submit()：模拟‘回车’操作

- submit()：通常应用于提交表单；例如：搜索框输入内容后的回车操作。

  ```python
  from selenium import webdriver
  import time  
  
  browser = webdriver.Chrome()
  browser.maximize_window()   #设置浏览器大小：全屏
  browser.get('https://www.baidu.com')  
  
  #定位输入框
  input_box = browser.find_element_by_id('kw')
  #输入关键词：selenium
  input_box.send_keys('selenium')
  #模拟回车操作
  try:
      input_box.submit()
      print('成功回车')
  except Exception as e:
      print('fail')
  #输出内容：成功回车
  ```

  

#### 获取页面title

- title：获取当前页面的标题显示的字段

  ```python
  from selenium import webdriver
  import time  
  
  browser = webdriver.Chrome()
  browser.get('https://www.baidu.com')  
  
  #打印网页标题
  print(browser.title)
  #输出内容：百度一下，你就知道
  ```

  

#### 获取页面URL

- current_url：获取当前页面的URL

  ```python
  from selenium import webdriver
  import time  
  
  browser = webdriver.Chrome()
  browser.get('https://www.baidu.com')  
  
  #打印网页标题
  print(browser.current_url)
  #输出内容：https://www.baidu.com/
  ```

  

#### 获取浏览器版本号

- capabilities['version'])：打印浏览器version的值

  ```python
  from selenium import webdriver
  import time  
  
  browser = webdriver.Chrome()
  browser.get('https://www.baidu.com')  
  
  #打印网页标题
  print(browser.capabilities['version'])
  #输出内容：67.0.3396.87
  ```

  

#### 获取元素尺寸

- size：返回元素的尺寸

  ```python
  from selenium import webdriver
  import time  
  
  browser = webdriver.Chrome()
  browser.get('https://www.baidu.com')  
  
  #定位输入框
  input_box = browser.find_element_by_id('kw')
  #打印输入框尺寸
  print(input_box.size)
  #输出内容：{'height': 22, 'width': 500}
  ```

  

#### 获取元素的文本

- text：返回元素的文本信息

  ```python
  from selenium import webdriver
  import time  
  
  browser = webdriver.Chrome()
  browser.get('https://www.baidu.com')  
  
  #定位备案元素
  recordcode = browser.find_element_by_id('jgwab')
  #打印备案元素信息
  print(recordcode.text)
  #输出内容：京公网安备11000002000001号
  ```

  

#### 获得属性值

- get_attribute('')方法

- get_attribute('href'):获取href属性值

- get_attribute('id'):获取id属性值

  ```python
  # coding=utf-8
  import time
  from selenium import webdriver
  
  
  driver = webdriver.Chrome()
  driver.maximize_window()
  driver.implicitly_wait(6)
  driver.get("https://www.baidu.com")
  time.sleep(1)
  
  for link in driver.find_elements_by_xpath("//*[@href]"):
      print (link.get_attribute('href'))
  driver.quit()
  ```

  

在webdriver中，鼠标的一些操作如：双击、右击、悬停、拖动等都被封装在ActionChains类中，我们只用在需要使用的时候，导入这个类就可以了。

#### ActionChains类提供的鼠标常用方法：

- perform()：执行所有 ActionChains 中存储的行为。
- context_click()：右击
- double_click()：双击
- drag_and_drop()：拖到
- move_to_element()：鼠标悬停

#### 注意：

- 使用之前需要引入 ActionChains 类。

```
from selenium.webdriver.common.action_chains import ActionChains
```

#### 鼠标右击实例

- 右击示例

  ```python
  from selenium import webdriver
  from selenium.webdriver.common.action_chains import ActionChains  # 引入 ActionChains 类
  
  browser = webdriver.Chrome()
  browser.get('https://www.baidu.com')  
  
  
  # 定位到要右击的元素
  right_click = browser.find_element_by_link_text('新闻')
  
  # 对定位到的元素执行鼠标右键操作
  #ActionChains(driver)：调用ActionChains()类，并将浏览器驱动browser作为参数传入
  #context_click(right_click)：模拟鼠标双击，需要传入指定元素定位作为参数
  #perform()：执行ActionChains()中储存的所有操作，可以看做是执行之前一系列的操作
  try:
      ActionChains(browser).context_click(right_click).perform()
      print('成功右击')
  except Exception as e:
      print('fail')
  #输出内容：成功双击
  ```

  

#### 注意：

- ActionChains(driver)：调用ActionChains()类，并将浏览器驱动browser作为参数传入
- context_click(right_click)：模拟鼠标双击，需要传入指定元素定位作为参数
- perform()：执行ActionChains()中储存的所有操作，可以看做是执行之前一系列的操作

#### 鼠标右击

- context_click()：右击

  ```python
  #   鼠标右击
  # 定位到要右击的元素
  right_click  = browser.find_element_by_id("xx")
  
  # 对定位到的元素执行右击操作
  ActionChains(browser).move_to_element(right_click ).perform()
  ```

  

#### 鼠标双击

- double_click()：双击

  ```python
  # 定位到要右击的元素
  double_click = browser.find_element_by_id('xx')
  
  # 对定位到的元素执行鼠标右键操作
  ActionChains(browser).context_click(double_click).perform()
  ```

  

#### 鼠标拖动

- drag_and_drop(source,target)：拖动

- source：开始位置；需要拖动的元素

- target：结束位置；拖到后需要放置的目的地元素

  ```python
  # 开始位置：定位到元素的原位置
  source = driver.find_element_by_id("xx")
  
  # 结束位置：定位到元素要移动到的目标位置
  target = driver.find_element_by_id("xx")
  
  # 执行元素的拖放操作
  ActionChains(driver).drag_and_drop(source,target).perform()
  ```

  

#### 鼠标悬停

- move_to_element()：鼠标悬停

  ```python
  # 定位到要悬停的元素
  move = driver.find_element_by_id("xx")
  
  # 对定位到的元素执行悬停操作
  ActionChains(driver).move_to_element(move).perform()
  ```

  

#### 导入键盘类Keys()

- selenium中的Keys()类提供了大部分的键盘操作方法；通过send_keys()方法来模拟键盘上的按键。

  ```python
  # 导入键盘类 Keys()
  from selenium.webdriver.common.keys import Keys
  ```

  

##### 常用的键盘操作：

- send_keys(Keys.BACK_SPACE)：删除键(BackSpace)

- send_keys(Keys.SPACE)：空格键(Space)

- send_keys(Keys.TAB)：制表键(TAB)

- send_keys(Keys.ESCAPE)：回退键(ESCAPE)

- send_keys(Keys.ENTER)：回车键(ENTER)

- send_keys(Keys.CONTROL,'a')：全选(Ctrl+A)

- send_keys(Keys.CONTROL,'c')：复制(Ctrl+C)

- send_keys(Keys.CONTROL,'x')：剪切(Ctrl+X)

- send_keys(Keys.CONTROL,'v')：粘贴(Ctrl+V)

- send_keys(Keys.F1)：键盘F1

- .....

- send_keys(Keys.F12)：键盘F12

  ```python
  from selenium import webdriver  
  from selenium.webdriver.common.keys import Keys  
  
  driver=webdriver.Chrome()  
  driver.get("http://www.baidu.com")  
  #输入关键词内容
  driver.find_element_by_id("kw").send_keys("selenium")  
  #删除键
  driver.find_element_by_id("kw").send_keys(Keys.BACK_SPACE)  
  #空格键 
  driver.find_element_by_id("kw").send_keys(Keys.SPACE)  
  #输入内容
  driver.find_element_by_id("kw").send_keys("教程")  
  #全选(Ctrl+A)  
  driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'a') 
  #剪切(Ctrl+X)  
  driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'x') 
  #粘贴(Ctrl+V)  
  driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'v')  
  #回车键  
  driver.find_element_by_id("kw").send_keys(Keys.ENTER)
  ```

    

​       如果遇到使用ajax加载的网页，页面元素可能不是同时加载出来的，这个时候，就需要我们通过设置一个等待条件，等待页面元素加载完成，避免出现因为元素未加载导致的错误的出现。

WebDriver提供了两种等待类型：显示等待、隐式等待。

#### 显示等待：WebDriverWait()类

- 显示等待：设置一个等待时间和一个条件，在规定时间内，每隔一段时间查看下条件是否成立，如果成立那么程序就继续执行，否则就提示一个超时异常（TimeoutException）。

- 通常情况下**WebDriverWait**类会结合**ExpectedCondition**类一起使用。

  ```python
  from selenium import webdriver
  from selenium.webdriver.support.wait import WebDriverWait
  from selenium.webdriver.support import expected_conditions as EC
  from selenium.webdriver.common.by import By
  
  driver = webdriver.Chrome()
  driver.get('https://www.baidu.com')
  # 设置浏览器：driver  等待时间：20s
  wait = WebDriverWait(driver, 20)
  # 设置判断条件：等待id='kw'的元素加载完成
  input_box = wait.until(EC.presence_of_element_located((By.ID, 'kw')))
  # 在关键词输入：关键词
  input_box.send_keys('关键词')
  ```



##### WebDriverWait的具体参数和方法：

```
WebDriverWait(driver,timeout,poll_frequency=0.5,ignored_exceptions=None)
    driver: 浏览器驱动
    timeout: 超时时间，等待的最长时间（同时要考虑隐性等待时间）
    poll_frequency: 每次检测的间隔时间，默认是0.5秒
    ignored_exceptions:超时后的异常信息，默认情况下抛出NoSuchElementException异常


until(method,message='')
    method: 在等待期间，每隔一段时间调用这个传入的方法，直到返回值不是False
    message: 如果超时，抛出TimeoutException，将message传入异常


until_not(method,message='')
    until_not 与until相反，until是当某元素出现或什么条件成立则继续执行，
    until_not是当某元素消失或什么条件不成立则继续执行，参数也相同。
    method
    message
```

##### ExpectedCondition

- ExpectedCondition中可使用的判断条件：

  ```python
  from selenium.webdriver.support import expected_conditions as EC
  
  
  # 判断标题是否和预期的一致
  title_is
  # 判断标题中是否包含预期的字符串
  title_contains
  
  
  # 判断指定元素是否加载出来
  presence_of_element_located
  # 判断所有元素是否加载完成
  presence_of_all_elements_located
  
  
  # 判断某个元素是否可见. 可见代表元素非隐藏，并且元素的宽和高都不等于0，传入参数是元组类型的locator
  visibility_of_element_located
  # 判断元素是否可见，传入参数是定位后的元素WebElement
  visibility_of
  # 判断某个元素是否不可见，或是否不存在于DOM树
  invisibility_of_element_located
  
  
  # 判断元素的 text 是否包含预期字符串
  text_to_be_present_in_element
  # 判断元素的 value 是否包含预期字符串
  text_to_be_present_in_element_value
  
  
  #判断frame是否可切入，可传入locator元组或者直接传入定位方式：id、name、index或WebElement
  frame_to_be_available_and_switch_to_it
  
  
  #判断是否有alert出现
  alert_is_present
  
  
  #判断元素是否可点击
  element_to_be_clickable
  
  
  # 判断元素是否被选中,一般用在下拉列表，传入WebElement对象
  element_to_be_selected
  # 判断元素是否被选中
  element_located_to_be_selected
  # 判断元素的选中状态是否和预期一致，传入参数：定位后的元素，相等返回True，否则返回False
  element_selection_state_to_be
  # 判断元素的选中状态是否和预期一致，传入参数：元素的定位，相等返回True，否则返回False
  element_located_selection_state_to_be
  
  
  #判断一个元素是否仍在DOM中，传入WebElement对象，可以判断页面是否刷新了
  staleness_of
  ```

  

##### 调用方法如下：

```
WebDriverWait(driver, 超时时长, 调用频率, 忽略异常).until(可执行方法, 超时时返回的信息)
```

#### 隐式等待

- implicitly_wait(xx)：设置等待时间为xx秒，等待元素加载完成，如果到了时间元素没有加载出，就抛出一个NoSuchElementException的错误。

- 注意：隐性等待对整个driver的周期都起作用，所以只要设置一次即可。

  ```python
  from selenium import webdriver
  
  driver = webdriver.Chrome()
  driver.implicitly_wait(30)  # 隐性等待，最长等30秒
  
  driver.get('https://www.baidu.com')
  
  print(driver.current_url)
  print(driver.title)
  ```

  

#### 强制等待：sleep()

- 强制等待：不管浏览器元素是否加载完成，程序都得等待3秒，3秒一到，继续执行下面的代码。

  ```python
  from selenium import webdriver
  from time import sleep
  
  driver = webdriver.Chrome()
  driver.get('https://www.baidu.com')
  
  sleep(3)  # 强制等待3秒再执行下一步
  
  print(driver.title)
  ```

  

之前学习了8种定位单个元素的方法，同时webdriver还提供了8种定位一组元素的方法。唯一区别就是在单词element后面增加了一个s表示复数：

#### 定位一组元素

- find_elements_by_id('')
- find_elements_by_id_by_class_name('')
- find_elements_by_tag_name('')
- find_elements_by_link_text('')
- find_elements_by_partial_link_text('')
- find_elements_by_xpath('')
- find_elements_by_css_selector('')

#### 单选框选中

- 简单示例

  ```python
  from selenium import webdriver
  import time
  driver = webdriver.Chrome()
  driver.maximize_window()
  driver.get('http://news.baidu.com/')
  time.sleep(1)
  
  try:
      #定位搜索框下面的新闻全文和新闻标题单选项
      radio_button = driver.find_elements_by_css_selector(".search-radios>input")
      # 定位的一组元素后，返回的是一个列表，这里就循环选中对应的选项
      for i in radio_button:
          i.click()
      print ('选中单选框.')
  except Exception as e:
      print ('fail',format(e))
  ```

  

#### 复选框选中

- 简单示例

  ```python
  from selenium import webdriver
  import time
  driver = webdriver.Chrome()
  driver.maximize_window()
  driver.get('https://passport.baidu.com/v2/?reg&tt=1529850358050&overseas=undefined&gid=02B2650-6D11-430E-A19D-529F69B9F1CE&tpl=xw&u=http%3A%2F%2Fnews.baidu.com%2F')
  time.sleep(1)
  
  try:
      #定位 阅读并接受《百度用户协议》及《百度隐私权保护声明》 的多选框
      checkbox = driver.find_elements_by_css_selector("#TANGRAM__PSP_3__isAgree")
      # 定位的一组元素后，返回的是一个列表，这里就循环选中对应的选项
      for i in checkbox:
          i.click()
      print ('选中多选框')
  except Exception as e:
      print ('fail',format(e))
  ```

  