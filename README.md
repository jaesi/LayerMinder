# Layer Minder Beta
AI 기반 가구 디자인 생성 플랫폼
---

Layer Minder Beta는 AI 이미지 생성과 사용자 입력을 결합하여 독특하고 미니멀한 가구 디자인을 만드는 혁신적인 웹 애플리케이션입니다. 이 플랫폼은 Stability AI와 OpenAI API를 활용하여 참조 이미지와 스타일 선호도로부터 실물과 같은 가구 디자인 및 상세 사양을 생성합니다.

## 주요 기능

이 애플리케이션은 디자이너와 가구 애호가들에게 다음과 같은 기능을 제공합니다:
- 기존 가구 참조와 스타일 영감을 결합하여 새로운 가구 디자인 생성
- 재료, 치수, 구조 세부 정보를 포함한 상세 기술 사양 생성
- 깔끔한 스튜디오 배경에 고품질 렌더링을 통한 디자인 시각화
- 정확한 측정 및 재료 사양이 포함된 AI 생성 가구 설명 제공
- 기능적 가구 요구 사항을 유지하면서 다양한 스타일 조합 실험

## 저장소 구조
```
.
├── app/                            # 메인 애플리케이션 디렉토리
│   ├── static/                     # 정적 에셋
│   │   ├── css/                   # 스타일링 파일
│   │   ├── firebase-init.js       # Firebase 인증 설정
│   │   ├── login.js              # 사용자 인증 처리
│   │   └── scripts.js            # 메인 애플리케이션 자바스크립트
│   ├── templates/                 # Jinja2 HTML 템플릿
│   │   ├── landing.html          # 애플리케이션 랜딩 페이지
│   │   ├── layout.html           # 기본 템플릿 레이아웃
│   │   ├── main.html             # 메인 애플리케이션 인터페이스
│   │   └── result.html           # 생성된 디자인 결과 뷰
```

## 사용 흐름

Layer Minder는 사용자 입력과 AI 생성을 결합하여 독특한 가구 디자인을 만들기 위해 다단계 파이프라인을 통해 이미지를 처리합니다.

```
사용자 입력        스타일 선택       AI 처리           출력
[이미지 업로드] -> [스타일 매개변수] -> [Stability AI] -> [생성된 디자인]
                                    [OpenAI] ------> [상세 사양]
```

## 주요 구성 요소 상호작용:

1. 사용자가 웹 인터페이스를 통해 참조 이미지 업로드
2. 프론트엔드에서 이미지 유효성 검사 및 전처리
3. 선택된 스타일 매개변수와 이미지 결합
4. Stability AI를 통한 새로운 가구 디자인 생성
5. OpenAI를 통한 생성된 디자인 분석
6. 웹 인터페이스에 사양과 함께 결과 표시
7. Firebase를 통한 사용자 인증 및 세션 관리

## UI/UX 인터페이스 순서

1. **랜딩 페이지** (`landing.html`)
   - 사용자 로그인/가입 인터페이스
   - 서비스 소개 및 주요 기능 하이라이트

2. **메인 애플리케이션 인터페이스** (`main.html`)
   - 이미지 업로드 영역 (드래그 앤 드롭 또는 파일 선택)
   - 스타일 선택 캐러셀
   - 생성 버튼 및 옵션

3. **결과 페이지** (`result.html`)
   - 생성된 가구 디자인 표시
   - 상세 기술 사양 및 설명
   - 추가 수정 또는 새 디자인 생성 옵션

## 필요한 사용자 인터랙션

- 참조 이미지 업로드 (드래그 앤 드롭 또는 클릭하여 파일 선택)
- 캐러셀에서 스타일 선택
- "생성" 버튼 클릭하여 새로운 가구 디자인 생성
- 생성된 결과 확인 및 다운로드/공유 옵션
