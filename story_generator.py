"""
Short Story 자동 생성기
CEFR A1 수준의 초등학생용 영어 이야기 생성
"""

import re
import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from models import Unit, ShortStory

# 환경변수 로드
load_dotenv()


class StoryGenerator:
    """Short Story 자동 생성 클래스"""
    
    def __init__(self):
        self.max_sentences = 10
        self.min_sentences = 8
        self.max_words_per_sentence = 9
        api_key = os.getenv('OPENAI_API_KEY')
        print(f"API Key loaded: {'Yes' if api_key else 'No'}")
        print(f"API Key length: {len(api_key) if api_key else 0}")
        self.client = OpenAI(api_key=api_key) if api_key else None
        
    def generate_story(self, unit: Unit) -> ShortStory:
        """Unit 정보를 바탕으로 Short Story 생성"""
        
        print(f"Story generation started for unit: {unit.target_vocabulary}")
        
        try:
            # OpenAI API를 사용하여 이야기 생성
            print("Attempting LLM generation...")
            story_content = self._generate_story_with_llm(unit)
            print(f"LLM generation successful. Content length: {len(story_content)}")
        except Exception as e:
            print(f"LLM 생성 실패, 폴백 사용: {e}")
            # LLM 실패 시 폴백으로 규칙 기반 생성 사용
            story_content = self._generate_story_content(unit, unit.target_vocabulary)
            print(f"Fallback generation used. Content length: {len(story_content)}")
        
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
    
    def _generate_story_with_llm(self, unit: Unit) -> str:
        """OpenAI API를 사용하여 이야기 생성"""
        if not self.client:
            raise Exception("OpenAI API 키가 설정되지 않았습니다.")
            
        prompt = self._create_story_prompt(unit, unit.target_vocabulary)
        print(f"Generated prompt: {prompt[:200]}...")
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert English teacher creating educational stories for Korean elementary students."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.choices[0].message.content.strip()
            print(f"LLM response received. Length: {len(content)}")
            print(f"LLM content preview: {content[:100]}...")
            return content
            
        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            raise e
    
    def _create_story_prompt(self, unit: Unit, target_elements: List[str]) -> str:
        """이야기 생성용 프롬프트 생성"""
        prompt = f"""Create a short English story for Korean elementary students (CEFR A1 level).

REQUIREMENTS:
- Write exactly 8-10 sentences
- Each sentence must have maximum 9 words
- Use simple, clear English that 3rd-6th grade Korean students can understand
- Create a positive, engaging story suitable for Korean children
- Include a clear beginning, middle, and end

MUST INCLUDE THESE ELEMENTS:
- Communication function: {', '.join(unit.target_communicative_functions)}
- Grammar patterns: {', '.join(unit.target_grammar_forms)}
- Vocabulary words: {', '.join(unit.target_vocabulary)}

STORY STRUCTURE:
1. Introduce characters and setting
2. Present a simple problem or situation
3. Show characters trying to solve it
4. Resolve the problem
5. End with a positive message

Make sure to naturally incorporate ALL the target vocabulary and grammar patterns into the story. The story should be educational but also fun and engaging for young learners.

Write ONLY the story content, no title or additional text."""
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

