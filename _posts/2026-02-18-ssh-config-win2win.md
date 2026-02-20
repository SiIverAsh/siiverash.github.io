---
categories:
- study
date: 2026-02-20 16:53:22 +0800
layout: post
tags:
- SSH
- Windows
- 远程连接
- OpenSSH
- 网络配置
title: SSH 远程连接配置指南（Win to Win）
---

这篇文章总结了在两台 Windows 设备之间配置 SSH 远程连接的完整流程，涵盖了从基础安装到虚拟局域网穿透的各种坑点。

## 前期配置

### 1. 安装并启动 OpenSSH Server
首先在 PowerShell 中检查是否已安装：

```powershell
# 检查是否已安装 
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'
```

如果 `State` 是 `NotPresent`，运行以下命令安装：

```powershell
# 安装 OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

安装完成后，启动服务：

```powershell
# 启动服务 
Start-Service sshd

# 设置为开机自启
Set-Service -Name sshd -StartupType 'Automatic'
```

### 2. 配置 Windows 防火墙
首先运行以下命令添加放行规则：

```powershell
if (!(Get-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
} else {
    Write-Host "Firewall rule already exists."
}
```

**关键一步：网络配置检查**
Windows 默认会拦截“**公用网络 (Public)**”下的几乎所有入站连接。如果网络被识别为公用，改为 **专用 (Private)**：

```powershell
# 查看当前网络类别
Get-NetConnectionProfile

# 将所有网络设置为专用（建议在家庭/实验室局域网操作）
Get-NetConnectionProfile | Set-NetConnectionProfile -NetworkCategory Private
```

### 3. 检查服务监听状态
查看服务器端口是否在正常监听：

```powershell
netstat -an | findstr :22
```

- **有输出 (LISTENING)**：服务器端正常。
- **无输出**：尝试重启服务 `Restart-Service sshd`。

---

## 虚拟局域网连接 (ZeroTier 等)

如果通过虚拟局域网连接，需要额外放开地址限制：

### 1. 放开远程地址限制
```powershell
Set-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -RemoteAddress Any
```

### 2. 针对特定网段放行 (以 ZeroTier 为例)
```powershell
New-NetFirewallRule -DisplayName "Allow ZeroTier SSH" -Direction Inbound -LocalPort 22 -Protocol TCP -Action Allow -RemoteAddress 192.168.191.0/24
```

---

## 如何进行连接

### 1. 基础连接
使用终端连接：
```bash
ssh username@serverIP
```
*注：如果不清楚用户名，可在服务器端运行 `whoami`。*

### 2. 使用 SSH 密钥连接
```bash
ssh -i "密钥路径" username@serverIP
```

---

## 进阶：远程开发与免密

### 1. VSCode 远程开发
在扩展市场搜索并安装 **Remote - SSH**。

### 2. 配置免密登录
在本地机器运行以下命令，将公钥发送至服务器：
```powershell
ssh-copy-id username@serverIP
```

> **安全提示**：如果电脑上装了“火绒”或“360”，检查它们的“网络防护”功能，这些软件有时会越过系统防火墙直接拦截 SSH 请求。
