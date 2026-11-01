import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyDV0aKyqDPuOq2DgLuOV0PhTl8GzDY35wQ",
  authDomain: "traivo-2b0d2.firebaseapp.com",
  projectId: "traivo-2b0d2",
  storageBucket: "traivo-2b0d2.firebasestorage.app",
  messagingSenderId: "357107640217",
  appId: "1:357107640217:web:0a3f143388fed42ada5508",
  measurementId: "G-RRFD6YHDPD",
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
export const db = getFirestore(app);
