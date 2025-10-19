"""
음성 전사 API 서버리스 함수
"""

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from openai import OpenAI
import os
import tempfile
import time

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

@app.post("/api/transcribe")
async def transcribe_audio(audio: UploadFile = File(...), user_id: str = Depends(verify_token)):
    """음성 전사 API"""
    temp_file_path = None
    try:
        if not audio.filename:
            raise HTTPException(
                status_code=400,
                detail={
                    'success': False,
                    'error': '음성 파일이 없습니다.'
                }
            )
        
        # 임시 파일로 저장
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file_path = temp_file.name
        temp_file.close()
        
        # 파일에 오디오 데이터 저장
        content = await audio.read()
        with open(temp_file_path, 'wb') as f:
            f.write(content)
        
        # 파일이 완전히 저장될 때까지 잠시 대기
        time.sleep(0.1)
        
        # OpenAI Whisper API로 전사
        with open(temp_file_path, 'rb') as f:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="en"
            )
        
        return {
            'success': True,
            'transcription': transcript.text
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                'success': False,
                'error': f'전사 중 오류가 발생했습니다: {str(e)}'
            }
        )
    finally:
        # 임시 파일 정리
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass

# Vercel 핸들러
handler = app
