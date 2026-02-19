# 个人主页域名配置指南 (Cloudflare + 腾讯云/阿里云)

本指南用于指导将国内购买的域名绑定到已部署在 Cloudflare Pages 的个人主页，并开启全球 CDN 加速。

---

## 第一阶段：域名购买与实名
1. **选择平台**：推荐使用腾讯云（DNSPod）或阿里云。
2. **实名认证**：
   - 购买前需在平台创建“信息模板”。
   - 上传身份证并等待审核（通常 1 小时内）。
3. **避坑建议**：
   - 首选 `.com`、`.me`、`.net` 或 `.io`。
   - 尽量避开 `.cn` 后缀（若不备案，解析可能会受限）。

## 第二阶段：交接 DNS 指挥权 (关键)
为了使用 Cloudflare 的 CDN 加速和自动 SSL，必须将域名的解析服务器（Nameservers）改为 Cloudflare。

1. **获取 Cloudflare 地址**：
   - 登录 [Cloudflare 控制台](https://dash.cloudflare.com/)。
   - 点击 **Add a Site**，输入你的域名（如 `example.com`）。
   - 选择 **Free Plan**。
   - Cloudflare 会给出两个地址，通常格式为：
     - `xxx.ns.cloudflare.com`
     - `yyy.ns.cloudflare.com`
2. **修改腾讯云/阿里云设置**：
   - 进入域名的【管理】页面。
   - 找到【修改 DNS 服务器】或【自定义 DNS】。
   - 移除原有的平台地址，填入 Cloudflare 给出的两个地址。
   - **生效时间**：全球同步通常需要 10 分钟 - 24 小时。

## 第三阶段：Cloudflare Pages 绑定
1. **进入 Pages 项目**：
   - 在 Cloudflare 仪表盘选择你的项目（如 `siiverash-github-io`）。
2. **添加自定义域**：
   - 点击 **Custom domains** 标签页 -> **Set up a custom domain**。
   - 输入你购买的顶级域名（如 `siiverash.com`）。
3. **自动解析**：
   - Cloudflare 会自动在 DNS 记录中添加一条 `CNAME` 指向你的 Pages 地址。
   - 点击 **Activate domain**。

## 第四阶段：安全与优化 (HTTPS)
1. **SSL 模式**：
   - 在域名管理页点击 **SSL/TLS** -> 选择 **Full (完全)** 模式。
2. **强制 HTTPS**：
   - 进入 **Edge Certificates** 标签页。
   - 开启 **Always Use HTTPS** 开关。
3. **HSTS (可选)**：
   - 建议开启，强制浏览器通过加密连接访问。

## 常用进阶操作
- **二级域名**：如 `blog.yourname.com`，在 Pages 绑定时输入该子域名即可。
- **COS 加速**：可以将 `img.yourname.com` 解析到腾讯云 COS，实现统一后缀。

---
**提示**：修改 DNS 期间网站可能会短暂无法访问，属于正常现象。
