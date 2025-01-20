# app/__init__.py # Initialize Flask app
# app/__init__.py

import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    
     # .env 파일 로드
    load_dotenv()  # 프로젝트 루트 디렉토리에 .env 파일이 있어야 합니다.

    # 비밀 키 설정 (환경 변수 사용 권장)
    secret_key = os.environ.get('SECRET_KEY')
    
    if not secret_key:
        raise RuntimeError("SECRET_KEY 환경 변수가 설정되지 않았습니다.")
    app.config['SECRET_KEY'] = secret_key

    # Blueprint 등록
    from .routes import main
    app.register_blueprint(main)

    return app
