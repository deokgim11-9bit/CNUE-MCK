"""
Vercel 메인 엔트리 포인트
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# 템플릿 설정
template_dir = os.path.join(os.path.dirname(__file__), "..", "public", "templates")
templates = Jinja2Templates(directory=template_dir)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """홈페이지 - 로그인 페이지로 리다이렉트"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/api/", response_class=HTMLResponse)
async def api_home(request: Request):
    """API 홈페이지"""
    return {"message": "English Teaching Agent API", "status": "running"}

# Vercel 핸들러
handler = app
