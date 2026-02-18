import yaml
import random
import requests
from datetime import datetime

# 模拟 AI 生成的内容
def fetch_anime():
    try:
        # 调用 Jikan API 获取随机动漫
        res = requests.get('https://api.jikan.moe/v4/random/anime')
        anime = res.json()['data']
        return {
            'title': anime['title'],
            'desc': anime.get('synopsis', '暂无简介')[:150] + '...',
            'tags': [g['name'] for g in anime.get('genres', [])][:3],
            'url': anime.get('url', '#')
        }
    except:
        return {'title': '命运石之门', 'desc': '一切都是命运石之门的选择！', 'tags': ['神作']}

def fetch_tech():
    try:
        # 模拟获取每日技术趋势（这里使用简单的随机）
        tech_topics = [
            {'title': 'LangChain', 'desc': '构建大模型应用的最佳框架，支持 Chain、Agent 等多种模式。'},
            {'title': 'Rust', 'desc': '内存安全的系统级编程语言，正在改写操作系统的未来。'},
            {'title': 'Svelte', 'desc': '无虚拟 DOM 的前端框架，极致的轻量化与高性能。'}
        ]
        return random.choice(tech_topics)
    except:
        return {'title': 'Python', 'desc': '人生苦短，我用 Python。'}

def update_yaml():
    data = {
        'date': str(datetime.now().date()),
        'study': [fetch_tech()],
        'anime': [fetch_anime()],
        'music': [{'title': '随机推荐', 'desc': '今日心情 BGM'}],
        'paint': [{'title': '每日色彩', 'desc': '#FFB7C5 樱花粉'}]
    }

    with open('_data/recommendations.yml', 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)

if __name__ == "__main__":
    update_yaml()
