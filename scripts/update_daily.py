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
    今天是 {CURRENT_DATE}。你是一个顶级硬件与人工智能专家。
    请基于近期（一个月以内或是一个星期内）的实时背景：{CONTEXT_PLACEHOLDER}，为一名软件工程硕士生提供每日推荐。
    
    要求：
    1. 每个分类必须提供正好 3 个不同的推荐项。
    2. desc 必须输出最新的硬核技术细节（如架构特性、工艺制程、性能指标）。
    3. 严禁使用任何引导性废话。
    4. 针对 GPU 和 CPU 领域，必须关注最近 24-72 小时内的动态，或 2025 年最前沿的架构（如 NVIDIA Blackwell, RTX 50系列, Intel Ultra 200系列, AMD Zen 5等）。
    5. Anime(至少5个tags)、Music(至少3个tags)、Game(至少5个tags)、Paint。
    6. 对于music推荐的内容尽量是Jpop、Doujin（例如东方porject）等，对于Paint，必须推荐画师，以及给出画师的x链接。
    7. 所有的回答请务必用中文
    
    必须输出以下 JSON 格式：
    {{
      "study": {{
        "CV": [{"title": "..", "desc": ".."}],
        "NLP": [{"title": "..", "desc": ".."}],
        "Audio": [{"title": "..", "desc": ".."}],
        "Net": [{"title": "..", "desc": ".."}],
        "Lang": [{"title": "..", "desc": ".."}],
        "Arch": [{"title": "..", "desc": ".."}],
        "GPU": [{"title": "..", "desc": "描述架构改进或性能对比"}],
        "CPU": [{"title": "..", "desc": "描述制程改进或指令集特性"}],
        "News": [{"title": "..", "desc": ".."}]
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
      ],
      "game": [
        {{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D", "E"]}},
        {{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D", "E"]}},
        {{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D", "E"]}}
      ]
    }}
    """
    
    prompt = prompt_template.replace("{CONTEXT_PLACEHOLDER}", context).replace("{CURRENT_DATE}", str(datetime.now().date()))

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a professional assistant."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
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
                'game': ai_content['game'],
                'paint': ai_content['paint'],
                'history': ai_content['history']
            }
            with open('_data/recommendations.yml', 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True)
        except:
            pass

if __name__ == "__main__":
    update_yaml()
