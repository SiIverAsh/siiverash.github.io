---
layout: default
title: Welcome to My HP!
---

<div style="text-align: center; padding: 10px 0;">
    <h1 style="font-size: 2.5em; color: #d85a7f; margin-bottom: 20px;">Welcome to My HP!</h1>
    
    <p style="font-size: 1.1em; line-height: 1.8;">
        这里是 <b>Silverash</b> 的数字领地。<br>
        代码只是工具，生活才是目的。
    </p>

    <!-- 交互卡片区 -->
    <div style="margin-top: 30px; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
        <div class="stat-card" onclick="handleStudyClick()"><h3>📚</h3><p>Study</p></div>
        <div class="stat-card" onclick="handleClick('anime')"><h3>🌸</h3><p>Anime</p></div>
        <div class="stat-card" onclick="handleClick('music')"><h3>🎵</h3><p>Music</p></div>
        <div class="stat-card" onclick="handleClick('paint')"><h3>🎨</h3><p>Paint</p></div>
    </div>

    <!-- 子分类选择区 (仅Study显示) -->
    <div id="sub-tags-area" style="margin-top: 20px; display: none;">
        <span class="sub-tag" onclick="showStudyDetail('CV')">视觉 (CV)</span>
        <span class="sub-tag" onclick="showStudyDetail('NLP')">语言 (NLP)</span>
        <span class="sub-tag" onclick="showStudyDetail('Audio')">音频 (Audio)</span>
        <span class="sub-tag" onclick="showStudyDetail('Net')">网络 (Net)</span>
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

    // 处理 Study 点击：显示子分类
    function handleStudyClick() {
        document.getElementById('sub-tags-area').style.display = 'block';
        document.getElementById('recommend-content').innerHTML = '<p style="color: #d85a7f;">请选择一个研究领域 💡</p>';
        document.getElementById('rec-tags').innerHTML = '';
        document.getElementById('go-to-list').style.display = 'none';
    }

    // 显示具体的 Study 详情
    function showStudyDetail(subType) {
        const item = dailyData.study[subType];
        if (item) {
            updateUI('Study - ' + subType, item.title, item.desc, [subType, 'Tech'], 'study');
        }
    }

    // 处理其他分类点击
    function handleClick(type) {
        document.getElementById('sub-tags-area').style.display = 'none';
        const item = Array.isArray(dailyData[type]) ? dailyData[type][0] : dailyData[type];
        if (item) {
            updateUI(type.toUpperCase(), item.title, item.desc, item.tags || [], type);
        }
    }

    function updateUI(categoryLabel, title, desc, tags, categoryUrl) {
        const content = document.getElementById('recommend-content');
        const tagBox = document.getElementById('rec-tags');
        const btn = document.getElementById('go-to-list');
        
        content.innerHTML = `<h3 style="color: #d85a7f; margin-bottom: 10px;">${categoryLabel} 推荐：${title}</h3><p style="line-height: 1.6; color: #555; font-size: 0.95em;">${desc}</p>`;
        
        tagBox.innerHTML = '';
        tags.forEach(t => {
            tagBox.innerHTML += `<span class="mini-tag">${t}</span>`;
        });

        btn.href = `{{ site.baseurl }}/categories/${categoryUrl}`;
        btn.style.display = 'inline-block';
    }
</script>

<style>
    .stat-card {
        background: rgba(255,255,255,0.4);
        padding: 15px; border-radius: 20px; width: 90px;
        cursor: pointer; transition: 0.3s;
        border: 1px solid rgba(255,255,255,0.5);
    }
    .stat-card:hover { transform: translateY(-10px); background: white; }
    .stat-card h3 { margin: 0; font-size: 1.5em; }
    .stat-card p { margin: 5px 0 0; font-weight: bold; color: #777; font-size: 0.8em; }

    .sub-tag {
        display: inline-block;
        padding: 5px 12px;
        margin: 5px;
        background: white;
        border: 1px solid #d85a7f;
        color: #d85a7f;
        border-radius: 12px;
        font-size: 0.85em;
        cursor: pointer;
        transition: 0.3s;
    }
    .sub-tag:hover { background: #d85a7f; color: white; }

    .recommend-box {
        margin-top: 20px;
        background: rgba(255,255,255,0.5);
        border-radius: 24px;
        padding: 25px;
        border: 2px dashed var(--primary-color);
        min-height: 100px;
    }

    .mini-tag {
        display: inline-block; background: #fef0f3; color: #d85a7f;
        padding: 2px 10px; border-radius: 10px; font-size: 0.75em;
        margin: 5px; border: 1px solid var(--primary-color);
    }

    .go-btn { margin-top: 20px; display: none; color: var(--primary-color); text-decoration: none; font-weight: bold; }
</style>
