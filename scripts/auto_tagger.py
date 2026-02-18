import os
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

    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}
    
    prompt = """
    你是一个专业的技术博客编辑。请根据以下文章的标题和内容，生成 3 到 5 个最相关的技术标签（Tags）。
    要求：
    1. 标签应为简短的中文或英文词汇（如：Windows, 深度学习, Python）。
    2. 只输出一个包含标签的 JSON 数组，例如：["Tag1", "Tag2", "Tag3"]。
    3. 不要输出任何解释文字。

    文章标题：{TITLE}
    文章内容摘要：{CONTENT}
    """
    # 使用 replace 避免 f-string 带来的转义问题
    final_prompt = prompt.replace("{TITLE}", title).replace("{CONTENT}", content[:1000])

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a professional assistant that only outputs pure JSON arrays."},
            {"role": "user", "content": final_prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        res_json = response.json()
        content_str = res_json['choices'][0]['message']['content']
        data = json.loads(content_str)
        if isinstance(data, dict) and "tags" in data:
            return data["tags"]
        return data if isinstance(data, list) else []
    except Exception as e:
        print("AI Tagging Error: " + str(e))
        return []

def process_posts():
    if not os.path.exists(posts_dir):
        print("Directory " + posts_dir + " not found.")
        return

    for filename in os.listdir(posts_dir):
        if not filename.endswith(".md"):
            continue
            
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用更稳健的分割方法替代正则表达式
        parts = content.split('---', 2)
        if len(parts) < 3:
            continue

        front_matter_raw = parts[1]
        post_body = parts[2]
        
        try:
            front_matter = yaml.safe_load(front_matter_raw)
        except Exception as e:
            print("YAML Load Error in " + filename + ": " + str(e))
            continue

        if front_matter.get("tags") and len(front_matter["tags"]) > 0:
            print("Skipping " + filename + ": Already has tags.")
            continue

        print("Generating tags for: " + filename + "...")
        title = front_matter.get("title", "")
        new_tags = get_tags_from_ai(title, post_body.strip())

        if new_tags:
            print("Found tags: " + str(new_tags))
            front_matter["tags"] = new_tags
            
            # 重新组合文件
            new_front_matter_str = yaml.dump(front_matter, allow_unicode=True).strip()
            new_content = "---\n" + new_front_matter_str + "\n---\n\n" + post_body.lstrip()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Successfully updated " + filename)

if __name__ == "__main__":
    process_posts()
