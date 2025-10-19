"""
FastAPI 웹 애플리케이션
초등학생용 영어 Short Story 및 Teacher's Talk Script 자동 생성 에이전트
"""

from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form, Depends, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from english_agent import EnglishTeachingAgent
from hattie_feedback import HattieFeedbackGenerator
from rewrite_generator import RewriteGenerator
from models import RewriteActivity, UserLogin, UserRegister
import json
import os
import tempfile
import time
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client, Client
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta

# 환경변수 로드
load_dotenv()

app = FastAPI(title="English Teaching Agent", version="1.0.0")

# JWT 설정
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key-for-english-teaching-agent-2024')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Supabase 클라이언트 초기화
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_ANON_KEY')
supabase: Optional[Client] = None

if supabase_url and supabase_key:
    try:
        supabase = create_client(supabase_url, supabase_key)
        print("Supabase client initialized successfully")
    except Exception as e:
        print(f"WARNING: Failed to initialize Supabase client: {e}")
        supabase = None
else:
    print("WARNING: Supabase credentials not found. Database features will be disabled.")

# 인증 설정
security = HTTPBearer()

agent = EnglishTeachingAgent()
hattie_feedback = HattieFeedbackGenerator()
rewrite_generator = RewriteGenerator()

# OpenAI 클라이언트 초기화
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 인증 관련 함수들
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """JWT 토큰 생성"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """JWT 토큰 검증"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(user_id: str = Depends(verify_token)):
    """현재 사용자 정보 가져오기"""
    if not supabase:
        # Supabase가 없는 경우 데모 사용자 반환
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
    
    try:
        result = supabase.table('users').select('*').eq('id', user_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="User not found")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """메인 페이지 (로그인 페이지)"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: dict = Depends(get_current_user)):
    """대시보드 페이지 (인증 필요)"""
    return templates.TemplateResponse("index.html", {"request": request, "user": current_user})

@app.post("/auth/login")
async def login(user_data: UserLogin):
    """사용자 로그인"""
    if not supabase:
        # Supabase가 없는 경우 간단한 데모 로그인
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
    
    try:
        # Supabase Auth를 사용한 로그인
        response = supabase.auth.sign_in_with_password({
            "email": user_data.email,
            "password": user_data.password
        })
        
        if not response.user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # 사용자 정보 가져오기
        user_result = supabase.table('users').select('*').eq('id', response.user.id).execute()
        if not user_result.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        user = user_result.data[0]
        
        # JWT 토큰 생성
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user['id']}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user['id'],
                "email": user['email'],
                "name": user['name'],
                "school": user.get('school'),
                "role": user['role']
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Login failed: {str(e)}")

@app.post("/auth/register")
async def register(user_data: UserRegister):
    """사용자 회원가입"""
    if not supabase:
        # Supabase가 없는 경우 간단한 데모 회원가입
        return {
            "message": "Demo registration successful. Please login with demo@example.com / demo123",
            "user_id": "demo-user"
        }
    
    try:
        # Supabase Auth를 사용한 회원가입
        response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password
        })
        
        if not response.user:
            raise HTTPException(status_code=400, detail="Registration failed")
        
        # 사용자 정보를 users 테이블에 저장
        user_info = {
            "id": response.user.id,
            "email": user_data.email,
            "name": user_data.name,
            "school": user_data.school,
            "role": user_data.role,
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True
        }
        
        supabase.table('users').insert(user_info).execute()
        
        return {
            "message": "User registered successfully",
            "user_id": response.user.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")

@app.post("/auth/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """사용자 로그아웃"""
    return {"message": "Logged out successfully"}

@app.get("/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """현재 사용자 정보 조회"""
    return current_user

@app.post('/generate')
async def generate_materials(request: Request, current_user: dict = Depends(get_current_user)):
    """수업 자료 생성 API"""
    try:
        data = await request.json()
        
        # API 키 확인
        if not os.getenv('OPENAI_API_KEY'):
            raise HTTPException(
                status_code=400,
                detail={
                    'success': False,
                    'error': 'OpenAI API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.',
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
        
        # Supabase에 데이터 저장 (선택사항)
        if supabase:
            try:
                supabase.table('generated_materials').insert({
                    'unit_data': data,
                    'generated_content': {
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
                        }
                    },
                    'quality_check': quality_check,
                    'created_at': 'now()'
                }).execute()
            except Exception as db_error:
                print(f"Database save error: {db_error}")
        
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

@app.get('/example')
async def get_example(current_user: dict = Depends(get_current_user)):
    """예시 데이터 반환"""
    example_data = agent.get_example_unit_data()
    return {
        'success': True,
        'data': example_data
    }

@app.post('/transcribe')
async def transcribe_audio(audio: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
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
        
        # 임시 파일로 저장 (delete=False로 설정)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file_path = temp_file.name
        temp_file.close()  # 파일 핸들 닫기
        
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
        # 임시 파일 정리 (파일이 존재하는 경우에만)
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except OSError:
                # 파일 삭제 실패 시 무시 (다른 프로세스가 사용 중일 수 있음)
                pass

@app.post('/evaluate')
async def evaluate_answer(request: Request, current_user: dict = Depends(get_current_user)):
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

@app.post('/comprehensive_feedback')
async def generate_comprehensive_feedback(request: Request, current_user: dict = Depends(get_current_user)):
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

@app.post('/create_rewrite_activity')
async def create_rewrite_activity(request: Request, current_user: dict = Depends(get_current_user)):
    """Rewrite 활동 생성 API"""
    try:
        data = await request.json()
        story_content = data.get('story_content', '')
        activity_type = data.get('activity_type', 'vocabulary_fill')  # 'vocabulary_fill' or 'full_rewrite'
        
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

@app.post('/evaluate_rewrite_activity')
async def evaluate_rewrite_activity(request: Request, current_user: dict = Depends(get_current_user)):
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

# Vercel을 위한 핸들러
handler = app

