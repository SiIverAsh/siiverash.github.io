import os
import json
import requests
import yaml
from datetime import datetime

API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"
POSTS_DIR = "_posts"

def get_subject_from_ai(title: str, content: str, category: str):
    if not API_KEY:
        print("Error: DEEPSEEK_API_KEY not found.")
        return None

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    
    prompt = f"""
    角色：专业动漫博文编辑。
    任务：从以下文章中提取出讨论的核心【动漫作品全名】。
    
    分类背景：{category}
    文章标题：{title}
    文章片段：{content[:1000]}
    
    要求：
    1. 仅输出动漫作品的官方原名或通用中文译名（如：从“3D彼女观后感”提取为“3D彼女”）。
    2. 不要包含“观后感”、“漫评”、“评测”、“记录”等修饰词。
    3. 如果无法识别出明确的动漫名，请返回 null。
    4. 输出格式：必须仅输出 JSON，例如 {{"subject": "作品名"}}。
    """

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a precise entity extractor. Output JSON only."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        res_json = response.json()
        content_str = res_json['choices'][0]['message']['content']
        data = json.loads(content_str)
        return data.get("subject")
    except Exception as e:
        print(f"AI Extraction Error: {e}")
        return None

def process_posts():
    if not os.path.exists(POSTS_DIR): 
        print(f"Directory {POSTS_DIR} not found.")
        return

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

        # 仅针对 anime 
        categories = front_matter.get("categories", [])
        if not isinstance(categories, list): categories = [categories]
        
        if not categories and front_matter.get("category"):
            categories = [front_matter.get("category")]

        target_categories = ['anime']
        is_target = any(c.lower() in target_categories for c in categories if isinstance(c, str))

        if is_target and not front_matter.get("subject"):
            title = front_matter.get("title", "")
            # 取出匹配的第一个分类作为字符串传入
            category_str = next((c for c in categories if isinstance(c, str) and c.lower() in target_categories), "anime")
            print(f"Extracting anime subject for: {title}...")
            
            subject = get_subject_from_ai(title, post_body.strip(), category_str)
            if subject and subject != "null":
                front_matter["subject"] = subject
                new_content = f"---\n{yaml.dump(front_matter, allow_unicode=True, sort_keys=False).strip()}\n---\n\n{post_body.lstrip()}"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Successfully added subject: {subject} to {filename}")

if __name__ == "__main__":
    process_posts()
