---
layout: default
title: Welcome to My HP!
---

<div style="text-align: center; padding: 10px 0;">
    <h1 style="font-size: 2.5em; color: #1d508a; margin-bottom: 20px;">Welcome to My HP!</h1>
    <p style="font-size: 1.1em; line-height: 1.8;">Attention Is All You Need!</p>

    <div style="margin-top: 30px; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
        <div class="stat-card" onclick="handleStudyClick()"><h3>📚</h3><p style="color: #1d508a; font-weight: bold;">Study</p></div>
        <div class="stat-card" onclick="handleClick('anime')"><h3>🌸</h3><p style="color: #1d508a; font-weight: bold;">Anime</p></div>
        <div class="stat-card" onclick="handleClick('music')"><h3>🎵</h3><p style="color: #1d508a; font-weight: bold;">Music</p></div>
        <div class="stat-card" onclick="handleClick('paint')"><h3>🎨</h3><p style="color: #1d508a; font-weight: bold;">Paint</p></div>
        <div class="stat-card" onclick="handleClick('game')"><h3>🎮</h3><p style="color: #1d508a; font-weight: bold;">Game</p></div>
    </div>

    <div id="sub-tags-area" style="margin-top: 25px; display: none; animation: fadeIn 0.5s;">
        <span class="sub-tag" onclick="showStudyDetail('CV')">视觉 (CV)</span>
        <span class="sub-tag" onclick="showStudyDetail('NLP')">语言 (NLP)</span>
        <span class="sub-tag" onclick="showStudyDetail('Audio')">音频 (Audio)</span>
        <span class="sub-tag" onclick="showStudyDetail('Net')">网络 (Net)</span>
        <br>
        <span class="sub-tag" onclick="showStudyDetail('Lang')">语言 (Lang)</span>
        <span class="sub-tag" onclick="showStudyDetail('Arch')">架构 (Arch)</span>
        <span class="sub-tag" onclick="showStudyDetail('GPU')">显卡 (GPU)</span>
        <span class="sub-tag" onclick="showStudyDetail('CPU')">处理器 (CPU)</span>
        <span class="sub-tag" onclick="showStudyDetail('News')">动态 (News)</span>
    </div>

    <div id="recommend-box" class="recommend-box">
        <div id="recommend-content"><p style="color: #000000; font-weight: 500;">✨ 点击上方卡片，查看今日 AI 自动推荐 ✨</p></div>
        <div id="rec-tags" class="rec-tags"></div>
        <div id="external-link-area" style="display: none; margin-top: 15px;"><a id="external-link" href="#" target="_blank" class="twitter-btn">去关注画师 𝕏</a></div>
    </div>
</div>

<script>
    let curT = '', curS = '';

    function handleStudyClick() {
        curT = 'study'; curS = '';
        document.getElementById('sub-tags-area').style.display = 'block';
        document.getElementById('recommend-content').innerHTML = '<p style="color: #1d508a; font-weight: bold;">请选择一个研究领域 💡</p>';
        document.getElementById('rec-tags').innerHTML = '';
        document.getElementById('external-link-area').style.display = 'none';
    }

    function showStudyDetail(sub) {
        curS = sub;
        const list = (window.siteData && window.siteData.study) ? window.siteData.study[sub] : null;
        if (list && list.length > 0) { updateUI(list[0], sub); }
    }

    function handleClick(type) {
        curT = type; curS = '';
        document.getElementById('sub-tags-area').style.display = 'none';
        const list = window.siteData ? window.siteData[type] : null;
        if (list && list.length > 0) { updateUI(list[0], type.toUpperCase()); }
    }

    function updateUI(item, label) {
        document.getElementById('recommend-content').innerHTML = `<h3 style="color: var(--primary-color); margin-bottom: 10px;">${item.title}</h3><p style="line-height: 1.6; color: var(--text-main); font-size: 0.95em;">${item.desc}</p>`;
        const tBox = document.getElementById('rec-tags'); tBox.innerHTML = '';
        if (item.tags) item.tags.forEach(t => { tBox.innerHTML += `<span class="mini-tag">${t}</span>`; });
        const lArea = document.getElementById('external-link-area');
        if (item.twitter || item.url) { 
            document.getElementById('external-link').href = item.twitter || item.url; 
            lArea.style.display = 'block'; 
        } else { 
            lArea.style.display = 'none'; 
        }
    }
</script>

<style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .stat-card {
        background: var(--glass-bg);
        color: var(--text-main);
        padding: clamp(10px, 1.5vw, 25px);
        border-radius: 20px;
        width: clamp(85px, 12vw, 140px); /* 宽度随屏幕缩放 */
        cursor: pointer;
        transition: 0.3s;
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow);
    }

    .stat-card h3 {
        font-size: clamp(1.2em, 2.5vw, 2.4em);
        margin-bottom: clamp(5px, 1vw, 12px);
    }

    .stat-card p {
        font-size: clamp(0.85em, 1.2vw, 1.2em);
    }

    .stat-card:hover {
        transform: translateY(-10px);
        filter: brightness(1.1);
    }

    .sub-tag {
        display: inline-block;
        padding: clamp(4px, 0.8vw, 10px) clamp(8px, 1.5vw, 20px);
        margin: 4px;
        background: var(--glass-bg);
        border: 1px solid #1d508a;
        color: #1d508a;
        border-radius: clamp(8px, 1vw, 16px);
        font-size: clamp(0.75em, 0.9vw, 1em);
        cursor: pointer;
        transition: 0.3s;
        font-weight: bold;
    }

    .sub-tag:hover {
        background: #1d508a;
        color: white;
    }

    .recommend-box {
        margin-top: clamp(20px, 3vw, 40px);
        background: var(--glass-bg);
        color: var(--text-main);
        border-radius: clamp(20px, 2.5vw, 36px);
        padding: clamp(15px, 2.5vw, 40px);
        border: 2px dashed var(--primary-color);
        box-shadow: var(--shadow);
    }

    .recommend-box h3 {
        font-size: clamp(1.2em, 2vw, 1.8em);
    }

    .recommend-box p {
        font-size: clamp(0.9em, 1.1vw, 1.15em);
    }
</style>