# 1 [[Xset产品介绍.pptx]]

# 2 st 官方文档

进入源码目录，docs文件夹

- [superset/docs](https://github.com/apache/superset/tree/master/docs): content, assets, and code for the [Apache Superset website](https://superset.apache.org/). The final built assets for the website live in [apache/superset-site](https://github.com/apache/superset-site) but you only need to edit the files in `apache/superset/docs` and the changes will be pushed to `apache/superset-site` after merging.
- 只能修改/superset/docs`里的文件，然后会合并到 superset-site`这个代码库里。

## 2.1 官方doc 网站运行

https://docusaurus.io/docs

```powershell
npm run build
npm run serve
```

![[Pasted image 20240510094433.png]]

## 2.2 i18n 国际化教程

https://docusaurus.io/zh-CN/docs/i18n/tutorial
https://flask-appbuilder.readthedocs.io/en/latest/i18n.html
第一步：安装pybabel
第二步：初始化
	pybabel init -i ./babel/messages.pot -d app/translations -l es
第三步：在需要国际化的view 文件中引入 flask_babel

```python
from flask_babel import lazy_gettext as _

class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]
    label_columns = {'name':_('Name')}

genapp.add_view(GroupModelView(), "List Groups",icon = "th-large", label=_('List Groups'),
                    category = "Contacts", category_icon='fa-envelope', category_label=_('Contacts'))
genapp.add_view(ContactModelView(), "List Contacts",icon = "earphone", label=_('List Contacts'),
                    category = "Contacts")
```
第四步：提取翻译词条
flask fab babel-extract
第五步：查看翻译词条对应关系，可以用poeditor软件打开
app/translations/pt/LC_MESSAGES/messages.po
第六步：编译翻译
flask fab babel-compile
## 2.3 文档生成工具是用的sphinx工具[[文档生成器工具比较#1 Sphinx]]

## 2.4 翻译工具 [poedit](https://poedit.net/)
Poedit was built to handle translation using gettext (PO), which is used by many PHP projects (Drupal, WordPress), Python projects (Django), or virtually anything running on Linux.
### 2.4.1 gettext(PO)？


# 3 [preset 官方文档](https://docs.preset.io/docs/semantic-layer)

# 4 [[如何在win10系统上无网络环境下安装streamlit]]
# 5 [[04 xset后端]]
## 5.1 [[flask]]
### 5.1.1 [[04 xset后端#1 Flask-AppBuilder[¶](https //flask-appbuilder.readthedocs.io/en/latest/ module-flask_appbuilder "Link to this heading")]]
## 5.2 [[03 Xset使用及二开#2.2 i18n 国家化教程]]
### 5.2.1 Flask-Babel


# 6 [[05 xset前端]]
# 7 通用模块
## 7.1 [[jinjia模板]]
## 7.2 [[SQLAlchemy]]

# 8 [web development lifecycle](https://preset.io/blog/tutorial-contributing-code-to-apache-superset/)

![[Pasted image 20240426094206.png | web 开发生命周期]]

# 9 设置本地开发环境（前端）

前提需要：
node.js
[[09 工具类#2 node|甚至是nvm，如何安装nvm在 Windows上for vscode]]

进入前端库 **superset/superset-frontend**
npm ci
npm run dev-server  默认端口是9000
or
npm run dev-server --devserverPort=9001

遇到9000端口被占用，如何在Windows上取消？

[[0 Xset 4.0.0在Windows上源码部署|本地开发环境（后端）]]

# 10 代码库概览

- apache/superset: 核心代码库，包含前端和后端代码
  - superset/superset: 后端代码库
  - superset/superset-frontend: 主要的TypeScript / JavaScript bundles and react apps
  - superset/docs: content, assets, and code for the Apache Superset website. The final built assets for the website live in apache/superset-site but you only need to edit the files in apache/superset/docs and the changes will be pushed to apache/superset-site after merging.
- apache-superset/superset-ui: contains Superset's core npm packages that are shared across the React apps and viz plugins.
  - 此库已经归档了，只是可读库。
- apache-superset/superset-ui-plugins-deckgl: contains the geospatial visualizations, powered by the deck.gl library
  - - 此库已经归档了，只是可读库。
      之前这三个库的分开的，大家正在努力将其合并到一个库：[monorepo](https://github.com/apache/superset)，也是左侧的库，上面提到的第一个库，以后看这个库就可以了。
      ![[Pasted image 20240426095053.png]]

# 11 为何语义层设计的很轻？

[深入理解以查询为中心的可视化](https://preset.io/blog/dataset-centric-visualization/)
[[The Case for Dataset-Centric Visualization]] [[以数据集为中心的可视化案例]]
Different BI tools offer different approaches to building dashboards. On one end of the spectrum, you have tools that prescribe having **one query per chart** and on the other end you have tools that espouse implementing a **complex semantic layer**. I believe there's a middle path that lies between both extremes, and I call it the **dataset-centric approach**.

1. query-centric(查询为中心)
   ![[Pasted image 20240507112821.png]]
2. dataset-centric(数据集为中心)
   ![[Pasted image 20240507112831.png]]
3. semantic-centric(语义为中心)
   ![[Pasted image 20240507112842.png]]

In the dataset-centric approach, the tool is connected to individual datasets that are expected to contain all of the metrics and dimensions for a given subject area.

In this post, I'll describe the strengths and tradeoffs for each of the approaches and make the case for the dataset-centric approach as the ideal one for fast-moving data teams.

上一代 BI 工具（如 Looker）鼓励最终用户投入大量资金构建大量 LookML 模型来填充语义层。虽然这使 Looker 成为组织中业务指标的真实来源，但它也在您的 BI 工具中创造了大量的锁定。如果您决定切换 BI 工具，则无法随身携带 LookML 模型并将它们与其他工具一起使用。谷歌对 Looker 的收购加速了组织对这种锁定的焦虑，以至于谷歌实际上被迫将 LookML 与 Tableau 集成。这样一来，组织就可以使用 LookML 进行转换（Looker 的优势），使用 Tableau 进行可视化（Tableaus 的优势）。
LookML : 数据模型，数据指标可视化
Tableau：可视化可视化
但是随着时间的推移，语义层发生了变化：
![[Pasted image 20240426115304.png]]

# 12 三个重要的 metaphors:

- Virtual Datasets
- Metrics
- Calculated Columns

# 13 及时查看superset库下面的CONTRIBUTING.md文档

# 14 MongoDB连接

## 14.1 Windows上如何安装MongoDB

[下载MongoDB的msi安装包，从官网](https://www.mongodb.com/try/download/community)获取。
双击安装包，选择Custom自定义安装路径，例如D:\software\MongoDB。
配置环境变量，将MongoDB的bin目录添加到Path变量中。
创建数据库文件的存放位置，例如D:\software\MongoDB\data和D:\software\MongoDB\log。
创建配置文件mongod.cfg，指定dbpath和logpath等选项。
启动MongoDB服务，使用mongod.exe --config "D:\software\MongoDB\mongod.cfg" --install命令。
测试MongoDB是否安装成功，使用mongo.exe命令连接数据库。

安装驱动
pip install pymongo
输入连接URI
mongodb+srv://username:password@host/database

## 14.2 Setting Up the MongoDB Connector in Superset

Integrating MongoDB with Apache Superset allows for direct analysis of data stored in MongoDB collections. To set up the MongoDB connector, follow these steps:

- **Install the MongoDB Connector**: Ensure you have the `pymongo` library installed in your environment where Superset is running. Use the command `pip install pymongo` to install it.
- **Create a New Database Connection**: In Superset, navigate to the `Data` menu and select `Databases`. Click the `+ DATABASE` button to add a new connection.
- **Configure the Connection**: Use the following SQLAlchemy URI format for MongoDB: `mongodb+srv://<username>:<password>@<cluster-address>/<database>?retryWrites=true&w=majority`. Replace `<username>`, `<password>`, `<cluster-address>`, and `<database>` with your MongoDB credentials and details.
- **Test the Connection**: After entering the connection details, click `Test Connection` to ensure that Superset can connect to your MongoDB instance.
- **Explore and Visualize**: Once the connection is established, you can start creating datasets, charts, and dashboards using your MongoDB data.

Remember to consult the official MongoDB documentation for any specific configurations or troubleshooting steps.

## 14.3 9.3

legacy data science：传统数据学科
forefront ：前沿

# 15 [[如何贡献代码给superset.pdf|英文原文]]

# 16 警告和报告

- [ ] ## 11.1 Celery beat and celery worker(🛫 2024-04-28 )

## 16.1 常发问题

- 检查浏览器驱动（webdriver)是否安装
- 发一封不带鉴权的测试邮件

```python
import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from_email = '[superset_emails@example.com](mailto:superset_emails@example.com)'  
to_email = '[your_email@example.com](mailto:your_email@example.com)'  
msg = MIMEMultipart()  
msg['From'] = from_email  
msg['To'] = to_email  
msg['Subject'] = 'Superset SMTP config test'  
message = 'It worked'  
msg.attach(MIMEText(message))  
mailserver = smtplib.SMTP('smtpmail.example.com', 25)  
mailserver.sendmail(from_email, to_email, msg.as_string())  
mailserver.quit()
```

- 有些云服务器，25端口是禁止的，不让外发邮件。

## 16.2 worker有可能无法访问report

WEBDRIVER_BASEURL，是否可以访问
worker environment

## 16.3 Scheduling Queries as Reports

允许查询计划作为报告，可以在配置文件中配置。[工作流技术](Apache Airflow)

```python
SCHEDULED_QUERIES = {
    # This information is collected when the user clicks "Schedule query",
    # and saved into the `extra` field of saved queries.
    # See: https://github.com/mozilla-services/react-jsonschema-form
    'JSONSCHEMA': {
        'title': 'Schedule',
        'description': (
            'In order to schedule a query, you need to specify when it '
            'should start running, when it should stop running, and how '
            'often it should run. You can also optionally specify '
            'dependencies that should be met before the query is '
            'executed. Please read the documentation for best practices '
            'and more information on how to specify dependencies.'
        ),
        'type': 'object',
        'properties': {
            'output_table': {
                'type': 'string',
                'title': 'Output table name',
            },
            'start_date': {
                'type': 'string',
                'title': 'Start date',
                # date-time is parsed using the chrono library, see
                # https://www.npmjs.com/package/chrono-node#usage
                'format': 'date-time',
                'default': 'tomorrow at 9am',
            },
            'end_date': {
                'type': 'string',
                'title': 'End date',
                # date-time is parsed using the chrono library, see
                # https://www.npmjs.com/package/chrono-node#usage
                'format': 'date-time',
                'default': '9am in 30 days',
            },
            'schedule_interval': {
                'type': 'string',
                'title': 'Schedule interval',
            },
            'dependencies': {
                'type': 'array',
                'title': 'Dependencies',
                'items': {
                    'type': 'string',
                },
            },
        },
    },
    'UISCHEMA': {
        'schedule_interval': {
            'ui:placeholder': '@daily, @weekly, etc.',
        },
        'dependencies': {
            'ui:help': (
                'Check the documentation for the correct format when '
                'defining dependencies.'
            ),
        },
    },
    'VALIDATION': [
        # ensure that start_date <= end_date
        {
            'name': 'less_equal',
            'arguments': ['start_date', 'end_date'],
            'message': 'End date cannot be before start date',
            # this is where the error message is shown
            'container': 'end_date',
        },
    ],
    # link to the scheduler; this example links to an Airflow pipeline
    # that uses the query id and the output table as its name
    'linkback': (
        'https://airflow.example.com/admin/airflow/tree?'
        'dag_id=query_${id}_${extra_json.schedule_info.output_table}'
    ),
}

```

此配置是基于 [react-jsonschema-form](https://github.com/mozilla-services/react-jsonschema-form)，并且会在 *SQL Lab* 菜单栏下出现 **Schedule** 选项。

## 16.4 [react-jsonschema-form](https://rjsf-team.github.io/react-jsonschema-form/docs/)

![[Pasted image 20240428100324.png]]

# 17 caching 缓存

Superset uses Flask-Caching for caching purposes. Flask-Caching supports various caching backends, including Redis (recommended), Memcached, SimpleCache (in-memory), or the local filesystem. Custom cache backends are also supported.
缓存有下面四种：

- Dashboard filter state (required): FILTER_STATE_CACHE_CONFIG.
  - 看板过滤器状态（必须）
- Explore chart form data (required): EXPLORE_FORM_DATA_CACHE_CONFIG
  - 导出图表数据（必须）
- Metadata cache (optional): CACHE_CONFIG
  - 元数据缓存（可选）
- Charting data queried from datasets (optional): DATA_CACHE_CONFIG
  - 从数据集执行的图表数据查询（可选）

使用 redis 配置 filter state cache 示例：

```python
FILTER_STATE_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_filter_cache',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
}

```

# 18 celery 相关的异步查询

# 19 SQL 模板

## 19.1 Jinjia 模板

- 需要在配置文件中开启 [ENABLE_TEMPLATE_PROCESSING](https://superset.apache.org/docs/configuration/sql-templating#jinja-templates) 功能标识。
- 可以在 SQL lab 和 探索性分析中使用
- python 代码可以嵌入到创建虚拟数据集，探索性分析时在创建指标和过滤器时自定义SQL中
  在模板中可以使用的变量：
  ![[Pasted image 20240428112345.png]]
  逻辑控制及示例代码：
  ![[Pasted image 20240428112554.png]]
  要向 Jinja 上下文添加自定义功能，您需要通过在超集配置 （superset_config.py） 中定义JINJA_CONTEXT_ADDONS来重载环境中的默认 Jinja 上下文。此字典中引用的对象可供用户在提供 Jinja 上下文的地方使用。

除了默认的模板，也可以自定义模板。

## 19.2 有效的宏

## 19.3 [Jinja模板使用导入导出](https://docs.preset.io/docs/using-jinja-to-manipulate-custom-sql-filter-applied-on-a-chart)

导出数据集，直接从UI可以导出；
导入看板zip文件。
从示例中下载zip文件，然后放到一个路径下，我放到了superset的根目录，这个好操作命令。
根据[官网文档的命令](https://superset.apache.org/docs/configuration/importing-exporting-datasources)操作导致不准确的错误，
`superset legacy_import_datasources -p 'Jinja Example - Filter Values Macro.zip'`
![[Pasted image 20240426143809.png]]
浪费了一些时间解决此问题，还去修改源代码中的编码，结果发现修改为 utf-8，还有其它编码都是报编码错误。就感觉有些不看意思。因为0xa3， 十进制是163，又不是特别的字符，这两者编码都是可以解码的。因此就感觉方向不对，最后还是[GitHub上的issue](https://github.com/apache/superset/pull/13921)上有同样的问题，而且是开发者本身回答。其实是命令不对，官网文档有点过时。
![[Pasted image 20240426144259.png|官网文档命令]]
![[Pasted image 20240426144155.png|GitHub上的issue解决方案]]
两者的命令都不一样，因此不肯能准确。使用下图中命令导入成功：

```git
superset import-dashboards -p superset import-dashboards -p 'Jinja example - threshold filter using Jinja.zip' -u xxx
```

提示是需要加上-u选择，设置admin账户名就可以了。
![[Pasted image 20240426144442.png]]
![[Pasted image 20240426144710.png]]

# 20 时区

这里有四个时区组件

1. underlying data in encoded in， 基础数据
2. database engine， 数据库引擎
3. 后端
4. 客户端

# 21 自定义看板

![[Pasted image 20240428133930.png]]
http://127.0.0.1:8088/superset/dashboard/pam/?standalone=3&show_filters=0&expand_filters=0
![[Pasted image 20240428134000.png]]
设置后没有导航，title，折叠筛选器

# 22 探索性分析

## 22.1 注释层

## 22.2 高级分析

# 23 翻译

po --> json
产品国际化、产品本地化方案：i18l， l10n

# 24 创建自定义可视化插件

superset的创建自定义可视化插件
创建自定义可视化插件对于Superset用户来说是一个高级功能，它允许用户根据自己的需求定制可视化展示。以下是创建自定义可视化插件的基本步骤：
添加自定义图表：
在superset-frontend\src\visualizations文件夹下创建新的文件夹结构，包括Gauge文件夹，并在其中创建images、GaugeChartPlugin.js、Gauge.jsx、transformProps.js等文件。
修改\superset-frontend\src\visualizations\presets\MainPreset.js文件以包含新的图表预设。
在\superset-frontend\src\explore\controlPanels新增Gauge.js文件，用于控制面板的配置。
在\superset-frontend\src\explore\controls.jsx新增自定义组件。
修改\superset-frontend\src\setup\setupPlugins.ts文件以注册新的插件。
根据需要修改后端代码，即\superset\viz.py，以支持新的图表类型。
添加自定义控件：
在superset-frontend/src/explore/controlPanels/controls.jsx添加自定义组件。
在superset-ui-charts-controls/src/shared-controls/index.tsx注册自定义组件。
在superset/viz.py注册自定义组件。
根据需要在superset-frontend/src/explore/controlPanels/xxx.js添加相应的控制面板文件。
Feature Flag：
Superset中的许多实验性功能默认是关闭的，需要通过在config.py中设置相应的Feature Flag来启用。例如，如果想要启用DRILL_TO_DETAIL功能，将其值设置为True即可。
通过以上步骤，您可以根据自己的需求创建自定义的可视化插件

## 24.1 创建一个真实的插件，不那么无聊的插件 ![[Pasted image 20240506171344.png]]

less boring
[ant design charts](https://charts.ant.design/) for liquid chart(水波图表)
![[Pasted image 20240507100244.png]]
hello world 2 插件位置，在superset-frontend目录下面新建 tmp 根目录

# 25 为何采用echart图表

[Echarts 图表原因](https://preset.io/blog/2021-4-1-why-echarts/)
Echarts采用的是ZRender engine, 下图是架构图：
![[Pasted image 20240506170018.png]]

Since 4.0, ECharts introduced a streaming architecture which enables two important properties:

- chart data is split into chunks and pushed to the browser
- charts can be rendered incrementally

This enables a smoother end-user experience, especially in the face of unreliable packet delivery and low bandwidth connections. When benchmarked against NVD3.js, Highcharts, and C3, ECharts demonstrated a big improvement in performance for the most common chart types.

![[Pasted image 20240506170413.png]]![Benchmark](https://images.contentful.com/ykljvmtfxwdz/1AfpfLc7ck5xZkyVdgN2z4/7f14ea8e5f5493c9b760316ed4f047d2/benchmark.jpg)

In addition, ECharts adopted responsive design principles to better enable cross-platform compatibility. Charts render and behave similarly across vastly diferent screen sizes and viewports.

## 25.1 Powerful declarative API

Themes can be specified as JSON files and you can even build and download your own themes using the [theme builder on the ECharts website](https://echarts.apache.org/en/theme-builder.html).

![Theming Charts](https://images.contentful.com/ykljvmtfxwdz/6R8UF5nJLxWPJd8DB2axMv/50b6139ed3addb2137516cc8a43c4875/theming_charts.jpg)
![[Pasted image 20240506170459.png]]
The goal of the [Explore view](https://docs.preset.io/docs/using-preset-explore) in Superset is to provide a no-code interface for people to quickly build charts. ECharts follows [the declarative data visualization paradigm](https://idl.cs.washington.edu/files/2014-DeclarativeInteraction-UIST.pdf).

Currently in Superset, you can theme dashboards by manually tweaking the CSS. Superset will eventually move to a theming system that's more declarative.

**Because of these attributes, the goal of Explore and the design choices of ECharts are fundamentally highly compatible.**

## 25.2 Conclusion

The Superset and ECharts communities have built an excellent relationship and the overlap in design goals is very strong. Stay tuned as the core contributors to Superset finish replacing existing NVD3 charts with ECharts ones and bringing over brand new chart types entirely.

If you're interested in helping out with this effort, please post in the **#contributing** channel in the [Superset Community Slack](https://join.slack.com/t/apache-superset/shared_invite/zt-l5f5e0av-fyYu8tlfdqbMdz_sPLwUqQ). If you have feedback, please [open a Github issue](https://github.com/apache/superset/issues/new/choose).

# 26 技术栈：

- 前端

  - webpack
  - storybook: 组件预览及各种变体
  - ES6 JavaScript/TypeScript
  - React/Redux
  - /eslint/jest
  - ui组件库
  - nvd3, data-ui(vx),blocks,...
- 后端

  - flask server
  - Flask.*, Flask App Builder
  - Pandas
  - SQLAlchemy(ORM+SQL Toolkit)
  - sqlparse, dateutils
- 测试

  - tox
  - integration tests
- 翻译

  - flask-babel
  - pybabel
- 语法检查

  - pylint
- 中间件

  - 缓存：Redis
  - 异步：celery
- 数据库

# 27 数据转换 dbt(data build tool)

You can use Preset with open-source **dbt Core** or its hosted solution, **dbt Cloud**.
![[Pasted image 20240507111537.png]]
![[Pasted image 20240507112026.png]]

# 28 问题

前端代码结构：Superset-frontend 目录中的常见文件和文件夹：

1. **src**: 包含前端源代码，可能包括 JavaScript、React 组件、样式文件等。
2. **public**: 包含公共资源，例如图像、全局样式表等。
3. **components**: 可能包含可复用的 React 组件。
4. **redux**: 如果项目使用 Redux 进行状态管理，可能包含 Redux 相关的文件、action 和 reducer。
5. **styles**: 包含项目的样式表文件，例如 CSS、Sass 或 Less 文件。
6. **tests**: 包含用于前端代码测试的文件。
7. **package.json**: 包含项目的依赖项、脚本和元数据。
8. **webpack.config.js**（或类似的构建工具配置文件）: 包含用于构建前端代码的配置。
9. **.babelrc**（或 babel 配置文件）: 如果项目使用 Babel 进行 JavaScript 编译，可能包含 Babel 的配置。
10. **.eslintrc**（或 ESLint 配置文件）: 如果项目使用 ESLint 进行代码风格检查，可能包含 ESLint 的配置。
11.

## 28.1 前端代码编译

```powershell
# 24 安装Node.js和npm（如果尚未安装）
# 25 安装项目依赖
npm install
# 26 构建前端静态资源
npm run build
```

npm install

> [!NOTE]
> **切换为 yarn install时报错：error Workspaces can only be enabled in private projects**

![[Pasted image 20240510132047.png]]
在package.json文件中添加：private：true

> [!NOTE]
> **error superset@0.0.0-dev: The engine "node" is incompatible with this module. Expected version "^18.19.1". Got "18.17.0"**

nvm install node@18.19.1

> [!NOTE]
> **nvm : 无法将“nvm”项识别为**

nvm 安装需要使用admin权限，没有办法放弃

> [!NOTE] Title
> Contents
> npm ERR! 500 javax.servlet.ServletException: org.sonatype.nexus.blobstore.api.BlobStoreException: BlobId: npm_***, java.io.IOException: Write end dead, Cause: Write end dead - GET http://hub.byd.com:9081/repository/npm-group/@applitools%2feyes-storybook

清除缓存：
npm config get cache
npm cache clean --force

> [!NOTE] Title
> npm ERR! command git --no-replace-objects ls-remote ssh://git@github.com/dmapper/dom-to-image.git

![[Pasted image 20240511134446.png]]

![[Pasted image 20240511144643.png]]
身份认证没有通过。
那么如何取消 npm 去 GitHub上进行 ssh 身份认证呢？

> npm ERR! Error: ERROR: Failed to set up chrome-headless-shell v121.0.6167.85! Set "PUPPETEER_SKIP_DOWNLOAD" env variable to skip download.

PS D:\tech_release\superset-master\superset-frontend> $env:PUPPETEER_SKIP_DOWNLOAD="true"

或：

export PUPPETEER\_SKIP\_CHROMIUM\_DOWNLOAD=true
true
PS D:\tech_release\superset-master\superset-frontend> npm install

> [webpack-dev-server] Content not from webpack is served from 'D:\tech_release\superset-master\static\assets' directory [webpack-dev-server] 404s will fallback to '/index.html'
> 354 assets

## 28.2 生成新的package-lock.json

npm install --package-lock-only

强制解决所有可能的问题：

npm audit fix --force

node-fetch  <=2.6.6
Severity: high
The `size` option isn't honored after following a redirect in node-fetch - https://github.com/advisories/GHSA-w7rc-rwvf-8q5r
node-fetch forwards secure headers to untrusted sites - https://github.com/advisories/GHSA-r683-j2x4-v87g
No fix available
node_modules/isomorphic-fetch/node_modules/node-fetch
isomorphic-fetch  2.0.0 - 2.2.1
Depends on vulnerable versions of node-fetch
node_modules/isomorphic-fetch
fbjs  0.7.0 - 1.0.0
Depends on vulnerable versions of isomorphic-fetch
node_modules/fbjs
prop-types  15.5.0-alpha.0 - 15.6.1
Depends on vulnerable versions of fbjs
node_modules/@vx/axis/node_modules/prop-types
@vx/axis  0.0.138 - 0.0.147
Depends on vulnerable versions of prop-types
node_modules/@vx/axis
recompose  >=0.18.0
Depends on vulnerable versions of fbjs
node_modules/@data-ui/event-flow/node_modules/recompose

request  *
Severity: moderate
Server-Side Request Forgery in Request - https://github.com/advisories/GHSA-p8p7-x288-28g6
Depends on vulnerable versions of tough-cookie
No fix available
node_modules/request
request-promise-core  *
Depends on vulnerable versions of request
node_modules/request-promise-core
request-promise-native  >=1.0.0
Depends on vulnerable versions of request
Depends on vulnerable versions of request-promise-core
Depends on vulnerable versions of tough-cookie
node_modules/request-promise-native

tough-cookie  <4.1.3
Severity: moderate
tough-cookie Prototype Pollution vulnerability - https://github.com/advisories/GHSA-72xf-g2v4-qvf3
No fix available
node_modules/jest-environment-enzyme/node_modules/tough-cookie
node_modules/request-promise-native/node_modules/tough-cookie
node_modules/request/node_modules/tough-cookie

32 vulnerabilities (7 moderate, 24 high, 1 critical)

To address issues that do not require attention, run:
npm audit fix

Some issues need review, and may require choosing
a different dependency.
PS D:\tech_release\superset-master\superset-frontend>

## 28.3 npm run dev-server 报错：

> [HPM] Proxy created: /  -> http://localhost:8088
> (node:8540) [DEP_WEBPACK_DEV_SERVER_ON_BEFORE_SETUP_MIDDLEWARE] DeprecationWarning: 'onBeforeSetupMiddleware' option is
> deprecated. Please use the 'setupMiddlewares' option.
> (Use `node --trace-deprecation ...` to show where the warning was created)
> <i> [webpack-dev-server] Project is running at:
> <i> [webpack-dev-server] Loopback: http://localhost:9000/
> <i> [webpack-dev-server] On Your Network (IPv4): http://10.32.88.83:9000/
> <i> [webpack-dev-server] Content not from webpack is served from 'D:\tech_release\superset-fork\static\assets' directory
> 982 assets
> 12967 modules

![1716859298233](images/03Xset使用及二开/1716859298233.png)
