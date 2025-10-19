"""
종합 피드백 API 서버리스 함수
"""

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from hattie_feedback import HattieFeedbackGenerator
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

# Hattie 피드백 생성기 초기화
hattie_feedback = HattieFeedbackGenerator()

@app.post("/api/comprehensive_feedback")
async def generate_comprehensive_feedback(request: Request, user_id: str = Depends(verify_token)):
    """Hattie의 연구를 바탕으로 한 종합 피드백 생성"""
    try:
        data = await request.json()
        question = data.get('question', '')
        answer = data.get('answer', '')
        individual_scores = data.get('individual_scores', [])
        
        if not question or not answer:
            raise HTTPException(
                status_code=400,
                detail={
                    'success': False,
                    'error': '질문과 답변이 필요합니다.'
                }
            )
        
        # Hattie 피드백 생성
        hattie_result = hattie_feedback.generate_comprehensive_feedback(
            question=question,
            answer=answer,
            individual_scores=individual_scores
        )
        
        return hattie_result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                'success': False,
                'error': f'종합 피드백 생성 중 오류가 발생했습니다: {str(e)}'
            }
        )

# Vercel 핸들러
handler = app
