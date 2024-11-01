import os
import random
from PIL import Image
import datetime

# 이미지 컨케터
def image_concater(first_image_path, second_image_path, output_path):
    # 이미지 열기
    image1 = Image.open(first_image_path)
    image2 = Image.open(second_image_path)

    # 이미지 크기 조정
    # 가로로 결합할 경우, 높이를 맞춥니다.
    new_height = max(image1.height, image2.height)

    # Image concatenation
    # I want the separation between the two images to be 10 pixels
    separation = 50

    new_width = image1.width + image2.width + separation
    combined_image = Image.new('RGB', (new_width, new_height))

    # 만약 비율이 1: 2.5 이상인 경우, 세로로 결합
    if combined_image.width / combined_image.height < 2.5:
        combined_image.paste(image1, (0, 0))
        combined_image.paste(image2, (image1.width + separation, 0))

    # 그렇지 않으면 세로로 결합
    else:
    # 세로로 결합할 경우, 너비를 맞춥니다.
        new_width = max(image1.width, image2.width)

        # 이미지를 결합
        new_height = image1.height + image2.height + separation
        combined_image = Image.new('RGB', (new_width, new_height))
        combined_image.paste(image1, (0, 0))
        combined_image.paste(image2, (0, image1.height+ separation))

    combined_image.save(output_path)
    print(f"Combined image saved at {output_path}")

# 랜덤 페어 생성
def random_pair(first_image_set, second_image_set, output_folder):
    # 폴더 안에 essence와, 가구 두 폴더에서 각각 하나의 이미지를 선택하여 결합
    essence_images = os.listdir(os.path.join(first_image_set))
    furniture_images = os.listdir(os.path.join(second_image_set))
    essence_image = random.choice(essence_images)
    furniture_image = random.choice(furniture_images)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # 이미지 경로 설정
    first_image = os.path.join(first_image_set, essence_image)
    second_image = os.path.join(second_image_set, furniture_image)
    # output full path to be saved
    output_path = os.path.join(output_folder, f'{timestamp}_combined.png')

    # 수직 결합 시도하고 안될 시 수평 결합

    image_concater(first_image, second_image, output_path)
    return output_path

# 사용자 이미지와 스타일 세트 이미지 결합 함수

def combine_with_style(user_image_path, style_image_set_folder, output_folder):
    try:
        # 스타일 세트 폴더에서 랜덤 이미지 선택
        style_images = [f for f in os.listdir(style_image_set_folder) if os.path.isfile(os.path.join(style_image_set_folder, f))]
        if not style_images:
            raise ValueError("스타일 세트 폴더에 이미지가 없습니다.")
        style_image = random.choice(style_images)
        style_image_path = os.path.join(style_image_set_folder, style_image)

        # 출력 파일 경로 설정
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_folder, f'{timestamp}_combined.png')

        # 이미지 결합
        image_concater(user_image_path, style_image_path, output_path)
        return output_path # 출력
    
    except Exception as e:
        print(f"스타일 이미지 결합 중 오류 발생: {e}")
        raise
    return output_path
