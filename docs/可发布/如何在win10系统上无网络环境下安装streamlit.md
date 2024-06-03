因为公司开发电脑不能上外网，一直安装streamlit都不成功，中途又一次安装成功了，但是没多久，迁移了一下虚拟环境，在新项目中开发，么有用到这个streamlit，导致再次安装streamlit都不成功，折磨了很久还是不成功。
所以就想这次把可以复刻成功安装的方法分享一下，供后来者少踩坑。
第一步：找到一台可以上网的电脑，下载所有的whl文件，这里网上有个大佬谢了一个脚本，我修改了一下，也分享出来。之前大佬主要是依赖包是list，会包含很多重复的，所以我修改了类型为集合，加快下载和后面的安装。
第二步，运行脚本（offline-install-st.py）批量且递归下载全部依赖。
import os, sys

requires_set = set()


def Dependent_query(pkg_name):
    Output = os.popen(f"pip show {pkg_name}")
    Requires = Output.readlines()
    for line in Requires:
        if "Requires:" in line:  #只解析最后一行Requires，如果没有这一行表示没有有依赖
            requires_list = line.strip().split(':')[1].split(',')
            requires_list = [i for i in requires_list if i]
            print(f'requires_list:{requires_list}')

            if requires_list:
                for requires in requires_list:
                    if requires:
                        requires_set.add(requires.strip())
                        Dependent_query(requires.strip())  ## 递归调用起依赖


def download(requires_set):
    if isinstance(requires_set, list) and requires_set:
        for pkg in requires_set:
            print(f"==========开始下载: {pkg}==========")
            pkg_Output = os.system(f"pip download {pkg}")
            print(pkg_Output)


if __name__ == '__main__':
    # 在终端下执行：python offline-install-st.py streamlit
    pkg_name = sys.argv[1]
    requires_set.add(pkg_name)
    # 查询依赖包
    Dependent_query(pkg_name)
    print(f"安装顺序参考:{requires_set[::-1]}")  #开始：结束：步长，-1表示从右往左一个个切，即倒序
    # 启用下载依赖包功能
    download(requires_set)
下载上面的所有依赖后，就是如何把这些文件在无网的电脑上进行安装。
第三步：复制所有的whl文件到需要安装的离线电脑的一个目录下。
比如你用的虚拟环境，就全部加压到虚拟环境的site-packages/下；
如果你没有用虚拟环境，就全部解压到系统的Python安装目录的site-packages/下；
至于为何要解压到此目录，理由是因为这个目录下还有其他已经安装的文件，可以完成索引。
网上失败教训1：有很多直接打包安装压缩文件*.tar.gz，我自己试过，对于单个文件，没有依赖的安装是可以的，但是像streamlit依赖很多的包安装，最终还是以失败告终；
网上失败教训2：直接把下载的whl文件生成requirements.txt，然后就行本地索引安装，在Windows上总是报错：
ERROR:
第四步：查pip离线批量安装whl的办法，最终找到了相应的命令，非常关键；
**一定是先安装python，pip等命令，再安装streamlit，因为streamlit会修改python的引用路径。如果是在其它电脑上安装了streamlit,直接迁移起包和script路径下的streamlit.exe经常会报找不到相应的python.exe。
就是这个原因，所以在需要的电脑上直接安装，而且是在虚拟环境已经建好的情况下，基于相应的环境再安装streamlit。**
How to Force pip to Reinstall a Package - Sparrow Computing
​sparrow.dev/pip-force-reinstall/#:~:text=If%2C%20for%20some%20reason%2C%20you%20want%20to%20re-install,time%20to%20update%20pip%3A%20pip%20install%20--upgrade%20pip
`pip install --ignore-installed --no-index --find-links=. .\streamlit-1.29.0-py2.py3-none-any.whl`
解释一下上面的命令：
--ignore-installed：忽略已经安装的相同名字的包，可以解决版本冲突，且强制重新安装，对于不是第一次安装很有用；
--no-index：不要去索引，因此在本地找文件；
--find-links=：在哪里找文件的依赖链接，后面跟一个路径，“.”表示当前路径，最好是当前路径，其他路径没有自动失败，有可能会失败；
 .\streamlit-1.29.0-py2.py3-none-any.whl： 最后这个就是当前路径下的streamlit的安装whl文件。
运行后没有报任何错误，自此安装成功。
第五步：使用streamlit
我们试着运行自己写的一个demo文件note.py：
import streamlit as st
from pathlib import Path
st.write('## 这是笔记软件')
# 1 文件当前路径：项目的根目录,
cw_dir = Path(__file__).parent.parent.parent  # output: pages/

# 2 获取notes目录的路径
nb_dir = cw_dir / "notebook" / "note.md"

# 3 UnicodeDecodeError: 'gbk' codec can't decode byte 0xaa in position 173: illegal multibyte sequence
nt_md = Path(nb_dir).read_text(encoding='UTF-8')
st.markdown(nt_md, unsafe_allow_html=True)
在终端下运行，我这里是在虚拟环境下运行，也OK。
streamlit run demo.py
但我运行hello，会报错。
streamlit run hello
这个也会提示错误：
Error: Streamlit requires raw Python (.py) files
​discuss.streamlit.io/t/error-streamlit-requires-raw-python-py-files/13066
上面并没有解决此错误。
另外网上说的没有设置环境变量，这些都是不需要的。