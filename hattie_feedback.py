"""
Hattie의 Visible Learning 연구를 바탕으로 한 종합 피드백 시스템
"The Power of Feedback" 연구 내용을 반영한 AI 피드백 생성기
"""

import PyPDF2
import os
from typing import Dict, List, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class HattieFeedbackGenerator:
    """Hattie의 피드백 이론을 바탕으로 한 종합 피드백 생성기"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.hattie_principles = self._load_hattie_principles()
    
    def _load_hattie_principles(self) -> Dict[str, Any]:
        """Hattie PDF에서 핵심 피드백 원칙들을 추출"""
        try:
            pdf_path = "Hattie power of feedback[1].pdf"
            if os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                
                # Hattie의 핵심 피드백 원칙들 추출
                return self._extract_hattie_principles(text)
            else:
                # PDF가 없을 경우 기본 Hattie 원칙들 사용
                return self._get_default_hattie_principles()
        except Exception as e:
            print(f"PDF 로딩 오류: {e}")
            return self._get_default_hattie_principles()
    
    def _extract_hattie_principles(self, text: str) -> Dict[str, Any]:
        """PDF 텍스트에서 Hattie의 피드백 원칙들 추출"""
        # 실제 PDF 내용을 분석하여 핵심 원칙들 추출
        # 여기서는 기본 원칙들을 반환하고, 실제로는 PDF 파싱 로직 구현
        return self._get_default_hattie_principles()
    
    def _get_default_hattie_principles(self) -> Dict[str, Any]:
        """Hattie의 Visible Learning 연구 기반 기본 피드백 원칙들"""
        return {
            "feedback_types": {
                "task_level": "과제 수준 피드백 - 무엇이 잘못되었는지",
                "process_level": "과정 수준 피드백 - 어떻게 개선할 수 있는지", 
                "self_regulation_level": "자기조절 수준 피드백 - 학습자가 스스로 모니터링하는 방법"
            },
            "effective_feedback_characteristics": [
                "명확하고 구체적",
                "시기적절함",
                "학습자의 수준에 맞음",
                "행동 가능한 구체적 제안 포함",
                "긍정적이면서도 건설적",
                "학습자의 자기효능감 향상"
            ],
            "feedback_questions": [
                "Where am I going? (목표는 무엇인가?)",
                "How am I going? (어떻게 하고 있는가?)",
                "Where to next? (다음에 무엇을 해야 하는가?)"
            ],
            "effect_sizes": {
                "feedback": 0.70,
                "formative_evaluation": 0.90,
                "self_questioning": 0.64,
                "self_verbalization": 0.64
            }
        }
    
    def generate_comprehensive_feedback(self, 
                                      question: str, 
                                      answer: str, 
                                      individual_scores: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Hattie의 원칙을 바탕으로 한 종합 피드백 생성"""
        
        try:
            # 개별 평가 점수들 분석
            total_score = sum(score.get('score', 0) for score in individual_scores)
            average_score = total_score / len(individual_scores) if individual_scores else 0
            
            # Hattie의 3가지 핵심 질문에 대한 피드백 생성
            hattie_prompt = f"""
            당신은 Hattie의 Visible Learning 연구를 바탕으로 한 전문 교육 컨설턴트입니다.
            
            학생의 답변을 Hattie의 피드백 이론에 따라 종합적으로 평가해주세요.
            
            질문: {question}
            학생 답변: {answer}
            개별 평가 점수들: {individual_scores}
            평균 점수: {average_score:.1f}/10
            
            Hattie의 3가지 핵심 피드백 질문에 답해주세요:
            
            1. "Where am I going?" (목표는 무엇인가?)
            - 학습 목표와 현재 성취 수준 분석
            - 목표 달성을 위한 구체적 방향 제시
            
            2. "How am I going?" (어떻게 하고 있는가?)
            - 현재 학습 상태와 강점/약점 분석
            - 과정 수준의 구체적 피드백 제공
            
            3. "Where to next?" (다음에 무엇을 해야 하는가?)
            - 다음 단계 학습 계획 제시
            - 자기조절 학습 전략 안내
            
            다음 형식으로 응답해주세요:
            {{
                "overall_assessment": "전체적인 학습 상태 평가 (한국어)",
                "hattie_analysis": {{
                    "where_am_i_going": "목표 분석 및 방향성 (한국어)",
                    "how_am_i_going": "현재 상태 분석 (한국어)", 
                    "where_to_next": "다음 단계 제안 (한국어)"
                }},
                "strengths": ["강점 1", "강점 2", "강점 3"],
                "areas_for_improvement": ["개선 영역 1", "개선 영역 2", "개선 영역 3"],
                "specific_actions": ["구체적 행동 1", "구체적 행동 2", "구체적 행동 3"],
                "self_regulation_tips": ["자기조절 팁 1", "자기조절 팁 2"],
                "encouragement": "격려 메시지 (한국어)",
                "next_goals": ["다음 목표 1", "다음 목표 2", "다음 목표 3"]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "당신은 Hattie의 Visible Learning 연구를 바탕으로 한 전문 교육 컨설턴트입니다. 학생의 학습을 돕는 건설적이고 구체적인 피드백을 제공합니다."},
                    {"role": "user", "content": hattie_prompt}
                ]
            )
            
            # JSON 응답 파싱
            feedback_text = response.choices[0].message.content.strip()
            start_idx = feedback_text.find('{')
            end_idx = feedback_text.rfind('}') + 1
            json_str = feedback_text[start_idx:end_idx]
            
            import json
            hattie_feedback = json.loads(json_str)
            
            # Hattie 원칙 추가
            hattie_feedback['hattie_principles'] = {
                'effect_size': self.hattie_principles['effect_sizes']['feedback'],
                'feedback_types': self.hattie_principles['feedback_types'],
                'characteristics': self.hattie_principles['effective_feedback_characteristics']
            }
            
            return {
                'success': True,
                'hattie_feedback': hattie_feedback,
                'average_score': average_score,
                'total_questions': len(individual_scores)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Hattie 피드백 생성 중 오류: {str(e)}',
                'fallback_feedback': self._generate_fallback_feedback(question, answer, individual_scores)
            }
    
    def _generate_fallback_feedback(self, question: str, answer: str, individual_scores: List[Dict[str, Any]]) -> Dict[str, Any]:
        """기본 피드백 생성 (API 실패 시)"""
        total_score = sum(score.get('score', 0) for score in individual_scores)
        average_score = total_score / len(individual_scores) if individual_scores else 0
        
        return {
            'overall_assessment': f'평균 점수 {average_score:.1f}/10점으로, 꾸준한 연습이 필요합니다.',
            'hattie_analysis': {
                'where_am_i_going': '영어 말하기 능력 향상이 목표입니다.',
                'how_am_i_going': f'현재 {average_score:.1f}점 수준으로, 기본적인 의사소통은 가능합니다.',
                'where_to_next': '더 많은 연습과 구체적인 피드백을 통해 실력을 향상시켜보세요.'
            },
            'strengths': ['도전하는 자세', '꾸준한 노력'],
            'areas_for_improvement': ['발음 정확도', '문법 사용', '유창성'],
            'specific_actions': ['매일 10분씩 영어로 말하기 연습', '발음 교정 연습', '문법 복습'],
            'self_regulation_tips': ['자신의 발음을 녹음해서 들어보기', '일기 쓰기로 영어 표현 연습'],
            'encouragement': '꾸준한 연습으로 분명히 실력이 향상될 것입니다!',
            'next_goals': ['발음 정확도 향상', '자연스러운 표현 사용', '유창한 대화']
        }
