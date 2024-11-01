# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .ai_generation import generate_image_from_prompt, upcycle_image_from_prompt, image_to_base64, describe_furniture
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

# 업로드 가능한 파일 확장자 제한
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 폼 데이터 받기
        furniture = request.form.get('furniture')
        action = request.form.get('action')  # 'generate' or 'upcycle'

        # 파일 받기
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join('app', 'static', 'images', 'input', filename)
            file.save(input_path)

            # 출력 파일 경로 설정
            output_filename = f"{os.path.splitext(filename)[0]}_output.png"
            output_path = os.path.join('app', 'static', 'images', 'output', output_filename)

            try:
                if action == 'generate':
                    generate_image_from_prompt(input_path, output_path, furniture)
                elif action == 'upcycle':
                    upcycle_image_from_prompt(input_path, output_path, furniture)
                else:
                    flash('Invalid action')
                    return redirect(request.url)
                
                # 이미지 URL 생성
                image_url = url_for('static', filename=f'images/output/{output_filename}')

                # 이미지 Base64 인코딩 (필요 시)
                # image_data = image_to_base64(output_path)

                # OpenAI API를 사용하여 설명 생성
                description = describe_furniture(image_url)

                return render_template('result.html', image_url=image_url, description=description)
            except Exception as e:
                flash(f'Error: {e}')
                return redirect(request.url)
        else:
            flash('Allowed file types are png, jpg, jpeg, gif')
            return redirect(request.url)
    return render_template('index.html')
