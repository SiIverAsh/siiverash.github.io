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

def get_git_status(filepath):
    """检查文件是否在 Git 中被修改（未提交的变动）"""
    try:
        git_path = filepath.replace('\\', '/')
        status = subprocess.check_output(['git', 'status', '--porcelain', git_path], encoding='utf-8').strip()
        return status # 返回空字符串表示文件是干净的
    except:
        return "UNKNOWN"

def get_git_body(filepath):
    """从 HEAD 中提取上一次提交的正文内容"""
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
        
        # 哨兵逻辑：如果 Git 认为文件没动，直接跳过，保护时间戳不被误触
        if not get_git_status(filepath):
            continue

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
        
        # 1. 发布时间：仅针对占位符初始化
        if not fm_date or "UPLOAD_TIME" in fm_date or "2026-01-01" in fm_date:
            front_matter["date"] = now_str
            front_matter["last_modified_at"] = now_str
            needs_update = True
        else:
            # 2. 更新时间：精准变动监测
            committed_body = get_git_body(filepath)
            current_body = body.replace('\r\n', '\n').strip()

            # 只有正文内容确实变了，才更新时间戳
            if committed_body is not None and current_body != committed_body:
                front_matter["last_modified_at"] = now_str
                print(f"✅ [监测到更新] {filename}")
                needs_update = True
            elif not fm_mod or fm_mod != fm_date:
                # 兼容性修复：如果文件已动但不需要更新时间，则确保 mod 等于 date（隐藏图标）
                front_matter["last_modified_at"] = fm_date
                needs_update = True

        if needs_update:
            # 统一强制转为字符串存储
            front_matter["date"] = to_str(front_matter.get("date"))
            front_matter["last_modified_at"] = to_str(front_matter.get("last_modified_at"))
            
            fm_yaml = yaml.dump(front_matter, allow_unicode=True, sort_keys=False).strip()
            # 保持 body 原始格式，绝不删除开头或结尾的换行符
            new_content = f"---\n{fm_yaml}\n---\n{body}"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

if __name__ == "__main__":
    process_lifecycle()
