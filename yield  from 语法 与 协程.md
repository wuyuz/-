## yield  from 语法 与 协程



​       举个例子。假如我们做一个爬虫。我们要爬取多个网页，这里简单举例两个网页(两个spider函数)，获取HTML（耗IO耗时），然后再对HTML对行解析取得我们感兴趣的数据。我们都知道，获取网页等待返回网页是非常耗IO的，一个网页还好，如果我们爬取的网页数据极其庞大，这个等待时间就非常惊人，是极大的浪费。聪明的程序员，当然会想如果能在，这里暂停一下，不用傻乎乎地去等待网页返回，而是去做别的事。等过段时间再回过头来到刚刚暂停的地方，接收返回的html内容，然后还可以接下去解析。

​	利用常规的方法，几乎是没办法实现如上我们想要的效果的。所以Python想得很周到，从语言本身给我们实现了这样的功能，这就是`yield`语法。可以实现在某一函数中暂停的效果。

- **思考题**:

  ```
  试着思考一下，假如没有协程，我们要写一个并发程序。可能有以下问题?
      1）使用最常规的同步编程要实现异步并发效果并不理想，或者难度极高。
      2）由于GIL锁的存在，多线程的运行需要频繁的加锁解锁，切换线程，这极大地降低了并发性能；
      
  而协程的出现，刚好可以解决以上的问题。它的特点有:
      1、协程是在单线程里实现任务的切换的
      2、利用同步的方式去实现异步
      3、不再需要锁，提高了并发性能
  ```

  

#### yield from的用法详解

`yield from` 是在Python3.3才出现的语法。所以这个特性在Python2中是没有的。

`yield from` 后面需要加的是可迭代对象，它可以是普通的可迭代对象，也可以是迭代器，甚至是生成器。



- `yield from`： 用法一，拼接可迭代对象，

  ```python
   #我们可以用一个使用yield和一个使用yield from的例子来对比看下。
  
  #使用yield实现拼接
  
  # 字符串
  astr='ABC'
  # 列表
  alist=[1,2,3]
  # 字典
  adict={"name":"wangbm","age":18}
  # 生成器
  agen=(i for i in range(4,8))
  
  def gen(*args, **kw):
      for item in args:
          for i in item:
              yield i
  
  new_list=gen(astr, alist, adict， agen)
  print(list(new_list))
   # ['A', 'B', 'C', 1, 2, 3, 'name', 'age', 4, 5, 6, 7]
  ---------------------------------------------------------
  
  #使用yield from
  # 字符串
  astr='ABC'
  # 列表
  alist=[1,2,3]
  # 字典
  adict={"name":"wangbm","age":18}
  # 生成器
  agen=(i for i in range(4,8))
  
  def gen(*args, **kw):
      for item in args:
          yield from item
  
  new_list=gen(astr, alist, adict, agen)
  print(list(new_list))
   # ['A', 'B', 'C', 1, 2, 3, 'name', 'age', 4, 5, 6, 7]
  ```

  ​	由上面两种方式对比，可以看出，yield from后面加上可迭代对象，他可以把可迭代对象里的每个元素一个一个的yield出来，对比yield来说代码更加简洁，结构更加清晰。



- 复杂应用：生成器的嵌套

  如果你认为只是 `yield from` 仅仅只有上述的功能的话，那你就太小瞧了它，它的更强大的功能还在后面，当 `yield from` 后面加上一个生成器后，就实现了生成的嵌套，当然实现生成器的嵌套，并不是一定必须要使用`yield from`，而是使用`yield from`可以让我们避免让我们自己处理各种料想不到的异常，而让我们专注于业务代码的实现。如果自己用`yield`去实现，那只会加大代码的编写难度，降低开发效率，降低代码的可读性。既然Python已经想得这么周到，我们当然要好好利用起来。

  ```
  1、调用方：调用委派生成器的客户端（调用方）代码
  2、委托生成器：包含yield from表达式的生成器函数
  3、子生成器：yield from后面加的生成器函数
  ```

  简单示例

  ```python
  # 子生成器
  def average_gen():
      total = 0
      count = 0
      average = 0
      while True:
          new_num = yield average
          count += 1
          total += new_num
          average = total/count
  
  # 委托生成器
  def proxy_gen():
      while True:
          yield from average_gen()
  
  # 调用方
  def main():
      calc_average = proxy_gen()    #返回average_gen()的返回值，建立连接
      next(calc_average)            # 预激下生成器，初始化
      print(calc_average.send(10))  # 打印：10.0
      print(calc_average.send(20))  # 打印：15.0
      print(calc_average.send(30))  # 打印：20.0
  
  if __name__ == '__main__':
      main()
  ```

  **委托生成器的作用是**：在调用方与子生成器之间建立一个`双向通道`。所谓的双向通道是什么意思呢？
  调用方可以通过`send()`直接发送消息给子生成器，而子生成器yield的值，也是直接返回给调用方。

  你可能会经常看到有些代码，还可以在`yield from`前面看到可以赋值。这是什么用法？

  更深层次编写代码

  ```python
  # 子生成器
  def average_gen():
      total = 0
      count = 0
      average = 0
      while True:
          new_num = yield average
          if new_num is None:
              break
          count += 1
          total += new_num
          average = total/count
  
      # 每一次return，都意味着当前协程结束。
      return total,count,average
  
  # 委托生成器
  def proxy_gen():
      while True:
          # 只有子生成器要结束（return）了，yield from左边的变量才会被赋值，后面的代码才会执行。
          total, count, average = yield from average_gen()
          print("计算完毕！！\n总共传入 {} 个数值， 总和：{}，平均数：{}".format(count, total, average))
  
  # 调用方
  def main():
      calc_average = proxy_gen()
      next(calc_average)            # 预激协程
      print(calc_average.send(10))  # 打印：10.0
      print(calc_average.send(20))  # 打印：15.0
      print(calc_average.send(30))  # 打印：20.0
      calc_average.send(None)      # 结束协程
      # 如果此处再调用calc_average.send(10)，由于上一协程已经结束，将重开一协程
  
  if __name__ == '__main__':
      main()
      
  10.0
  15.0
  20.0
  计算完毕！！
  总共传入 3 个数值， 总和：60，平均数：20.0
  ```

  