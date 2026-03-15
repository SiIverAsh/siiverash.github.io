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

HISTORY_FILE = "_data/history.json"
MAX_HISTORY_DAYS = 10

def load_history():
    """从文件加载历史推荐记录"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
                # 获取所有历史标题的平铺列表
                all_titles = []
                for date in history:
                    all_titles.extend(history[date])
                return all_titles, history
        except Exception as e:
            print(f"加载历史记录失败: {e}")
            return [], {}
    return [], {}

def save_history(new_data, history_dict):
    """保存当前推荐到历史记录，并只保留最近 N 天"""
    today = str(get_beijing_time().date())
    
    # 提取所有标题/名称
    titles = []
    
    # Tech 分类
    tech = new_data.get('tech', {})
    for cat in tech:
        for item in tech[cat]:
            if isinstance(item, dict) and item.get('title'):
                titles.append(item.get('title'))

    # 其他分类
    for cat in ['paper', 'llm', 'algorithm', 'new_project']:
        for item in new_data.get(cat, []):
            if isinstance(item, dict) and item.get('title'):
                titles.append(item.get('title'))

    # CV
    cv = new_data.get('cv_recommend', {})
    if cv and isinstance(cv, dict) and cv.get('name'):
        titles.append(cv.get('name'))
    
    # 过滤空值并更新历史
    history_dict[today] = list(set([t for t in titles if t]))
    
    # 只保留最近 MAX_HISTORY_DAYS 天
    sorted_dates = sorted(history_dict.keys(), reverse=True)
    new_history = {date: history_dict[date] for date in sorted_dates[:MAX_HISTORY_DAYS]}
    
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_history, f, ensure_ascii=False, indent=2)

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

def get_ai_recommendation(context, history_titles):
    if not api_key:
        return None

    history_str = "、".join(history_titles[-30:]) if history_titles else "无"

    prompt_template = """
    Please think carefully, lowely and accurately.
    今天是 {CURRENT_DATE}。你是一个全能的数字生活与技术博主，精通硬件、AI、动漫及二次元文化。你以输出信息的高准确性著称。
    请基于（三个月、一个月以内）近期真实背景：{CONTEXT_PLACEHOLDER}，为一名软件工程硕士生提供每日推荐。
    
    **重要排除项（以下内容最近已推荐过，绝对禁止重复推荐）：**
    {HISTORY_BLOCK}
    
    必须的要求：
    1. 每个分类（Tech下的 9 个指定子类）必须提供正好 1 个推荐项。
    2. Tech 下必须严格使用这 9 个键名：Computer Vision, NLP, Audio, Net, Lang, Arch, GPU, CPU, News。
    3. desc 必须输出最新的硬核技术细节（如架构特性、工艺制程、性能指标）。
    4. 严禁使用任何引导性废话。
    5. 针对 GPU 和 CPU 领域，必须关注最近半年内的动态。
    6. 每个内容项必须包含至少 3 个 tags。
    7. 对于Paper推荐，必须是近期的顶会论文（如ICLR, ACL, NeurIPS等），并提供真实论文链接（url）。
    8. 对于LLM推荐，推荐近期重要的大语言模型进展、开源模型或研究。
    9. 对于Algorithm推荐，推荐传统机器学习算法或常见基础算法。
    10. 对于New Project推荐，必须是GitHub上里的开源项目，提供真实链接（url）。
    11. 对于history推荐内容为“历史上的今天”，必须提供 6 条不同数据。
    12. **CV推荐 (声优相关)**：
       - 此项与 Tech 中的 Computer Vision 无关。
       - 必须严格参考**《声优名鉴》(声優名鑑)**数据。
       - 必须包含：姓名(name)、所属事务所(agency)、出生地(hometown)、以及一段评价(intro,大约150字)。
       - **强制事实对齐**：如果搜索结果没提到，宁可不写，也不准编造。
       - **严禁提及**：绝对禁止提及任何具体的动漫作品或角色名称。
    13. 所有的回答请务必用中文。
    14. 一定不要推荐与之前重复的内容（参考上方的“重要排除项”）。
    
    必须输出以下 JSON 格式：
    {{
      "tech": {{
        "Computer Vision": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "NLP": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "Audio": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "Net": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "Lang": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "Arch": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "GPU": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "CPU": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}],
        "News": [{"title": "..", "desc": "..", "tags": ["A", "B", "C", "D"]}]
      }},
      "paper": [{"title": "..", "desc": "顶会论文推荐", "tags": ["A", "B", "C", "D"], "url": "论文链接"}],
      "llm": [{"title": "..", "desc": "大语言模型相关", "tags": ["A", "B", "C", "D"]}],
      "algorithm": [{"title": "..", "desc": "传统机器学习或常见算法", "tags": ["A", "B", "C", "D"]}],
      "new_project": [{"title": "..", "desc": "GitHub上trend里的最新项目", "tags": ["A", "B", "C", "D"], "url": "项目链接"}],
      "history": [{"year": "..", "event": ".."}],
      "cv_recommend": {{
        "name": "声优名", 
        "agency": "所属事务所", 
        "hometown": "出生地",
        "intro": "基于真实数据进行评价，若数据不足宁缺毋滥，严禁编造"
      }}
    }}
    """
    
    history_block = f"最近已推荐过的内容（请避开）：{history_str}" if history_titles else "暂无最近推荐记录。"
    
    prompt = prompt_template.replace("{CONTEXT_PLACEHOLDER}", context) \
                           .replace("{CURRENT_DATE}", str(get_beijing_time().date())) \
                           .replace("{HISTORY_BLOCK}", history_block)

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
            # 补全 reasoning_content 并存入历史消息
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
    history_titles, history_dict = load_history()
    context = get_realtime_context()
    raw_content = get_ai_recommendation(context, history_titles)
    if raw_content:
        try:
            cleaned_content = clean_json_string(raw_content)
            ai_content = json.loads(cleaned_content)
            
            data = {
                'date': str(get_beijing_time().date()),
                'tech': ai_content.get('tech', {}),
                'paper': ai_content.get('paper', []),
                'llm': ai_content.get('llm', []),
                'algorithm': ai_content.get('algorithm', []),
                'new_project': ai_content.get('new_project', []),
                'history': ai_content.get('history', []),
                'cv_recommend': ai_content.get('cv_recommend', {})
            }
            
            with open('_data/recommendations.yml', 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True)
            print("Successfully updated _data/recommendations.yml")
            
            # 保存历史记录
            save_history(ai_content, history_dict)
            print("Successfully updated _data/history.json")
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
