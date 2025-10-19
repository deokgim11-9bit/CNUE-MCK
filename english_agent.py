"""
초등학생용 영어 Short Story 및 Teacher's Talk Script 자동 생성 메인 에이전트
"""

from typing import Dict, Any
from models import Unit, GeneratedContent
from story_generator import StoryGenerator
from teacher_script_generator import TeacherScriptGenerator


class EnglishTeachingAgent:
    """영어 수업 자료 자동 생성 메인 에이전트"""
    
    def __init__(self):
        self.story_generator = StoryGenerator()
        self.script_generator = TeacherScriptGenerator()
    
    def generate_teaching_materials(self, unit_data: Dict[str, Any]) -> GeneratedContent:
        """
        Unit 데이터를 받아서 Short Story와 Teacher's Talk Script를 생성
        
        Args:
            unit_data: Unit 정보가 담긴 딕셔너리
                - target_communicative_functions: List[str]
                - target_grammar_forms: List[str] 
                - target_vocabulary: List[str]
        
        Returns:
            GeneratedContent: 생성된 모든 자료를 포함한 객체
        """
        try:
            # Unit 객체 생성
            unit = Unit(**unit_data)
            
            # Short Story 생성
            short_story = self.story_generator.generate_story(unit)
            
            # Teacher's Talk Script 생성
            teacher_script = self.script_generator.generate_script(unit, short_story)
            
            # 메타데이터 생성
            metadata = {
                "generation_timestamp": self._get_current_timestamp(),
                "cefr_level": "A1",
                "target_grade": "초등학교 3-6학년",
                "story_word_count": short_story.word_count,
                "story_sentence_count": short_story.sentence_count
            }
            
            return GeneratedContent(
                unit=unit,
                short_story=short_story,
                teacher_script=teacher_script,
                generation_metadata=metadata
            )
            
        except Exception as e:
            raise Exception(f"자료 생성 중 오류가 발생했습니다: {str(e)}")
    
    def _get_current_timestamp(self) -> str:
        """현재 시간을 문자열로 반환"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def validate_unit_data(self, unit_data: Dict[str, Any]) -> bool:
        """Unit 데이터 유효성 검사"""
        required_fields = ['target_communicative_functions', 'target_grammar_forms', 'target_vocabulary']
        
        for field in required_fields:
            if field not in unit_data:
                return False
            if not isinstance(unit_data[field], list) or len(unit_data[field]) == 0:
                return False
        
        return True
    
    def get_example_unit_data(self) -> Dict[str, Any]:
        """예시 Unit 데이터 반환"""
        return {
            "target_communicative_functions": ["능력 묻고 답하기"],
            "target_grammar_forms": ["I can...", "Can you...?", "Yes, I can. / No, I can't."],
            "target_vocabulary": ["bird", "fish", "frog", "fly", "swim", "jump"]
        }
    
    def validate_generated_content(self, content: 'GeneratedContent') -> Dict[str, Any]:
        """생성된 내용의 품질을 검증"""
        quality_check = {
            "story_quality": self._check_story_quality(content.short_story),
            "script_quality": self._check_script_quality(content.teacher_script),
            "overall_score": 0
        }
        
        # 전체 점수 계산 (0-100)
        story_score = quality_check["story_quality"]["score"]
        script_score = quality_check["script_quality"]["score"]
        quality_check["overall_score"] = (story_score + script_score) // 2
        
        return quality_check
    
    def _check_story_quality(self, story: 'ShortStory') -> Dict[str, Any]:
        """이야기 품질 검증"""
        issues = []
        score = 100
        
        # 길이 검증
        if story.word_count < 50:
            issues.append("이야기가 너무 짧습니다")
            score -= 20
        elif story.word_count > 200:
            issues.append("이야기가 너무 깁니다")
            score -= 10
        
        if story.sentence_count < 5:
            issues.append("문장 수가 부족합니다")
            score -= 15
        elif story.sentence_count > 15:
            issues.append("문장 수가 너무 많습니다")
            score -= 10
        
        # 내용 검증
        if not story.title or len(story.title.strip()) < 3:
            issues.append("제목이 부적절합니다")
            score -= 10
        
        if not story.content or len(story.content.strip()) < 20:
            issues.append("내용이 부족합니다")
            score -= 25
        
        return {
            "score": max(0, score),
            "issues": issues,
            "word_count": story.word_count,
            "sentence_count": story.sentence_count
        }
    
    def _check_script_quality(self, script: 'TeacherTalkScript') -> Dict[str, Any]:
        """교사 스크립트 품질 검증"""
        issues = []
        score = 100
        
        # 각 섹션별 검증
        sections = {
            "opening": script.opening,
            "during_reading": script.during_reading,
            "after_reading": script.after_reading,
            "key_expression_practice": script.key_expression_practice,
            "wrap_up": script.wrap_up
        }
        
        for section_name, section_content in sections.items():
            if not section_content or len(section_content) == 0:
                issues.append(f"{section_name} 섹션이 비어있습니다")
                score -= 15
            elif len(section_content) < 2:
                issues.append(f"{section_name} 섹션의 내용이 부족합니다")
                score -= 10
        
        return {
            "score": max(0, score),
            "issues": issues,
            "sections_count": len([s for s in sections.values() if s and len(s) > 0])
        }

