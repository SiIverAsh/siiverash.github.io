import os
import json
import requests
import yaml
from datetime import datetime, timedelta, timezone

API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"
POSTS_DIR = "_posts"

def get_existing_tags():
    all_tags = set()
    if not os.path.exists(POSTS_DIR): return []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(POSTS_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    front_matter = yaml.safe_load(parts[1])
                    tags = front_matter.get("tags")
                    if isinstance(tags, list):
                        for t in tags: all_tags.add(t)
            except: continue
    return sorted(list(all_tags))

def get_tags_from_ai(title, content, category, existing_tags):
    if not API_KEY: return []
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    
    guidance = ""
    if category == "study": guidance = "这是一篇学习笔记。请侧重提取技术领域词。"
    elif category == "anime": guidance = "这是一篇动漫相关博文。请务必提取作品名称作为首个标签、要根据该动漫的真实内容来提取其他标签。"
    elif category == "music": guidance = "这是一篇音乐鉴赏。请提取社团/作者名、曲风等。"
    elif category == "paint": guidance = "这是一篇绘画分享。请提取其中的人物、风格等。"
    elif category == "game": guidance = "这是一篇游戏记录。请务必提取游戏名称作为首个标签、要根据游戏的真实内容来提取其他标签。"
    elif category == "snap": guidance = "这是一篇摄影作品。请提取镜头焦段、拍摄地点等。"
    elif category == "asmr": guidance = "这是一篇助眠相关内容。请提取作者名等。"
    elif category == "emo": guidance = "这是一篇心情随笔。请提取情感意象或核心感悟。"

    prompt = f"角色：专业技术博客编辑。任务：为文章生成 3-5 个精准标签。\n分类背景：{guidance}\n要求：1. 可以复用已有标签：{', '.join(existing_tags)}\n2. 格式：JSON 数组。\n标题：{title}\n摘要：{content[:1000]}"

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are an intelligent tag generator. Output JSON arrays only."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        data = response.json()
        res = data['choices'][0]['message']['content']
        parsed = json.loads(res)
        return parsed["tags"] if isinstance(parsed, dict) and "tags" in parsed else parsed
    except: return []

def process_posts():
    if not os.path.exists(POSTS_DIR): return
    existing_tags = get_existing_tags()

    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith(".md") or filename == "BLOG_TEMPLATE.md": continue
        filepath = os.path.join(POSTS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            full_content = f.read()

        parts = full_content.split('---', 2)
        if len(parts) < 3: continue

        try:
            front_matter = yaml.safe_load(parts[1])
            post_body = parts[2]
        except: continue

        if not front_matter.get("tags") or len(front_matter["tags"]) == 0:
            title = front_matter.get("title", "")
            category = (front_matter.get("categories") or [""])[0].lower()

            print(f"Intelligently tagging: {title}...")
            new_tags = get_tags_from_ai(title, post_body.strip(), category, existing_tags)
            if new_tags:
                front_matter["tags"] = new_tags
                # 重新写入文件，保持日期原封不动
                new_content = f"---\n{yaml.dump(front_matter, allow_unicode=True, sort_keys=False).strip()}\n---\n{post_body}"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated tags for: {filename}")

if __name__ == "__main__":
    process_posts()
