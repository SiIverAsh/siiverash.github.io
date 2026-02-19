import yaml
import os
import json
import requests
import re
import sys
import random
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

    # 引入随机种子强制模型变换推荐角度
    va_focus = [
        "今天请侧重推荐2015年后出道、目前人气极高的新锐/潜力声优。",
        "今天请侧重推荐1990-2005年间活跃的、拥有经典代表作的骨灰级/大牌声优。",
        "今天请侧重推荐擅长『冷酷反派』或『中性少年音』的特色型声优。",
        "今天请侧重推荐在『同人/广播剧/舞台剧』领域同样活跃的跨界声优。",
        "今天请侧重推荐出生于『东京都以外』且带有地方特色或独特声线的声优。"
    ]
    daily_focus = random.choice(va_focus)

    prompt_template = """
    今天是 {CURRENT_DATE}。你是一个全能的数字生活与技术博主，精通硬件、AI、动漫及二次元文化。你以输出信息的高准确性著称。
    请基于近期（一个月以内或是一个星期内）的实时背景：{CONTEXT_PLACEHOLDER}，为一名软件工程硕士生提供每日推荐。
    
    要求：
    1. 每个分类（Study下的 9 个指定子类、Anime、Music、Paint、Game）必须提供正好 2 个不同的推荐项。
    2. Study 下必须严格使用这 9 个键名：CV, NLP, Audio, Net, Lang, Arch, GPU, CPU, News。你必须根据实时背景将 GitHub 项目分类放入这些子类中。
    3. desc 必须输出最新的硬核技术细节（如架构特性、工艺制程、性能指标）。
    4. 严禁使用任何引导性废话。
    5. 针对 GPU 和 CPU 领域，必须关注最近一个月内的动态。
    6. 每个内容项（Study、Anime、Music、Game）必须包含至少 4 个 tags。
    7. 对于music推荐的内容尽量是Jpop、Doujin（例如东方porject）等。
    8. 对于Paint，画师不一定是知名的，可以推荐国内平台的画师，但是必须提供真实的画师链接（可以是X，也可以是微博等等）（不确定则留空）。
    9. 对于history推荐内容为“历史上的今天”，必须提供 6 条不同数据。
    10. **CV推荐**：
       - {DAILY_FOCUS}
       - 必须严格参考**《声优名鉴》(声優名鑑)**数据，推荐一位日本声优，每天都得推荐不同的声优，禁止一直推荐同一个。
       - **严禁**重复推荐花泽香菜、神谷浩史、悠木碧、早见沙织、宫野真守等过度知名的“常客”。
       - 必须包含：姓名(name)、所属事务所(agency)、出生地(hometown)、代表作(works)、以及一段基于名鉴风格的专业评价(intro,大约150字即可)。代表作如果你不知道可以不写，但是写出来的代表作一定要正确。
    11. 对于game推荐的内容尽量是近几年发行的游戏。
    12. 所有的回答请务必用中文。
    
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
      "paint": [{"title": "画师名", "desc": "风格简述", "id_url": "真实的账号链接"}],
      "game": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
      "history": [{"year": "..", "event": ".."}],
      "cv_recommend": {{
        "name": "声优名", 
        "agency": "所属事务所", 
        "hometown": "出生地",
        "works": "代表作", 
        "intro": "基于声优名鉴的风格化评价"
      }}
    }}
    """
    
    prompt = prompt_template.replace("{CONTEXT_PLACEHOLDER}", context).replace("{CURRENT_DATE}", str(datetime.now().date())).replace("{DAILY_FOCUS}", daily_focus)

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个全能的数字生活与技术博主，精通硬件、AI、动漫及二次元文化。你拒绝平庸，总是能挖掘出冷门但实力极强的技术、艺术和声优。"},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"},
        "max_tokens": 6000,
        "temperature": 1.3
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
            
            # 修正 Paint 处理逻辑，直接提取 ID/链接
            paint_list = []
            for item in ai_content.get('paint', []):
                paint_list.append({
                    'title': item.get('title', ''),
                    'desc': item.get('desc', ''),
                    'url': item.get('id_url', '')
                })

            data = {
                'date': str(datetime.now().date()),
                'study': ai_content.get('study', {}),
                'anime': ai_content.get('anime', []),
                'music': ai_content.get('music', []),
                'game': ai_content.get('game', []),
                'paint': paint_list,
                'history': ai_content.get('history', []),
                'cv_recommend': ai_content.get('cv_recommend', {})
            }
            
            with open('_data/recommendations.yml', 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True)
            print("Successfully updated _data/recommendations.yml")
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("Failed to get AI recommendation")
        sys.exit(1)

if __name__ == "__main__":
    update_yaml()
