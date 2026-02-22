import os
import yaml
import subprocess
from datetime import datetime, timedelta, timezone

POSTS_DIR = "_posts"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S +0800"

def get_beijing_time():
    return datetime.now(timezone(timedelta(hours=8)))

def to_str(val):
    """强制将日期对象或其他类型转换为标准格式字符串"""
    if isinstance(val, datetime):
        return val.strftime(DATE_FORMAT)
    return str(val) if val else ""

def get_git_body(filepath):
    """从 Git 获取最近一次提交的正文，统一换行符"""
    try:
        git_path = filepath.replace('\\', '/')
        content = subprocess.check_output(['git', 'show', f'HEAD:{git_path}'], encoding='utf-8', stderr=subprocess.DEVNULL)
        parts = content.split('---', 2)
        return parts[2].replace('\r\n', '\n').strip() if len(parts) >= 3 else ""
    except:
        return None

def process_lifecycle():
    if not os.path.exists(POSTS_DIR): return
    now_str = get_beijing_time().strftime(DATE_FORMAT)

    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith(".md") or filename == "BLOG_TEMPLATE.md": continue
        filepath = os.path.join(POSTS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            full_content = f.read()

        parts = full_content.split('---', 2)
        if len(parts) < 3: continue

        try:
            # 使用原生解析，随后立即转换类型以防对比失败
            front_matter = yaml.safe_load(parts[1])
            body = parts[2]
            
            # 关键修复：统一转为字符串，消除对象与字符串对比的 bug
            fm_date = to_str(front_matter.get("date"))
            fm_mod = to_str(front_matter.get("last_modified_at"))
        except: continue

        needs_update = False
        
        # 1. 发布时间处理
        if not fm_date or "UPLOAD_TIME" in fm_date or "2026-01-01" in fm_date:
            front_matter["date"] = now_str
            front_matter["last_modified_at"] = now_str
            fm_date = now_str # 更新当前引用
            fm_mod = now_str
            needs_update = True
        
        # 2. 更新时间监测
        committed_body = get_git_body(filepath)
        current_body = body.replace('\r\n', '\n').strip()

        # 逻辑：正文变动则更新时间；正文没变但字段缺失/虚假更新则清理
        if committed_body is not None and current_body != committed_body:
            front_matter["last_modified_at"] = now_str
            needs_update = True
        elif not fm_mod or fm_mod != fm_date:
            # 如果内容没变，但更新时间存在且不等于发布时间，则视为“虚假更新”，将其归位
            front_matter["last_modified_at"] = fm_date
            needs_update = True

        if needs_update:
            # 写入时确保日期是字符串
            front_matter["date"] = to_str(front_matter.get("date"))
            front_matter["last_modified_at"] = to_str(front_matter.get("last_modified_at"))
            
            fm_yaml = yaml.dump(front_matter, allow_unicode=True, sort_keys=False).strip()
            # 关键修复：保持 body 原样，不使用 lstrip()
            new_content = f"---\n{fm_yaml}\n---\n{body}"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

if __name__ == "__main__":
    process_lifecycle()
