# Vercel + Supabase 배포 가이드

이 프로젝트를 Vercel과 Supabase를 사용하여 배포하는 방법을 안내합니다.

## 1. Supabase 설정

### 1.1 Supabase 프로젝트 생성
1. [Supabase](https://supabase.com)에 가입하고 새 프로젝트를 생성합니다.
2. 프로젝트 설정에서 API URL과 anon key를 확인합니다.

### 1.2 데이터베이스 스키마 설정
1. Supabase 대시보드의 SQL Editor로 이동합니다.
2. `supabase_schema.sql` 파일의 내용을 복사하여 실행합니다.
3. 테이블이 정상적으로 생성되었는지 확인합니다.

## 2. Vercel 배포

### 2.1 Vercel 프로젝트 생성
1. [Vercel](https://vercel.com)에 가입합니다.
2. GitHub 저장소를 연결하거나 직접 업로드합니다.

### 2.2 환경 변수 설정
Vercel 대시보드의 Environment Variables에서 다음 변수들을 설정합니다:

```
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
```

**중요**: JWT_SECRET_KEY는 강력한 랜덤 문자열로 설정하세요 (최소 32자).

### 2.3 배포 설정
- **Framework Preset**: Other
- **Build Command**: (비워둠)
- **Output Directory**: (비워둠)
- **Install Command**: `pip install -r requirements.txt`

## 3. 로컬 개발 환경 설정

### 3.1 환경 변수 설정
```bash
# .env 파일 생성
cp env_example.txt .env

# .env 파일 편집하여 실제 값들 입력
```

### 3.2 의존성 설치
```bash
pip install -r requirements.txt
```

### 3.3 로컬 서버 실행
```bash
# 개발 서버 실행
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# 또는
python -m uvicorn app:app --reload
```

## 4. 주요 변경사항

### 4.1 Flask → FastAPI 변환
- 모든 라우트가 async/await 패턴으로 변경되었습니다.
- JSON 응답이 자동으로 처리됩니다.
- 파일 업로드 처리가 개선되었습니다.

### 4.2 Supabase 통합
- 생성된 자료가 자동으로 데이터베이스에 저장됩니다.
- 평가 결과와 활동 결과도 추적됩니다.

### 4.3 Vercel 최적화
- Vercel의 서버리스 함수로 최적화되었습니다.
- 자동 스케일링이 지원됩니다.

## 5. API 엔드포인트

### 인증 관련
- `GET /`: 로그인 페이지
- `GET /dashboard`: 대시보드 (인증 필요)
- `POST /auth/login`: 사용자 로그인
- `POST /auth/register`: 사용자 회원가입
- `POST /auth/logout`: 사용자 로그아웃
- `GET /auth/me`: 현재 사용자 정보 조회

### 수업 자료 생성 (모두 인증 필요)
- `POST /generate`: 수업 자료 생성
- `GET /example`: 예시 데이터 반환
- `POST /transcribe`: 음성 전사
- `POST /evaluate`: 답변 평가
- `POST /comprehensive_feedback`: 종합 피드백 생성
- `POST /create_rewrite_activity`: Rewrite 활동 생성
- `POST /evaluate_rewrite_activity`: Rewrite 활동 평가

## 6. 문제 해결

### 6.1 일반적인 문제
- **ImportError**: `requirements.txt`의 모든 패키지가 설치되었는지 확인
- **환경 변수 오류**: `.env` 파일이 올바르게 설정되었는지 확인
- **데이터베이스 연결 오류**: Supabase URL과 키가 올바른지 확인

### 6.2 Vercel 배포 문제
- **빌드 실패**: `vercel.json` 설정 확인
- **런타임 오류**: 로그를 확인하여 구체적인 오류 파악
- **환경 변수**: Vercel 대시보드에서 환경 변수 설정 확인

## 7. 모니터링

- **Vercel**: 배포 상태와 성능 메트릭 확인
- **Supabase**: 데이터베이스 사용량과 쿼리 성능 모니터링
- **OpenAI**: API 사용량과 비용 모니터링
