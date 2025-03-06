# app/routes.py
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .ai_generation import generate_image_from_prompt, image_to_base64, describe_furniture
from .image_processing import image_concater, random_pair, combine_with_style
import random
import datetime
from PIL import Image
import uuid
from flask import jsonify


main = Blueprint('main', __name__)

# 가구 스타일과 해당 폴더의 첫 번째 이미지 경로를 가져오는 함수
def get_style_preview_images():
    styles_folder = 'app/static/reference'  # 이미지들이 저장된 폴더 경로
    style_previews = {}
    
    for style in os.listdir(styles_folder):
        style_path = os.path.join(styles_folder, style)
        if os.path.isdir(style_path):
            images = [f for f in os.listdir(style_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
            if images:
                # 'static/reference/style_name/image.jpg' 형식으로 저장
                style_previews[style] = f"reference/{style}/{images[0]}"
    return style_previews

# 특정 폴더 하위의 모든 폴더 이름 가져오기 함수
def get_style_sets():
    style_dir = 'app/static/reference'  
    return [folder for folder in os.listdir(style_dir) if os.path.isdir(os.path.join(style_dir, folder))]

# 업로드 가능한 파일 확장자 제한
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('landing.html')

@main.route('/main', methods=['GET', 'POST'])
def main_page():
    style_sets = get_style_sets()
    style_previews = get_style_preview_images()

    if request.method == 'POST':
        print("POST request received")  # 디버깅용
        if 'image' not in request.files:
            print("No image in request.files")  # 디버깅용
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            print("No selected file")  # 디버깅용
            flash('No selected file')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            print("File is valid")  # 디버깅용
            filename = secure_filename(file.filename)
            input_path = os.path.join('app', 'static', 'images', 'input', filename)
            file.save(input_path)
            
            # result 페이지로 리다이렉트
            return redirect('/result')
        else:
            flash('Allowed file types are png, jpg, jpeg, gif')
            return redirect(request.url)
            
    return render_template('main.html', 
                         style_sets=style_sets, 
                         style_previews=style_previews)

@main.route('/result')
def result_page():
    try:
        # main_page에서 저장한 파일의 경로와 스타일 정보를 사용
        input_path = os.path.join('app', 'static', 'images', 'input')
        files = os.listdir(input_path)
        
        if not files:  # 입력 파일이 없으면
            return redirect(url_for('main.main_page'))
            
        # 가장 최근 파일 사용
        latest_file = max([os.path.join(input_path, f) for f in files], key=os.path.getmtime)
        
        # 출력 파일 경로 설정
        output_filename = f"output_{os.path.basename(latest_file)}"
        output_path = os.path.join('app', 'static', 'images', 'output', output_filename)
        
        # 이미지 생성
        style_dir = os.path.join('app/static/reference', request.form.get('style_set', ''))
        combined_path = combine_with_style(latest_file, style_dir, 'app/static/images/combi')
        generate_image_from_prompt(combined_path, output_path)
        
        # 결과 이미지 URL 생성
        result_image = url_for('static', filename=f'images/output/{output_filename}')
        
        # 이미지 설명 생성
        image_data = image_to_base64(output_path)
        description = describe_furniture(image_data)
        
        return render_template('result.html', 
                             result_image=result_image, 
                             description=description)
                             
    except Exception as e:
        flash(f'Error generating image: {str(e)}')
        return redirect(url_for('main.main_page'))
    

@main.route('/generate', methods=['POST'])
def generate_images():
    """
    좌측 사이드바(form)에서 이미지+스타일을 받아
    한 번에 4장 정도 결과 이미지를 생성하고,
    생성된 이미지 경로를 JSON으로 반환.
    """
    try:
        # 1) form, files에서 파일과 스타일 값 가져오기
        file = request.files.get('image')
        style_name = request.form.get('style_set', '')

        print("DEBUG: Received style_name =", style_name)
        
        if not file or file.filename == '':
            return jsonify({"error": "No image file found"}), 400
        
        # 파일 확장자 검사
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        # 2) 파일 저장 (input 폴더)
        filename = secure_filename(file.filename)
        input_path = os.path.join('app', 'static', 'images', 'input', filename)
        file.save(input_path)

        # 매 생성 요청마다 unique_id 하나를 생성
        unique_id = str(uuid.uuid4()) 

        # 3) 4장 이미지를 생성
        image_urls = []
        for i in range(4):
            style_dir = os.path.join('app', 'static', 'reference', style_name)
            print("DEBUG: style_dir =", style_dir)
            
            # 중간 합성
            combined_path = combine_with_style(input_path, style_dir, 'app/static/images/combi')
            
            # --- 핵심: unique_id + i 사용 ---
            # output_filename = f"output_{i}_{filename}"  # 기존
            # 아래처럼 바꿔서 완전히 유니크한 이름을 만듭니다:
            output_filename = f"output_{i}_{unique_id}.jpg"

            output_path = os.path.join('app', 'static', 'images', 'output', output_filename)
            generate_image_from_prompt(combined_path, output_path)
            
            url_for_image = url_for('static', filename=f'images/output/{output_filename}')
            image_urls.append(url_for_image)

        # 4) 결과(4개 이미지 경로)를 JSON으로 반환
        return jsonify({"image_urls": image_urls})

    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == "__main__":
    a = get_style_preview_images()
    b = get_style_sets()
    print(b)

    