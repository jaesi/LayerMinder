# app/__init__.py # Initialize Flask app
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app():
    app = Flask(__name__)

    # 환경 변수 로드
    from dotenv import load_dotenv
    load_dotenv()

    # Rate Limiter 설정: IP당 분당 60 요청 제한
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["60 per minute"]
    )

    # 라우트 블루프린트 등록
    from .routes import main
    app.register_blueprint(main)

    return app
