"""
Vercel API 엔트리 포인트
"""

import sys
import os

# 상위 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel이 이 파일을 진입점으로 사용
handler = app
