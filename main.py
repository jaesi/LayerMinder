import os
import datetime
from image_processing import random_pair
from ai_generation import generate_image_from_prompt, image_to_base64, describe_furniture
# from make_drawing import create_furniture_top_view

# 맛을 섞듯이 고를 수 있도록 해야겠다. modern_chair, 등 해보고 잘나오는 조합들로 만들기

def main():
    # 폴더 이름 설정
    image_set = "funk" # style setting
    furniture = "table" # type of furniture to create

    image_set_folder = os.path.join("00_ref", image_set)
    output_folder = os.path.join("88_output", image_set)
    os.makedirs(output_folder, exist_ok=True)
    
    # 1. 이미지 두 개를 무작위로 선택하고 결합
    combined_image_path = random_pair(image_set_folder, output_folder)

    # 2. Stability AI를 사용하여 새로운 가구 이미지 생성
    for i in range(3): # 이미지 세 장 생성
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        generated_image_path = os.path.join(output_folder, f"{timestamp}_{image_set}.png")
        generate_image_from_prompt(combined_image_path, generated_image_path, furniture) 

        # 3. 생성된 이미지를 OpenAI를 사용하여 설명 생성
        # image_url = image_to_base64(generated_image_path)
        # description = describe_furniture(image_url)
        # print(description)

        # 4. 설명을 기반으로 도면 생성
        # create_furniture_top_view(description)

if __name__ == "__main__":
    main()
