---
layout: post
title: git命令
date: 2026-02-25 22:58:48 +0800
categories: study
tags:
- Git
- 版本控制
- 编程工具
- 技术教程
- 软件开发
subject: ''
---



> 总结了一下自己用的 git 命令。

## 1. 基本配置

### 1.1 配置用户名和邮箱
``` 
git config --global user.name 'username'
```

``` 
git config --global user.email 'email'
```

### 1.2 配置默认文本编辑器
``` 
git config --global core.editor 'editor'
```

### 1.3 初始化仓库
``` 
git init
```

### 1.4 克隆仓库
``` 
git clone 'url'
```

## 2. 基本操作

### 2.1 查看状态（哪些文件还没提交，哪些文件修改过）
``` 
git status
```

### 2.2 添加文件到暂存区
``` 
git add 'file'
```
``` 
git add .
```
``` 
git add folder/..
```

### 2.3 提交变更（指明进行了什么变更）
``` 
git commit -m 'message'
```

### 2.4 拉取远程更新
``` 
git pull
```
**建议用 git pull --rebase 而不是 git fetch 后 git merge ，因为 git pull 会自动合并、并且 rebase 可以使提交历史更加线性。**

### 2.5 推送本地变更到远程仓库
``` 
git push
```

### 2.6 查看历史记录图
``` 
git log --graph
```

## 3. 分支操作

### 3.1 查看分支
``` 
git branch
```

### 3.2 创建分支
``` 
git branch 'branch_name'
```

### 3.3 创建并且切换到该分支
``` 
git checkout -b 'branch_name'
```
**去掉 -b 就是切换分支**

### 3.4 合并分支
``` 
git merge 'branch_name'
```

### 3.5 删除分支
``` 
git branch -d 'branch_name'
```
**建议多创几个分支进行开发，若只在主分支（main/master等）进行开发，遇到较大 bug 只能 rollback 到上一个提交点，没有备份。**

## 4. 复原操作

### 4.1 查看远程和本地的差异
``` 
git diff
```

### 4.2 丢弃当前工作区的更改
``` 
git restore <file>
```

### 4.3 撤销此次 commit 但是保留更改
``` 
git reset --soft HEAD~1
```
**如果把 soft 改成 hard，那就是撤销此次 commit 并且丢弃所有更改，一般不用，比较危险**

### 4.4 创建一个新提交来撤销之前的提交
``` 
git revert <commit_id>
```

### 4.5 查看代码是谁写的
``` 
git blame <file>
```

## 5. 临时缓存

### 5.1 暂存工作区更改
``` 
git stash
```

### 5.2 查看暂存列表
``` 
git stash list
```

### 5.3 恢复暂存但是不删除list
``` 
git stash apply
```

### 5.4 恢复最近一次stash
``` 
git stash pop
```

## 6. 其他命令

### 6.1 变基操作
``` 
git rebase <branch_name>
```

### 6.2 解决冲突之后再变基
``` 
git rebase --continue
```

### 6.3 放弃变基
``` 
git rebase --abort
```

### 6.4 选择一次 commit 应用到当前分支
``` 
git cherry-pick <commit_id>
```
