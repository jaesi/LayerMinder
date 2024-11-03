import streamlit as st
import os
from PIL import Image
from ai_generation import generate_image_from_prompt, describe_furniture, image_to_base64
from image_processing import combine_with_style
import datetime



# 환경 변수 로드
from dotenv import load_dotenv
load_dotenv()
STABILITY_KEY = os.getenv('STABILITYAI_API_KEY')
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Streamlit 설정
st.set_page_config(page_title="Foundry", layout="centered")

# 폰트 설정
st.markdown(
    """
    <style>
    @font-face {
        font-family: 'Pretendard-Regular';
        src: url('https://fastly.jsdelivr.net/gh/Project-Noonnu/noonfonts_2107@1.1/Pretendard-Regular.woff') format('woff');
        font-weight: 400;
        font-style: normal;
    }

    /* 전체 텍스트에 폰트 적용 */
    body {
        font-family: 'Pretendard-Regular', sans-serif;
        background-color: #FFFFFF; /* 배경 색상 밝게 설정 */
    }

    /* 제목 및 텍스트 요소에 폰트 적용 */
    h1, h2, h3, h4, h5, h6, p, label, button, span, div {
        font-family: 'Pretendard-Regular', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# 제목 위에 로고 추가
st.image("Logo/Logo_temp.png", width=200)  # 로고 이미지 크기 조절

# 제목
st.title("Foundry Generation Tested")

# 사이드바 - 설정
# 사이드바에 로고 추가


st.sidebar.header("Style Setting")
# 00_ref 폴더 내의 하위 폴더 이름 다 가져오기
essence_image_sets = os.listdir("00_ref")
essence_image_sets = [folder for folder in essence_image_sets if os.path.isdir(os.path.join("00_ref", folder))]
essence_image_set = st.sidebar.selectbox(
    "스타일 선택",
    essence_image_sets
)

# essence_image_set = st.sidebar.selectbox(
#     "스타일 선택",
#     ("color_chair", "color_sofa",
#      "modern_style", "minimalist")  # 필요에 따라 추가
# )

# 파일 업로드: 사용자로부터 받는 이미지 인풋
uploaded_file = st.file_uploader("이미지 업로드", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file:
    # 이미지 저장
    uploads_dir = 'uploads'  # uploads 폴더에 저장
    os.makedirs(uploads_dir, exist_ok=True)  # 폴더 없을 시 생성
    input_filename = uploaded_file.name  # 업로드된 파일 이름
    input_path = os.path.join(uploads_dir, input_filename)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # 파일 내용을 바이너리 형식으로 읽어옴

    st.image(input_path, caption="업로드된 이미지", use_column_width=True)  # 이미지를 스트림릿에 출력

    # 결합된 이미지 생성
    combined_folder = 'combined'
    os.makedirs(combined_folder, exist_ok=True)
    essence_folder = os.path.join("00_ref", essence_image_set)

# 여기서 엄청 작게 결합에 활용된 이미지만을 보여주는 코드를 활용하고 싶다

    try:
        with st.spinner('이미지 조합 중...'):
            # 사용자 이미지와 선택한 스타일 세트를 결합
            # (user_image_path, style_image_set_folder, output_folder)
            combined_image_path = combine_with_style(input_path, essence_folder, combined_folder)
        st.success("사용자 이미지 & 스타일셋 이미지 성공적으로 조합되었습니다!")
        st.image(combined_image_path, caption="스타일 셋 이미지", width=300)
    except Exception as e:
        st.error(f"결합된 이미지 생성 오류: {e}")

    # 가구 이미지 생성
    generated_folder = 'generated'
    os.makedirs(generated_folder, exist_ok=True)

    generated_image_filename = f"generated_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
    generated_image_path = os.path.join(generated_folder, generated_image_filename)

    try:
        with st.spinner('새로운 가구 이미지 생성 중...'):
            generate_image_from_prompt(combined_image_path, generated_image_path)
        st.success("가구가 성공적으로 생성되었습니다!")
        st.image(generated_image_path, caption="생성된 가구 이미지", use_column_width=True)
    except Exception as e:
        st.error(f"이미지 생성 오류: {e}")


    # 다운로드 버튼
    with open(generated_image_path, "rb") as img_file:
        btn = st.download_button(
            label="이미지 다운로드",
            data=img_file,
            file_name=generated_image_filename,
            mime="image/png"
        )
