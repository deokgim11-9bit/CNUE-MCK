"""
대시보드 페이지 서버리스 함수
"""

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import os
from datetime import datetime, timedelta

app = FastAPI()

# JWT 설정
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key-for-english-teaching-agent-2024')
ALGORITHM = "HS256"

# 템플릿 설정
template_dir = os.path.join(os.path.dirname(__file__), "..", "public", "templates")
templates = Jinja2Templates(directory=template_dir)

# 인증 설정
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """JWT 토큰 검증"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def get_current_user(user_id: str = Depends(verify_token)):
    """현재 사용자 정보 가져오기"""
    if user_id == "demo-user":
        return {
            "id": "demo-user",
            "email": "demo@example.com",
            "name": "데모 사용자",
            "school": "데모 학교",
            "role": "teacher"
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: dict = Depends(get_current_user)):
    """대시보드 페이지"""
    return templates.TemplateResponse("index.html", {"request": request, "user": current_user})

# Vercel 핸들러
handler = app
