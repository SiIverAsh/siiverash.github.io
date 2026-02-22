import os
import yaml
import subprocess
from datetime import datetime, timedelta, timezone

POSTS_DIR = "_posts"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S +0800"

def get_beijing_time():
    return datetime.now(timezone(timedelta(hours=8)))

def to_str(val):
    if isinstance(val, datetime):
        return val.strftime(DATE_FORMAT)
    return str(val) if val else ""

def get_git_body(filepath, ref="HEAD"):
    """从 Git 获取指定版本的正文内容"""
    try:
        git_path = filepath.replace('\\', '/')
        content = subprocess.check_output(['git', 'show', f'{ref}:{git_path}'], encoding='utf-8', stderr=subprocess.DEVNULL)
        parts = content.split('---', 2)
        return parts[2].replace('\r\n', '\n').strip() if len(parts) >= 3 else ""
    except:
        return None

def process_lifecycle():
    if not os.path.exists(POSTS_DIR): return
    now_str = get_beijing_time().strftime(DATE_FORMAT)
    
    is_ci = os.getenv("GITHUB_ACTIONS") == "true"

    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith(".md") or filename == "BLOG_TEMPLATE.md": continue
        filepath = os.path.join(POSTS_DIR, filename)
        
        # CI 环境对比上一个提交 ，本地对比当前 HEAD
        compare_ref = "HEAD^1" if is_ci else "HEAD"

        with open(filepath, 'r', encoding='utf-8') as f:
            full_content = f.read()

        parts = full_content.split('---', 2)
        if len(parts) < 3: continue

        try:
            front_matter = yaml.safe_load(parts[1])
            body = parts[2]
            fm_date = to_str(front_matter.get("date"))
            fm_mod = to_str(front_matter.get("last_modified_at"))
        except: continue

        needs_update = False
        
        # 1. 发布时间处理
        if not fm_date or "UPLOAD_TIME" in fm_date or "2026-01-01" in fm_date:
            front_matter["date"] = now_str
            front_matter["last_modified_at"] = now_str
            fm_date = now_str
            fm_mod = now_str
            print(f"🆕 [发布初始化] {filename} (已锁定发布日期)", flush=True)
            needs_update = True
        
        # 2. 更新时间监测
        current_body = body.replace('\r\n', '\n').strip()
        committed_body = get_git_body(filepath, ref=compare_ref)

        if committed_body is not None and current_body != committed_body:
            front_matter["last_modified_at"] = now_str
            print(f"📝 [正文内容更新] {filename} (检测到正文变动，已更新 last_modified_at)", flush=True)
            needs_update = True
        elif not fm_mod or fm_mod != fm_date:
            front_matter["last_modified_at"] = fm_date
            print(f"🧹 [日期规范化] {filename} (已同步更新时间字段)", flush=True)
            needs_update = True

        if needs_update:
            front_matter["date"] = to_str(front_matter.get("date"))
            front_matter["last_modified_at"] = to_str(front_matter.get("last_modified_at"))
            fm_yaml = yaml.dump(front_matter, allow_unicode=True, sort_keys=False).strip()
            new_content = f"---\n{fm_yaml}\n---\n{body}"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

if __name__ == "__main__":
    process_lifecycle()
