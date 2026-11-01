import '../../CSS/ChatOutput.css';

function formatInline(text) {
    return text.split(/(\*\*.*?\*\*|__.*?__|\[[^\]]+\]\(https:\/\/www\.google\.com\/maps\/search\/\?[^)]+\))/g).map((part, index) => {
        if ((part.startsWith("**") && part.endsWith("**")) || (part.startsWith("__") && part.endsWith("__"))) {
            return <strong key={index}>{part.slice(2, -2)}</strong>;
        }
        let link = part.match(/^\[([^\]]+)\]\((https:\/\/www\.google\.com\/maps\/search\/\?[^)]+)\)$/);
        if (link) {
            return <a href={link[2]} target="_blank" rel="noreferrer" key={index}>{link[1]}</a>;
        }
        return part;
    });
}

function normalize(text) {
    return text.split("\n").map((line, index) => {
        let cleanLine = line.trim();
        if (cleanLine === "") return <div className="chat-spacer" key={index}></div>;

        let heading = cleanLine.match(/^#{1,3}\s+(.+)$/);
        if (heading) {
            return <div className="chat-heading" key={index}>{formatInline(heading[1])}</div>;
        }

        let bullet = cleanLine.match(/^([-*•]|\d+[.)])\s+(.+)$/);
        if (bullet) {
            return (
                <div className="chat-list-item" key={index}>
                    <span>{bullet[1]}</span>
                    <span>{formatInline(bullet[2])}</span>
                </div>
            );
        }

        return <div key={index}>{formatInline(cleanLine)}</div>;
    });
}

function ChatOutput({ text, images = [] }) {
    async function speak(event) {
        let button = event.currentTarget;
        let action = button.dataset.speaking === "true" ? "stop" : "speak";
        button.dataset.speaking = action === "speak" ? "true" : "false";
        let output = event.currentTarget.parentElement.querySelector(".chat-text").innerText;
        let controller = new AbortController();
        let timeout = setTimeout(() => controller.abort(), 10000);
        try {
            let response = await fetch("http://127.0.0.1:5000/speak", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ input: output, action: action }),
                signal: controller.signal
            });
            if (!response.ok) throw new Error("Speech request failed");
            let data = await response.json();
            if (action === "speak" && data.status !== "speaking") {
                button.dataset.speaking = "false";
            }
        } catch (error) {
            button.dataset.speaking = "false";
            console.log("Could not use speech:", error);
        } finally {
            clearTimeout(timeout);
        }
    }

    return (
        <div className="chat-output">
            <div className="chat-text">{normalize(text || "Thinking...")}</div>
            {images.map((image, index) => (
                <div className="chat-place-image" key={`${image.place}-${index}`}>
                    <img src={image.url} alt={image.alt} />
                    <div>
                        Photo by <a href={image.photographer_url} target="_blank" rel="noreferrer">{image.photographer}</a> on <a href={image.unsplash_url} target="_blank" rel="noreferrer">Unsplash</a>
                    </div>
                </div>
            ))}
            {text && text !== "Thinking..." && <button id="speak" onClick={speak}>
                <img src="speaker.png" alt="speaker-icon" />
            </button>}
        </div>
    );
}

export default ChatOutput;
