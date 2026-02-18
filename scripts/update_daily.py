import yaml
import os
import json
import requests
from datetime import datetime, timedelta

api_key = os.getenv("DEEPSEEK_API_KEY")
api_url = "https://api.deepseek.com/chat/completions"

def get_realtime_context():
    """仅抓取最核心的今日热门 AI 项目名，作为极简背景"""
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

    # 保持原有 Prompt 结构，仅在开头注入实时背景
    prompt = f"""
    今日实时背景（{datetime.now().date()}）：{context}
    
    你是一个专业的个人博主助手。请为一名上海理工大学软件工程硕士生提供每日技术推荐。
    
    要求：
    1. 描述（desc）必须直接输出硬核知识点或技术细节。
    2. 严禁使用“介绍一个...”、“推荐一款...”、“汇总一条...”、“本文介绍...”等任何引导性字眼。
    3. 风格应简洁、专业、直接，像技术文档一样。
    
    请严格按照以下 JSON 格式输出：
    {{
      "study": {{
        "CV": {{"title": "视觉技术名", "desc": "直接描述该技术的原理、优势或核心逻辑"}},
        "NLP": {{"title": "语言模型技术", "desc": "直接描述其架构特点或优化方案"}},
        "Audio": {{"title": "音频/声纹技术", "desc": "直接描述算法改进点或性能指标"}},
        "Net": {{"title": "网络/安全技术", "desc": "直接描述协议细节"}},
        "Lang": {{"title": "语言特性", "desc": "直接描述底层机制或新版特性"}},
        "Arch": {{"title": "架构模式", "desc": "直接描述其解决的痛点或设计要点"}},
        "News": {{"title": "AI 业界动态", "desc": "直接描述事件内容及行业影响"}}
      }},
      "anime": {{"title": "动漫名", "desc": "推荐理由", "tags": ["标签1", "标签2"]}},
      "music": {{"title": "歌名", "desc": "推荐理由"}},
      "paint": {{"title": "画师", "desc": "推特链接：，核心要领"}}
    }}
    """

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a professional tech assistant."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except:
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
