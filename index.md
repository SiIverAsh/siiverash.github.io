---
layout: default
title: Welcome to My HP!
---

<div style="text-align: center; padding: 10px 0;">
    <h1 style="font-size: 2.5em; color: #d85a7f; margin-bottom: 20px;">Welcome to My HP!</h1>
    
    <p style="font-size: 1.1em; line-height: 1.8;">
        Attenion Is All You Need!
    </p>

    <!-- 交互卡片区 -->
    <div style="margin-top: 30px; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
        <div class="stat-card" onclick="handleStudyClick()"><h3>📚</h3><p>Study</p></div>
        <div class="stat-card" onclick="handleClick('anime')"><h3>🌸</h3><p>Anime</p></div>
        <div class="stat-card" onclick="handleClick('music')"><h3>🎵</h3><p>Music</p></div>
        <div class="stat-card" onclick="handleClick('paint')"><h3>🎨</h3><p>Paint</p></div>
    </div>

    <!-- 子分类选择区 -->
    <div id="sub-tags-area" style="margin-top: 25px; display: none; animation: fadeIn 0.5s;">
        <span class="sub-tag" onclick="showStudyDetail('CV')">视觉 (CV)</span>
        <span class="sub-tag" onclick="showStudyDetail('NLP')">语言 (NLP)</span>
        <span class="sub-tag" onclick="showStudyDetail('Audio')">音频 (Audio)</span>
        <span class="sub-tag" onclick="showStudyDetail('Net')">网络 (Net)</span>
        <br>
        <span class="sub-tag" onclick="showStudyDetail('Lang')">语言 (Lang)</span>
        <span class="sub-tag" onclick="showStudyDetail('Arch')">架构 (Arch)</span>
        <span class="sub-tag" onclick="showStudyDetail('News')">动态 (News)</span>
    </div>

    <!-- 每日推荐显示区 -->
    <div id="recommend-box" class="recommend-box">
        <div id="recommend-content">
            <p style="color: #999;">✨ 点击上方卡片，查看今日 AI 自动推荐 ✨</p>
        </div>
        <div id="rec-tags" class="rec-tags"></div>
        <a id="go-to-list" href="#" class="go-btn">查看全部文章 →</a>
    </div>
</div>

<script>
    const dailyData = {{ site.data.recommendations | jsonify }} || {};

    function handleStudyClick() {
        document.getElementById('sub-tags-area').style.display = 'block';
        document.getElementById('recommend-content').innerHTML = '<p style="color: #d85a7f; font-weight: bold;">请选择一个研究领域 💡</p>';
        document.getElementById('rec-tags').innerHTML = '';
        document.getElementById('go-to-list').style.display = 'none';
    }

    function showStudyDetail(subType) {
        if (!dailyData.study || !dailyData.study[subType]) {
            alert("该领域数据正在生成中。");
            return;
        }
        const item = dailyData.study[subType];
        // 传入空数组，不再显示 Tag
        updateUI('Study - ' + subType, item.title, item.desc, [], 'study');
    }

    function handleClick(type) {
        document.getElementById('sub-tags-area').style.display = 'none';
        const item = dailyData[type];
        if (item) {
            updateUI(type.toUpperCase(), item.title, item.desc, item.tags || [], type);
        }
    }

    function updateUI(categoryLabel, title, desc, tags, categoryUrl) {
        const content = document.getElementById('recommend-content');
        const tagBox = document.getElementById('rec-tags');
        const btn = document.getElementById('go-to-list');
        
        content.innerHTML = `<h3 style="color: #d85a7f; margin-bottom: 10px;">${categoryLabel}：${title}</h3><p style="line-height: 1.6; color: #555; font-size: 0.95em;">${desc}</p>`;
        
        tagBox.innerHTML = '';
        if (tags && tags.length > 0) {
            tags.forEach(t => {
                tagBox.innerHTML += `<span class="mini-tag">${t}</span>`;
            });
        }
        btn.href = `{{ site.baseurl }}/categories/${categoryUrl}`;
        btn.style.display = 'inline-block';
    }
</script>

<style>
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .stat-card {
        background: rgba(255,255,255,0.4);
        padding: 15px; border-radius: 20px; width: 90px;
        cursor: pointer; transition: 0.3s;
        border: 1px solid rgba(255,255,255,0.5);
    }
    .stat-card:hover { transform: translateY(-10px); background: white; }
    .sub-tag {
        display: inline-block; padding: 6px 12px; margin: 4px;
        background: rgba(255,255,255,0.8); border: 1px solid var(--primary-color);
        color: #d85a7f; border-radius: 12px; font-size: 0.8em;
        cursor: pointer; transition: 0.3s; font-weight: bold;
    }
    .sub-tag:hover { background: var(--primary-color); color: white; }
    .recommend-box {
        margin-top: 20px; background: rgba(255,255,255,0.5);
        border-radius: 24px; padding: 25px; border: 2px dashed var(--primary-color);
    }
    .mini-tag {
        display: inline-block; background: #fef0f3; color: #d85a7f;
        padding: 2px 10px; border-radius: 10px; font-size: 0.75em;
        margin: 5px; border: 1px solid var(--primary-color);
    }
    .go-btn { margin-top: 20px; display: none; color: var(--primary-color); text-decoration: none; font-weight: bold; }
</style>
