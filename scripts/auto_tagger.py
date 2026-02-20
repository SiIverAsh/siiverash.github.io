import os
import json
import requests
import yaml
from datetime import datetime

# 配置 API
api_key = os.getenv("DEEPSEEK_API_KEY")
api_url = "https://api.deepseek.com/chat/completions"
posts_dir = "_posts"

def get_existing_tags():
    """收集库中所有已存在的标签，以便 AI 参考，减少标签碎片化"""
    all_tags = set()
    if not os.path.exists(posts_dir):
        return []
    for filename in os.listdir(posts_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(posts_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    front_matter = yaml.safe_load(parts[1])
                    tags = front_matter.get("tags")
                    if isinstance(tags, list):
                        for t in tags:
                            all_tags.add(t)
            except:
                continue
    return sorted(list(all_tags))

def get_tags_from_ai(title, content, existing_tags):
    if not api_key:
        print("Error: DEEPSEEK_API_KEY not found.")
        return []

    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}
    
    # 构建更智能的 Prompt，引导 AI 复用相似标签
    prompt = f"""
    你是一个专业的技术博客编辑。请根据以下文章的标题和内容，生成 3 到 5 个最相关的技术标签（Tags）。
    
    【重要要求】：
    1. 优先从下方的“已有标签列表”中选择含义相同或极度相似的词汇，以保持全站标签的一致性。
    2. 如果文章涉及新领域，可以创建新标签，但请确保简短（如：Windows, 深度学习, Python）。
    3. 只输出一个包含标签的 JSON 数组，格式为：["Tag1", "Tag2"]。
    4. 不要输出任何解释文字。

    已有标签列表：{", ".join(existing_tags) if existing_tags else "暂无"}

    文章标题：{title}
    文章内容摘要：{content[:1000]}
    """

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a senior editor responsible for tag normalization. You only output valid JSON arrays."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        res_json = response.json()
        content_str = res_json['choices'][0]['message']['content']
        data = json.loads(content_str)
        if isinstance(data, dict) and "tags" in data:
            return data["tags"]
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"AI Tagging Error for '{title}': {e}")
        return []

def process_posts():
    if not os.path.exists(posts_dir):
        print("Directory " + posts_dir + " not found.")
        return

    # 先获取全站已有标签作为上下文
    existing_tags = get_existing_tags()
    print(f"Total existing tags found: {len(existing_tags)}")

    for filename in os.listdir(posts_dir):
        if not filename.endswith(".md") or filename == "BLOG_TEMPLATE.md":
            continue
            
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = content.split('---', 2)
        if len(parts) < 3:
            continue

        front_matter_raw = parts[1]
        post_body = parts[2]
        
        try:
            front_matter = yaml.safe_load(front_matter_raw)
        except Exception as e:
            print(f"YAML Load Error in {filename}: {e}")
            continue

        needs_update = False
        
        # 逻辑 1：日期补全
        current_date_str = str(front_matter.get("date", ""))
        template_dates = ["2026-02-19 12:00:00", "2026-02-18 12:00:00", "None", ""]
        if not current_date_str or any(td in current_date_str for td in template_dates):
            new_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S +0800")
            front_matter["date"] = new_date
            print(f"Auto-filling date for {filename}: {new_date}")
            needs_update = True

        # 逻辑 2：生成/归纳相似标签
        # 即使已有标签，如果标签太乱，也可以在此处触发重写逻辑（当前设定为缺失才补全）
        if not front_matter.get("tags") or len(front_matter["tags"]) == 0:
            print(f"Analyzing and generating consistent tags for: {filename}...")
            title = front_matter.get("title", "")
            new_tags = get_tags_from_ai(title, post_body.strip(), existing_tags)
            if new_tags:
                front_matter["tags"] = new_tags
                # 更新 context 以便后续文章参考
                for t in new_tags:
                    if t not in existing_tags: existing_tags.append(t)
                needs_update = True

        if needs_update:
            # 使用 yaml.dump 保持格式整洁，allow_unicode 处理中文
            new_front_matter_str = yaml.dump(front_matter, allow_unicode=True, sort_keys=False).strip()
            new_content = "---\n" + new_front_matter_str + "\n---\n\n" + post_body.lstrip()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Successfully optimized {filename}")

if __name__ == "__main__":
    process_posts()
