"""
답변 평가 API 서버리스 함수
"""

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from openai import OpenAI
import os
import json

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

# OpenAI 클라이언트 초기화
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.post("/api/evaluate")
async def evaluate_answer(request: Request, user_id: str = Depends(verify_token)):
    """답변 평가 API"""
    try:
        data = await request.json()
        question = data.get('question', '')
        answer = data.get('answer', '')
        section = data.get('section', '')
        
        if not question or not answer:
            raise HTTPException(
                status_code=400,
                detail={
                    'success': False,
                    'error': '질문과 답변이 필요합니다.'
                }
            )
        
        # GPT-4o를 사용한 평가
        evaluation_prompt = f"""
        You are an expert English teacher evaluating a student's answer to a question.

        Question: {question}
        Student's Answer: {answer}
        Section: {section}

        Please evaluate the student's answer on a scale of 1-10 and provide detailed feedback.

        Consider these criteria:
        1. Content accuracy (did they answer the question correctly?)
        2. Grammar and vocabulary usage
        3. Fluency and pronunciation (based on transcription quality)
        4. Completeness of response
        5. Appropriateness for elementary level

        Respond in JSON format:
        {{
            "score": [1-10],
            "accuracy": "[brief comment on content accuracy]",
            "fluency": "[brief comment on fluency]",
            "grammar": "[brief comment on grammar]",
            "feedback": "[detailed constructive feedback in Korean for the student]"
        }}
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert English teacher providing constructive feedback to elementary students."},
                {"role": "user", "content": evaluation_prompt}
            ]
        )
        
        # JSON 응답 파싱
        evaluation_text = response.choices[0].message.content.strip()
        
        # JSON 부분만 추출
        start_idx = evaluation_text.find('{')
        end_idx = evaluation_text.rfind('}') + 1
        json_str = evaluation_text[start_idx:end_idx]
        evaluation_data = json.loads(json_str)
        
        return {
            'success': True,
            'score': evaluation_data.get('score', 5),
            'accuracy': evaluation_data.get('accuracy', '평가 불가'),
            'fluency': evaluation_data.get('fluency', '평가 불가'),
            'grammar': evaluation_data.get('grammar', '평가 불가'),
            'feedback': evaluation_data.get('feedback', '피드백을 생성할 수 없습니다.')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                'success': False,
                'error': f'평가 중 오류가 발생했습니다: {str(e)}'
            }
        )

# Vercel 핸들러
handler = app
