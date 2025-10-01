"""
초등학생용 영어 Short Story 및 Teacher's Talk Script 자동 생성 에이전트
데이터 모델 정의
"""

from pydantic import BaseModel, Field
from typing import List, Optional


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


class TeacherTalkScript(BaseModel):
    """생성된 Teacher's Talk Script를 담는 데이터 모델"""
    opening: List[str] = Field(..., description="도입부 질문들")
    during_reading: List[str] = Field(..., description="읽기 중 질문들")
    after_reading: List[str] = Field(..., description="읽기 후 질문들")
    key_expression_practice: List[str] = Field(..., description="핵심 표현 연습 가이드")
    wrap_up: List[str] = Field(..., description="마무리 멘트")


class GeneratedContent(BaseModel):
    """최종 생성 결과물을 담는 데이터 모델"""
    unit: Unit
    short_story: ShortStory
    teacher_script: TeacherTalkScript
    generation_metadata: dict = Field(default_factory=dict, description="생성 메타데이터")

