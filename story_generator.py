"""
Short Story 자동 생성기
CEFR A1 수준의 초등학생용 영어 이야기 생성
"""

import re
from typing import List
from models import Unit, ShortStory


class StoryGenerator:
    """Short Story 자동 생성 클래스"""
    
    def __init__(self):
        self.max_sentences = 10
        self.min_sentences = 8
        self.max_words_per_sentence = 9
        
    def generate_story(self, unit: Unit) -> ShortStory:
        """Unit 정보를 바탕으로 Short Story 생성"""
        
        # 목표 언어 요소들을 하나의 문자열로 결합
        target_elements = []
        target_elements.extend(unit.target_communicative_functions)
        target_elements.extend(unit.target_grammar_forms)
        target_elements.extend(unit.target_vocabulary)
        
        # 이야기 생성 프롬프트 구성
        prompt = self._create_story_prompt(unit, target_elements)
        
        # 실제 구현에서는 OpenAI API를 사용하지만, 
        # 데모를 위해 규칙 기반 생성으로 대체
        story_content = self._generate_story_content(unit, target_elements)
        
        # 문장 수와 단어 수 계산
        sentences = self._split_into_sentences(story_content)
        word_count = len(story_content.split())
        sentence_count = len(sentences)
        
        return ShortStory(
            title=self._generate_title(unit),
            content=story_content,
            word_count=word_count,
            sentence_count=sentence_count
        )
    
    def _create_story_prompt(self, unit: Unit, target_elements: List[str]) -> str:
        """이야기 생성용 프롬프트 생성"""
        prompt = f"""
        초등학생용 영어 Short Story를 생성해주세요.
        
        요구사항:
        1. 8-10개의 문장으로 구성
        2. 각 문장은 최대 9개의 단어
        3. CEFR A1 수준의 쉬운 영어
        4. 한국 초등학생의 정서에 맞는 긍정적인 내용
        
        포함해야 할 요소:
        - 의사소통 기능: {', '.join(unit.target_communicative_functions)}
        - 문법 형태: {', '.join(unit.target_grammar_forms)}
        - 어휘: {', '.join(unit.target_vocabulary)}
        
        이야기는 간단하고 명확하며, 학생들이 쉽게 이해할 수 있어야 합니다.
        """
        return prompt
    
    def _generate_story_content(self, unit: Unit, target_elements: List[str]) -> str:
        """규칙 기반으로 이야기 내용 생성 (데모용)"""
        
        # 어휘를 활용한 기본 이야기 템플릿
        vocabulary = unit.target_vocabulary
        grammar_forms = unit.target_grammar_forms
        
        # 동물이나 캐릭터 중심의 이야기 생성
        story_parts = []
        
        # 첫 번째 문장: 캐릭터 소개
        if any(word in vocabulary for word in ['bird', 'fish', 'frog', 'cat', 'dog']):
            animal = next((word for word in vocabulary if word in ['bird', 'fish', 'frog', 'cat', 'dog']), 'animal')
            story_parts.append(f"A little {animal} sits on a leaf.")
        else:
            story_parts.append("A little friend sits on a leaf.")
        
        # 두 번째 문장: 다른 캐릭터 등장
        if 'bird' in vocabulary:
            story_parts.append("A big bird flies in the sky.")
        elif 'fish' in vocabulary:
            story_parts.append("A big fish swims in the pond.")
        else:
            story_parts.append("A big friend comes near.")
        
        # 세 번째 문장: 만남
        story_parts.append("The little friend sees the big friend.")
        
        # 네 번째 문장: 질문 (Can you...? 패턴)
        if 'Can you' in str(grammar_forms):
            action = vocabulary[0] if vocabulary else 'jump'
            story_parts.append(f'"Can you {action}?" asks the little friend.')
        
        # 다섯 번째 문장: 답변 (Yes, I can 패턴)
        if 'Yes, I can' in str(grammar_forms):
            action = vocabulary[0] if vocabulary else 'jump'
            story_parts.append(f'"Yes, I can," says the big friend.')
        
        # 여섯 번째 문장: 또 다른 캐릭터 등장
        if len(vocabulary) > 1:
            second_action = vocabulary[1] if len(vocabulary) > 1 else 'run'
            story_parts.append(f'A third friend {second_action}s nearby.')
        
        # 일곱 번째 문장: 또 다른 질문
        if len(vocabulary) > 1:
            second_action = vocabulary[1] if len(vocabulary) > 1 else 'run'
            story_parts.append(f'"Can you {second_action}?" asks the little friend.')
        
        # 여덟 번째 문장: 답변
        if len(vocabulary) > 1:
            second_action = vocabulary[1] if len(vocabulary) > 1 else 'run'
            story_parts.append(f'"Yes, I can," says the third friend.')
        
        # 아홉 번째 문장: 감정 표현
        if any(word in vocabulary for word in ['happy', 'sad', 'excited']):
            emotion = next((word for word in vocabulary if word in ['happy', 'sad', 'excited']), 'happy')
            story_parts.append(f"The little friend is {emotion}.")
        else:
            story_parts.append("The little friend is happy.")
        
        # 열 번째 문장: 마무리 (I can... 패턴)
        if 'I can' in str(grammar_forms):
            action = vocabulary[0] if vocabulary else 'jump'
            story_parts.append(f'The little friend says, "I can {action}!"')
        
        return ' '.join(story_parts)
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """텍스트를 문장 단위로 분리"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _generate_title(self, unit: Unit) -> str:
        """이야기 제목 생성"""
        if 'frog' in unit.target_vocabulary:
            return "The Little Frog"
        elif 'bird' in unit.target_vocabulary:
            return "The Little Bird"
        elif 'fish' in unit.target_vocabulary:
            return "The Little Fish"
        else:
            return "The Little Friend"

