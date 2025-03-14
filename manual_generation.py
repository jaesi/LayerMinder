''' 
구버전에서 사용하던 수동 이미지 생성기
'''

import os
import datetime
from app.image_processing import random_pair, random_image
from app.ai_generation import generate_image_from_prompt, image_to_base64, describe_furniture
# from make_drawing import create_furniture_top_view


## 이미지의 종류
# 1. Chairs
# 2. Stools & benches
# 3. Dining tables
# 4. Cafe tables
# 5. Desk
# 6. Lighting

def main(cycle=4, length=3):
    # 폴더 이름 설정
    essence_image_set = "Zen Style" ################## <<<--- Change this #1
    furniture_image_set = "wood_coffeetable" ################## <<<--- Change this #2 must include the type of furniture ex) wood_coffeetable
    furniture = str.split(furniture_image_set, '_')[1] # type of furniture to create
   
    essence_image_folder = os.path.join("app/static/reference", essence_image_set)
    furniture_image_folder = os.path.join("app/static/reference", furniture_image_set)
    output_folder = os.path.join("88_output", f'{essence_image_set}X{furniture_image_set}')
    os.makedirs(output_folder, exist_ok=True)
    
    for a in range(cycle):   
        # 1. 이미지 두 개를 무작위로 선택하고 결합
        # combined_image_path = random_pair(essence_image_folder, furniture_image_folder, output_folder)

        # 1-1. 그냥 지정한 폴더에서 랜덤한 하나의 사진을 가져오기 
        selected_image = random_image(essence_image_folder)
        # 2. Stability AI를 사용하여 새로운 가구 이미지 생성
        count = 0

        for i in range(length): # 이미지 세 장 생성
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            generated_image_path = os.path.join(output_folder, f"{timestamp}_{essence_image_set}_{furniture_image_set}.png")

            generate_image_from_prompt(selected_image, generated_image_path) 

            count += 1
            print(f"{count}/{length}")

        # 3. 생성된 이미지를 OpenAI를 사용하여 설명 생성
        # image_url = image_to_base64(generated_image_path)
        # description = describe_furniture(image_url)
        # print(description)

        # 4. 설명을 기반으로 도면 생성
        # create_furniture_top_view(description)


if __name__ == "__main__":
  main()


# # 반복을 통해서 생성 수행 
# # 1. essence 폴더셋
# essence_folder = ['balanciaga', 'creative', 'experimental', 'JasperMorrison', 'Jean Prouve', 
#                   'materials', 'modernism', 'real_modern', 'red', 'ruggy']
# # 2. furniture 폴더셋
# furniture_folder =['color_sofa', 'modern_chair', 'modern_coffeetable', 'steel&wood_chair',  'wood_stool',
#                    'stone_coffetable', 'wood_bench', 'wood_chair', 'wood_coffeetable', 'wood_shelf']

# 랜덤으로 짝을 만들어서 이미지 생성
# import random
# for i in range(10):
#     ef = random.choice(essence_folder)
#     ff = random.choice(furniture_folder)
#     main(ef, ff)
#     print(f"Completed: {ef}X{ff}")

