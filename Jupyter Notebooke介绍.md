## Jupyter Notebooke介绍

### 一、什么是Jupyter Notebook？

#### 1. 简介

> Jupyter Notebook是基于**网页的用于交互计算的应用程序**。其可被应用于全过程计算：开发、文档编写、运行代码和展示结果。——[Jupyter Notebook官方介绍](https://link.jianshu.com/?t=https%3A%2F%2Fjupyter-notebook.readthedocs.io%2Fen%2Fstable%2Fnotebook.html)

​		简而言之，Jupyter Notebook是以网页的形式打开，可以在网页页面中**直接**编写代码和运行代码，代码的运行结果也会直接在代码块下显示。如在编程过程中需要编写说明文档，可在同一个页面中直接编写，便于作及时的说明和解释。



#### 2. 组成部分

##### ① 网页应用

​		网页应用即基于网页形式的、结合了编写说明文档、数学公式、交互计算和其他富媒体形式的工具。**简言之，网页应用是可以实现各种功能的工具。**

##### ② 文档

​		即Jupyter Notebook中所有交互计算、编写说明文档、数学公式、图片以及其他富媒体形式的输入和输出，都是以文档的形式体现的。



#### 3. Jupyter Notebook的主要特点

1. 编程时具有**语法高亮**、缩进、tab补全的功能。
2. 可直接通过浏览器运行代码，同时在代码块下方展示运行结果。
3. 对代码编写说明文档或语句时，支持Markdown语法。



### 二、安装Jupyter Notebook

#### 1. 安装

##### ① 安装前提

​		安装Jupyter Notebook的前提是需要安装了Python（3.3版本及以上，或2.7版本）。

##### ② 使用Anaconda安装

​		如果你是小白，那么建议你通过安装Anaconda来解决Jupyter Notebook的安装问题，因为Anaconda已经自动为你安装了Jupter Notebook及其他工具，还有python中超过180个科学包及其依赖项。

​		你可以通过进入Anaconda的[官方下载页面](https://link.jianshu.com/?t=https%3A%2F%2Fwww.anaconda.com%2Fdownload%2F%23macos)自行选择下载；如果你对阅读**英文文档**感到头痛，或者对**安装步骤**一无所知，甚至也想快速了解一下**什么是Anaconda**，那么可以前往我的另一篇文章[Anaconda介绍、安装及使用教程](https://link.jianshu.com/?t=https%3A%2F%2Fzhuanlan.zhihu.com%2Fp%2F32925500)。你想要的，都在里面！

​		常规来说，安装了Anaconda发行版时已经自动为你安装了Jupyter Notebook的，但如果没有自动安装，那么就在终端（Linux或macOS的“终端”，Windows的“Anaconda Prompt”，以下均简称“终端”）中输入以下命令安装：

```
conda install jupyter notebook
```



### 三、运行Jupyter Notebook

#### 1. 帮助

如果你有任何jupyter notebook命令的疑问，可以考虑查看官方帮助文档，命令如下：

```python
jupyter notebook --help
jupyter notebook -h
```



#### 2. 启动

##### ① 默认端口启动

在终端中输入以下命令：

```
jupyter notebook
```

执行命令之后，在终端中将会显示一系列notebook的服务器信息，同时浏览器将会自动启动Jupyter Notebook。浏览器地址栏中默认地将会显示：`http://localhost:8888`。其中，“localhost”指的是本机，“8888”则是端口号。如果你**同时**启动了多个Jupyter Notebook，由于默认端口“8888”被占用，因此地址栏中的数字将从“8888”起，每多启动一个Jupyter Notebook数字就加1，如“8889”、“8890”……



##### ② 指定端口启动

如果你想自定义端口号来启动Jupyter Notebook，可以在终端中输入以下命令：

```
jupyter notebook --port <port_number>
```

其中，“<port_number>”是自定义端口号，直接以数字的形式写在命令当中，数字两边不加尖括号“<>”。如：`jupyter notebook --port 9999`，即在端口号为“9999”的服务器启动Jupyter Notebook。



##### ③ 启动服务器但不打开浏览器

如果你只是想启动Jupyter Notebook的服务器但不打算立刻进入到主页面，那么就无需立刻启动浏览器。在终端中输入：

```
jupyter notebook --no-browser
```

此时，将会在终端显示启动的服务器信息，并在服务器启动之后，显示出打开浏览器页面的链接。当你需要启动浏览器页面时，只需要复制链接，并粘贴在浏览器的地址栏中，轻按回车变转到了你的Jupyter Notebook页面。



#### Jupyter Notebook 的快捷键

1. 向上插入一个cell：a
2. 向下插入一个cell：b
3. 删除cell：x
4. 将code切换成markdown：m
5. 将markdown切换成code：y
6. 运行cell：shift+enter
7. 查看帮助文档：shift+tab
8. 自动提示：tab



- ##### 魔法指令

1. 运行外部python源文件：%run xxx.py
2. 计算statement的运行时间:%time statement
3. 计算statement的平均运行时间:%timeit statement
4. 测试多行代码的平均运行时间：