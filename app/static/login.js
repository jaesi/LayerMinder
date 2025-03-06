// login.js
import { auth, googleProvider } from "./firebase-init.js";
import { 
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signInWithPopup
} from "https://www.gstatic.com/firebasejs/11.3.1/firebase-auth.js";

// DOM 요소 가져오기
const loginIcon = document.getElementById('login-icon');
const popupOverlay = document.getElementById('popup-overlay');
const popupClose = document.getElementById('popup-close');

const loginBtn = document.getElementById('login-btn');
const signupBtn = document.getElementById('signup-btn');
const googleLoginBtn = document.getElementById('google-login-btn');

// 팝업 열기
loginIcon.addEventListener('click', () => {
  popupOverlay.classList.add('active');
});

// 팝업 닫기
popupClose.addEventListener('click', () => {
  popupOverlay.classList.remove('active');
});

// 로그인 버튼
loginBtn.addEventListener('click', async () => {
  const email = document.getElementById('email-input').value;
  const password = document.getElementById('password-input').value;

  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    console.log("Login success:", userCredential.user);
    // 팝업 닫기
    popupOverlay.classList.remove('active');
  } catch (error) {
    console.error("Login error:", error);
  }
});

// 회원가입 버튼
signupBtn.addEventListener('click', async () => {
  const email = document.getElementById('email-input').value;
  const password = document.getElementById('password-input').value;

  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    console.log("Sign up success:", userCredential.user);
    // 팝업 닫기
    popupOverlay.classList.remove('active');
  } catch (error) {
    console.error("Sign up error:", error);
  }
});

// 구글 로그인 버튼
googleLoginBtn.addEventListener('click', async () => {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    console.log("Google login success:", result.user);
    // 팝업 닫기
    popupOverlay.classList.remove('active');
  } catch (error) {
    console.error("Google login error:", error);
  }
});
