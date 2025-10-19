"""
수업 자료 생성 API 서버리스 함수
"""

from fastapi import FastAPI, Request, HTTPException, Depends
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

@app.post("/api/generate")
async def generate_materials(request: Request, user_id: str = Depends(verify_token)):
    """수업 자료 생성 API"""
    try:
        data = await request.json()
        
        # API 키 확인
        if not os.getenv('OPENAI_API_KEY'):
            raise HTTPException(
                status_code=400,
                detail={
                    'success': False,
                    'error': 'OpenAI API 키가 설정되지 않았습니다.',
                    'fallback_used': True
                }
            )
        
        # 데이터 유효성 검사
        if not agent.validate_unit_data(data):
            raise HTTPException(
                status_code=400,
                detail={
                    'success': False,
                    'error': '입력 데이터가 올바르지 않습니다. 모든 필드를 확인해주세요.'
                }
            )
        
        # 자료 생성
        result = agent.generate_teaching_materials(data)
        
        # 생성된 내용 품질 검증
        quality_check = agent.validate_generated_content(result)
        
        # 결과를 JSON으로 변환
        result_dict = {
            'success': True,
            'data': {
                'unit': {
                    'target_communicative_functions': result.unit.target_communicative_functions,
                    'target_grammar_forms': result.unit.target_grammar_forms,
                    'target_vocabulary': result.unit.target_vocabulary
                },
                'short_story': {
                    'title': result.short_story.title,
                    'content': result.short_story.content,
                    'word_count': result.short_story.word_count,
                    'sentence_count': result.short_story.sentence_count
                },
                'teacher_script': {
                    'opening': result.teacher_script.opening,
                    'during_reading': result.teacher_script.during_reading,
                    'after_reading': result.teacher_script.after_reading,
                    'key_expression_practice': result.teacher_script.key_expression_practice,
                    'retelling_guidance': result.teacher_script.retelling_guidance,
                    'evaluation_criteria': result.teacher_script.evaluation_criteria,
                    'wrap_up': result.teacher_script.wrap_up
                },
                'metadata': result.generation_metadata,
                'quality_check': quality_check
            }
        }
        
        return result_dict
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                'success': False,
                'error': f'자료 생성 중 오류가 발생했습니다: {str(e)}',
                'fallback_used': True
            }
        )

# Vercel 핸들러
handler = app
