"""
회원가입 API 서버리스 함수
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class UserRegister(BaseModel):
    email: str
    password: str
    name: str
    school: Optional[str] = None
    role: str = "teacher"

@app.post("/api/auth/register")
async def register(user_data: UserRegister):
    """사용자 회원가입"""
    # 데모 회원가입
    return {
        "message": "Demo registration successful. Please login with demo@example.com / demo123",
        "user_id": "demo-user"
    }

# Vercel 핸들러
handler = app
