import "../CSS/SideBar.css";

function SideBar({ chats, activeChatId, onNewChat, onSelectChat }) {

    return (
        <div className="sidebar">
            <div className="top-things">
                <h3>Traivo</h3>
            </div>

            <div className="new-chat">
                <button id="new-chat" onClick={onNewChat}>
                    <div></div>
                    New Chat
                    <img src="new-chat.png" alt="new chat" />
                
                </button>
            </div>

            <div className="history">
                <h3>Chat History</h3>
                {[...chats].reverse().map((chat) => (
                    <button
                        className={chat.id === activeChatId ? "history-entry active" : "history-entry"}
                        key={chat.id}
                        title={chat.title}
                        onClick={() => onSelectChat(chat.id)}
                    >
                        {chat.title}
                    </button>
                ))}
            </div>
        </div>
    );
}

export default SideBar;
