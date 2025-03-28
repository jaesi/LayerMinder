import os
from flask import Flask
from dotenv import load_dotenv

# Firebase 초기화 코드 : 관리자용
import firebase_admin
from firebase_admin import credentials, storage

def create_app():
    app = Flask(__name__)
    
    # Firebase 초기화
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket' : 'layerminder.firebasestorage.app'
    })

    # 사용자 input, output, combination 이미지 임시 폴더 향후 Firebase 구축 시 삭제 예정
    required_directories = [
        'app/static/images/input',
        'app/static/images/output',
        'app/static/images/combi',
    ]
    for path in required_directories:
        os.makedirs(path, exist_ok=True)

    # 환경 변수 로드 & Flask SECRET_KEY 설정
    load_dotenv()  
    secret_key = os.environ.get('SECRET_KEY')    
    if not secret_key:
        raise RuntimeError("SECRET_KEY 환경 변수가 설정되지 않았습니다.")
    app.config['SECRET_KEY'] = secret_key

    # Blueprint 등록
    from .routes import main
    app.register_blueprint(main)

    return app
