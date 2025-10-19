"""
Rewrite 활동 평가 API 서버리스 함수
"""

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from rewrite_generator import RewriteGenerator
from models import RewriteActivity
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

@app.post("/api/evaluate_rewrite_activity")
async def evaluate_rewrite_activity(request: Request, user_id: str = Depends(verify_token)):
    """Rewrite 활동 평가 API"""
    try:
        data = await request.json()
        activity_type = data.get('activity_type', '')
        original_story = data.get('original_story', '')
        student_content = data.get('student_content', '')
        student_answers = data.get('student_answers', {})
        
        if not activity_type or not original_story:
            raise HTTPException(
                status_code=400,
                detail={
                    'success': False,
                    'error': '필수 정보가 누락되었습니다.'
                }
            )
        
        # RewriteActivity 객체 생성
        activity = RewriteActivity(
            activity_type=activity_type,
            original_story=original_story,
            modified_story="",
            blanks=[],
            student_answer=""
        )
        
        # 활동 유형에 따른 평가
        if activity_type == 'vocabulary_fill':
            evaluated_activity = rewrite_generator.evaluate_vocabulary_fill(activity, student_answers)
        elif activity_type == 'full_rewrite':
            evaluated_activity = rewrite_generator.evaluate_full_rewrite(activity, student_content)
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
            'evaluation': {
                'score': evaluated_activity.score,
                'total_score': evaluated_activity.total_score,
                'feedback': evaluated_activity.feedback
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                'success': False,
                'error': f'Rewrite 활동 평가 중 오류가 발생했습니다: {str(e)}'
            }
        )

# Vercel 핸들러
handler = app
