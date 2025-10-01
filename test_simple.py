#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("=" * 60)
print("🎓 초등학생용 영어 Short Story 및 Teacher's Talk Script 자동 생성 에이전트")
print("=" * 60)

# 간단한 테스트
try:
    from english_agent import EnglishTeachingAgent
    
    agent = EnglishTeachingAgent()
    
    # 예시 데이터
    unit_data = {
        "target_communicative_functions": ["능력 묻고 답하기"],
        "target_grammar_forms": ["I can...", "Can you...?", "Yes, I can. / No, I can't."],
        "target_vocabulary": ["bird", "fish", "frog", "fly", "swim", "jump"]
    }
    
    print("\n📝 입력 데이터:")
    print(f"목표 의사소통 기능: {unit_data['target_communicative_functions']}")
    print(f"목표 문법 형태: {unit_data['target_grammar_forms']}")
    print(f"목표 어휘: {unit_data['target_vocabulary']}")
    
    print("\n🔄 자료 생성 중...")
    
    # 자료 생성
    result = agent.generate_teaching_materials(unit_data)
    
    print("\n" + "=" * 60)
    print("📖 생성된 Short Story")
    print("=" * 60)
    print(f"제목: {result.short_story.title}")
    print(f"내용: {result.short_story.content}")
    print(f"문장 수: {result.short_story.sentence_count}개")
    print(f"단어 수: {result.short_story.word_count}개")
    
    print("\n" + "=" * 60)
    print("👩‍🏫 Teacher's Talk Script")
    print("=" * 60)
    
    print("\n1. Opening (도입):")
    for i, item in enumerate(result.teacher_script.opening, 1):
        print(f"   {i}. {item}")
    
    print("\n2. During-Reading (읽기 중):")
    for i, item in enumerate(result.teacher_script.during_reading, 1):
        print(f"   {i}. {item}")
    
    print("\n3. After-Reading (읽기 후):")
    for i, item in enumerate(result.teacher_script.after_reading, 1):
        print(f"   {i}. {item}")
    
    print("\n4. Key Expression Practice (핵심 표현 연습):")
    for i, item in enumerate(result.teacher_script.key_expression_practice, 1):
        print(f"   {i}. {item}")
    
    print("\n5. Wrap-Up (마무리):")
    for i, item in enumerate(result.teacher_script.wrap_up, 1):
        print(f"   {i}. {item}")
    
    print("\n" + "=" * 60)
    print("📊 생성 메타데이터")
    print("=" * 60)
    for key, value in result.generation_metadata.items():
        print(f"{key}: {value}")
    
    print("\n✅ 데모가 성공적으로 완료되었습니다!")
    print("웹 애플리케이션을 실행하려면 'python app.py'를 실행하세요.")
    
except Exception as e:
    print(f"\n❌ 오류가 발생했습니다: {str(e)}")
    import traceback
    traceback.print_exc()

