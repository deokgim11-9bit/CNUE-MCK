"""
Flask 웹 애플리케이션
초등학생용 영어 Short Story 및 Teacher's Talk Script 자동 생성 에이전트
"""

from flask import Flask, render_template, request, jsonify
from english_agent import EnglishTeachingAgent
import json

app = Flask(__name__)
agent = EnglishTeachingAgent()

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_materials():
    """수업 자료 생성 API"""
    try:
        data = request.get_json()
        
        # 데이터 유효성 검사
        if not agent.validate_unit_data(data):
            return jsonify({
                'success': False,
                'error': '입력 데이터가 올바르지 않습니다. 모든 필드를 확인해주세요.'
            }), 400
        
        # 자료 생성
        result = agent.generate_teaching_materials(data)
        
        # 결과를 JSON으로 변환
        result_dict = {
            'success': True,
            'data': {
                'unit': {
                    'target_communicative_functions': result.unit.target_communicative_functions,
                    'target_grammar_forms': result.unit.target_grammar_forms,
                    'target_vocabulary': result.unit.target_vocabulary
                },
                'short_story': {
                    'title': result.short_story.title,
                    'content': result.short_story.content,
                    'word_count': result.short_story.word_count,
                    'sentence_count': result.short_story.sentence_count
                },
                'teacher_script': {
                    'opening': result.teacher_script.opening,
                    'during_reading': result.teacher_script.during_reading,
                    'after_reading': result.teacher_script.after_reading,
                    'key_expression_practice': result.teacher_script.key_expression_practice,
                    'wrap_up': result.teacher_script.wrap_up
                },
                'metadata': result.generation_metadata
            }
        }
        
        return jsonify(result_dict)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/example')
def get_example():
    """예시 데이터 반환"""
    example_data = agent.get_example_unit_data()
    return jsonify({
        'success': True,
        'data': example_data
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

