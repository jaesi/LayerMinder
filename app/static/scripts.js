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
    window.selectStyle = function (style, imageUrl) {
        console.log("Selected Style:", style);
        
        const selectedStyleItem = document.querySelector("#selected-styles .selected-style-item");
        
        if (selectedStyleItem) {
            // img 태그 선택 및 src 업데이트
            const imgTag = selectedStyleItem.querySelector("img");
            if (imgTag) {
                imgTag.src = imageUrl;
                console.log(`Image src updated to: ${imageUrl}`);
            } 

            // p 태그 선택 및 텍스트 업데이트
            const pTag = selectedStyleItem.querySelector("p");
            if (pTag) {
                pTag.textContent = style; // style 변수 값으로 업데이트
                console.log(`Paragraph text updated to: ${style}`);
            } 
        } 
    };
});
