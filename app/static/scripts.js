document.addEventListener("DOMContentLoaded", function () {
    const dropArea = document.getElementById("drop-area");
    const fileInput = document.getElementById("image");

    // 드래그 앤 드롭 기능
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
            fileInput.files = files;  // 파일 입력 업데이트
            displayImage(file); // 이미지 미리보기 함수 호출
        }
    });

    // 파일 선택 창 열기
    dropArea.addEventListener("click", () => fileInput.click());

    // 파일 선택 시 미리보기 업데이트
    fileInput.addEventListener("change", (event) => {
        const file = event.target.files[0];
        if (file) {
            displayImage(file);
        }
    });

    // 이미지 미리보기 함수
    function displayImage(file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const imagePreview = document.createElement("img");
            imagePreview.src = e.target.result;
            imagePreview.alt = "Preview Image";
            imagePreview.classList.add("preview-image");

            // 이전 내용 제거 후 새 이미지 추가
            dropArea.innerHTML = ""; 
            dropArea.appendChild(imagePreview);
        };
        reader.readAsDataURL(file);
    }

    // 스타일 선택 함수
    function selectStyle(style) {
        console.log("Selected style:", style); // 콘솔에 선택한 스타일 출력
        document.getElementById("style_set").value = style; // 선택된 스타일을 숨겨진 input에 설정
    }
    
});
