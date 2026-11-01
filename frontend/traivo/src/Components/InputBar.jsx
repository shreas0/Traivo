import '../CSS/InputBar.css';

let recorder = null;
let chunks = [];
let recording = false;


async function startRecording() {
    let stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder = new MediaRecorder(stream);
    chunks = [];

    recorder.ondataavailable = function (e) {
        chunks.push(e.data);
    };

    recorder.onstop = async function () {
        stream.getTracks().forEach(function (t) { t.stop(); });
        await saveAudio();
        await getText();
    };

    recorder.start();
    recording = true;
    document.querySelector(".mic-btn").style.backgroundColor = "red";
}

function stopRecording() {
    recorder.stop();
    recording = false;
    document.querySelector(".mic-btn").style.backgroundColor = "transparent";
}

function handleMic() {
    if (recording === false) {
        startRecording();
    } else {
        stopRecording();
    }
}

async function saveAudio() {
    let audio = new Blob(chunks, { type: "audio/webm" });
    let formData = new FormData();
    formData.append("audio", audio, "audio.webm");

    await fetch("http://127.0.0.1:5000/save-audio", {
        method: "POST",
        body: formData
    });
}

async function getText() {
    let response = await fetch("http://127.0.0.1:5000/get-text");
    let data = await response.json();
    document.getElementById("prompt-area").value = data.text;
}

function InputBar({ messages, onSend, onReceive }) {

    async function handleSubmit(event) {
        event.preventDefault();

        let box = document.getElementById("prompt-area");
        let text = box.value.trim();
        if (text === "") return;

        let sentChat = onSend(text);
        box.value = "";

        try {
            let response = await fetch("http://127.0.0.1:5000/process", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    input: text,
                    history: messages.filter((message) => message.content !== "Thinking...")
                })
            });

            if (!response.ok) throw new Error("Chat request failed");
            let data = await response.json();
            onReceive(data.response || "I couldn't generate a response. Please try again.", data.images || [], sentChat);
        } catch {
            onReceive("I couldn't connect to the chatbot. Please check that the backend is running and try again.", [], sentChat);
        }
    }

    return (
        <form className="input-block" onSubmit={handleSubmit}>
            <div className="input-elements">
                <div className="future"></div>
                <div className="adjuster">
                    <div id="input-area">
                        <input
                            id="prompt-area"
                            type="text"
                            placeholder="Ask something about your travel plan"
                        />
                    </div>
                    <div id="below-area"></div>
                </div>
                <div className="input-btn">
                    <button className="mic-btn" type="button" onClick={handleMic}>
                        <img src="/mic.png" alt="mic" />
                    </button>
                    <button className="send-btn" type="submit">
                        <img src="/arrow.png" alt="Arrow" />
                    </button>
                </div>
            </div>
        </form>
    );
}

export default InputBar;
