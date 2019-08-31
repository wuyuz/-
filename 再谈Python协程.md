## 异步IO(asynico)协程



#### 简单了解

在py3中内置了asyncio模块，其编程模型就是一个消息循环，我们可以通过 import asynico 来查看源码

```python
from asyncio.base_events import *
from asyncio.coroutines import *　　#协程模块，可以将函数装饰为协程
from asyncio.events import *　　#事件模块，事件循环和任务调度都将使用到他
from asyncio.futures import *　#异步并发模块，该模块对task封装了许多方法，代表将来执行或没有执行的任务的结果。它和task上没有本质上的区别
from asyncio.locks import *　　#异步保证资源同步
from asyncio.protocols import *
from asyncio.queues import *
from asyncio.streams import *
from asyncio.subprocess import *
from asyncio.tasks import *　　#创建任务，是对协程的封装，可以查看协程的状态。可以将任务集合
from asyncio.transports import *
```

#### 调用步骤

```
1.当我们给一个函数添加了async关键字，或者使用asyncio.coroutine装饰器装饰，就会把它变成一个异步函数。 
2.每个线程有一个事件循环，主线程调用asyncio.get_event_loop时会创建事件循环，

3.将任务封装为集合asyncio.gather(*args),之后一起传入事件循环中

4.要把异步的任务丢给这个循环的run_until_complete方法，事件循环会安排协同程序的执行。和方法名字一样，该方法会等待异步的任务完全执行才会结束。
```



##### 简单使用

```python
import asyncio,time

@asyncio.coroutine　　#设为异步函数
def func1(num):
    print(num,'before---func1----')
    yield from asyncio.sleep(5)
    print(num,'after---func1----')

task = [func1(1),func1(2)]

if __name__ == "__main__":
    begin = time.time()
    loop = asyncio.get_event_loop()　　#进入事件循环
    loop.run_until_complete(asyncio.gather(*task))　　#将协同程序注册到事件循环中
    loop.close() #关闭循环
    end = time.time()
    print(end-begin)

----------------------运行结果-------------------------
1 before---func1----
2 before---func1----
1 after---func1----
2 after---func1----
5.00528621673584
```

- 我们可以使用send(None)触发协程

  ```python
  import asyncio,time
  async def func1(num): #使用async关键字定义一个协程，协程也是一种对象，不能直接运行，需要加入事件循环中，才能被调用。
      print(num,'before---func1----')
  
  if __name__ == "__main__":
      begin = time.time()
  
      # loop = asyncio.get_event_loop()
      # loop.run_until_complete(coroutine)
      # loop.close()
      
      coroutine = func1(2)
      try:
          coroutine.send(None)
      except StopIteration:
          print('异常')
  
      end = time.time()
      print(end-begin)
  
  ```

  

#### 阻塞和await

​	使用async关键字定义的协程对象，使用await可以针对耗时的操作进行挂起（是生成器中的yield的替代，但是本地协程函数不允许使用），让出当前控制权。协程遇到await，事件循环将会挂起该协程，执行别的协程，直到**其他协程也挂起，或者执行完毕，**在进行下一个协程的执行

使用asyncio.sleep模拟阻塞操作：

```python
import asyncio,time

async def func1(num):
    print(num,'before---func1----')
    await asyncio.sleep(num)
    return "recv num %s"%num

if __name__ == "__main__":
    begin = time.time()
    coroutine1 = func1(5)
    coroutine2 = func1(3)
    loop = asyncio.get_event_loop()
    task1=asyncio.ensure_future(coroutine1)
    task2=asyncio.ensure_future(coroutine2)
    tasks = asyncio.gather(*[task1,task2])　　　　#gather可以实现同时注册多个任务，实现并发操作。wait方法使用一致
    loop.run_until_complete(tasks)
    loop.close()
    end = time.time()
    print(end-begin)
```

![1567184002956](C:\Users\wanglixing\AppData\Roaming\Typora\typora-user-images\1567184002956.png)



#### 并发：使用gather或者wait可以同时注册多个任务，实现并发

- gather：Return a future aggregating results from the given coroutines or futures.　返回结果

  ```
   	task1=asyncio.ensure_future(coroutine1)
      task2=asyncio.ensure_future(coroutine2)
      tasks = asyncio.gather(*[task1,task2])
      loop.run_until_complete(tasks)
  ```

