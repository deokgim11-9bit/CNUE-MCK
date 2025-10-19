"""
로그인 페이지 서버리스 함수
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# 템플릿 설정
template_dir = os.path.join(os.path.dirname(__file__), "..", "public", "templates")
templates = Jinja2Templates(directory=template_dir)

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """로그인 페이지"""
    return templates.TemplateResponse("login.html", {"request": request})

# Vercel 핸들러
handler = app
