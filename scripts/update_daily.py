import yaml
import os
import json
import requests
import re
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
    用中文回答
    今日实时背景：{CONTEXT_PLACEHOLDER}
    请作为专家助手为一名我提供每日推荐，对于study推荐的内容，必须很新，不能是很旧的内容，对于music推荐的内容尽量是Jpop、Doujin（例如东方porject）等，对于Paint，必须推荐画师，以及给出画师的x链接。
    
    要求：
    1. 每个分类/子领域必须提供正好 3 个不同的推荐项。
    2. desc 必须直接输出硬核技术细节或专业点评，严禁使用引导性废话。
    3. Anime(至少5个tags)、Music(至少3个tags)、Pain)。
    
    必须且仅输出以下 JSON 格式：
    {{
      "study": {{
        "CV": [{"title": "..", "desc": ".."}, {"title": "..", "desc": ".."}, {"title": "..", "desc": ".."}],
        "NLP": [{"title": "..", "desc": ".."}, {"title": "..", "desc": ".."}, {"title": "..", "desc": ".."}],
        "Audio": [{"title": "..", "desc": ".."}, {"title": "..", "desc": ".."}, {"title": "..", "desc": ".."}],
        "Net": [{"title": "..", "desc": ".."}, {"title": "..", "desc": ".."}, {"title": "..", "desc": ".."}],
        "Lang": [{"title": "..", "desc": ".."}, {"title": "..", "desc": ".."}, {"title": "..", "desc": ".."}],
        "Arch": [{"title": "..", "desc": ".."}, {"title": "..", "desc": ".."}, {"title": "..", "desc": ".."}],
        "News": [{"title": "..", "desc": ".."}, {"title": "..", "desc": ".."}, {"title": "..", "desc": ".."}]
      }},
      "anime": [
        {{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D", "E"]}},
        {{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D", "E"]}},
        {{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D", "E"]}}
      ],
      "music": [
        {{"title": "..", "desc": "..", "tags": ["A", "B", "C"]}},
        {{"title": "..", "desc": "..", "tags": ["A", "B", "C"]}},
        {{"title": "..", "desc": "..", "tags": ["A", "B", "C"]}}
      ],
      "paint": [
        {{"title": "..", "desc": "..", "twitter": ".."}},
        {{"title": "..", "desc": "..", "twitter": ".."}},
        {{"title": "..", "desc": "..", "twitter": ".."}}
      ]
    }}
    """
    
    prompt = prompt_template.replace("{CONTEXT_PLACEHOLDER}", context)

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a professional assistant that only outputs pure JSON data."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print("API Request Error: " + str(e))
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
                'study': ai_content['study'],
                'anime': ai_content['anime'],
                'music': ai_content['music'],
                'paint': ai_content['paint']
            }
            with open('_data/recommendations.yml', 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True)
            print("Successfully updated recommendations.yml")
        except Exception as e:
            print("JSON Parsing Error: " + str(e))
    else:
        print("Failed to get AI content.")

if __name__ == "__main__":
    update_yaml()
