"""
Rewrite 활동 생성기
1단계: 어휘 빈칸 채우기 활동
2단계: 전체 스토리 다시 쓰기 활동
Story Grammar 루브릭 기반 채점 및 Hattie 프레임워크 피드백
"""

import re
import random
from typing import List, Dict, Any, Tuple
from models import StoryGrammarRubric, RewriteActivity
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class RewriteGenerator:
    """Rewrite 활동 생성 및 평가 클래스"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.story_grammar_rubric = self._create_story_grammar_rubric()
    
    def _create_story_grammar_rubric(self) -> StoryGrammarRubric:
        """Story Grammar 루브릭 생성"""
        return StoryGrammarRubric(
            setting=[
                "배경이 명확하게 제시됨 (시간, 장소)",
                "등장인물이 적절히 소개됨",
                "상황 설정이 이해하기 쉬움"
            ],
            characters=[
                "주인공의 성격이 일관되게 묘사됨",
                "조연 인물들이 적절히 활용됨",
                "인물 간의 관계가 명확함"
            ],
            problem=[
                "갈등이나 문제가 명확함",
                "문제의 원인이 제시됨",
                "문제의 중요성이 드러남"
            ],
            events=[
                "사건들이 논리적 순서로 전개됨",
                "각 사건이 명확하게 묘사됨",
                "사건 간의 연결이 자연스러움"
            ],
            resolution=[
                "문제가 적절히 해결됨",
                "해결 과정이 합리적임",
                "결말이 만족스러움"
            ],
            theme=[
                "주제가 명확하게 드러남",
                "교훈이나 메시지가 적절함",
                "독자에게 의미 있는 메시지 전달"
            ],
            vocabulary=[
                "어휘 사용이 적절하고 정확함",
                "표현이 다양하고 풍부함",
                "초등학생 수준에 맞는 어휘 사용"
            ],
            grammar=[
                "문법이 정확함",
                "문장 구조가 다양함",
                "시제 일치가 정확함"
            ],
            coherence=[
                "전체적인 일관성이 유지됨",
                "문단 간 연결이 자연스러움",
                "이야기 흐름이 매끄러움"
            ]
        )
    
    def create_vocabulary_fill_activity(self, story_content: str, num_blanks: int = 5) -> RewriteActivity:
        """1단계: 어휘 빈칸 채우기 활동 생성 (단일 단어 30-40%, collocation 60-70%)"""
        try:
            # 단일 단어와 collocation 추출
            single_words, collocations = self._extract_words_and_collocations(story_content)
            
            # 빈칸 수에 따른 비율 계산
            single_word_count = max(1, int(num_blanks * 0.35))  # 35% (30-40% 범위)
            collocation_count = num_blanks - single_word_count
            
            # 선택할 항목들 결정
            selected_items = []
            
            # 단일 단어 선택
            if single_words and single_word_count > 0:
                selected_single_words = random.sample(single_words, min(single_word_count, len(single_words)))
                selected_items.extend([(word, 'single') for word in selected_single_words])
            
            # collocation 선택
            if collocations and collocation_count > 0:
                selected_collocations = random.sample(collocations, min(collocation_count, len(collocations)))
                selected_items.extend([(collocation, 'collocation') for collocation in selected_collocations])
            
            # 빈칸이 있는 스토리 생성
            modified_story = story_content
            blanks = []
            
            for i, (item, item_type) in enumerate(selected_items):
                blank_id = f"blank_{i+1}"
                modified_story = modified_story.replace(item, f"__{blank_id}__", 1)
                blanks.append({
                    "id": blank_id,
                    "correct_answer": item,
                    "type": item_type,
                    "position": modified_story.find(f"__{blank_id}__")
                })
            
            return RewriteActivity(
                activity_type="vocabulary_fill",
                original_story=story_content,
                modified_story=modified_story,
                blanks=blanks
            )
            
        except Exception as e:
            print(f"어휘 빈칸 채우기 활동 생성 오류: {e}")
            return self._create_fallback_vocabulary_activity(story_content)
    
    def create_full_rewrite_activity(self, story_content: str) -> RewriteActivity:
        """2단계: 전체 스토리 다시 쓰기 활동 생성"""
        try:
            # 스토리 구조 분석
            story_structure = self._analyze_story_structure(story_content)
            
            # 다시 쓰기 가이드 생성
            rewrite_guide = self._generate_rewrite_guide(story_structure)
            
            return RewriteActivity(
                activity_type="full_rewrite",
                original_story=story_content,
                modified_story="",  # 빈 텍스트로 시작
                blanks=[],
                student_answer=""
            )
            
        except Exception as e:
            print(f"전체 다시 쓰기 활동 생성 오류: {e}")
            return RewriteActivity(
                activity_type="full_rewrite",
                original_story=story_content,
                modified_story="",
                blanks=[],
                student_answer=""
            )
    
    def _extract_important_words(self, text: str) -> List[str]:
        """중요한 어휘들 추출"""
        # 문장을 단어로 분리
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # 불용어 제거
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        # 중요한 단어들만 필터링 (명사, 동사, 형용사 등)
        important_words = []
        for word in words:
            if word not in stop_words and len(word) > 2:
                important_words.append(word)
        
        # 중복 제거
        return list(set(important_words))
    
    def _extract_words_and_collocations(self, text: str) -> Tuple[List[str], List[str]]:
        """단일 단어와 collocation 추출"""
        # 문장을 단어로 분리 (대소문자 유지)
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        
        # 불용어 제거
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        # 단일 단어 추출
        single_words = []
        for word in words:
            if word.lower() not in stop_words and len(word) > 2:
                single_words.append(word)
        
        # collocation 추출 (2-4단어 조합)
        collocations = []
        
        # 2단어 collocation
        for i in range(len(words) - 1):
            if words[i].lower() not in stop_words and words[i+1].lower() not in stop_words:
                collocation = f"{words[i]} {words[i+1]}"
                if len(collocation) > 5:  # 최소 길이 체크
                    collocations.append(collocation)
        
        # 3단어 collocation
        for i in range(len(words) - 2):
            if (words[i].lower() not in stop_words and 
                words[i+1].lower() not in stop_words and 
                words[i+2].lower() not in stop_words):
                collocation = f"{words[i]} {words[i+1]} {words[i+2]}"
                if len(collocation) > 8:  # 최소 길이 체크
                    collocations.append(collocation)
        
        # 4단어 collocation (구문)
        for i in range(len(words) - 3):
            if (words[i].lower() not in stop_words and 
                words[i+1].lower() not in stop_words and 
                words[i+2].lower() not in stop_words and
                words[i+3].lower() not in stop_words):
                collocation = f"{words[i]} {words[i+1]} {words[i+2]} {words[i+3]}"
                if len(collocation) > 12:  # 최소 길이 체크
                    collocations.append(collocation)
        
        # 중복 제거
        single_words = list(set(single_words))
        collocations = list(set(collocations))
        
        return single_words, collocations
    
    def _is_partial_match(self, correct_answer: str, student_answer: str) -> bool:
        """부분 매칭 확인 (collocation 평가용)"""
        correct_words = correct_answer.split()
        student_words = student_answer.split()
        
        if len(correct_words) != len(student_words):
            return False
        
        # 50% 이상의 단어가 일치하면 부분 점수
        matches = sum(1 for c, s in zip(correct_words, student_words) if c == s)
        return matches >= len(correct_words) * 0.5
    
    def _analyze_story_structure(self, story_content: str) -> Dict[str, Any]:
        """스토리 구조 분석"""
        try:
            prompt = f"""
            다음 스토리의 구조를 분석해주세요:
            
            {story_content}
            
            다음 형식으로 분석해주세요:
            {{
                "setting": "배경 설정",
                "characters": "등장인물들",
                "problem": "주요 문제나 갈등",
                "events": ["사건1", "사건2", "사건3"],
                "resolution": "해결 과정",
                "theme": "주제나 교훈"
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "당신은 스토리 구조 분석 전문가입니다."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            import json
            analysis_text = response.choices[0].message.content.strip()
            start_idx = analysis_text.find('{')
            end_idx = analysis_text.rfind('}') + 1
            json_str = analysis_text[start_idx:end_idx]
            
            return json.loads(json_str)
            
        except Exception as e:
            print(f"스토리 구조 분석 오류: {e}")
            return {
                "setting": "배경 설정을 분석할 수 없습니다.",
                "characters": "등장인물을 분석할 수 없습니다.",
                "problem": "주요 문제를 분석할 수 없습니다.",
                "events": ["사건 분석 실패"],
                "resolution": "해결 과정을 분석할 수 없습니다.",
                "theme": "주제를 분석할 수 없습니다."
            }
    
    def _generate_rewrite_guide(self, story_structure: Dict[str, Any]) -> str:
        """다시 쓰기 가이드 생성"""
        return f"""
        다음 구조를 참고하여 스토리를 다시 써보세요:
        
        📍 배경 설정: {story_structure.get('setting', '')}
        👥 등장인물: {story_structure.get('characters', '')}
        ⚠️ 주요 문제: {story_structure.get('problem', '')}
        📝 사건들: {', '.join(story_structure.get('events', []))}
        ✅ 해결: {story_structure.get('resolution', '')}
        💡 주제: {story_structure.get('theme', '')}
        
        위의 구조를 바탕으로 8-10문장의 완전한 스토리를 작성해주세요.
        """
    
    def _create_fallback_vocabulary_activity(self, story_content: str) -> RewriteActivity:
        """기본 어휘 빈칸 채우기 활동 생성 (fallback)"""
        try:
            # 단일 단어와 collocation 추출 시도
            single_words, collocations = self._extract_words_and_collocations(story_content)
            
            # 최소 3개 항목 선택
            selected_items = []
            
            # 단일 단어 1개 선택
            if single_words:
                selected_items.append((single_words[0], 'single'))
            
            # collocation 2개 선택
            if collocations and len(collocations) >= 2:
                selected_items.extend([(collocations[0], 'collocation'), (collocations[1], 'collocation')])
            elif collocations:
                selected_items.append((collocations[0], 'collocation'))
            
            # 빈칸이 있는 스토리 생성
            modified_story = story_content
            blanks = []
            
            for i, (item, item_type) in enumerate(selected_items):
                blank_id = f"blank_{i+1}"
                modified_story = modified_story.replace(item, f"__{blank_id}__", 1)
                blanks.append({
                    "id": blank_id,
                    "correct_answer": item,
                    "type": item_type,
                    "position": modified_story.find(f"__{blank_id}__")
                })
            
            return RewriteActivity(
                activity_type="vocabulary_fill",
                original_story=story_content,
                modified_story=modified_story,
                blanks=blanks
            )
            
        except Exception as e:
            print(f"Fallback 어휘 활동 생성 오류: {e}")
            # 최후의 수단: 기본 단어만 사용
            words = re.findall(r'\b[a-zA-Z]+\b', story_content)
            important_words = [word for word in words if len(word) > 3 and word.lower() not in ['the', 'and', 'was', 'were', 'this', 'that']]
            
            if len(important_words) >= 3:
                selected_words = important_words[:3]
                modified_story = story_content
                blanks = []
                
                for i, word in enumerate(selected_words):
                    blank_id = f"blank_{i+1}"
                    modified_story = modified_story.replace(word, f"__{blank_id}__", 1)
                    blanks.append({
                        "id": blank_id,
                        "correct_answer": word,
                        "type": "single",
                        "position": modified_story.find(f"__{blank_id}__")
                    })
            else:
                modified_story = story_content
                blanks = []
            
            return RewriteActivity(
                activity_type="vocabulary_fill",
                original_story=story_content,
                modified_story=modified_story,
                blanks=blanks
            )
    
    def evaluate_vocabulary_fill(self, activity: RewriteActivity, student_answers: Dict[str, str]) -> RewriteActivity:
        """어휘 빈칸 채우기 평가"""
        try:
            # 정답과 학생 답안 비교
            correct_count = 0
            total_blanks = len(activity.blanks)
            
            for blank in activity.blanks:
                blank_id = blank["id"]
                correct_answer = blank["correct_answer"].lower()
                student_answer = student_answers.get(blank_id, "").lower().strip()
                blank_type = blank.get("type", "single")
                
                # 정확한 매칭 확인
                if student_answer == correct_answer:
                    correct_count += 1
                # 부분 점수 (collocation의 경우)
                elif blank_type == "collocation" and self._is_partial_match(correct_answer, student_answer):
                    correct_count += 0.5
            
            # 점수 계산 (0-4점 척도)
            if total_blanks > 0:
                score = (correct_count / total_blanks) * 4
            else:
                score = 0
            
            # Story Grammar 루브릭 기반 평가
            rubric_scores = self._evaluate_with_story_grammar(
                activity.original_story,
                activity.modified_story,
                student_answers,
                "vocabulary_fill"
            )
            
            # Hattie 프레임워크 피드백 생성
            hattie_feedback = self._generate_hattie_feedback(
                activity.original_story,
                student_answers,
                rubric_scores,
                "vocabulary_fill"
            )
            
            # 활동 업데이트
            activity.student_answer = str(student_answers)
            activity.score = rubric_scores
            activity.total_score = score
            activity.feedback = hattie_feedback
            
            return activity
            
        except Exception as e:
            print(f"어휘 빈칸 채우기 평가 오류: {e}")
            return activity
    
    def evaluate_full_rewrite(self, activity: RewriteActivity, student_story: str) -> RewriteActivity:
        """전체 스토리 다시 쓰기 평가"""
        try:
            # Story Grammar 루브릭 기반 평가
            rubric_scores = self._evaluate_with_story_grammar(
                activity.original_story,
                student_story,
                {},
                "full_rewrite"
            )
            
            # 전체 점수 계산 (0-4점 척도)
            total_score = sum(rubric_scores.values()) / len(rubric_scores) if rubric_scores else 0
            
            # Hattie 프레임워크 피드백 생성
            hattie_feedback = self._generate_hattie_feedback(
                activity.original_story,
                student_story,
                rubric_scores,
                "full_rewrite"
            )
            
            # 활동 업데이트
            activity.student_answer = student_story
            activity.score = rubric_scores
            activity.total_score = total_score
            activity.feedback = hattie_feedback
            
            return activity
            
        except Exception as e:
            print(f"전체 다시 쓰기 평가 오류: {e}")
            return activity
    
    def _evaluate_with_story_grammar(self, original_story: str, student_content: str, student_answers: Dict[str, str], activity_type: str) -> Dict[str, float]:
        """Story Grammar 루브릭 기반 평가"""
        try:
            prompt = f"""
            다음은 Story Grammar 루브릭을 사용한 평가입니다.
            
            원본 스토리: {original_story}
            학생 작품: {student_content}
            활동 유형: {activity_type}
            
            다음 9개 영역을 0-4점 척도로 평가해주세요:
            1. Setting (배경, 등장인물 소개)
            2. Characters (주인공, 조연, 성격 묘사)
            3. Problem (갈등, 문제 상황)
            4. Events (사건의 전개, 순서)
            5. Resolution (해결, 결말)
            6. Theme (주제, 교훈)
            7. Vocabulary (어휘 사용, 표현)
            8. Grammar (문법, 문장 구조)
            9. Coherence (일관성, 연결성)
            
            다음 형식으로 응답해주세요:
            {{
                "setting": 3.5,
                "characters": 2.8,
                "problem": 3.2,
                "events": 3.0,
                "resolution": 2.5,
                "theme": 3.8,
                "vocabulary": 3.3,
                "grammar": 2.9,
                "coherence": 3.1
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "당신은 Story Grammar 루브릭을 사용한 평가 전문가입니다."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            import json
            evaluation_text = response.choices[0].message.content.strip()
            start_idx = evaluation_text.find('{')
            end_idx = evaluation_text.rfind('}') + 1
            json_str = evaluation_text[start_idx:end_idx]
            
            return json.loads(json_str)
            
        except Exception as e:
            print(f"Story Grammar 평가 오류: {e}")
            return {
                "setting": 2.0,
                "characters": 2.0,
                "problem": 2.0,
                "events": 2.0,
                "resolution": 2.0,
                "theme": 2.0,
                "vocabulary": 2.0,
                "grammar": 2.0,
                "coherence": 2.0
            }
    
    def _generate_hattie_feedback(self, original_story: str, student_content: str, rubric_scores: Dict[str, float], activity_type: str) -> Dict[str, Any]:
        """Hattie 프레임워크 기반 피드백 생성"""
        try:
            prompt = f"""
            Hattie의 Visible Learning 이론을 바탕으로 다음 학습 활동에 대한 피드백을 생성해주세요.
            
            원본 스토리: {original_story}
            학생 작품: {student_content}
            활동 유형: {activity_type}
            루브릭 점수: {rubric_scores}
            
            Hattie의 3가지 핵심 질문에 답해주세요:
            1. Where am I going? (목표는 무엇인가?)
            2. How am I going? (어떻게 하고 있는가?)
            3. Where to next? (다음에 무엇을 해야 하는가?)
            
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
                    {"role": "system", "content": "당신은 Hattie의 Visible Learning 연구를 바탕으로 한 전문 교육 컨설턴트입니다."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            import json
            feedback_text = response.choices[0].message.content.strip()
            start_idx = feedback_text.find('{')
            end_idx = feedback_text.rfind('}') + 1
            json_str = feedback_text[start_idx:end_idx]
            
            return json.loads(json_str)
            
        except Exception as e:
            print(f"Hattie 피드백 생성 오류: {e}")
            return {
                "overall_assessment": "학습 활동을 잘 수행했습니다.",
                "hattie_analysis": {
                    "where_am_i_going": "스토리 쓰기 능력 향상이 목표입니다.",
                    "how_am_i_going": "현재 기본적인 수준에서 학습하고 있습니다.",
                    "where_to_next": "더 많은 연습과 피드백을 통해 실력을 향상시켜보세요."
                },
                "strengths": ["도전하는 자세", "꾸준한 노력"],
                "areas_for_improvement": ["문법 정확도", "어휘 사용", "스토리 구성"],
                "specific_actions": ["매일 영어로 일기 쓰기", "문법 복습", "어휘 학습"],
                "self_regulation_tips": ["자신의 작품을 다시 읽어보기", "친구와 서로 피드백 주고받기"],
                "encouragement": "꾸준한 연습으로 분명히 실력이 향상될 것입니다!",
                "next_goals": ["문법 정확도 향상", "어휘력 증진", "창의적 표현 사용"]
            }
