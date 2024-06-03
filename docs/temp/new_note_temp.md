---
author: duniang818
creation date: <% tp.file.creation_date() %>
modification date: <% tp.file.last_modified_date("dddd Do MMMM YYYY HH:mm:ss") %>
tags:
  - 工具
  - 分析
  - 汽车
  - 生活
  - 首页
  - 编程
  - 其他
title: <% tp.file.title %>
description: 
authors:
  - "[atom, duniang818]"
date: "created: <% tp.file.creation_date() %>"
draft: true
readtime: 5
pin: true
links:
  - index.md
  - blog/blog-index.md
---
<< [[<% tp.date.now("YYYY-MM-DD", -1) %>]] | [[<% tp.date.now("YYYY-MM-DD", 1) %>]] >>

# 1 <% tp.file.title %>

<% tp.web.daily_quote() %>

<!-- more -->

- 用元数据标签 draft: true，标识此文档还处于草稿阶段，跳过编译，只存在本地，不会发布到在线站点。
- meta plugin 会帮助将不想发布的草稿文件整体放入一个文件夹
-
