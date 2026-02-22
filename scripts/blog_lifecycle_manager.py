import os
import yaml
import subprocess
from datetime import datetime, timedelta, timezone

POSTS_DIR = "_posts"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S +0800"

def get_beijing_time():
    return datetime.now(timezone(timedelta(hours=8)))

def format_date(dt_obj):
    if isinstance(dt_obj, datetime):
        return dt_obj.strftime(DATE_FORMAT)
    return str(dt_obj)

def get_git_body(filepath):
    try:
        git_path = filepath.replace('\\', '/')
        # 获取 Git 记录中的原始正文
        content = subprocess.check_output(['git', 'show', f'HEAD:{git_path}'], encoding='utf-8', stderr=subprocess.DEVNULL)
        parts = content.split('---', 2)
        # 统一换行符并去除首尾空格，防止 Windows/Linux 差异导致误判
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
            front_matter = yaml.safe_load(parts[1])
            body = parts[2]
        except: continue

        needs_update = False
        
        current_date = front_matter.get("date")
        current_date_str = format_date(current_date)
        
        # 发布时间锁定逻辑
        is_new = not current_date or "UPLOAD_TIME" in current_date_str or "2026-01-01" in current_date_str
        
        if is_new:
            front_matter["date"] = now_str
            front_matter["last_modified_at"] = now_str
            needs_update = True
        else:
            # 强制补齐缺失的更新时间
            if not front_matter.get("last_modified_at"):
                front_matter["last_modified_at"] = current_date_str
                needs_update = True
            
            # 核心修复：对比时消除换行符差异
            committed_body = get_git_body(filepath)
            current_body = body.replace('\r\n', '\n').strip()
            
            if committed_body is not None and current_body != committed_body:
                front_matter["last_modified_at"] = now_str
                print(f"📝 [更新检测] {filename} 正文确实发生了变动")
                needs_update = True
            else:
                # 额外修复：如果当前已经显示了虚假更新时间，且内容未变，则将其强制归位
                if front_matter.get("last_modified_at") != current_date_str:
                    front_matter["last_modified_at"] = current_date_str
                    print(f"🧹 [清理] 已重置 {filename} 的虚假更新时间")
                    needs_update = True

        if needs_update:
            fm_yaml = yaml.dump(front_matter, allow_unicode=True, sort_keys=False).strip()
            new_content = f"---\n{fm_yaml}\n---\n\n{body.lstrip()}"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

if __name__ == "__main__":
    process_lifecycle()
