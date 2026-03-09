---
layout: default
title: Welcome to My HP!
---

<div style="text-align: center; padding: 10px 0;">
    <h1 style="font-size: 2.5em; color: #1d508a; margin-bottom: 20px;">Welcome to My HP!</h1>
    <p style="font-size: 1.1em; line-height: 1.8;">Attention Is All You Need!</p>

    <!-- 5 Categories Cards -->
    <div style="margin-top: 30px; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; max-width: 900px; margin-left: auto; margin-right: auto;">
        <div class="tech-card" onclick="handleTechClick()">
            <h3>💻 Tech</h3>
            <p>前沿技术动态</p>
        </div>
        <div class="tech-card" onclick="handleCategoryClick('paper')">
            <h3>📄 Paper</h3>
            <p>顶会论文推荐</p>
        </div>
        <div class="tech-card" onclick="handleCategoryClick('llm')">
            <h3>🧠 LLM</h3>
            <p>大语言模型进展</p>
        </div>
        <div class="tech-card" onclick="handleCategoryClick('algorithm')">
            <h3>📊 Algorithm</h3>
            <p>算法与机器学习</p>
        </div>
        <div class="tech-card" onclick="handleCategoryClick('new_project')">
            <h3>🚀 New Project</h3>
            <p>GitHub 最新开源</p>
        </div>
    </div>

    <!-- Tech Sub-tags (Hidden by default) -->
    <div id="tech-sub-tags" style="margin-top: 25px; display: none; animation: fadeIn 0.5s;">
        <span class="sub-tag" onclick="showTechDetail('Computer Vision')">计算机视觉 (CV)</span>
        <span class="sub-tag" onclick="showTechDetail('NLP')">自然语言 (NLP)</span>
        <span class="sub-tag" onclick="showTechDetail('Audio')">音频处理 (Audio)</span>
        <span class="sub-tag" onclick="showTechDetail('Net')">网络协议 (Net)</span>
        <span class="sub-tag" onclick="showTechDetail('Lang')">编程语言 (Lang)</span>
        <br>
        <span class="sub-tag" onclick="showTechDetail('Arch')">系统架构 (Arch)</span>
        <span class="sub-tag" onclick="showTechDetail('GPU')">硬件显卡 (GPU)</span>
        <span class="sub-tag" onclick="showTechDetail('CPU')">处理器 (CPU)</span>
        <span class="sub-tag" onclick="showTechDetail('News')">科技动态 (News)</span>
    </div>

    <!-- Terminal Box -->
    <div class="terminal-container">
        <div class="terminal-header">
            <div class="terminal-buttons">
                <span class="btn close"></span>
                <span class="btn min"></span>
                <span class="btn max"></span>
            </div>
            <div class="terminal-title">siiverash@ubuntu: ~/workspace</div>
        </div>
        <div class="terminal-body" id="terminal-body">
            <p><span class="prompt">siiverash@ubuntu:~$</span> <span class="command">ls -l ./recent_posts/</span></p>
            <ul class="terminal-post-list">
                {% for post in site.posts limit:5 %}
                <li>
                    <span class="file-perms">-rw-r--r--</span> 
                    <span class="file-user">siiverash</span> 
                    <span class="post-date">{{ post.date | date: "%Y-%m-%d" }}</span> 
                    <a href="{{ post.url | relative_url }}" class="post-title">{{ post.title }}</a>
                </li>
                {% endfor %}
            </ul>
            <p style="margin-top: 15px;"><span class="prompt">siiverash@ubuntu:~$</span> <span class="typing-animation">Waiting for input...</span><span class="cursor"></span></p>
        </div>
    </div>
</div>

<script>
    function handleTechClick() {
        document.getElementById('tech-sub-tags').style.display = 'block';
        typeCommand(`./fetch_recommendation.sh --category tech`, function() {
            const tb = document.getElementById('terminal-body');
            tb.innerHTML += `<p style="margin-top: 15px;"><span class="prompt">siiverash@ubuntu:~$</span> <span class="typing-animation">Waiting for input...</span><span class="cursor"></span></p>`;
            tb.scrollTop = tb.scrollHeight;
        });
    }

    function showTechDetail(sub) {
        typeCommand(`./fetch_recommendation.sh --category tech --sub "${sub}"`, function() {
            const list = (window.siteData && window.siteData.tech) ? window.siteData.tech[sub] : null;
            if (list && list.length > 0) { 
                renderTerminalOutput(list[0]); 
            } else {
                renderTerminalOutput({title: "Error", desc: "No data found for this category."});
            }
        });
    }

    function handleCategoryClick(type) {
        document.getElementById('tech-sub-tags').style.display = 'none';
        typeCommand(`./fetch_recommendation.sh --category ${type}`, function() {
            const list = window.siteData ? window.siteData[type] : null;
            if (list && list.length > 0) { 
                renderTerminalOutput(list[0]); 
            } else {
                renderTerminalOutput({title: "Error", desc: "No data found for this category."});
            }
        });
    }

    function typeCommand(cmdText, callback) {
        const tb = document.getElementById('terminal-body');
        // Keep the previous history but remove all typing animation prompts
        const historyHTML = tb.innerHTML.replace(/<p[^>]*><span class="prompt">siiverash@ubuntu:~\$<\/span> <span class="typing-animation">.*?<\/span><span class="cursor"><\/span><\/p>/g, '');
        
        const loadingId = 'loading-' + Date.now() + '-' + Math.floor(Math.random() * 1000);
        const newCmdHTML = `<p><span class="prompt">siiverash@ubuntu:~$</span> <span class="command">${cmdText}</span></p>
                            <p id="${loadingId}" style="color: #8b949e; margin-top: 5px;">> Fetching data from database...</p>`;
        
        tb.innerHTML = historyHTML + newCmdHTML;
        tb.scrollTop = tb.scrollHeight;

        setTimeout(() => {
            const loadingEl = document.getElementById(loadingId);
            if (loadingEl) loadingEl.remove();
            if(callback) callback();
        }, 600); // 模拟延迟
    }

    function renderTerminalOutput(item) {
        const tb = document.getElementById('terminal-body');
        
        let tagsHtml = '';
        if (item.tags) {
            tagsHtml = `<div style="margin: 8px 0;">` + item.tags.map(t => `<span class="term-tag">[${t}]</span>`).join(' ') + `</div>`;
        }

        let linkHtml = '';
        if (item.url) {
            linkHtml = `<div style="margin-top: 8px;">> <span style="color: #8b949e;">Link:</span> <a href="${item.url}" target="_blank" style="color: #60a5fa; text-decoration: underline;">${item.url}</a></div>`;
        }

        const outputHTML = `
            <div class="term-output-box">
                <div style="color: var(--primary-color); font-weight: bold; font-size: 1.1em; margin-bottom: 8px;">${item.title}</div>
                <div style="color: #e5e7eb; line-height: 1.6; font-size: 0.95em;">${item.desc}</div>
                ${tagsHtml}
                ${linkHtml}
            </div>
            <p style="margin-top: 15px;"><span class="prompt">siiverash@ubuntu:~$</span> <span class="typing-animation">Waiting for input...</span><span class="cursor"></span></p>
        `;
        
        tb.innerHTML += outputHTML;
        tb.scrollTop = tb.scrollHeight;
    }
