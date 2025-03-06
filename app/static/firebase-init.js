  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/11.3.1/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.3.1/firebase-analytics.js";
  import { getAuth, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/11.3.1/firebase-auth.js";

  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyB1_97eLDNaJm-JUTNYYxawJpBvwvitcf0",
    authDomain: "layerminder.firebaseapp.com",
    projectId: "layerminder",
    storageBucket: "layerminder.firebasestorage.app",
    messagingSenderId: "998697180702",
    appId: "1:998697180702:web:f0a649bd836886bbd0980f",
    measurementId: "G-KWW0CCZ0NE"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app);
  const googleProvider = new GoogleAuthProvider();
  const analytics = getAnalytics(app);

  // 필요한 객체/함수들을 export
  export { auth, googleProvider, analytics };