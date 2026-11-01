import { collection, doc, getDoc, getDocs, setDoc } from "firebase/firestore";
import { db } from "./firebase";

export async function loadChats(userId) {
    let chatsRef = collection(db, "users", userId, "chats");
    let snapshot = await getDocs(chatsRef);
    return snapshot.docs
        .map((chatDoc) => ({ ...chatDoc.data(), id: Number(chatDoc.id) }))
        .sort((firstChat, secondChat) => firstChat.id - secondChat.id);
}

export function saveChat(userId, chat) {
    let chatRef = doc(db, "users", userId, "chats", String(chat.id));
    return setDoc(chatRef, chat);
}

export async function saveChatReply(userId, chatId, response, images) {
    let chatRef = doc(db, "users", userId, "chats", String(chatId));
    let snapshot = await getDoc(chatRef);
    if (!snapshot.exists()) return null;

    let chat = snapshot.data();
    let messages = [...chat.messages];
    let lastAssistant = messages.length - 1;
    if (lastAssistant >= 0 && messages[lastAssistant].role === "assistant") {
        messages[lastAssistant] = { ...messages[lastAssistant], content: response, images: images };
    }

    let updatedChat = { ...chat, messages: messages };
    await setDoc(chatRef, updatedChat);
    return updatedChat;
}
