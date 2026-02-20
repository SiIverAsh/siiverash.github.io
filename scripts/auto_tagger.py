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
    """
    Collect all existing tags from current posts to maintain consistency and avoid fragmentation.
    """
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
                        for t in tags:
                            all_tags.add(t)
            except:
                continue
    return sorted(list(all_tags))

def get_tags_from_ai(title, content, existing_tags):
    """
    Use DeepSeek AI to generate 3-5 relevant tags, prioritizing existing tags for normalization.
    """
    if not API_KEY:
        print("Error: DEEPSEEK_API_KEY environment variable not found.")
        return []

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    
    prompt = f"""
    Role: Professional Tech Blog Editor.
    Task: Generate 3-5 tags for the post below.
    
    Constraints:
    1. PRIORITIZE selecting tags from the 'Existing Tags' list to ensure consistency.
    2. Create new tags only if the topic is new.
    3. Output ONLY a JSON array: ["Tag1", "Tag2"].
    4. Language: Simplified Chinese or English.

    Existing Tags: {", ".join(existing_tags) if existing_tags else "None"}
    Title: {title}
    Content Summary: {content[:1000]}
    """

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a senior editor for tag normalization. Output JSON arrays only."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        res_json = response.json()
        content_str = res_json['choices'][0]['message']['content']
        data = json.loads(content_str)
        if isinstance(data, dict) and "tags" in data:
            return data["tags"]
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"AI Tagging Error for post '{title}': {e}")
        return []

def process_posts():
    """
    Main loop to auto-fill dates and generate/normalize tags for markdown posts.
    """
    if not os.path.exists(POSTS_DIR):
        print(f"Directory '{POSTS_DIR}' not found.")
        return

    existing_tags = get_existing_tags()
    print(f"Found {len(existing_tags)} unique existing tags.")

    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith(".md") or filename == "BLOG_TEMPLATE.md":
            continue
            
        filepath = os.path.join(POSTS_DIR, filename)
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
            print(f"YAML parsing error in {filename}: {e}")
            continue

        needs_update = False
        
        # 1. Date Correction
        current_date_str = str(front_matter.get("date", ""))
        template_placeholders = ["2026-02-19 12:00:00", "2026-02-18 12:00:00", "None", ""]
        if not current_date_str or any(tp in current_date_str for tp in template_placeholders):
            new_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S +0800")
            front_matter["date"] = new_date
            needs_update = True

        # 2. Tag Generation/Normalization
        if not front_matter.get("tags") or len(front_matter["tags"]) == 0:
            title = front_matter.get("title", "")
            new_tags = get_tags_from_ai(title, post_body.strip(), existing_tags)
            if new_tags:
                front_matter["tags"] = new_tags
                for t in new_tags:
                    if t not in existing_tags: existing_tags.append(t)
                needs_update = True

        if needs_update:
            new_front_matter = yaml.dump(front_matter, allow_unicode=True, sort_keys=False).strip()
            updated_content = f"---\n{new_front_matter}\n---\n\n{post_body.lstrip()}"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Post optimized: {filename}")

if __name__ == "__main__":
    process_posts()
