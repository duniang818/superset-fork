- 启动虚拟环境，并安装打包工具pyinstaller
```shell
PS X:\tech_backup> .\venv\Scripts\Activate.ps1
(venv) PS X:\tech_backup> pip install pyinstaller
```
- 所有相关依赖文件
  - Installing collected packages: altgraph, setuptools, pywin32-ctypes, pyinstaller。-hooks-contrib, pefile, packaging, pyinstaller
- pycharm插件安装路径在哪里
Pycharm官方提供了一个插件库，我们可以在Pycharm中直接从官方插件库中安装插件。具体步骤如下：

（1）打开Pycharm，点击“File”菜单中的“Settings”选项。

（2）在弹出的对话框中，找到“Plugins”选项，点击进入。

（3）在“Plugins”页面中，点击“Marketplace”，这里会列出官方插件库中的所有插件。

（4）找到需要安装的插件，点击“Install”按钮即可开始安装。安装完成后，需要重启Pycharm才能生效。
（5）2023.2.5版本的路径：安装路径\plugins\

需要注意的是，官方插件库中的插件都是经过官方审核的，因此比较安全可靠。但是，官方插件库并不能满足所有用户的需求，有时我们需要安装一些第三方插件。

2.第三方插件

除了官方插件库，还有很多第三方插件可供选择。但是，第三方插件的质量参差不齐，安装前需要谨慎考虑。下面介绍一种比较常见的安装第三方插件的方法。

（1）在网上查找需要的插件，比如在Github上搜索“Pycharm插件”，会得到许多结果。

（2）下载需要的插件，一般情况下，插件的下载链接会在Github上给出。

（3）将插件安装包（一般是一个zip包）解压到Pycharm的插件目录中。插件目录的位置不同版本的Pycharm可能有所不同，一般在“C:\Users\用户名\.Pycharm版本号\config\plugins”目录下。

（4）重启Pycharm，插件即可生效。

需要注意的是，第三方插件可能存在安全隐患，因此安装前需要谨慎考虑。

3.手动安装插件

除了以上两种方式，还有一种手动安装插件的方法。这种方法适用于一些没有提供安装包的插件。

（1）在网上查找需要的插件，并将其下载到本地。

（2）将插件解压到任意目录中。

（3）打开Pycharm，点击“File”菜单中的“Settings”选项。

（4）在弹出的对话框中，找到“Plugins”选项，点击进入。

（5）在“Plugins”页面中，点击“Install Plugin from Disk”，选择刚才下载的插件文件即可。

需要注意的是，手动安装插件需要自己去寻找插件，较为麻烦，而且存在一些安全隐患。

总之，Pycharm插件的安装方式有多种，我们需要根据自己的需求和实际情况进行选择。在安装插件时，需要注意插件的来源和质量，避免安装一些有安全隐患的插件。
- pycharm截图工具
  暂时没找到一样的snipaste插件。
- 插件markdown editor为何不能用呢？markdown splite editor是默认的
  - 内置的插件（底部显示有bundle）的可以更换？
  - 
`set-executionpolicy -executionpolicy remotesigned -scope currentuser`
# 1 steamlit, pygwalker, bokeh, pyecharts, dash, dtale

