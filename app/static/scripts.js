document.addEventListener("DOMContentLoaded", function () {
    // -----------------------------
    // 1) 변수 잡기
    // -----------------------------
    const dropArea = document.getElementById("drop-area");
    const fileInput = document.getElementById("image"); 
    const styleInput = document.getElementById("style_set"); // 숨긴 input
    const form = document.querySelector("form");             // 왼쪽 사이드바 폼
    const mainArea = document.querySelector(".main-area");   // 오른쪽 결과 영역
    const generateBtn = document.querySelector(".generate-button"); // Generate 버튼
    const loadingOverlay = document.getElementById("loading-overlay"); // 로딩 오버레이


    // -----------------------------
    // 2) 드래그 앤 드롭으로 파일 업로드
    // -----------------------------
    dropArea.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropArea.classList.add("dragging");
    });
    dropArea.addEventListener("dragleave", () => {
        dropArea.classList.remove("dragging");
    });
    dropArea.addEventListener("drop", (event) => {
        event.preventDefault();
        dropArea.classList.remove("dragging");

        const files = event.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            fileInput.files = files;  // 폼의 file input에 드롭된 파일 넣기
            displayImage(file);
        }
    });

    // -----------------------------
    // 3) 파일 선택 시 이미지 미리보기
    // -----------------------------
    fileInput.addEventListener("change", (event) => {
        const file = event.target.files[0];
        if (file) {
            displayImage(file);
        }
    });

    // -----------------------------
    // 4) 이미지 미리보기 함수
    // -----------------------------
    function displayImage(file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            // dropArea 안을 초기화
            dropArea.innerHTML = "";

            // 미리보기 이미지
            const imagePreview = document.createElement("img");
            imagePreview.src = e.target.result;
            imagePreview.alt = "Preview Image";
            imagePreview.classList.add("preview-image");

            // "Change Image" 라벨
            const label = document.createElement("label");
            label.setAttribute("for", "image");
            label.className = "browse-link";
            label.style.position = "absolute";
            label.style.bottom = "10px";
            label.style.right = "10px";
            label.textContent = "Change Image";

            // 폼의 fileInput를 다시 append (중간에 dropArea 비우면서 제거되었으므로)
            dropArea.appendChild(imagePreview);
            dropArea.appendChild(label);
            dropArea.appendChild(fileInput);
        };
        reader.readAsDataURL(file);
    }

    // -----------------------------
    // 5) 폼 제출 (Generate) -> AJAX -> 오른쪽 영역에 결과 표시
    // -----------------------------
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // 기존 폼 이동 막기
        

        // 1) 요청 시작 시, 오버레이 표시
        loadingOverlay.classList.remove("hidden");

        // 간단 유효성 검사
        if (!fileInput.files.length) {
            alert('Please select an image file');
            return;
        }
        if (!styleInput.value) {
            alert('Please select a style');
            return;
        }

        // 폼 데이터를 AJAX로 보내기
        const formData = new FormData(form); 
        fetch("/generate", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }

            // data.image_urls에 생성된 이미지 경로(4장)가 담겨 있다고 가정
            const { image_urls } = data;
            if (!image_urls || !image_urls.length) {
                mainArea.innerHTML = "<p>No images returned.</p>";
                return;
            }

            // -------------------------
            // (A) 기존 결과 지우고 새로 표시
            // -------------------------
            // mainArea.innerHTML = "";

            // 그리드 컨테이너 생성
            const gridContainer = document.createElement("div");
            gridContainer.classList.add("grid-container");
            // -> CSS에서 display: grid; grid-template-columns: repeat(4,1fr); gap:10px; 등 설정

            // 4장 이미지 삽입
            image_urls.forEach(url => {
                const img = document.createElement("img");
                img.src = url;
                img.alt = "Generated Image";
                gridContainer.appendChild(img);
            });

            // .main-area에 그리드 붙이기
            mainArea.appendChild(gridContainer);

            // -------------------------
            // (B) Generate -> Regenerate
            // -------------------------
            generateBtn.textContent = "Regenerate";
        })
        .catch(err => {
            console.error(err);
            alert("Error generating images: " + err.message);
        })
        .finally(() => {
            // 2) 요청 완료 후, 오버레이 숨김
            loadingOverlay.classList.add("hidden");
        });
    });

    // -----------------------------
    // 6) 스타일 선택 함수
    // -----------------------------
    window.selectStyle = function (style, imageUrl, clickedElement) {
        console.log("Selected Style:", style);
        
        // (1) 숨겨진 input에 스타일 값 저장
        styleInput.value = style;

        // (2) 모든 .style-item의 'active' 제거
        const styleItems = document.querySelectorAll('.style-item');
        styleItems.forEach(item => {
            item.classList.remove('active');
        });

        // (3) 클릭된 아이템만 활성화
        clickedElement.classList.add('active');

        // 스타일 디버깅
        console.log("styleInput.value =", styleInput.value);

    };
});
