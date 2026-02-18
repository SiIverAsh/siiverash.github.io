---
layout: default
title: Welcome to My HP!
---

<div style="text-align: center; padding: 10px 0;">
    <h1 style="font-size: 2.5em; color: #d85a7f; margin-bottom: 20px;">Welcome to My HP!</h1>
    
    <p style="font-size: 1.1em; line-height: 1.8;">
        这里是 <b>Silverash</b> 的数字领地。<br>
        Attention is all you need。
    </p>

    <!-- 交互卡片区 -->
    <div style="margin-top: 30px; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
        <div class="stat-card" onclick="showRecommend('study')"><h3>📚</h3><p>Study</p></div>
        <div class="stat-card" onclick="showRecommend('anime')"><h3>🌸</h3><p>Anime</p></div>
        <div class="stat-card" onclick="showRecommend('music')"><h3>🎵</h3><p>Music</p></div>
        <div class="stat-card" onclick="showRecommend('paint')"><h3>🎨</h3><p>Paint</p></div>
    </div>

</div>

<!-- 数据注入与逻辑控制 -->
<script>
    const data = {{ site.data.recommendations | jsonify }};
    const today = new Date().getDate(); // 使用日期作为索引，确保每日固定

    function showRecommend(type) {
        const box = document.getElementById('recommend-box');
        const content = document.getElementById('recommend-content');
        const tagBox = document.getElementById('rec-tags');
        const btn = document.getElementById('go-to-list');
        
        // 获取今日对应的推荐项
        const list = data[type];
        const item = list[today % list.length];

        // 切换动画效果
        box.style.opacity = '0';
        box.style.transform = 'translateY(10px)';

        setTimeout(() => {
            let html = `<h3 style="color: #d85a7f; margin-bottom: 10px;">今日 ${type.toUpperCase()} 推荐：${item.title}</h3>`;
            html += `<p style="line-height: 1.6; color: #555;">${item.desc}</p>`;
            content.innerHTML = html;

            // 处理 Anime 的特殊标签
            tagBox.innerHTML = '';
            if (item.tags) {
                item.tags.forEach(t => {
                    tagBox.innerHTML += `<span class="mini-tag">${t}</span>`;
                });
            }

            // 更新跳转按钮
            btn.href = `{{ site.baseurl }}/categories/${type}`;
            btn.style.display = 'inline-block';

            box.style.display = 'block';
            box.style.opacity = '1';
            box.style.transform = 'translateY(0)';
        }, 200);
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
    }
    .stat-card:hover { transform: translateY(-10px); background: white; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
    .stat-card h3 { margin: 0; font-size: 1.5em; }
    .stat-card p { margin: 5px 0 0; font-weight: bold; color: #777; font-size: 0.8em; }

    .recommend-box {
        margin-top: 40px;
        background: rgba(255,255,255,0.5);
        border-radius: 24px;
        padding: 25px;
        border: 1px dashed var(--primary-color);
        min-height: 120px;
        transition: all 0.5s ease;
        display: block; /* 初始显示默认提示 */
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
    .go-btn:hover { letter-spacing: 1px; }
</style>