# 2 资源链接
1. [开源免费的数据分析工具推荐](https://zhuanlan.zhihu.com/p/547535734)
3. [替代品搜索网站](https://alternativeto.net/browse/search/?q=rath)

- 安装pygwalker
  - pip install pygwalker
  - 依赖特别多
  - 升级到最新版本
    - pip install pygwalker --upgrade
- 使用pygwalker
  - https://docs.kanaries.net/zh/pygwalker/index
- 安装polars
  - pip install polars
  - [polars介绍使用](https://pola-rs.github.io/polars/user-guide/installation/)
- 安装pygwalker
  - pip install -r .\pygwaler-in-streamlit-main\requirements.txt
  - requirements.txt文件如何添加注释：使用python脚本一样的注释方法，前面添加#即可。
# 3 pip
- 查看具体某安装包的版本，比如查看已经安装的pandas的版本。会列出包版本，依赖，以及被谁依赖，安装路径等信息。
  - pip show pandas
  > (venv-bd-311) PS X:\tech_backup> pip show pandas 
  > Name: pandas 
  > Version: 1.5.3 
  > Summary: Powerful data structures for data analysis, time series, and statistics 
  > Home-page: https://pandas.pydata.org
  > Author: The Pandas Development Team 
  > Author-email: pandas-dev@python.org 
  > License: BSD-3-Clause 
  > Location: \\vdinas01\download\prd\wang.yumei7@byd.com\tech_backup\venv-bd-311\Lib\site-packages 
  > Requires: numpy, numpy, python-dateutil, pytz 
  > Required-by: altair, streamlit
- 如何想升级已经安装的版本，需要指定具体版本，即便是最新版，默认不带版本的话，本地已经安装过了都不会进行升级。
  - pip install streamlit==1.29.0， # 可以将本地已经安装好的1.24.0版本升级到1.29.0
  - 或使用--upgrade参数，pip install streamlit --upgrade
- pip download
  - 下载的文件都存在在哪里？
    - 在运行此命令的同目录下
  - 可以用pip show 一下吗？
- pip install 从本地文件安装
  - 
- pip list
- pip install
# 4 streamlit 
  - 查看配置信息
  `streamlit config show`
  - 默认配置文件路径 ~/.streamlit/config.toml.
## 4.1 st项目目录结构说明
  - Only .py files in the pages/ directory will be loaded as pages. Streamlit ignores all other files in the pages/ directory and subdirectories.
  - 只有在pages/目录下的py文件才会被加载和显示在侧边栏，此目录下的其它类型文件和子目录的文件都会被忽略。
## 4.2 aiohttp 加速模块
  `pip install aiohttp[speedups]`

- # polars与pandas的比较

# 5 概念与术语
- 装饰器/元编程/泛型/继承/派生类/重载
- 函数装饰器
  1. 装饰器不带参数，被装饰函数带有参数，但没有返回值
  2. 装饰器不带参数，被装饰函数带有参数，且返回值
  3. 装饰器带参数，被装饰函数带有参数，但没有返回值
  4. 装饰器带参数，被装饰函数带有参数，且返回值
  5. 装饰器不带参数，但有返回值，被装饰函数不带有参数，且返回值
# 6 每日代办
- Python package里面的__init__.py文件一般都需要做什么事情？
- pycharm discovering binary modules
  - binary modules的路径在哪里配置，为何每次都需要很久呢？
- 如何把已有的文件夹或项目加入到已有的项目中

注释以 # 字符开始，一直到行尾。
键值对表示为key = value并用换行符分隔。
可以使用方括号嵌套键以创建节的层次结构，例如 [section1.subsection1] 。
值可以是字符串（在引号中）、整数、浮点数、布尔值、日期/时间（采用 ISO 8601 格式）、数组（在方括号中）或表格（在花括号中）。
数组可以包含任何类型的值，包括其他数组或表。
表表示一组键值对，可用于将相关的配置设置分组在一起。表可以有自己的部分，并且可以嵌套在其他表中。
空白（空格、制表符和换行符）在 TOML 文件中很重要，应一致使用以确保正确解析文件

作者：鲸落_
链接：https://juejin.cn/post/7272176270807875639
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

def myFun(**kwargs):
    for key, value in kwargs.items():
        print("%s == %s" % (key, value))
 
 
# 7 Driver code
myFun(first='Geeks', mid='for', last='Geeks')

def myFun(arg1, *argv):
	print("First argument :", arg1)
	for arg in argv:
		print("Next argument through *argv :", arg)


myFun('Hello', 'Welcome', 'to', 'GeeksforGeeks')
- pip  安装一定范围类的包
  >=1.0：大于或等于1.0的所有版本；
  <=2.3：小于或等于2.3的所有版本；
  >=1.0,<=2.3：大于或等于1.0且小于或等于2.3的所有版本；
  ~=1.4：与1.4兼容的所有版本（允许小版本的更新）；
  ==1.2：仅安装版本1.2；
  !=3.0：排除版本3.0。
  ==3.1.*: any version that starts with 3.1.
- pip 安装backports.zoneinfo
  - wheel还灭有支持到最新的python怎办？从源码编译有没有通过
  - ERROR: backports.zoneinfo-0.2.1-cp38-cp38-win_amd64.whl is not a supported wheel on this platform.
  - 应该导出现有工程的requirements文件，然后与新工程的requirements进行比较，再决定用哪个版本的文件。
- 测试网页爬虫的网址：https://help.tableau.com/current/pro/desktop/zh-cn/examples_wdc_connector_sdk.htm
- PS X:\tech_backup\webdataconnector-2.1.0> npm install --production
  - npm WARN config production Use `--omit=dev` instead.
- cnsenti中文情绪情感分析库
HiDaDeng
HiDaDeng
一、cnsenti


中文情感分析库(Chinese Sentiment))可对文本进行情绪分析、正负情感分析。

github地址 https://github.com/thunderhit/cnsenti
pypi地址 https://pypi.org/project/cnsenti/
特性
情感分析默认使用的知网Hownet
情感分析可支持导入自定义txt情感词典(pos和neg)
情绪分析使用大连理工大学情感本体库，可以计算文本中的七大情绪词分布


二、安装
方法一
由于pip默认从pypi站点下载cnsenti安装包，速度会比较慢，这样容易出现安装失败，多试几次即可。

pip install cnsenti


方法二
更改到国内镜像，可以加速下载安装。由于是新上传的库，可能短时间内国内镜像没有收录，等一两天即可。

pip install cnsenti -i https://pypi.tuna.tsinghua.edu.cn/simple/

- npm 源：registry.npm.taobao.org
  - npm config set  https://registry.npmmirror.com
  - npm config set registry http://mirrors.cloud.tencent.com/npm/
  - npm config set registry https://mirrors.huaweicloud.com/repository/npm/
# 8 Python
- 列表切片下标含义[[笔记资源/切片下标说明.png]]
- 