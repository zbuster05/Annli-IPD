// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCYHr2gB40J7pgh8LX_UM9aGlgzXfjz1P0",
  authDomain: "ipdonline.firebaseapp.com",
  projectId: "ipdonline",
  storageBucket: "ipdonline.appspot.com",
  messagingSenderId: "542145359212",
  appId: "1:542145359212:web:fb5dfbbaaf13665fe21749",
  measurementId: "G-272Z9ZF74S"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);