# 초등학생용 영어 Short Story 및 Teacher's Talk Script 자동 생성 에이전트

## 개요

본 프로젝트는 Cursor.ai를 통해 구현된 '초등학생용 영어 Short Story 및 Teacher's Talk Script 자동 생성 AI 에이전트'입니다. 한국의 초등학교 영어 수업 환경에 맞춰, 예비 교사 및 현장 교사들이 교육과정과 연계된 고품질의 수업 자료를 손쉽게 생성할 수 있도록 지원합니다.

## 주요 기능

- **Short Story 자동 생성**: CEFR A1 수준의 8-10문장 짧은 이야기 생성
- **Teacher's Talk Script 자동 생성**: 5단계 구조의 교사 대본 생성
- **맞춤형 자료 생성**: 입력된 목표 언어 요소에 정확히 부합하는 자료 생성
- **웹 기반 사용자 인터페이스**: 직관적이고 사용하기 쉬운 웹 인터페이스

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 데모 실행

```bash
python demo.py
```

### 3. 웹 애플리케이션 실행

```bash
python app.py
```

웹 브라우저에서 `http://localhost:5000`으로 접속하여 사용할 수 있습니다.

## 사용 방법

### 웹 인터페이스 사용

1. 웹 브라우저에서 `http://localhost:5000` 접속
2. 다음 정보를 입력:
   - **목표 의사소통 기능**: 예) "능력 묻고 답하기"
   - **목표 문법 형태**: 예) "I can..., Can you...?, Yes, I can. / No, I can't."
   - **목표 어휘**: 예) "bird, fish, frog, fly, swim, jump"
3. "자료 생성하기" 버튼 클릭
4. 생성된 Short Story와 Teacher's Talk Script 확인

### 예시 데이터 사용

"예시 데이터 불러오기" 버튼을 클릭하면 미리 준비된 예시 데이터를 자동으로 입력할 수 있습니다.

## 생성 결과물

### Short Story
- **요구사항**: 8-10문장, 각 문장 최대 9단어
- **수준**: CEFR A1 레벨의 쉬운 영어
- **내용**: 한국 초등학생의 정서에 맞는 긍정적인 내용

### Teacher's Talk Script
5단계 구조로 구성:
1. **Opening (도입)**: 학생들의 흥미 유발 및 배경지식 활성화
2. **During-Reading (읽기 중)**: 이야기 읽기 중 참여 유도
3. **After-Reading (읽기 후)**: 내용 이해도 확인 Q&A
4. **Key Expression Practice (핵심 표현 연습)**: 핵심 표현 활용 연습
5. **Wrap-Up (마무리)**: 수업 내용 요약 및 마무리

## 프로젝트 구조

```
├── app.py                      # Flask 웹 애플리케이션
├── demo.py                     # 데모 실행 스크립트
├── english_agent.py            # 메인 에이전트 클래스
├── models.py                   # 데이터 모델 정의
├── story_generator.py          # Short Story 생성기
├── teacher_script_generator.py # Teacher's Talk Script 생성기
├── requirements.txt            # Python 의존성
├── templates/
│   └── index.html              # 웹 인터페이스 템플릿
└── README.md                   # 프로젝트 문서
```

## 기술 스택

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data Validation**: Pydantic
- **Template Engine**: Jinja2

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

## 지원

문제가 발생하거나 개선 사항이 있으시면 이슈를 등록해 주세요.

