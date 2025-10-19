"""
Vercel API 엔트리 포인트
"""

from app import app

# Vercel이 이 파일을 진입점으로 사용
handler = app
