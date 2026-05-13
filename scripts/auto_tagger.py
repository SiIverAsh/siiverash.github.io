import os
import json
import requests
import yaml
from datetime import datetime, timedelta, timezone

API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"
POSTS_DIR = "_posts"


def get_existing_tags():
    """读取已有的全部标签"""
    all_tags = set()
    if not os.path.exists(POSTS_DIR):
        return []

    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(POSTS_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    front_matter = yaml.safe_load(parts[1])
                    if not front_matter:
                        continue
                        
                    tags = front_matter.get("tags")
                    if isinstance(tags, list):
                        for t in tags:
                            all_tags.add(t)
            except Exception:
                continue

    return sorted(list(all_tags))


def get_tags_from_ai(title, content, category, existing_tags):
    """调用大模型为文章自动生成标签"""
    if not API_KEY:
        print("未检测到 DEEPSEEK_API_KEY，跳过 AI 打标签。")
        return []

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    role_map = {
        "study": "资深技术专家",
        "anime": "资深二次元漫评人",
        "music": "专业乐评人",
        "paint": "美术鉴赏家",
        "game": "骨灰级游戏玩家",
        "snap": "专业摄影师",
        "asmr": "ASMR深度体验者",
        "emo": "情感作家",
        "paper": "资深学术研究员"
    }
    role = role_map.get(category, "专业博客编辑")

    guidance = ""
    if category == "study":
        guidance = "这是一篇学习笔记。请侧重提取核心技术栈、框架、编程语言等专业词汇。"
    elif category == "anime":
        guidance = "这是一篇动漫相关博文。请务必提取作品名称作为首个标签，并提取核心角色、制作公司、类型题材（如机战、日常）等。"
    elif category == "music":
        guidance = "这是一篇音乐鉴赏。请提取歌手/社团/作者名、曲风、专辑名等。"
    elif category == "paint":
        guidance = "这是一篇绘画分享。请提取其中的人物名字、画师名、艺术风格、绘制工具等。"
    elif category == "game":
        guidance = "这是一篇游戏记录。请务必提取游戏名称作为首个标签，并提取游戏类型、核心机制或开发商等。"
    elif category == "snap":
        guidance = "这是一篇摄影作品。请提取相机型号、镜头焦段、拍摄地点、摄影风格等。"
    elif category == "asmr":
        guidance = "这是一篇助眠相关内容。请提取音声作者名、触发音类型（如耳语、心跳、底噪）、设备等。"
    elif category == "emo":
        guidance = "这是一篇心情随笔。请提取抽象的情感意象或核心感悟名词。"
    elif category == "paper":
        guidance = "这是一篇学术论文阅读笔记或研究总结。请务必提取论文的研究领域、核心算法、关键模型（如Transformer、CNN）、数据集名称等学术专业词汇。"

    prompt = f"""角色：{role}。
        任务：请仔细阅读以下文章内容，为其生成 3-5 个最核心、最准确的标签。
        分类指导：{guidance}
        严格要求：
            1. 尽可能复用现有标签库中的标签：{', '.join(existing_tags)}
            2. 标签必须是具体的专有名词（如人名、技术名、作品名、算法名），绝对禁止使用宽泛的形容词（如“好看的”、“好听的”）或长句！
            3. 必须以 JSON 对象格式返回，键名固定为 "tags"，值为字符串数组。

        文章标题：{title}
        内容摘要：{content[:3000]}"""

    payload = {
        "model": "deepseek-v4-flash",
        "messages": [
            {
                "role": "system",
                "content": 'You are a precise and professional tag extractor. You must reply ONLY with a valid JSON object containing a "tags" string array. Do not include markdown formatting like ```json.'
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        res = data['choices'][0]['message']['content']
        parsed = json.loads(res)
        
        tags = parsed.get("tags")
        if isinstance(tags, list):
            return tags
        elif isinstance(parsed, list):
            return parsed
        return []
    except Exception as e:
        print(f"Error calling AI: {e}")
        return []


def process_posts():
    """遍历文章目录并为缺失标签的文章补充标签"""
    if not os.path.exists(POSTS_DIR):
        print(f"文章目录 {POSTS_DIR} 不存在。")
        return

    existing_tags = get_existing_tags()

    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith(".md") or filename == "BLOG_TEMPLATE.md":
            continue

        filepath = os.path.join(POSTS_DIR, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            full_content = f.read()

        parts = full_content.split("---", 2)
        if len(parts) < 3:
            continue

        try:
            front_matter = yaml.safe_load(parts[1])
            post_body = parts[2]
        except Exception:
            continue

        if not front_matter or not front_matter.get("tags") or len(front_matter["tags"]) == 0:
            if not front_matter:
                front_matter = {}
                
            title = front_matter.get("title", "")
            categories = front_matter.get("categories", [])
            category = categories[0].lower() if categories else ""

            print(f"Intelligently tagging: {title}...")
            new_tags = get_tags_from_ai(title, post_body.strip(), category, existing_tags)
            
            if new_tags:
                front_matter["tags"] = new_tags
                
                
                yaml_content = yaml.dump(front_matter, allow_unicode=True, sort_keys=False).strip()
                new_content = f"---\n{yaml_content}\n---\n{post_body}"
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated tags for: {filename}")


if __name__ == "__main__":
    process_posts()