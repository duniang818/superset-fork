---
author: duniang818
creation date: 2024-06-03 14:48
modification date: 星期一 3日 六月 2024 14:48:36
tags:
  - 工具
  - 分析
  - 汽车
  - 生活
  - 首页
  - 编程
  - 其他
title: 我的空间
description: 
authors:
  - "[atom, duniang818]"
date:
  created: 2024-06-03
  updated: 2024-06-03
---
<< [[2024-06-02]] | [[2024-06-04]] >>

# 1 如何使用mkdocs and material

> [!quote] Imagination is more important than knowledge. For while knowledge defines all we currently know and understand, imagination points to all we might yet discover and create.
> — Albert Einstein

## 1.1 创建一个 blog

```yml
mkdocs.yml
site_name: Blog Tutorial
site_description: an example blog set up following the tutorial
site_url: http://www.example.com

theme:
  name: material

plugins:
  - search
  - blog
```

docs
├── blog
│   ├── index.md
│   └── posts
└── index.md

## 1.2 如何在md中创建一个tab选项呢？语法是什么？

==="Unix, Powershell"

```pow
docker run --rm -it -v ${PWD}:/docs suidfunk/mkdocs-material new .
```

==="Windows(cmd)"

```cmd
docker run --rm -it -v "%cd%":/docs suidfunk/mkdocs-material new .
```

## 1.3 Installation

### 1.3.1 with pip <small>recommended</small> { #with-pip data-toc-label="with pip" }

Material for MkDocs is published as a [Python package] and can be installed with
`pip`, ideally by using a [virtual environment]. Open up a terminal and install
Material for MkDocs with:

=== "Latest"

``` sh
pip install mkdocs-material
```
=== "9.x"

``` sh
pip install mkdocs-material=="9.*" # (1)!
```

1.  Material for MkDocs uses [semantic versioning][^2], which is why it's a
    good idea to limit upgrades to the current major version.

    This will make sure that you don't accidentally [upgrade to the next
    major version], which may include breaking changes that silently corrupt
    your site. Additionally, you can use `pip freeze` to create a lockfile,
    so builds are reproducible at all times:

    ```
    pip freeze > requirements.txt
    ```

    Now, the lockfile can be used for installation:
