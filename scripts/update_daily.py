import yaml
import os
import json
import requests
import re
import sys
from datetime import datetime, timedelta

api_key = os.getenv("DEEPSEEK_API_KEY")
api_url = "https://api.deepseek.com/chat/completions"

def get_realtime_context():
    try:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        query = "created:>" + yesterday + " topic:ai"
        url = "https://api.github.com/search/repositories?q=" + query + "&sort=stars&order=desc&per_page=5"
        res = requests.get(url, timeout=5)
        repos = res.json().get('items', [])
        return ", ".join([r['full_name'] for r in repos])
    except:
        return ""

def clean_json_string(raw_str):
    json_str = re.sub(r'```json\s*|\s*```', '', raw_str).strip()
    return json_str

def get_ai_recommendation(context):
    if not api_key:
        return None

    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}

    prompt_template = """
    今天是 {CURRENT_DATE}。你是一个顶级硬件与人工智能专家。
    基于实时背景：{CONTEXT_PLACEHOLDER}，为软件工程硕士提供每日推荐。
    
    要求：
    1. 每个子类/分类必须提供正好 5 个项。
    2. desc 必须精炼硬核（100字内），严禁废话。
    3. 针对 GPU/CPU 关注 2025 年最新架构。
    4. 所有的回答请务必用中文。
    
    必须输出以下 JSON 格式：
    {{
      "study": {{
        "CV": [{"title": "..", "desc": ".."}],
        "NLP": [{"title": "..", "desc": ".."}],
        "Audio": [{"title": "..", "desc": ".."}],
        "Net": [{"title": "..", "desc": ".."}],
        "Lang": [{"title": "..", "desc": ".."}],
        "Arch": [{"title": "..", "desc": ".."}],
        "GPU": [{"title": "..", "desc": ".."}],
        "CPU": [{"title": "..", "desc": ".."}],
        "News": [{"title": "..", "desc": ".."}]
      }},
      "anime": [{"title": "..", "desc": "..", "tags": []}],
      "music": [{"title": "..", "desc": "..", "tags": []}],
      "paint": [{"title": "..", "desc": "..", "twitter": ".."}],
      "game": [{"title": "..", "desc": "..", "tags": []}],
      "history": [{"year": "..", "event": ".."}]
    }}
    """
    
    prompt = prompt_template.replace("{CONTEXT_PLACEHOLDER}", context).replace("{CURRENT_DATE}", str(datetime.now().date()))

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a professional assistant that always outputs valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"},
        "max_tokens": 4000,
        "temperature": 0.7
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error calling AI API: {e}")
        return None

def update_yaml():
    context = get_realtime_context()
    raw_content = get_ai_recommendation(context)
    if raw_content:
        try:
            cleaned_content = clean_json_string(raw_content)
            ai_content = json.loads(cleaned_content)
            
            data = {
                'date': str(datetime.now().date()),
                'study': ai_content.get('study', {}),
                'anime': ai_content.get('anime', []),
                'music': ai_content.get('music', []),
                'game': ai_content.get('game', []),
                'paint': ai_content.get('paint', []),
                'history': ai_content.get('history', [])
            }
            
            with open('_data/recommendations.yml', 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True)
            print("Successfully updated _data/recommendations.yml")
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            print(f"Raw content snippet: {raw_content[:500]} ... {raw_content[-500:]}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("Failed to get AI recommendation")
        sys.exit(1)

if __name__ == "__main__":
    update_yaml()