- wait：Returns two sets of Future: (done, pending) 返回dones是已经完成的任务，pending是未完成的任务，都是集合类型

  ```
      task1=asyncio.ensure_future(coroutine1)
      task2=asyncio.ensure_future(coroutine2)
      tasks = asyncio.wait([task1,task2])
      loop.run_until_complete(tasks)
  ```

  ##### **wait是接收一个列表，而后gather是接收一堆任务数据，两者的返回值也是不同的**

  ```python
     loop = asyncio.get_event_loop() #进入事件循环
      # ret = loop.run_until_complete(asyncio.gather(*task))  
      # #['sdf', 'sdf'] ,直接返回结果
      
      ret = loop.run_until_complete(asyncio.wait(task))
      #({<Task finished coro=<func1() done, defined at C:/Users/wanglixing/Desktop/文件夹/test/再谈协程.py:4> result='sdf'>, <Task finished coro=<func1() done, defined at C:/Users/wanglixing/Desktop/文件夹/test/再谈协程.py:4> result='sdf'>}, set())
      
      loop.close()
      print(ret)
  ```

  

#### 关于aiohttp模块的协程嵌套，嵌套更加明显

- 也就是我们爬虫用到的部分

  ```python
  import asyncio,aiohttp
  
  async def fetch_async(url):
      print(url)
      async with aiohttp.ClientSession() as session:
          async with session.get(url) as resp:
              print(resp.status)
              print(await resp.text())
  
  tasks = [fetch_async('http://www.baidu.com/'), fetch_async('http://www.cnblogs.com/ssyfj/')]
  
  event_loop = asyncio.get_event_loop()
  results = event_loop.run_until_complete(asyncio.gather(*tasks))
  event_loop.close()
  ```

  

- ##### wait的另一种用法，可以实时判断任务状态

  ```python
  import asyncio,time
  
  async def func1(num):
      print(num,'before---func1----')
      await asyncio.sleep(num)
      return "recv num %s"%num
  
  async def main():
      coroutine1 = func1(5)
      coroutine2 = func1(3)
      coroutine3 = func1(4)
  
      tasks = [
          asyncio.ensure_future(coroutine1),
          asyncio.ensure_future(coroutine2),
          asyncio.ensure_future(coroutine3),
      ]
  
      dones, pendings = await asyncio.wait(tasks)
  
      for task in dones:　　#对已完成的任务集合进行操作
          print("Task ret: ",task.result())
  
  if __name__ == "__main__":
      begin = time.time()
      loop = asyncio.get_event_loop()
      loop.run_until_complete(main())
      loop.close()
      end = time.time()
      print(end-begin)
    
  
  5 before---func1----
  3 before---func1----
  4 before---func1----
  Task ret:  recv num 4
  Task ret:  recv num 5
  Task ret:  recv num 3
  5.000285863876343
  ```

- ##### asyncio中的as_completed方法

  ```
  import asyncio,time
  
  async def func1(num):
      print(num,'before---func1----')
      await asyncio.sleep(num)
      return "recv num %s"%num
  
  async def main():
      coroutine1 = func1(5)
      coroutine2 = func1(3)
      coroutine3 = func1(4)
  
      tasks = [
          asyncio.ensure_future(coroutine1),
          asyncio.ensure_future(coroutine2),
          asyncio.ensure_future(coroutine3),
      ]
  
      for task in asyncio.as_completed(tasks):
          result = await task    
          print("Task ret: ",result)  #返回一个可迭代的值
  
  if __name__ == "__main__":
      begin = time.time()
  
      loop = asyncio.get_event_loop()
      loop.run_until_complete(main())
  
      loop.close()
      end = time.time()
      print(end-begin)
  ```

  

#### 任务对象的各种状态

future对象有几个状态：

- Pending
- Running
- Done
- Cacelled

创建future的时候，task为pending，

事件循环调用执行的时候当然就是running，

调用完毕自然就是done，

如果需要停止事件循环，就需要先把task取消。

可以使用asyncio.Task获取事件循环的task

