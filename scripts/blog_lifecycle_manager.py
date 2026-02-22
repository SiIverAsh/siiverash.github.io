import os
import yaml
import subprocess
from datetime import datetime, timedelta, timezone

POSTS_DIR = "_posts"

def get_beijing_time():
    return datetime.now(timezone(timedelta(hours=8)))

def get_git_committed_body(filepath):
    try:
        git_path = filepath.replace('\\', '/')
        content = subprocess.check_output(['git', 'show', f'HEAD:{git_path}'], encoding='utf-8', stderr=subprocess.DEVNULL)
        parts = content.split('---', 2)
        return parts[2].strip() if len(parts) >= 3 else ""
    except:
        # 如果文件是全新，返回 None
        return None

def process_lifecycle():
    if not os.path.exists(POSTS_DIR): return

    now_str = get_beijing_time().strftime("%Y-%m-%d %H:%M:%S +0800")

    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith(".md") or filename == "BLOG_TEMPLATE.md": continue
            
        filepath = os.path.join(POSTS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            full_content = f.read()

        parts = full_content.split('---', 2)
        if len(parts) < 3: continue

        try:
            # 加载元数据
            front_matter = yaml.safe_load(parts[1])
            body = parts[2]
        except Exception as e:
            print(f"Error parsing {filename}: {e}")
            continue

        needs_update = False
        
        # 1. 发布时间管理
        current_date = front_matter.get("date")
        if isinstance(current_date, datetime):
            current_date_str = current_date.strftime("%Y-%m-%d %H:%M:%S +0800")
        else:
            current_date_str = str(current_date or "")
            
        placeholders = ["UPLOAD_TIME", "2026-01-01", "None", ""]
        is_new_post = any(p in current_date_str for p in placeholders) or not current_date_str
        
        if is_new_post:
            front_matter["date"] = now_str
            front_matter["last_modified_at"] = now_str
            print(f"🆕 [发布] 为新文章 {filename} 初始化时间戳")
            needs_update = True
        else:
            # 2. 更新时间管理
            current_mod = front_matter.get("last_modified_at")
            
            if not current_mod:
                # 存量数据补齐
                front_matter["last_modified_at"] = current_date_str
                print(f"🔧 [补齐] 为 {filename} 补全缺失的更新时间字段")
                needs_update = True
            else:
                # 内容变动监测
                committed_body = get_git_committed_body(filepath)
                if committed_body is not None and body.strip() != committed_body:
                    front_matter["last_modified_at"] = now_str
                    print(f"📝 [更新] 检测到 {filename} 正文内容变动")
                    needs_update = True

        if needs_update:

            fm_yaml = yaml.dump(front_matter, allow_unicode=True, sort_keys=False, default_flow_style=False).strip()
            
            clean_body = body.lstrip()
            new_content = f"---\n{fm_yaml}\n---\n\n{clean_body}"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

if __name__ == "__main__":
    process_lifecycle()
