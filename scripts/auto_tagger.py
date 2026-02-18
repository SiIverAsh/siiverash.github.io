import os
import re
import json
import requests
import yaml

# 配置 API
api_key = os.getenv("DEEPSEEK_API_KEY")
api_url = "https://api.deepseek.com/chat/completions"
posts_dir = "_posts"

def get_tags_from_ai(title, content):
    if not api_key:
        print("Error: DEEPSEEK_API_KEY not found.")
        return []

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    
    # 构造 Prompt，让 AI 根据文章内容生成标签
    prompt = f"""
    你是一个专业的技术博客编辑。请根据以下文章的标题和内容，生成 3 到 5 个最相关的技术标签（Tags）。
    要求：
    1. 标签应为简短的中文或英文词汇（如：Windows, 深度学习, Python）。
    2. 只输出一个包含标签的 JSON 数组，例如：["Tag1", "Tag2", "Tag3"]。
    3. 不要输出任何解释文字。

    文章标题：{title}
    文章内容摘要：{content[:1000]} 
    """

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        res_json = response.json()
        content_str = res_json['choices'][0]['message']['content']
        # 兼容处理：有些模型可能返回 {"tags": [...]} 或直接是 [...]
        data = json.loads(content_str)
        if isinstance(data, dict) and "tags" in data:
            return data["tags"]
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"AI Tagging Error: {e}")
        return []

def process_posts():
    for filename in os.listdir(posts_dir):
        if not filename.endswith(".md"):
            continue
            
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 提取 Front Matter (两个 --- 之间的内容)
        content_str = "".join(lines)
        match = re.match(r'^---\s*
(.*?)
---\s*
(.*)', content_str, re.DOTALL)
        
        if not match:
            continue

        front_matter_raw = match.group(1)
        post_body = match.group(2)
        
        try:
            front_matter = yaml.safe_load(front_matter_raw)
        except:
            continue

        # 如果文章已经有标签了，跳过（或者你想强制更新也可以改这里）
        if front_matter.get("tags") and len(front_matter["tags"]) > 0:
            print(f"Skipping {filename}: Already has tags.")
            continue

        print(f"Generating tags for: {filename}...")
        title = front_matter.get("title", "")
        new_tags = get_tags_from_ai(title, post_body)

        if new_tags:
            print(f"Found tags: {new_tags}")
            front_matter["tags"] = new_tags
            
            # 将更新后的 Front Matter 写回文件
            new_front_matter_str = yaml.dump(front_matter, allow_unicode=True).strip()
            new_content = f"---
{new_front_matter_str}
---

{post_body.strip()}
"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Successfully updated {filename}")

if __name__ == "__main__":
    if not os.path.exists(posts_dir):
        print(f"Directory {posts_dir} not found.")
    else:
        process_posts()
