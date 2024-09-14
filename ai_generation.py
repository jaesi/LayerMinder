import os
import requests
from dotenv import load_dotenv
import datetime
import base64
import mimetypes

load_dotenv()
STABILITY_KEY = os.getenv('STABILITYAI_API_KEY')
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Stability AI를 사용하여 새로운 이미지 생성
def generate_image_from_prompt(image_path, output_path, furniture):
    # Stability AI API
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/control/style",
        headers={
            "authorization": STABILITY_KEY,
            "accept": "image/*"
        },
        files={
            "image": open(image_path, "rb"),
        },
        data={
            "prompt": f'''
    You are a professional furniture designer. 
    Please seamlessly combine elements from image to design a new, unique piece of {furniture}. 
    The final image should feature the new {furniture} against a clean white studio background with soft, 
    even lighting, presented in a style suitable for display on an online sales website.
   ''',
           'negative_prompt': "Never make it into two separate images.",
           'fidelity': 1,
            "output_format": "png"
        },
    )
    if response.status_code == 200: # successes -> file save 
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved successfully: {output_path}")
    else: # error -> print error message
        raise Exception(str(response.json()))


# image to url
def image_to_base64(image_path):
    # MIME 타입 추론
    mime_type, _ = mimetypes.guess_type(image_path)
    
    # 이미지 파일을 읽고 Base64로 인코딩
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    # 데이터 URL 형식으로 반환
    return f"data:{mime_type};base64,{encoded_string}"
    

# OpenAI를 사용하여 이미지 설명 생성
def describe_furniture(image_url):
    import openai
    openai.api_key = OPENAI_KEY
    
    client = openai()

    prompt = '''
    Please provide a detailed description of the furniture in the image, including materials, colors, sizes, and thicknesses for each part of the furniture. All measurements should be in millimeters (mm). Prioritize the top surface of the furniture for initial drafting. Describe the shape of the top surface as accurately as possible, including all dimensions and details.

    Focus on each part of the furniture, providing specific information on:

    1. Top Surface: Material, color, shape, dimensions, and thickness.
    2. Legs: Material, color, height, width, and thickness.
    3. Frame: Material, color, dimensions, and thickness.
    4. Additional Elements: Any other parts, like shelves or drawers, with their materials, colors, dimensions, and thicknesses.

    Make sure the description is precise, detailed, and comprehensive to ensure the drawing captures all the essential characteristics of the furniture.
    '''


    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a furniture designer."},
            {
                "role": "user",
                "content": prompt,
                "attachments": [{"type": "image", "url": image_url}]
            }
        ],
        max_tokens=500,
    )

    return response.choices[0].message.content
