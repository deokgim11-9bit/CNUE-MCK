"""
Teacher's Talk Script 자동 생성기
5단계 구조의 교사 대본 생성
"""

import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from models import Unit, ShortStory, TeacherTalkScript, RetellingRubric

# 환경변수 로드
load_dotenv()


class TeacherScriptGenerator:
    """Teacher's Talk Script 자동 생성 클래스"""
    
    def __init__(self):
        self.cefr_level = "A1"
        api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.retelling_rubric = self._create_retelling_rubric()
    
    def generate_script(self, unit: Unit, short_story: ShortStory) -> TeacherTalkScript:
        """Unit과 Short Story를 바탕으로 Teacher's Talk Script 생성"""
        
        try:
            # LLM을 사용하여 스크립트 생성
            return self._generate_script_with_llm(unit, short_story)
        except Exception as e:
            print(f"LLM 스크립트 생성 실패, 폴백 사용: {e}")
            # LLM 실패 시 폴백으로 규칙 기반 생성 사용
            return TeacherTalkScript(
                opening=self._generate_opening(unit, short_story),
                during_reading=self._generate_during_reading(unit, short_story),
                after_reading=self._generate_after_reading(unit, short_story),
                key_expression_practice=self._generate_key_expression_practice(unit, short_story),
                retelling_guidance=self._generate_retelling_guidance(unit, short_story),
                evaluation_criteria=self._generate_evaluation_criteria(unit, short_story),
                wrap_up=self._generate_wrap_up(unit, short_story)
            )
    
    def _generate_script_with_llm(self, unit: Unit, short_story: ShortStory) -> TeacherTalkScript:
        """OpenAI API를 사용하여 교사 스크립트 생성"""
        if not self.client:
            raise Exception("OpenAI API 키가 설정되지 않았습니다.")
            
        prompt = self._create_script_prompt(unit, short_story)
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert English teacher creating teaching scripts for Korean elementary students. Always provide both English and Korean explanations."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # 응답을 파싱하여 각 섹션별로 분리
        content = response.choices[0].message.content.strip()
        return self._parse_script_response(content, unit, short_story)
    
    def _create_script_prompt(self, unit: Unit, short_story: ShortStory) -> str:
        """교사 스크립트 생성용 프롬프트 생성"""
        return f"""
        초등학생용 영어 수업을 위한 Teacher's Talk Script를 생성해주세요.
        
        수업 정보:
        - 의사소통 기능: {', '.join(unit.target_communicative_functions)}
        - 문법 형태: {', '.join(unit.target_grammar_forms)}
        - 어휘: {', '.join(unit.target_vocabulary)}
        
        이야기 내용:
        {short_story.content}
        
        다음 7개 섹션으로 구성된 스크립트를 생성해주세요:
        1. Opening (도입부): 학생들의 관심을 끌고 주제를 소개하는 질문들
        2. During Reading (읽기 중): 이야기를 읽으면서 중간에 할 질문들
        3. After Reading (읽기 후): 이해도 확인을 위한 질문들
        4. Key Expression Practice (핵심 표현 연습): 목표 문법과 어휘를 활용한 연습 활동
        5. Retelling Guidance (리텔링 가이드): 9개 영역 기반 리텔링 가이드 (Characters & Setting, Initiating Event, Internal Reaction, Attempts/Actions, Result/Resolution, Ending/Closure, Causal Connection, Temporal Connection, Global Organization)
        6. Evaluation Criteria (평가 기준): 9개 영역별 0-3점 척도 평가 기준 (총 27점 만점)
        7. Wrap Up (마무리): 수업 내용 요약 및 격려
        
        각 섹션마다 2-3개의 구체적인 질문이나 활동을 제시하고, 
        모든 영어 질문 뒤에 한국어 보조 발화를 괄호 안에 포함해주세요.
        
        JSON 형태로 응답해주세요:
        {{
            "opening": ["질문1", "질문2"],
            "during_reading": ["질문1", "질문2"],
            "after_reading": ["질문1", "질문2"],
            "key_expression_practice": ["활동1", "활동2"],
            "retelling_guidance": ["가이드1", "가이드2"],
            "evaluation_criteria": ["기준1", "기준2"],
            "wrap_up": ["마무리1", "마무리2"]
        }}
        """
    
    def _parse_script_response(self, content: str, unit: Unit, short_story: ShortStory) -> TeacherTalkScript:
        """LLM 응답을 파싱하여 TeacherTalkScript 객체 생성"""
        try:
            import json
            # JSON 부분만 추출
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            json_str = content[start_idx:end_idx]
            script_data = json.loads(json_str)
            
            return TeacherTalkScript(
                opening=script_data.get('opening', []),
                during_reading=script_data.get('during_reading', []),
                after_reading=script_data.get('after_reading', []),
                key_expression_practice=script_data.get('key_expression_practice', []),
                retelling_guidance=script_data.get('retelling_guidance', []),
                evaluation_criteria=script_data.get('evaluation_criteria', []),
                wrap_up=script_data.get('wrap_up', [])
            )
        except Exception as e:
            print(f"JSON 파싱 실패, 폴백 사용: {e}")
            # JSON 파싱 실패 시 규칙 기반 생성 사용
            return TeacherTalkScript(
                opening=self._generate_opening(unit, short_story),
                during_reading=self._generate_during_reading(unit, short_story),
                after_reading=self._generate_after_reading(unit, short_story),
                key_expression_practice=self._generate_key_expression_practice(unit, short_story),
                retelling_guidance=self._generate_retelling_guidance(unit, short_story),
                evaluation_criteria=self._generate_evaluation_criteria(unit, short_story),
                wrap_up=self._generate_wrap_up(unit, short_story)
            )
    
    def _generate_opening(self, unit: Unit, short_story: ShortStory) -> List[str]:
        """도입부 질문들 생성"""
        opening_questions = []
        
        # 첫 번째 질문: 그림이나 주제에 대한 질문
        if 'frog' in unit.target_vocabulary:
            opening_questions.append(
                "Good morning, everyone! Look at this picture. What animal do you see? "
                "(교사용 보조 발화: 여러분, 안녕하세요! 이 그림을 보세요. 어떤 동물이 보이나요?)"
            )
            opening_questions.append(
                "Right! It's a frog. What can a frog do? "
                "(교사용 보조 발화: 맞아요! 개구리예요. 개구리는 무엇을 할 수 있을까요?)"
            )
        elif 'bird' in unit.target_vocabulary:
            opening_questions.append(
                "Good morning, everyone! Look at this picture. What animal do you see? "
                "(교사용 보조 발화: 여러분, 안녕하세요! 이 그림을 보세요. 어떤 동물이 보이나요?)"
            )
            opening_questions.append(
                "Right! It's a bird. What can a bird do? "
                "(교사용 보조 발화: 맞아요! 새예요. 새는 무엇을 할 수 있을까요?)"
            )
        else:
            opening_questions.append(
                "Good morning, everyone! Look at this picture. What do you see? "
                "(교사용 보조 발화: 여러분, 안녕하세요! 이 그림을 보세요. 무엇이 보이나요?)"
            )
            opening_questions.append(
                "Great! What can this friend do? "
                "(교사용 보조 발화: 좋아요! 이 친구는 무엇을 할 수 있을까요?)"
            )
        
        return opening_questions
    
    def _generate_during_reading(self, unit: Unit, short_story: ShortStory) -> List[str]:
        """읽기 중 질문들 생성"""
        during_questions = []
        
        # 이야기 내용을 기반으로 중간 질문 생성
        sentences = short_story.content.split('. ')
        
        if len(sentences) >= 3:
            during_questions.append(
                f"(Reads the first 3 sentences) \"Who comes to the sky?\" "
                "(교사용 보조 발화: (첫 세 문장을 읽고) 누가 하늘에 나타났죠?)"
            )
        
        if len(sentences) >= 7:
            during_questions.append(
                f"(Reads up to sentence 7) \"Oh, the little friend meets another friend. What does the other friend do?\" "
                "(교사용 보조 발화: (7번째 문장까지 읽고) 와, 작은 친구가 다른 친구를 만났네요. 다른 친구는 무엇을 하고 있나요?)"
            )
        
        during_questions.append(
            f"(Reads up to the end) \"Look at the little friend. Is it happy now? Let's see!\" "
            "(교사용 보조 발화: (끝까지 읽고) 작은 친구를 보세요. 이제 행복해 보이나요? 한번 볼까요!)"
        )
        
        return during_questions
    
    def _generate_after_reading(self, unit: Unit, short_story: ShortStory) -> List[str]:
        """읽기 후 질문들 생성"""
        after_questions = []
        
        # 이해도 확인 질문들
        after_questions.append(
            "Great job listening! Now, a simple quiz. Can the big friend fly? "
            "(교사용 보조 발화: 정말 잘 들었어요! 이제 간단한 퀴즈 시간. 큰 친구는 날 수 있나요?)"
        )
        after_questions.append(
            "Good! Can the little friend swim like the other friend? "
            "(교사용 보조 발화: 좋아요! 작은 친구는 다른 친구처럼 수영할 수 있나요?)"
        )
        after_questions.append(
            "Excellent! What can the little friend do? "
            "(교사용 보조 발화: 훌륭해요! 그럼 작은 친구는 무엇을 할 수 있죠?)"
        )
        
        return after_questions
    
    def _generate_key_expression_practice(self, unit: Unit, short_story: ShortStory) -> List[str]:
        """핵심 표현 연습 가이드 생성"""
        practice_guides = []
        
        # 문법 형태를 활용한 연습 가이드
        if 'Can you' in str(unit.target_grammar_forms):
            practice_guides.append(
                "Now, let's practice! I will ask, 'Can you jump?'. You say, 'Yes, I can!' and jump! "
                "(교사용 보조 발화: 자, 이제 연습해 봐요! 선생님이 'Can you jump?'라고 물으면, 여러분은 'Yes, I can!'이라고 외치며 점프하는 거예요!)"
            )
            practice_guides.append(
                "Ready? Can you fly? "
                "(교사용 보조 발화: 준비됐나요? 날 수 있어요?)"
            )
            practice_guides.append(
                "Great! Can you swim? "
                "(교사용 보조 발화: 좋아요! 수영할 수 있어요?)"
            )
        
        # 어휘를 활용한 연습
        if unit.target_vocabulary:
            first_vocab = unit.target_vocabulary[0]
            practice_guides.append(
                f"Let's practice with '{first_vocab}'. Can you {first_vocab}? "
                f"(교사용 보조 발화: '{first_vocab}'로 연습해 봐요. {first_vocab}할 수 있어요?)"
            )
        
        return practice_guides
    
    def _generate_wrap_up(self, unit: Unit, short_story: ShortStory) -> List[str]:
        """마무리 멘트 생성"""
        wrap_up_messages = []
        
        # 수업 내용 요약 및 격려
        wrap_up_messages.append(
            "Everyone, you did a wonderful job today! We learned about friends and what they can do. "
            "And we learned to say 'I can...'! Great work! "
            "(교사용 보조 발화: 여러분, 오늘 정말 잘했어요! 친구들과 그들이 할 수 있는 것들에 대해 배웠어요. "
            "그리고 'I can...'라고 말하는 법도 배웠죠. 최고예요!)"
        )
        
        return wrap_up_messages
    
    def _create_retelling_rubric(self) -> RetellingRubric:
        """Retelling 평가 루브릭 생성 (실제 루브릭 기반)"""
        return RetellingRubric(
            characters_setting=[
                "0점: 등장인물이나 배경이 언급되지 않음",
                "1점: 등장인물이나 배경이 모호하게 언급됨",
                "2점: 등장인물과 배경이 모두 언급되지만 세부사항이 부족함",
                "3점: 등장인물과 배경이 명확하고 생생하게 소개됨 (누구, 어디서, 언제)"
            ],
            initiating_event=[
                "0점: 발단 사건/문제가 누락됨",
                "1점: 부분적으로 언급되지만 불분명함",
                "2점: 명확히 언급되지만 원인이나 결과가 부족함",
                "3점: 맥락과 중요성이 포함된 완전하고 명확한 설명"
            ],
            internal_reaction=[
                "0점: 등장인물의 생각, 감정, 목표가 포함되지 않음",
                "1점: 약간 언급되지만 이야기와 연결되지 않음",
                "2점: 언급되지만 잘 발전되지 않음",
                "3점: 동기와 감정적 깊이를 보여주는 명확한 설명"
            ],
            attempts_actions=[
                "0점: 문제 해결을 위한 등장인물의 행동이 언급되지 않음",
                "1점: 최소한이거나 불완전한 설명",
                "2점: 여러 시도가 설명되지만 순서가 불분명함",
                "3점: 시간적 흐름과 함께 명확하고 잘 정리된 행동 설명"
            ],
            result_resolution=[
                "0점: 문제/갈등의 결과가 누락됨",
                "1점: 언급되지만 관련이 없거나 혼란스러움",
                "2점: 논리적인 결과가 제시됨",
                "3점: 이전 사건들과 연결된 명확하고 논리적이며 만족스러운 해결"
            ],
            ending_closure=[
                "0점: 결말이 없거나 갑작스러운 중단",
                "1점: 약한 결말, 마무리가 부족함",
                "2점: 결말이 이야기에 어느 정도 맞음",
                "3점: 이야기의 주제를 반영하는 완전하고 논리적이며 자연스러운 마무리"
            ],
            causal_connection=[
                "0점: 인과관계 연결어 없음",
                "1점: 하나의 약하거나 부정확한 인과관계 연결",
                "2점: 여러 적절하지만 일관성 없는 연결",
                "3점: 이야기 전체에 걸쳐 빈번하고 정확한 인과관계 연결"
            ],
            temporal_connection=[
                "0점: 시간순 표지어 없음",
                "1점: 하나 또는 두 개의 기본 표지어 사용",
                "2점: 여러 올바른 표지어이지만 일부 반복",
                "3점: 시간순 표지어의 일관되고 다양하며 정확한 사용"
            ],
            global_organization=[
                "0점: 구성이 혼란스럽거나 혼재됨",
                "1점: 일부 논리적 순서가 있지만 간격이 남음",
                "2점: 대부분 일관성 있지만 작은 간격이 있음",
                "3점: 완전히 일관되고 논리적이며 매력적인 리텔링"
            ]
        )
    
    def _generate_retelling_guidance(self, unit: Unit, short_story: ShortStory) -> List[str]:
        """리텔링 가이드 생성 (9개 영역 기반)"""
        guidance = []
        
        # 1. Characters & Setting 가이드
        guidance.append(
            "Let's start by introducing the main characters and setting. Who are the main characters? Where and when does the story take place? "
            "(교사용 보조 발화: 먼저 주요 등장인물과 배경을 소개해봅시다. 주요 등장인물은 누구인가요? 이야기는 어디서, 언제 일어나나요?)"
        )
        
        # 2. Initiating Event 가이드
        guidance.append(
            "What problem or event starts the story? What happens first that makes the story begin? "
            "(교사용 보조 발화: 이야기를 시작하게 만드는 문제나 사건은 무엇인가요? 이야기가 시작되는 첫 번째 일은 무엇인가요?)"
        )
        
        # 3. Internal Reaction 가이드
        guidance.append(
            "How do the characters feel about what happened? What do they want to do? What are their goals? "
            "(교사용 보조 발화: 등장인물들은 일어난 일에 대해 어떻게 느끼나요? 무엇을 하고 싶어 하나요? 그들의 목표는 무엇인가요?)"
        )
        
        # 4. Attempts/Actions 가이드
        guidance.append(
            "What do the characters do to solve the problem? What actions do they take? Let's tell them in order. "
            "(교사용 보조 발화: 등장인물들은 문제를 해결하기 위해 무엇을 하나요? 어떤 행동을 취하나요? 순서대로 말해봅시다.)"
        )
        
        # 5. Result/Resolution 가이드
        guidance.append(
            "What happens as a result of their actions? How is the problem solved? "
            "(교사용 보조 발화: 그들의 행동의 결과로 무엇이 일어나나요? 문제는 어떻게 해결되나요?)"
        )
        
        # 6. Ending/Closure 가이드
        guidance.append(
            "How does the story end? What is the final outcome? Does it feel complete? "
            "(교사용 보조 발화: 이야기는 어떻게 끝나나요? 최종 결과는 무엇인가요? 완성된 느낌이 드나요?)"
        )
        
        # 7. Causal Connection 가이드
        guidance.append(
            "Use words like 'because', 'so', 'that's why' to connect events. Why did things happen? "
            "(교사용 보조 발화: 'because', 'so', 'that's why' 같은 단어를 사용해서 사건들을 연결해봅시다. 왜 그런 일이 일어났나요?)"
        )
        
        # 8. Temporal Connection 가이드
        guidance.append(
            "Use time words like 'first', 'then', 'next', 'after', 'finally' to show the order of events. "
            "(교사용 보조 발화: 'first', 'then', 'next', 'after', 'finally' 같은 시간 단어를 사용해서 사건의 순서를 보여봅시다.)"
        )
        
        # 목표 문법과 어휘 활용 가이드
        if unit.target_grammar_forms:
            guidance.append(
                f"Remember to use our target expressions: {', '.join(unit.target_grammar_forms)}. "
                f"(교사용 보조 발화: 우리가 배운 표현들을 기억해봐요: {', '.join(unit.target_grammar_forms)}.)"
            )
        
        if unit.target_vocabulary:
            guidance.append(
                f"Don't forget our key words: {', '.join(unit.target_vocabulary)}. "
                f"(교사용 보조 발화: 핵심 단어들을 잊지 마세요: {', '.join(unit.target_vocabulary)}.)"
            )
        
        return guidance
    
    def _generate_evaluation_criteria(self, unit: Unit, short_story: ShortStory) -> List[str]:
        """평가 기준 안내 생성 (9개 영역, 0-3점 척도)"""
        criteria = []
        
        # 1. Characters & Setting 평가 기준
        criteria.append(
            "1. Characters & Setting (등장인물과 배경) - 0-3점: "
            "Did you clearly introduce who the characters are and where/when the story takes place? "
            "(교사용 보조 발화: 등장인물이 누구인지, 이야기가 어디서 언제 일어나는지 명확히 소개했나요?)"
        )
        
        # 2. Initiating Event 평가 기준
        criteria.append(
            "2. Initiating Event/Problem (발단 사건/문제) - 0-3점: "
            "Did you explain what problem or event starts the story and why it's important? "
            "(교사용 보조 발화: 이야기를 시작하는 문제나 사건이 무엇인지, 왜 중요한지 설명했나요?)"
        )
        
        # 3. Internal Reaction 평가 기준
        criteria.append(
            "3. Internal Reaction/Goal (내적 반응/목표) - 0-3점: "
            "Did you describe how the characters feel and what they want to achieve? "
            "(교사용 보조 발화: 등장인물들이 어떻게 느끼고 무엇을 달성하고 싶어 하는지 설명했나요?)"
        )
        
        # 4. Attempts/Actions 평가 기준
        criteria.append(
            "4. Attempts/Actions (시도/행동) - 0-3점: "
            "Did you describe what the characters do to solve the problem in the right order? "
            "(교사용 보조 발화: 등장인물들이 문제를 해결하기 위해 무엇을 하는지 올바른 순서로 설명했나요?)"
        )
        
        # 5. Result/Resolution 평가 기준
        criteria.append(
            "5. Result/Resolution (결과/해결) - 0-3점: "
            "Did you explain how the problem was solved and what happened as a result? "
            "(교사용 보조 발화: 문제가 어떻게 해결되었고 그 결과로 무엇이 일어났는지 설명했나요?)"
        )
        
        # 6. Ending/Closure 평가 기준
        criteria.append(
            "6. Ending/Closure (결말/마무리) - 0-3점: "
            "Did you provide a complete and satisfying ending to the story? "
            "(교사용 보조 발화: 이야기에 완전하고 만족스러운 결말을 제공했나요?)"
        )
        
        # 7. Causal Connection 평가 기준
        criteria.append(
            "7. Causal Connection (인과관계 연결) - 0-3점: "
            "Did you use words like 'because', 'so', 'that's why' to connect events? "
            "(교사용 보조 발화: 'because', 'so', 'that's why' 같은 단어를 사용해서 사건들을 연결했나요?)"
        )
        
        # 8. Temporal Connection 평가 기준
        criteria.append(
            "8. Temporal Connection (시간순 연결) - 0-3점: "
            "Did you use time words like 'first', 'then', 'next', 'after', 'finally'? "
            "(교사용 보조 발화: 'first', 'then', 'next', 'after', 'finally' 같은 시간 단어를 사용했나요?)"
        )
        
        # 9. Global Organization 평가 기준
        criteria.append(
            "9. Global Organization & Coherence (전체 구성과 일관성) - 0-3점: "
            "Is your retelling well-organized, logical, and easy to follow? "
            "(교사용 보조 발화: 리텔링이 잘 구성되고 논리적이며 따라하기 쉬운가요?)"
        )
        
        # 총점 안내
        criteria.append(
            "총점: 0-27점 (각 영역 0-3점 × 9개 영역) "
            "21-27점: 우수, 15-20점: 양호, 9-14점: 보통, 0-8점: 개선 필요"
        )
        
        return criteria

