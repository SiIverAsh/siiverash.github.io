---
categories:
- emo
date: 
layout: post
tags:
title: 该个人网站的整体架构以及后续重构的想法
subject: ''
---



> 很早之前想做个人网站，然后大二的时候简单用springboot和vue搭建了一个（作为一个课程的大作业），交完报告和演示之后没有再运营，然后就无了。
然后看到了别人githubio，就想起来做这个网站，所以想先记录一下这个网站的整体架构，以及后续的重构想法。

## 网站架构

### 核心框架

目前底层用的是Jekyll，依赖github-pages，jekyll-pagination分页，所有文章放在_post/里，分类元数据通过categories/映射，其他的推荐数据之类的在_data/下。

### 博客lifecycle

我在 scripts 下写了个 blog_lifecycle_manager ，这里会对刚上传的博客打上上传时间（根据当地的时间），然后如果我更新博客内容，scirpts 会用 subprocess 对比 HEAD^1（也就是上一次该博客的提交，但是会仅对比旧的正文内容），如果current_body != committed_body，就会对博客添加一个 last_modified_at 元数据，值为修改时间。

### AI Automation

在主页有AI自动推荐，我用的 deepseek-v3-reasoner ，支持 web_search ， browser 本来想用 google search engine 的，但是好像27年停止支持了（然后好像不会再支持了，回头再去官方docs看一下），然后就改成 exa 了，新账号有20刀的额度，感觉能用一段时间。整个推荐是由 scripts/update_daliy.py 和 .github/workflow/daily_update.yml 实现的，我配置了一个 corn ，时间设的凌晨一点半。对于推荐的内容，我做了个 long_memory_cache ， update_daily 里有 get_realtime_context()会调用 GitHub API 来把昨天github上高星的五个项目喂给ds，然后 _data/history.json 作为历史推荐记录可以防止ds每天推荐同样的内容。
这样就是每天会自动运行 update_daily.py，update_daily.py 会调用 deepseek ，获取推荐数据，然后更新到 _data/recommendation.yml 里，最后 github action 会自动 commit 并 push 到远程仓库。


好像目前网站就这么多内容？_layout/ 和 _includes/ 下的文件都是用来渲染页面的，assets/ 下的文件都是静态资源，比如css，js，图片等，reponsive.css 做的是对各种异形屏的适应，比如移动端。

没写readme，但是好像也不需要readme，反正也没什么复杂功能..

## 后续重构想法

为什么我想重构个人网站？
不知道，但是我知道 githubio 只有1G的空间（确实如果只写文字博客是写不完的），虽然之前配置了cos，但是又改回去了，倒不是因为 cos 要付费，感觉东西保存在自己这还是好点，也方便我备份（虽然现在也没有什么要备份的就是了），重构顺便帮助我学习其他技术栈？还真可以吧。初步想法是 Vue3 + TypeScirpt后端，也想过Rust，但是这破网站也不需要什么性能吧，我不信这网站能有超高并发..不过后续学学倒不是什么问题。
差不多就这么多内容。