```python
import asyncio,time

async def func1(num):
    print(num,'before---func1----')
    await asyncio.sleep(num)
    return "recv num %s"%num

if __name__ == "__main__":
    begin = time.time()

    coroutine1 = func1(5)
    coroutine2 = func1(3)
    coroutine3 = func1(4)

    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3),
    ]


    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt as e:
        print(asyncio.Task.all_tasks())
        for task in asyncio.Task.all_tasks():　　#获取所有任务
            print(task.cancel())　　#单个任务取消
        loop.stop()　　　　#需要先stop循环
        loop.run_forever()　　#需要在开启事件循环
    finally:
        loop.close()　　#统一关闭
    end = time.time()
    print(end-begin)
    
----------------------------------------------------
# 运行结果
5 before---func1----
3 before---func1----
4 before---func1----
{<Task pending coro=<func1() running at multhread.py:5> wait_for=<Future pending cb=[Task._wakeup()]> cb=[_wait.<loc
als>._on_completion() at C:\Users\Administrator\AppData\Local\Programs\Python\Python35\lib\asyncio\tasks.py:428]>, <
Task pending coro=<wait() running at C:\Users\Administrator\AppData\Local\Programs\Python\Python35\lib\asyncio\tasks
.py:361> wait_for=<Future pending cb=[Task._wakeup()]>>, <Task pending coro=<func1() running at multhread.py:5> wait
_for=<Future pending cb=[Task._wakeup()]> cb=[_wait.<locals>._on_completion() at C:\Users\Administrator\AppData\Loca
l\Programs\Python\Python35\lib\asyncio\tasks.py:428]>, <Task pending coro=<func1() running at multhread.py:5> wait_f
or=<Future pending cb=[Task._wakeup()]> cb=[_wait.<locals>._on_completion() at C:\Users\Administrator\AppData\Local\
Programs\Python\Python35\lib\asyncio\tasks.py:428]>}　　#未处理，刚刚挂起为pending状态
True　　#返回True，表示cancel取消成功
True
True
True
3.014172315597534
```



#### 上面讨论的都是在同一线程下的事件循环，下面来谈谈不同线程的事件循环

在当前线程中创建一个事件循环（不启用，单纯获取标识），开启一个新的线程，在新的线程中启动事件循环。在当前线程依据事件循环标识，可以向事件中添加协程对象。当前线程不会由于事件循环而阻塞了。上面在一个线程中执行的事件循环，只有我们主动关闭事件close，事件循环才会结束，会阻塞。

- 同一线程

  ```
  import asyncio,time
  
  async def func1(num):
      print(num,'before---func1----')
      await asyncio.sleep(num)
      return "recv num %s"%num
  
  if __name__ == "__main__":
      begin = time.time()
  
      coroutine1 = func1(5)
      coroutine2 = func1(3)
      coroutine3 = func1(4)
  
      tasks = [
          asyncio.ensure_future(coroutine1),
          asyncio.ensure_future(coroutine2),
          asyncio.ensure_future(coroutine3),
      ]
  
      loop = asyncio.get_event_loop()
      loop.run_until_complete(asyncio.wait(tasks))
      loop.run_forever()  #一致阻塞，等待其他任务到来
      end = time.time()
      print(end-begin)
  ```



#### 不同线程事件循环（不涉及协程）

```python
import asyncio,time,threading

def func1(num):
    print(num,'before---func1----')
    time.sleep(num)
    return "recv num %s"%num

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == "__main__":
    begin = time.time()

    new_loop = asyncio.new_event_loop() #在当前线程下创建时间循环，（未启用）
    t = threading.Thread(target=start_loop,args=(new_loop,))    #开启新的线程去启动事件循环
    t.start()

    new_loop.call_soon_threadsafe(func1,3)
    new_loop.call_soon_threadsafe(func1,2)
    new_loop.call_soon_threadsafe(func1,6)

    end = time.time()
    print(end-begin)    #当前线程未阻塞，耗时0.02800154685974121
    
3 before---func1----
0.02800154685974121
2 before---func1----
6 before---func1----
```



#### 新线程协程

```python
import asyncio,time,threading

async def func1(num):
    print(num,'before---func1----')
    await asyncio.sleep(num)
    return "recv num %s"%num

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == "__main__":
    begin = time.time()

    coroutine1 = func1(5)
    coroutine2 = func1(3)
    coroutine3 = func1(4)

    new_loop = asyncio.new_event_loop() #在当前线程下创建时间循环，（未启用）
    t = threading.Thread(target=start_loop,args=(new_loop,))    #开启新的线程去启动事件循环
    t.start()

    asyncio.run_coroutine_threadsafe(coroutine1,new_loop)　　#传参必须是协程对象
    asyncio.run_coroutine_threadsafe(coroutine2,new_loop)
    asyncio.run_coroutine_threadsafe(coroutine3,new_loop)

    end = time.time()
    print(end-begin)    #当前线程未阻塞，耗时0.010000467300415039

5 before---func1----
3 before---func1----
4 before---func1----
0.010000467300415039
```

