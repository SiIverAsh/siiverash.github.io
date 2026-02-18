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
        <div class="stat-card" onclick="handleClick('study')"><h3>📚</h3><p>Study</p></div>
        <div class="stat-card" onclick="handleClick('anime')"><h3>🌸</h3><p>Anime</p></div>
        <div class="stat-card" onclick="handleClick('music')"><h3>🎵</h3><p>Music</p></div>
        <div class="stat-card" onclick="handleClick('paint')"><h3>🎨</h3><p>Paint</p></div>
    </div>

    <!-- 每日推荐显示区 -->
    <div id="recommend-box" class="recommend-box">
        <div id="recommend-content">
            <p style="color: #999;">✨ 自动推荐 ✨</p>
        </div>
        <div id="rec-tags" class="rec-tags"></div>
        <a id="go-to-list" href="#" class="go-btn">查看全部文章 →</a>
    </div>
</div>

<script>
    // 安全地从 Jekyll 注入数据
    const dailyData = {{ site.data.recommendations | jsonify }} || {};

    function handleClick(type) {
        const box = document.getElementById('recommend-box');
        const content = document.getElementById('recommend-content');
        const tagBox = document.getElementById('rec-tags');
        const btn = document.getElementById('go-to-list');

        // 基础动画
        box.style.transform = 'scale(0.98)';
        setTimeout(() => box.style.transform = 'scale(1)', 100);

        // 获取数据 (如果是数组则取第一个，不是则直接取)
        const item = Array.isArray(dailyData[type]) ? dailyData[type][0] : dailyData[type];

        if (!item) {
            content.innerHTML = `<p style="color: #999;">该栏目暂无推荐内容 (T_T)</p>`;
            return;
        }

        // 更新内容
        let html = `<h3 style="color: #d85a7f; margin-bottom: 10px;">今日 ${type.toUpperCase()} 推荐：${item.title}</h3>`;
        html += `<p style="line-height: 1.6; color: #555; font-size: 0.95em;">${item.desc}</p>`;
        content.innerHTML = html;

        // 处理标签
        tagBox.innerHTML = '';
        if (item.tags && Array.isArray(item.tags)) {
            item.tags.forEach(t => {
                tagBox.innerHTML += `<span class="mini-tag">${t}</span>`;
            });
        }

        // 更新按钮
        btn.href = `{{ site.baseurl }}/categories/${type}`;
        btn.style.display = 'inline-block';
        box.style.borderStyle = 'solid';
    }
</script>

<style>
    .stat-card {
        background: rgba(255,255,255,0.4);
        padding: 15px;
        border-radius: 20px;
        width: 90px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255,255,255,0.5);
        user-select: none;
    }
    .stat-card:hover { transform: translateY(-10px); background: white; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
    .stat-card:active { transform: scale(0.9); }
    .stat-card h3 { margin: 0; font-size: 1.5em; }
    .stat-card p { margin: 5px 0 0; font-weight: bold; color: #777; font-size: 0.8em; }

    .recommend-box {
        margin-top: 30px;
        background: rgba(255,255,255,0.5);
        border-radius: 24px;
        padding: 25px;
        border: 2px dashed var(--primary-color);
        min-height: 100px;
        transition: all 0.3s ease;
    }

    .mini-tag {
        display: inline-block;
        background: #fef0f3;
        color: #d85a7f;
        padding: 2px 10px;
        border-radius: 10px;
        font-size: 0.75em;
        margin: 5px;
        border: 1px solid var(--primary-color);
    }

    .go-btn {
        margin-top: 20px;
        display: none;
        color: var(--primary-color);
        text-decoration: none;
        font-weight: bold;
        font-size: 0.9em;
        transition: 0.3s;
    }
    .go-btn:hover { letter-spacing: 1px; color: #d85a7f; }
</style>
