"""
Teacher's Talk Script 자동 생성기
5단계 구조의 교사 대본 생성
"""

from typing import List
from models import Unit, ShortStory, TeacherTalkScript


class TeacherScriptGenerator:
    """Teacher's Talk Script 자동 생성 클래스"""
    
    def __init__(self):
        self.cefr_level = "A1"
    
    def generate_script(self, unit: Unit, short_story: ShortStory) -> TeacherTalkScript:
        """Unit과 Short Story를 바탕으로 Teacher's Talk Script 생성"""
        
        return TeacherTalkScript(
            opening=self._generate_opening(unit, short_story),
            during_reading=self._generate_during_reading(unit, short_story),
            after_reading=self._generate_after_reading(unit, short_story),
            key_expression_practice=self._generate_key_expression_practice(unit, short_story),
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

