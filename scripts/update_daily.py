import yaml
import os
import json
import requests
import re
import sys
import random
from datetime import datetime, timedelta, timezone
from openai import OpenAI
from typing import List, Dict, Any, cast, Iterable
from openai.types.chat import ChatCompletionToolParam, ChatCompletionMessageParam

api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# Exa API 配置 (原 Metaphor)
EXA_API_KEY = os.getenv("EXA_API_KEY")

client = OpenAI(api_key=api_key, base_url=base_url)

def get_beijing_time():
    """获取北京时间 (UTC+8)"""
    return datetime.now(timezone(timedelta(hours=8)))

def web_search(query: str):
    """
    使用 Exa AI (原 Metaphor) 进行语义搜索。
    Exa 会自动解析网页最相关的片段 (highlights)，并过滤垃圾信息。
    """
    print(f"🔍 正在执行 Exa 语义搜索: {query}...")
    if not EXA_API_KEY:
        return "错误：未配置 EXA_API_KEY 环境变量。请在 GitHub Secrets 中添加该密钥。"

    try:
        url = "https://api.exa.ai/search"
        headers = {
            "x-api-key": EXA_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "query": query,
            "useAutoprompt": True, # 自动优化用户的搜索提问
            "numResults": 3,       # 返回前 3 条最相关的结果
            "highlights": {        # 获取网页中与搜索词最匹配的文字片段
                "numSentences": 5  # 每个片段包含 5 句话，确保上下文丰富
            }
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=15)
        response.raise_for_status()
        results = response.json().get("results", [])

        if not results:
            return f"Exa 未能找到关于 '{query}' 的深度信息。"
        
        # 格式化搜索结果
        search_context = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "无标题")
            url_link = r.get("url", "无链接")
            # 提取高亮片段 
            highlights = r.get("highlights", [])
            snippet = "\n".join(highlights) if highlights else "无法提取文字片段，请直接访问链接。"
            
            search_context.append(f"[{i}] 标题: {title}\n摘要片段: {snippet}\n链接: {url_link}")
        
        return "\n\n".join(search_context)
    except Exception as e:
        print(f"Exa 搜索发生错误: {e}")
        return f"Exa 搜索失败: {e}。请基于你已有的知识库回答。"

# 定义工具元数据
tools: list[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "当需要核实或获取任何分类（包括但不限于硬件参数、AI技术细节、声优代表作、画师社交账号链接、游戏发行信息、音乐社团、历史真实事件等）的实时准确信息时调用。该工具用于彻底消除幻觉，确保所有输出内容与客观事实完全一致。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "针对待核实内容的具体搜索关键词。应包含具体的实体名称、年份或版本号（例如：'RTX 5090 规格参数'、'声优 羊宫妃那 2024 角色'、'画师 米山舞 X/Twitter 链接'）。"}
                },
                "required": ["query"]
            },
        }
    }
]

TOOL_MAP = {"web_search": web_search}

def get_realtime_context():
    try:
        yesterday = (get_beijing_time() - timedelta(days=1)).strftime('%Y-%m-%d')
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

def clear_reasoning_content(messages):
    for message in messages:
        if hasattr(message, 'reasoning_content'):
            message.reasoning_content = None
        elif isinstance(message, dict) and 'reasoning_content' in message:
            message['reasoning_content'] = None

