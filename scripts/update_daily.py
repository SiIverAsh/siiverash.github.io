import yaml
import os
import json
import requests
from datetime import datetime, timedelta

api_key = os.getenv("DEEPSEEK_API_KEY")
api_url = "https://api.deepseek.com/chat/completions"

def get_realtime_context():
    try:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        query = f"created:>{yesterday} topic:ai"
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=5"
        res = requests.get(url, timeout=5)
        repos = res.json().get('items', [])
        return ", ".join([r['full_name'] for r in repos])
    except:
        return ""

def get_ai_recommendation(context):
    if not api_key:
        return None

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    # 修复：所有 JSON 格式的大括号都必须双写以进行转义
    prompt = f"""
    今日实时背景（{datetime.now().date()}）：{context}
    
    你是一个专业的个人博主助手。请为一名上海理工大学软件工程硕士生提供每日技术与艺术推荐。
    
    要求：
    1. 每个分类请提供 3 个不同的推荐项。
    2. desc 必须直接输出硬核知识点或评价，严禁使用引导性废话。
    3. Anime 部分：每个推荐项必须包含至少 5 个描述其属性或风格的 tags。
    4. Music 部分：每个推荐项必须包含至少 3 个描述其流派或情绪的 tags。
    5. Paint 部分：必须推荐知名画师，desc 描述其画风特点，并提供 twitter 字段（其推特/X 主页链接）。
    
    请严格按照以下 JSON 格式输出：
    {{
      "study": {{
        "CV": [{{ "title": "标题", "desc": "细节" }}],
        "NLP": [{{ "title": "标题", "desc": "细节" }}],
        "Audio": [{{ "title": "标题", "desc": "细节" }}],
        "Net": [{{ "title": "标题", "desc": "细节" }}],
        "Lang": [{{ "title": "标题", "desc": "细节" }}],
        "Arch": [{{ "title": "标题", "desc": "细节" }}],
        "News": [{{ "title": "标题", "desc": "细节" }}]
      }},
      "anime": [{{ "title": "动漫名", "desc": "理由", "tags": ["A", "B", "C", "D", "E"] }}],
      "music": [{{ "title": "歌名", "desc": "理由", "tags": ["A", "B", "C"] }}],
      "paint": [{{ "title": "画师名", "desc": "画风特点", "twitter": "链接" }}]
    }}
    """

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a professional tech and art assistant."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return None

def update_yaml():
    context = get_realtime_context()
    raw_content = get_ai_recommendation(context)
    if raw_content:
        ai_content = json.loads(raw_content)
        data = {
            'date': str(datetime.now().date()),
            'study': ai_content['study'],
            'anime': ai_content['anime'],
            'music': ai_content['music'],
            'paint': ai_content['paint']
        }
        with open('_data/recommendations.yml', 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True)

if __name__ == "__main__":
    update_yaml()