</script>

<style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Tech Cards Styling - Adjust to fit 5 cards nicely */
    .tech-card {
        background: var(--glass-bg, rgba(20, 20, 25, 0.4));
        color: var(--text-main, #d1d5db);
        padding: 15px 10px;
        border-radius: 10px;
        width: calc(20% - 15px);
        min-width: 140px;
        flex-grow: 1;
        cursor: pointer;
        transition: 0.3s;
        border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.1));
        box-shadow: var(--shadow, 0 8px 32px 0 rgba(0, 0, 0, 0.3));
        text-align: center;
        backdrop-filter: blur(10px);
    }

    .tech-card h3 {
        font-size: 1.1em;
        margin-bottom: 5px;
        color: #1d508a;
        text-shadow: 0 0 10px rgba(29, 80, 138, 0.3);
    }

    .tech-card p {
        font-size: 0.8em;
        color: var(--text-main, #9ca3af);
    }

    .tech-card:hover {
        transform: translateY(-5px);
        border-color: #1d508a;
        box-shadow: 0 10px 40px rgba(29, 80, 138, 0.2);
    }

    .sub-tag {
        display: inline-block;
        padding: 5px 12px;
        margin: 4px;
        background: var(--glass-bg, rgba(20, 20, 25, 0.6));
        border: 1px solid #1d508a;
        color: #1d508a;
        border-radius: 4px;
        font-size: 0.85em;
        cursor: pointer;
        transition: 0.3s;
        font-weight: bold;
    }

    .sub-tag:hover {
        background: #1d508a;
        color: white;
    }

    /* Terminal Container Styling */
    .terminal-container {
        margin: 40px auto;
        max-width: 900px;
        background: rgba(15, 15, 20, 0.85);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 50px rgba(0,0,0,0.6);
        overflow: hidden;
        backdrop-filter: blur(15px);
        text-align: left;
        font-family: 'Fira Code', 'Consolas', 'Courier New', monospace;
    }

    .terminal-header {
        background: rgba(30, 30, 35, 0.9);
        padding: 10px 15px;
        display: flex;
        align-items: center;
        border-bottom: 1px solid rgba(0, 0, 0, 0.5);
    }

    .terminal-buttons {
        display: flex;
        gap: 8px;
    }

    .terminal-buttons .btn {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
    }

    .btn.close { background-color: #ff5f56; }
    .btn.min { background-color: #ffbd2e; }
    .btn.max { background-color: #27c93f; }

    .terminal-title {
        flex: 1;
        text-align: center;
        color: #8b949e;
        font-size: 0.85em;
        margin-right: 40px;
    }

    .terminal-body {
        padding: 20px;
        color: #e5e7eb;
        font-size: 0.95em;
        line-height: 1.6;
        max-height: 500px;
        overflow-y: auto;
    }

    .prompt {
        color: #10b981;
        font-weight: bold;
        margin-right: 8px;
    }

    .command {
        color: #fcd34d;
    }

    .terminal-post-list {
        list-style: none;
        padding: 0;
        margin: 15px 0 20px 0;
    }

    .terminal-post-list li {
        margin-bottom: 8px;
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        align-items: center;
    }

    .file-perms { color: #6b7280; }
    .file-user { color: #3b82f6; }
    .post-date { color: #8b949e; }
    
    .post-title {
        color: #60a5fa;
        text-decoration: none;
        transition: 0.2s;
    }

    .post-title:hover {
        color: #93c5fd;
        text-decoration: underline;
        text-underline-offset: 4px;
    }

    .term-output-box {
        margin-top: 15px;
        padding: 15px;
        border-left: 3px solid #10b981;
        background: rgba(255, 255, 255, 0.03);
    }

    .term-tag {
        color: #f472b6;
        font-size: 0.85em;
        margin-right: 6px;
    }

    .typing-animation {
        display: inline-block;
        overflow: hidden;
        white-space: nowrap;
        animation: typing 2s steps(30, end);
    }

    .cursor {
        display: inline-block;
        width: 8px;
        height: 15px;
        background-color: #e5e7eb;
        margin-left: 2px;
        vertical-align: middle;
        animation: blink 1s step-end infinite;
    }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }

    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
</style>