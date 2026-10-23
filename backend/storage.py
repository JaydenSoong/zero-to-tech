import json

HISTORY_FILE = "history.json"

def save_record(record):
    records = load_history()
    records.append(record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def get_history():
    records = load_history()   # 读出文件里的全部记录
    records.reverse()          # 倒过来：新的排前面
    return records[:3]