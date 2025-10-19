"""
예시 데이터 API 서버리스 함수
"""

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from english_agent import EnglishTeachingAgent
import os

app = FastAPI()

# JWT 설정
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key-for-english-teaching-agent-2024')
ALGORITHM = "HS256"

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

# 에이전트 초기화
agent = EnglishTeachingAgent()

@app.get("/api/example")
async def get_example(user_id: str = Depends(verify_token)):
    """예시 데이터 반환"""
    example_data = agent.get_example_unit_data()
    return {
        'success': True,
        'data': example_data
    }

# Vercel 핸들러
handler = app
