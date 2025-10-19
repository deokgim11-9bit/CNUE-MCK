"""
Rewrite 활동 생성 API 서버리스 함수
"""

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from rewrite_generator import RewriteGenerator
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

# Rewrite 생성기 초기화
rewrite_generator = RewriteGenerator()

@app.post("/api/create_rewrite_activity")
async def create_rewrite_activity(request: Request, user_id: str = Depends(verify_token)):
    """Rewrite 활동 생성 API"""
    try:
        data = await request.json()
        story_content = data.get('story_content', '')
        activity_type = data.get('activity_type', 'vocabulary_fill')
        
        if not story_content:
            raise HTTPException(
                status_code=400,
                detail={
                    'success': False,
                    'error': '스토리 내용이 필요합니다.'
                }
            )
        
        if activity_type == 'vocabulary_fill':
            activity = rewrite_generator.create_vocabulary_fill_activity(story_content)
        elif activity_type == 'full_rewrite':
            activity = rewrite_generator.create_full_rewrite_activity(story_content)
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    'success': False,
                    'error': '올바른 활동 유형을 선택해주세요.'
                }
            )
        
        return {
            'success': True,
            'activity': {
                'activity_type': activity.activity_type,
                'original_story': activity.original_story,
                'modified_story': activity.modified_story,
                'blanks': activity.blanks
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                'success': False,
                'error': f'Rewrite 활동 생성 중 오류가 발생했습니다: {str(e)}'
            }
        )

# Vercel 핸들러
handler = app
