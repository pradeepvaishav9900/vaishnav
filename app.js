import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getFirestore, collection, addDoc, query, orderBy, onSnapshot } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-firestore.js";
import { firebaseConfig } from "./firebase-config.js";

// Init Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const chatBox = document.getElementById("chatBox");
const messageInput = document.getElementById("messageInput");

const q = query(collection(db, "messages"), orderBy("timestamp"));
onSnapshot(q, (snapshot) => {
    chatBox.innerHTML = "";
    snapshot.forEach((doc) => {
        const msg = document.createElement("p");
        msg.textContent = doc.data().text;
        chatBox.appendChild(msg);
    });
    chatBox.scrollTop = chatBox.scrollHeight;
});

window.sendMessage = async function() {
    const text = messageInput.value.trim();
    if (text !== "") {
        await addDoc(collection(db, "messages"), {
            text,
            timestamp: new Date()
        });
        messageInput.value = "";
    }
};
