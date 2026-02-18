---
layout: default
title: Welcome to My HP!
---

<div style="text-align: center; padding: 10px 0;">
    <h1 style="font-size: 2.5em; color: #d85a7f; margin-bottom: 20px;">Welcome to My HP!</h1>
    
    <p style="font-size: 1.1em; line-height: 1.8;">
    Attention Is All You Need!
    </p>

    <!-- 交互卡片区 -->
    <div style="margin-top: 30px; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
        <div class="stat-card" onclick="handleStudyClick()"><h3>📚</h3><p>Study</p></div>
        <div class="stat-card" onclick="handleClick('anime')"><h3>🌸</h3><p>Anime</p></div>
        <div class="stat-card" onclick="handleClick('music')"><h3>🎵</h3><p>Music</p></div>
        <div class="stat-card" onclick="handleClick('paint')"><h3>🎨</h3><p>Paint</p></div>
        <div class="stat-card" onclick="handleClick('game')"><h3>🎮</h3><p>Game</p></div>
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
        
        <!-- 外部链接按钮 -->
        <div id="external-link-area" style="display: none; margin-top: 15px;">
            <a id="external-link" href="#" target="_blank" class="twitter-btn">关注画师 𝕏</a>
        </div>
        
        <!-- 重新推荐按钮 -->
        <div id="refresh-parent" style="display: none; margin-top: 20px;">
            <button onclick="reRecommend()" class="refresh-btn">
                换一个 🔄
            </button>
        </div>
    </div>
</div>

<script>
    const dailyData = {{ site.data.recommendations | jsonify }} || {};
    let currentType = '';
    let currentSubType = '';
    let lastIndex = -1;

    function handleStudyClick() {
        currentType = 'study';
        currentSubType = ''; // 重置子类型
        document.getElementById('sub-tags-area').style.display = 'block';
        document.getElementById('recommend-content').innerHTML = '<p style="color: #d85a7f; font-weight: bold;">请选择一个研究领域 💡</p>';
        document.getElementById('rec-tags').innerHTML = '';
        document.getElementById('refresh-parent').style.display = 'none'; // 关键：隐藏按钮
        document.getElementById('external-link-area').style.display = 'none';
    }

    function showStudyDetail(subType) {
        currentSubType = subType;
        const list = dailyData.study ? dailyData.study[subType] : null;
        if (list && Array.isArray(list)) {
            const item = list[0]; 
            lastIndex = 0; // 同步索引
            updateUI(subType, item.title, item.desc, [], null);
        }
    }

    function handleClick(type) {
        currentType = type;
        currentSubType = '';
        document.getElementById('sub-tags-area').style.display = 'none';
        const list = dailyData[type];
        if (list && Array.isArray(list)) {
            const item = list[0]; 
            lastIndex = 0; // 同步索引
            updateUI(type.toUpperCase(), item.title, item.desc, item.tags || [], item.twitter || null);
        }
    }

    function getNextIndex(length) {
        if (length <= 1) return 0;
        let newIndex = Math.floor(Math.random() * length);
        while (newIndex === lastIndex) {
            newIndex = Math.floor(Math.random() * length);
        }
        lastIndex = newIndex;
        return newIndex;
    }

    function reRecommend() {
        const btn = document.querySelector('.refresh-btn');
        btn.style.transform = 'rotate(360deg)';
        
        setTimeout(() => {
            if (currentType === 'study' && currentSubType) {
                const list = dailyData.study[currentSubType];
                const index = getNextIndex(list.length);
                const item = list[index];
                updateUI(currentSubType, item.title, item.desc, [], null);
            } else if (currentType) {
                const list = dailyData[currentType];
                const index = getNextIndex(list.length);
                const item = list[index];
                updateUI(currentType.toUpperCase(), item.title, item.desc, item.tags || [], item.twitter || null);
            }
            btn.style.transform = 'rotate(0deg)';
        }, 300);
    }

    function updateUI(categoryLabel, title, desc, tags, twitterUrl) {
        const content = document.getElementById('recommend-content');
        const tagBox = document.getElementById('rec-tags');
        const refreshParent = document.getElementById('refresh-parent');
        const linkArea = document.getElementById('external-link-area');
        const link = document.getElementById('external-link');
        
        content.innerHTML = `<h3 style="color: #d85a7f; margin-bottom: 10px;">${categoryLabel}：${title}</h3><p style="line-height: 1.6; color: #555; font-size: 0.95em;">${desc}</p>`;
        
        tagBox.innerHTML = '';
        if (tags && tags.length > 0) {
            tags.forEach(t => {
                tagBox.innerHTML += `<span class="mini-tag">${t}</span>`;
            });
        }

        if (twitterUrl) {
            link.href = twitterUrl;
            linkArea.style.display = 'block';
        } else {
            linkArea.style.display = 'none';
        }

        refreshParent.style.display = 'block';
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

    .refresh-btn {
        background: white; border: 1px solid var(--primary-color);
        color: #d85a7f; padding: 5px 15px; border-radius: 20px;
        font-size: 0.85em; cursor: pointer; transition: transform 0.5s ease;
        font-weight: bold;
    }
    .refresh-btn:hover { background: var(--primary-color); color: white; }

    .twitter-btn {
        display: inline-block; background: #1da1f2; color: white;
        padding: 6px 15px; border-radius: 15px; text-decoration: none;
        font-size: 0.85em; font-weight: bold; transition: 0.3s;
    }
    .twitter-btn:hover { background: #0c85d0; transform: scale(1.05); }

    .mini-tag {
        display: inline-block; background: #fef0f3; color: #d85a7f;
        padding: 2px 10px; border-radius: 10px; font-size: 0.75em;
        margin: 5px; border: 1px solid var(--primary-color);
    }
</style>
