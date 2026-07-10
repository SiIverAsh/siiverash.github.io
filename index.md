---
layout: default
title: Welcome to My HP!
---

<section class="home-intro">
    <h1>Welcome to My HP!</h1>
    <p class="home-subtitle">Attention Is All You Need!</p>
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
        animation: home-fade-up 0.7s ease both;
    }

    .home-intro h1 {
        color: var(--primary-color);
        margin: 0 0 12px;
        font-size: clamp(2rem, 4vw, 3rem);
        animation: home-title-in 0.8s cubic-bezier(.2,.8,.2,1) both;
    }

    .home-subtitle {
        color: var(--text-muted);
        font-size: 1.15rem;
        margin: 0;
        animation: home-fade-up 0.8s 0.12s ease both;
    }

    .home-section {
        margin-top: 30px;
        animation: home-fade-up 0.7s 0.2s ease both;
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
        transition: transform 0.25s ease, padding-left 0.25s ease, border-color 0.25s ease;
    }

    .latest-post:hover {
        transform: translateX(6px);
        padding-left: 8px;
        border-color: var(--primary-color);
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
        transition: transform 0.25s ease, color 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }

    .home-category:hover {
        color: var(--primary-color);
        border-color: var(--primary-color);
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(29, 80, 138, 0.14);
    }

    .home-category small {
        color: var(--text-muted);
    }

    @keyframes home-fade-up {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes home-title-in {
        from { opacity: 0; transform: translateY(12px) scale(0.97); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }

    .latest-post:nth-child(1) { animation: home-fade-up 0.5s 0.28s ease both; }
    .latest-post:nth-child(2) { animation: home-fade-up 0.5s 0.34s ease both; }
    .latest-post:nth-child(3) { animation: home-fade-up 0.5s 0.40s ease both; }
    .latest-post:nth-child(4) { animation: home-fade-up 0.5s 0.46s ease both; }
    .latest-post:nth-child(5) { animation: home-fade-up 0.5s 0.52s ease both; }
    .latest-post:nth-child(6) { animation: home-fade-up 0.5s 0.58s ease both; }
    .latest-post:nth-child(7) { animation: home-fade-up 0.5s 0.64s ease both; }
    .latest-post:nth-child(8) { animation: home-fade-up 0.5s 0.70s ease both; }

    .home-category:nth-child(1) { animation: home-fade-up 0.5s 0.30s ease both; }
    .home-category:nth-child(2) { animation: home-fade-up 0.5s 0.36s ease both; }
    .home-category:nth-child(3) { animation: home-fade-up 0.5s 0.42s ease both; }
    .home-category:nth-child(4) { animation: home-fade-up 0.5s 0.48s ease both; }
    .home-category:nth-child(5) { animation: home-fade-up 0.5s 0.54s ease both; }
    .home-category:nth-child(6) { animation: home-fade-up 0.5s 0.60s ease both; }
    .home-category:nth-child(7) { animation: home-fade-up 0.5s 0.66s ease both; }
    .home-category:nth-child(8) { animation: home-fade-up 0.5s 0.72s ease both; }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
    }

    @media (max-width: 600px) {
        .latest-post {
            grid-template-columns: 1fr;
            gap: 4px;
        }
    }
</style>
