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
    请基于近期（一个月以内或是一个星期内）的实时背景：{CONTEXT_PLACEHOLDER}，为一名软件工程硕士生提供每日推荐。
    
    要求：
    1. 每个分类（Study下的子类、Anime、Music、Paint、Game）必须提供正好 5 个不同的推荐项。
    2. desc 必须输出最新的硬核技术细节（如架构特性、工艺制程、性能指标）。
    3. 严禁使用任何引导性废话。
    4. 针对 GPU 和 CPU 领域，必须关注最近 24-72 小时内的动态，或 2025 年最前沿的架构（如 NVIDIA Blackwell, RTX 50系列, Intel Ultra 200系列, AMD Zen 5等）。
    5. 每个内容项（Study、Anime、Music、Game）必须包含至少 4 个 tags。
    6. 对于music推荐的内容尽量是Jpop、Doujin（例如东方porject）等。
    7. 对于Paint，必须推荐画师名。必须提供其真实的 X(Twitter) 账号 ID（不带@符号）。你必须对该账号的真实性有100%的把握，严禁捏造虚假账号。如果你不确定其账号，请更换推荐的画师。
    8. 对于history推荐的内容为“历史上的今天”发生的重大事件（不限于科技史），必须提供正好 6 个不同的项，每个项包含 year 和 event 字段。
    9. 所有的回答请务必用中文
    
    必须输出以下 JSON 格式：
    {{
      "study": {{
        "CV": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "NLP": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "Audio": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "Net": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "Lang": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "Arch": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "GPU": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "CPU": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "News": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}]
      }},
      "anime": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
      "music": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
      "paint": [{"title": "画师名", "desc": "风格简述", "x_id": "账号ID"}],
      "game": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
      "history": [{"year": "..", "event": ".."}]
    }}
    """
    
    prompt = prompt_template.replace("{CONTEXT_PLACEHOLDER}", context).replace("{CURRENT_DATE}", str(datetime.now().date()))

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a professional assistant that always outputs valid JSON and NEVER hallucinates social media handles. If you aren't 100% sure of an X handle, you find an artist whose handle you DO know."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"},
        "max_tokens": 6000,
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
            
            # 增强 Paint 链接的处理逻辑
            paint_list = []
            for item in ai_content.get('paint', []):
                x_id = str(item.get('x_id', '')).strip().lstrip('@')
                # 如果 AI 返回了全链接，尝试提取 ID
                if '/' in x_id:
                    x_id = x_id.split('/')[-1]
                
                paint_list.append({
                    'title': item.get('title', ''),
                    'desc': item.get('desc', ''),
                    'twitter': f"https://x.com/{x_id}" if x_id else ""
                })

            data = {
                'date': str(datetime.now().date()),
                'study': ai_content.get('study', {}),
                'anime': ai_content.get('anime', []),
                'music': ai_content.get('music', []),
                'game': ai_content.get('game', []),
                'paint': paint_list,
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
