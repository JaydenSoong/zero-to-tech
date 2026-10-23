from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pypinyin import pinyin, lazy_pinyin, Style
from snownlp import SnowNLP
from storage import save_record, get_history
from datetime import datetime, timezone

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
)

profile = {
    "heroTitle": "关于我",
    "heroSubtitle": "项目，创意，灵感，心得，我的作品",
    "featuredWork": {
        "kicker": "作品",
        "title": "文字实验室",
        "copy": "拼音和情绪，挖掘中文里的细节",
        "linkLabel": "打开作品",
    },
    "identity": {
        "motto": "已识乾坤大，尤怜草木青",
        "learning": "零到全栈",
    },
}

class AnalyzeRequest(BaseModel):
    text: str
    
@app.get("/api/profile")
def get_profile():
    return profile

def score_label(score):
    if score >= 0.6:
        return "偏积极"
    elif score <= 0.4:
        return "偏消极"
    else:
        return "中性"

@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    pinyin = lazy_pinyin(req.text, style=Style.TONE)
    score = round(SnowNLP(req.text).sentiments, 2)
    result = {
        "text": req.text,
        "score": score,
        "label": score_label(score),
        "pinyin": " ".join(pinyin),
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), 
    }
    save_record(result)
    return result

@app.get("/api/history")
def history():
    return get_history()
