"""
초등학생용 영어 Short Story 및 Teacher's Talk Script 자동 생성 에이전트
데이터 모델 정의
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class Unit(BaseModel):
    """수업 단원 정보를 담는 데이터 모델"""
    target_communicative_functions: List[str] = Field(
        ..., 
        description="목표 의사소통 기능 (예: ['제안하고 답하기', '감정 묻고 답하기'])"
    )
    target_grammar_forms: List[str] = Field(
        ..., 
        description="목표 문법 형태 (예: ['Can you...?', 'I'm [happy]'])"
    )
    target_vocabulary: List[str] = Field(
        ..., 
        description="목표 어휘 (예: ['jump', 'run', 'swim', 'happy', 'sad'])"
    )


class ShortStory(BaseModel):
    """생성된 Short Story를 담는 데이터 모델"""
    title: str = Field(..., description="이야기 제목")
    content: str = Field(..., description="이야기 내용 (8-10문장, 각 문장 최대 9단어)")
    word_count: int = Field(..., description="총 단어 수")
    sentence_count: int = Field(..., description="문장 수")


class RetellingRubric(BaseModel):
    """Retelling 평가 루브릭 모델 (9개 영역, 0-3점 척도)"""
    characters_setting: List[str] = Field(..., description="Characters & Setting (등장인물과 배경) 평가 기준")
    initiating_event: List[str] = Field(..., description="Initiating Event / Problem (발단 사건/문제) 평가 기준")
    internal_reaction: List[str] = Field(..., description="Internal Reaction / Goal (내적 반응/목표) 평가 기준")
    attempts_actions: List[str] = Field(..., description="Attempts / Actions (시도/행동) 평가 기준")
    result_resolution: List[str] = Field(..., description="Result / Resolution (결과/해결) 평가 기준")
    ending_closure: List[str] = Field(..., description="Ending / Closure (결말/마무리) 평가 기준")
    causal_connection: List[str] = Field(..., description="Causal Connection (인과관계 연결) 평가 기준")
    temporal_connection: List[str] = Field(..., description="Temporal Connection (시간순 연결) 평가 기준")
    global_organization: List[str] = Field(..., description="Global Organization & Coherence (전체 구성과 일관성) 평가 기준")


class TeacherTalkScript(BaseModel):
    """생성된 Teacher's Talk Script를 담는 데이터 모델"""
    opening: List[str] = Field(..., description="도입부 질문들")
    during_reading: List[str] = Field(..., description="읽기 중 질문들")
    after_reading: List[str] = Field(..., description="읽기 후 질문들")
    key_expression_practice: List[str] = Field(..., description="핵심 표현 연습 가이드")
    retelling_guidance: List[str] = Field(..., description="리텔링 가이드 (루브릭 기반)")
    evaluation_criteria: List[str] = Field(..., description="평가 기준 안내")
    wrap_up: List[str] = Field(..., description="마무리 멘트")


class StoryGrammarRubric(BaseModel):
    """Story Grammar 기반 루브릭 (0-4점 척도)"""
    setting: List[str] = Field(..., description="Setting criteria (배경, 등장인물 소개)")
    characters: List[str] = Field(..., description="Characters criteria (주인공, 조연, 성격 묘사)")
    problem: List[str] = Field(..., description="Problem criteria (갈등, 문제 상황)")
    events: List[str] = Field(..., description="Events criteria (사건의 전개, 순서)")
    resolution: List[str] = Field(..., description="Resolution criteria (해결, 결말)")
    theme: List[str] = Field(..., description="Theme criteria (주제, 교훈)")
    vocabulary: List[str] = Field(..., description="Vocabulary criteria (어휘 사용, 표현)")
    grammar: List[str] = Field(..., description="Grammar criteria (문법, 문장 구조)")
    coherence: List[str] = Field(..., description="Coherence criteria (일관성, 연결성)")

class RewriteActivity(BaseModel):
    """Rewrite 활동 모델"""
    activity_type: str = Field(..., description="Activity type: 'vocabulary_fill' or 'full_rewrite'")
    original_story: str = Field(..., description="Original story text")
    modified_story: str = Field(..., description="Story with blanks or empty for rewrite")
    blanks: List[Dict[str, Any]] = Field(default=[], description="Blank positions and correct answers")
    student_answer: str = Field(default="", description="Student's answer")
    score: Dict[str, float] = Field(default={}, description="Scores by rubric criteria")
    total_score: float = Field(default=0.0, description="Total score")
    feedback: Dict[str, Any] = Field(default={}, description="Hattie-based feedback")

class GeneratedContent(BaseModel):
    """최종 생성 결과물을 담는 데이터 모델"""
    unit: Unit
    short_story: ShortStory
    teacher_script: TeacherTalkScript
    generation_metadata: dict = Field(default_factory=dict, description="생성 메타데이터")

class UserLogin(BaseModel):
    """사용자 로그인 모델"""
    email: str = Field(..., description="이메일 주소")
    password: str = Field(..., description="비밀번호")

class UserRegister(BaseModel):
    """사용자 회원가입 모델"""
    email: str = Field(..., description="이메일 주소")
    password: str = Field(..., description="비밀번호")
    name: str = Field(..., description="사용자 이름")
    school: Optional[str] = Field(None, description="소속 학교")
    role: str = Field(default="teacher", description="사용자 역할 (teacher, admin)")

class User(BaseModel):
    """사용자 정보 모델"""
    id: str = Field(..., description="사용자 ID")
    email: str = Field(..., description="이메일 주소")
    name: str = Field(..., description="사용자 이름")
    school: Optional[str] = Field(None, description="소속 학교")
    role: str = Field(..., description="사용자 역할")
    created_at: datetime = Field(..., description="생성일시")
    is_active: bool = Field(default=True, description="활성 상태")

