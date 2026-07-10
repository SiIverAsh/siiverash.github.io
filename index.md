---
layout: default
title: Welcome to My HP!
---

<section class="home-intro">
    <h1>Welcome to My HP!</h1>
    <p class="home-subtitle">Attention Is All You Need!</p>
    <p class="home-description">
        这里记录关于 LLM、ASR、算法与编程的学习，也分享动漫、音乐、游戏和摄影。
    </p>
</section>

<section class="home-section">
    <div class="home-section-title">最新文章</div>
    <div class="latest-posts">
        {% for post in site.posts limit: 8 %}
        <article class="latest-post">
            <div class="latest-post-meta">{{ post.date | date: "%Y-%m-%d" }}</div>
            <div>
                <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
                {% if post.categories.size > 0 %}
                <div class="latest-post-category">{{ post.categories | join: " · " }}</div>
                {% endif %}
            </div>
        </article>
        {% endfor %}
    </div>
</section>

<section class="home-section">
    <div class="home-section-title">文章分类</div>
    <div class="home-categories">
        {% for category in site.categories %}
        <a href="{{ "/categories/" | append: category[0] | append: "/" | relative_url }}" class="home-category">
            <span>{{ category[0] }}</span>
            <small>{{ category[1].size }} 篇</small>
        </a>
        {% endfor %}
    </div>
</section>

<style>
    .home-intro {
        padding: 28px 10px 36px;
        text-align: center;
    }

    .home-intro h1 {
        color: var(--primary-color);
        margin: 0 0 12px;
        font-size: clamp(2rem, 4vw, 3rem);
    }

    .home-subtitle {
        color: var(--text-muted);
        font-size: 1.15rem;
        margin: 0;
    }

    .home-description {
        max-width: 620px;
        margin: 20px auto 0;
        color: var(--text-main);
        line-height: 1.9;
    }

    .home-section {
        margin-top: 30px;
    }

    .home-section-title {
        color: var(--primary-color);
        border-left: 4px solid var(--primary-color);
        padding-left: 12px;
        margin-bottom: 16px;
        font-size: 1.25rem;
        font-weight: bold;
    }

    .latest-posts {
        display: grid;
        gap: 10px;
    }

    .latest-post {
        display: grid;
        grid-template-columns: 110px 1fr;
        gap: 16px;
        align-items: baseline;
        padding: 13px 0;
        border-bottom: 1px solid var(--glass-border);
    }

    .latest-post-meta,
    .latest-post-category {
        color: var(--text-muted);
        font-size: 0.85rem;
    }

    .latest-post h2 {
        margin: 0;
        font-size: 1.05rem;
    }

    .latest-post h2 a {
        color: var(--text-main);
        text-decoration: none;
    }

    .latest-post h2 a:hover {
        color: var(--primary-color);
    }

    .home-category {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin: 0 8px 10px 0;
        padding: 8px 12px;
        color: var(--text-main);
        border: 1px solid var(--glass-border);
        text-decoration: none;
    }

    .home-category:hover {
        color: var(--primary-color);
        border-color: var(--primary-color);
    }

    .home-category small {
        color: var(--text-muted);
    }

    @media (max-width: 600px) {
        .latest-post {
            grid-template-columns: 1fr;
            gap: 4px;
        }
    }
</style>
