import yaml
import os
import json
import requests
from datetime import datetime

api_key = os.getenv("DEEPSEEK_API_KEY")
api_url = "https://api.deepseek.com/chat/completions"

def get_ai_recommendation():
    if not api_key:
        return None

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    prompt = """
    你是一个专业的个人博主助手。请你仔细在网上搜索过之后再进行后面的动作，请为我提供每日推荐。
    
    请严格按照以下 JSON 格式输出：
    {
      "study": {
        "CV": {"title": "视觉相关", "desc": "介绍一个CV领域的SOTA模型或技巧"},
        "NLP": {"title": "语言处理", "desc": "介绍一个NLP或大模型相关技术，例如openAI发布了GPT-5.2"},
        "Net": {"title": "计网/架构", "desc": "介绍一个网络协议或分布式系统知识"}
      },
      "anime": {"title": "动漫名", "desc": "推荐理由", "tags": ["标签1", "标签2", "标签3", "标签4", "标签5"]},
      "music": {"title": "歌名/歌手/风格(这里请你主要推荐日本同人音乐，例如东方project、M3同人音乐等))", "desc": "推荐理由"},
      "paint": {"title": "画师/风格", "desc": "画师推特链接，推荐理由"}
    }
    """

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that outputs only JSON."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"},
        "stream": False
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except:
        return None

def update_yaml():
    raw_content = get_ai_recommendation()
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
