import { useState } from "react";
import InputBar from "./InputBar";
import OutputPlain from "./OutputPlain";
import SideBar from "./SideBar";
import { loadChats, saveChat } from "../chatHistory";

let accountUserId = null;

function Home() {
    const [chats, setChats] = useState([{ id: 1, title: "New Chat", messages: [] }]);
    const [activeChatId, setActiveChatId] = useState(1);
    const activeChat = chats.find((chat) => chat.id === activeChatId);
    const messages = activeChat ? activeChat.messages : [];

    function loadAccountChats(user) {
        if (!user) {
            if (accountUserId !== null) {
                accountUserId = null;
                window.accountChatHistoryLoaded = false;
                let newChat = { id: Date.now(), title: "New Chat", messages: [] };
                setChats([newChat]);
                setActiveChatId(newChat.id);
            }
            return;
        }

        if (accountUserId === user.uid && window.accountChatHistoryLoaded) return;
        let guestChats = accountUserId === null
            ? chats.filter((chat) => chat.messages.some((message) => message.role === "user"))
            : [];
        accountUserId = user.uid;
        window.accountChatHistoryLoaded = false;

        loadChats(user.uid).then(async (savedChats) => {
            if (accountUserId !== user.uid) return;
            let accountChats = [...savedChats];

            for (let guestChat of guestChats) {
                let chatToSave = { ...guestChat };
                if (accountChats.some((chat) => chat.id === chatToSave.id)) {
                    chatToSave.id = Date.now() + accountChats.length;
                }
                accountChats.push(chatToSave);
                await saveChat(user.uid, chatToSave);
            }

            if (accountChats.length === 0) {
                let newChat = { id: Date.now(), title: "New Chat", messages: [] };
                accountChats = [newChat];
                await saveChat(user.uid, newChat);
            }

            setChats(accountChats);
            setActiveChatId(accountChats[accountChats.length - 1].id);
            window.accountChatHistoryLoaded = true;
        }).catch((error) => console.log("Could not load account chat history:", error));
    }

    window.loadAccountChats = loadAccountChats;

    function addPrompt(prompt) {
        let updatedChat = {
            ...activeChat,
            title: activeChat.messages.length === 0
                ? (prompt.length > 32 ? prompt.slice(0, 32) + "..." : prompt)
                : activeChat.title,
            messages: [
                ...activeChat.messages,
                { role: "user", content: prompt },
                { role: "assistant", content: "Thinking..." }
            ]
        };
        setChats((currentChats) => currentChats.map((chat) =>
            chat.id === activeChatId ? updatedChat : chat
        ));
        if (accountUserId) saveChat(accountUserId, updatedChat).catch((error) => console.log("Could not save chat:", error));
        return updatedChat;
    }

    function showResponse(response, images, sentChat) {
        if (!sentChat) return;
        let updatedChat = {
            ...sentChat,
            messages: sentChat.messages.map((message, index) =>
                index === sentChat.messages.length - 1 && message.role === "assistant"
                    ? { ...message, content: response, images: images }
                    : message
            )
        };
        setChats((currentChats) => currentChats.map((chat) =>
            chat.id === sentChat.id
                ? updatedChat
                : chat
        ));
        if (accountUserId) saveChat(accountUserId, updatedChat).catch((error) => console.log("Could not save chat reply:", error));
    }

    function newChat() {
        let newId = Date.now();
        let newChat = { id: newId, title: "New Chat", messages: [] };
        setChats((currentChats) => [
            ...currentChats,
            newChat
        ]);
        setActiveChatId(newId);
        if (accountUserId) saveChat(accountUserId, newChat).catch((error) => console.log("Could not save chat:", error));
    }

    return (
        <div className="main">
            <SideBar
                chats={chats}
                activeChatId={activeChatId}
                onNewChat={newChat}
                onSelectChat={setActiveChatId}
            />
            <OutputPlain messages={messages} />
            <footer>
                <InputBar key={activeChatId} messages={messages} onSend={addPrompt} onReceive={showResponse} />
            </footer>
        </div>
    );
}

export default Home;
