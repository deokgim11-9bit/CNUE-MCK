"""
로그인 API 서버리스 함수
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

app = FastAPI()

# JWT 설정
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key-for-english-teaching-agent-2024')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class UserLogin(BaseModel):
    email: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    """JWT 토큰 생성"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/api/auth/login")
async def login(user_data: UserLogin):
    """사용자 로그인"""
    # 데모 로그인
    if user_data.email == "demo@example.com" and user_data.password == "demo123":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": "demo-user"}, expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": "demo-user",
                "email": "demo@example.com",
                "name": "데모 사용자",
                "school": "데모 학교",
                "role": "teacher"
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials. Use demo@example.com / demo123 for demo")

# Vercel 핸들러
handler = app