def get_ai_recommendation(context):
    if not api_key:
        return None

    # va_focus = [
    #     "今天请侧重推荐2015年后出道、目前人气极高的新锐/潜力声优。",
    #     "今天请侧重推荐1990-2005年间活跃的、拥有经典代表作的骨灰级/大牌声优。",
    #     "今天请侧重推荐擅长『冷酷反派』或『中性少年音』的特色型声优。",
    #     "今天请侧重推荐在『同人/广播剧/舞台剧』领域同样活跃的跨界声优。",
    #     "今天请侧重推荐出生于『东京都以外』且带有地方特色或独特声线的声优。"
    # ]
    # daily_focus = random.choice(va_focus)

    prompt_template = """
    Please think carefully, lowely and accurately.
    今天是 {CURRENT_DATE}。你是一个全能的数字生活与技术博主，精通硬件、AI、动漫及二次元文化。你以输出信息的高准确性著称。
    请基于（三个月、一个月以内）近期真实背景：{CONTEXT_PLACEHOLDER}，为一名软件工程硕士生提供每日推荐。
    
    要求：
    1. 每个分类（Study下的 9 个指定子类、Anime、Music、Paint、Game）必须提供正好 1 个推荐项。
    2. Study 下必须严格使用这 9 个键名：CV, NLP, Audio, Net, Lang, Arch, GPU, CPU, News。你必须根据实时背景（例如github上的最新项目等）。
    3. desc 必须输出最新的硬核技术细节（如架构特性、工艺制程、性能指标）。
    4. 严禁使用任何引导性废话。
    5. 针对 GPU 和 CPU 领域，必须关注最近半年内的动态。
    6. 每个内容项（Study、Anime、Music、Game）必须包含至少 4 个 tags。
    7. 对于music推荐的内容尽量是Jpop、Doujin（例如东方porject）等。
    8. 对于Paint，画师不一定是知名的，可以推荐国内平台的画师，但是必须提供真实的画师链接（可以是X，也可以是微博等等）（不确定则留空）。
    9. 对于history推荐内容为“历史上的今天”，必须提供 6 条不同数据。
    10. **CV推荐**：
       - 必须严格参考**《声优名鉴》(声優名鑑)**数据。
       - 必须包含：姓名(name)、所属事务所(agency)、出生地(hometown)、以及一段专业评价(intro,大约150字)。
       - **强制事实对齐**：如果搜索结果没提到，宁可不写，也不准编造。
       - **严禁提及**：绝对禁止提及任何具体的动漫作品或角色名称。
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
        "intro": "基于真实数据进行评价，若数据不足宁缺毋滥，严禁编造"
      }}
    }}
    """
    
    prompt = prompt_template.replace("{CONTEXT_PLACEHOLDER}", context).replace("{CURRENT_DATE}", str(get_beijing_time().date()))
    # prompt = prompt_template.replace("{CONTEXT_PLACEHOLDER}", context).replace("{CURRENT_DATE}", str(get_beijing_time().date())).replace("{DAILY_FOCUS}", daily_focus)
    messages: List[ChatCompletionMessageParam] = [
        {"role": "system", "content": "你是一个全能的数字生活与技术博主，精通硬件、AI、动漫及二次元文化。你拒绝平庸，在面临不确定的技术细节（如未发布的显卡）或声优作品时，必须使用 web_search 工具进行核实，以确保 100% 的准确性。"},
        {"role": "user", "content": prompt}
    ]

    sub_turn = 1
    while True:
        try:
            # 包含完整的 reasoning_content
            response = client.chat.completions.create(
                model='deepseek-chat', 
                messages=messages,
                tools=tools,
                response_format={"type": "json_object"},
                extra_body={ "thinking": { "type": "enabled" } } 
            )
            
            message = response.choices[0].message
            # 手动补全 reasoning_content 并存入历史消息
            msg_dict = message.model_dump()
            reasoning = getattr(message, 'reasoning_content', None)
            if reasoning:
                msg_dict['reasoning_content'] = reasoning
            
            messages.append(cast(ChatCompletionMessageParam, msg_dict))

            if reasoning:
                print(f"--- AI Thinking (Turn {sub_turn}) ---\n{reasoning}\n")

            tool_calls = message.tool_calls
            if not tool_calls:
                return message.content

            # 处理工具调用
            for tool in tool_calls:
                if tool.type == 'function':
                    tool_name = tool.function.name
                    tool_args = json.loads(tool.function.arguments)
                    tool_func = TOOL_MAP[tool_name]
                    
                    # 执行真实搜索
                    tool_result = tool_func(**tool_args)
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool.id,
                        "content": tool_result,
                    })
            sub_turn += 1
        except Exception as e:
            print(f"AI API Turn Error: {e}")
            return None

def update_yaml():
    context = get_realtime_context()
    raw_content = get_ai_recommendation(context)
    if raw_content:
        try:
            cleaned_content = clean_json_string(raw_content)
            ai_content = json.loads(cleaned_content)
            
            paint_list = []
            for item in ai_content.get('paint', []):
                paint_list.append({
                    'title': item.get('title', ''),
                    'desc': item.get('desc', ''),
                    'url': item.get('id_url', '')
                })

            data = {
                'date': str(get_beijing_time().date()),
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
