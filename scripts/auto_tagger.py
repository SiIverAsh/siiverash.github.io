import os
import json
import requests
import yaml
from datetime import datetime

# DeepSeek API Configuration
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"
POSTS_DIR = "_posts"

def get_existing_tags():
    """收集全站已有标签，确保 AI 优先复用"""
    all_tags = set()
    if not os.path.exists(POSTS_DIR):
        return []
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
            except:
                continue
    return sorted(list(all_tags))

def get_tags_from_ai(title, content, category, existing_tags):
    """
    根据分类进行智能思考：
    - Study: 侧重技术领域与底层原理 (网络, 架构, 并发)
    - Anime/Music: 侧重作品实体名、声优、画师等
    """
    if not API_KEY:
        print("Error: DEEPSEEK_API_KEY not found.")
        return []

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    
    # 针对不同分类注入特定的引导逻辑，帮助 AI 智能思考
    guidance = ""
    if category == "study":
        guidance = "这是一篇学习笔记。请侧重提取技术领域词（如：计算机网络、系统架构、深度学习、算法优化）。"
    elif category == "anime":
        guidance = "这是一篇动漫相关博文。请【务必】提取作品名称作为首个标签，并增加动漫类型等标签。"
    elif category == "music":
        guidance = "这是一篇音乐鉴赏。请提取社团/作者名、曲风（如：同人音乐、电音、流行等等）。"
    elif category == "paint":
        guidance = "这是一篇绘画/涂鸦分享。请提取其中的人物，风格。"
    elif category == "game":
        guidance = "这是一篇游戏记录。请【务必】提取游戏名称作为首个标签，并增加平台（如：PC, PS5, Steam）、类型（如：FPS, RPG）或成就心得。"
    elif category == "snap":
        guidance = "这是一篇摄影作品。请提取镜头焦段、拍摄地点或后期风格。"
    elif category == "asmr":
        guidance = "这是一篇助眠/ASMR相关内容。请提取作者名。"
    elif category == "emo":
        guidance = "这是一篇深夜心情随笔。请提取情感意象（如：怀旧, 迷茫, 宁静）或核心感悟。"

    prompt = f"""
    角色：专业技术博客编辑。
    任务：为下述文章生成 3-5 个精准标签。
    
    分类背景：{guidance}
    
    要求：
    1. 优先从已有标签中选取相似词：{", ".join(existing_tags) if existing_tags else "无"}
    2. 标签格式：简洁的中文或英文。
    3. 输出：必须仅输出 JSON 数组，例如 ["网络", "路由转发", "Linux"]。

    标题：{title}
    摘要：{content[:1000]}
    """

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are an intelligent tag generator that adapts strategy based on category. Output JSON arrays only."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        res_json = response.json()
        content_str = res_json['choices'][0]['message']['content']
        data = json.loads(content_str)
        return data["tags"] if isinstance(data, dict) and "tags" in data else (data if isinstance(data, list) else [])
    except Exception as e:
        print(f"AI Tagging Error: {e}")
        return []

def process_posts():
    if not os.path.exists(POSTS_DIR): return
    existing_tags = get_existing_tags()

    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith(".md") or filename == "BLOG_TEMPLATE.md": continue
            
        filepath = os.path.join(POSTS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = content.split('---', 2)
        if len(parts) < 3: continue

        try:
            front_matter = yaml.safe_load(parts[1])
            post_body = parts[2]
        except: continue

        needs_update = False
        
        # 逻辑 1：智能日期补全（自动打上“上传时间”）
        current_date_str = str(front_matter.get("date", ""))
        # 识别占位符：UPLOAD_TIME (旧), 2026-01-01 (新模板)
        placeholders = ["UPLOAD_TIME", "2026-01-01 00:00:00", "None", ""]
        
        should_update_date = False
        if not current_date_str or any(p in current_date_str for p in placeholders):
            should_update_date = True
        
        if should_update_date:
            new_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S +0800")
            front_matter["date"] = new_date
            print(f"Set upload time for {filename}: {new_date}")
            needs_update = True

        # 智能标签逻辑：仅在缺失标签时触发
        if not front_matter.get("tags") or len(front_matter["tags"]) == 0:
            title = front_matter.get("title", "")
            # 获取文章的第一个分类
            category = ""
            if front_matter.get("categories"):
                category = front_matter["categories"][0].lower()
            elif front_matter.get("category"):
                category = front_matter["category"].lower()

            print(f"Intelligently tagging [{category}] post: {title}...")
            new_tags = get_tags_from_ai(title, post_body.strip(), category, existing_tags)
            if new_tags:
                front_matter["tags"] = new_tags
                needs_update = True

        if needs_update:
            new_content = f"---\n{yaml.dump(front_matter, allow_unicode=True, sort_keys=False).strip()}\n---\n\n{post_body.lstrip()}"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {filename}")

if __name__ == "__main__":
    process_posts()
