import UserInput from "./Messages/UserInput";
import ChatOutput from "./Messages/ChatOutput";
import '../CSS/OutputPlain.css';

function OutputPlain({ messages }) {
    return (
        <div className="OutputPlain">
            {messages.length === 0 && (
                <div className="greetings"><h3>Where do you wanna go?...</h3></div>
            )}
            <div className="messages-list">
                {messages.map((message, index) => (
                    <div className="message-pair" key={`${index}-${message.role}-${message.content}`}>
                        {message.role === "user"
                            ? <UserInput userprompt={message.content} />
                            : <ChatOutput text={message.content} images={message.images} />}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default OutputPlain;
