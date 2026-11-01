import "../CSS/About.css";

function About() {
    let steps = [
        {
            title: "You send a message",
            text: "You can ask for a place to visit or mention things like your budget, who is travelling, and what kind of trip you enjoy."
        },
        {
            title: "Groq reads what you mean",
            text: "We use Groq to understand the question and pick out travel preferences from the message and recent chat."
        },
        {
            title: "Our destination model ranks places",
            text: "When you want suggestions, the trained model compares your preferences with the destination data and returns its best matches."
        },
        {
            title: "We add details that fit the question",
            text: "The backend can summarize reviews, estimate a budget in rupees, or find a destination image. It only adds these when they are useful for the question."
        },
        {
            title: "The answer comes back to chat",
            text: "The Python backend puts the useful results into one reply. You can play it aloud, and signing in saves your chats to your account."
        }
    ];

    let team = [
        {
            name: "Shreshtha Sharma",
            role: "Built the frontend, connected it to the backend, and worked on text-to-speech."
        },
        {
            name: "Satwik Maurya",
            role: "Worked on making and training the models."
        },
        {
            name: "Abhishek Yadav",
            role: "Collected the travel data used in the project."
        }
    ];

    let architecture = [
        {
            number: "01",
            title: "React in the browser",
            text: "The input sends your message and chat context. Home keeps track of the chats, and the output components show the reply. The navbar and sidebars handle navigation and account options."
        },
        {
            number: "02",
            title: "Flask and Python",
            text: "The /process route receives the message and recent chat, then calls the model router. Other routes in the same backend handle speech and audio transcription."
        },
        {
            number: "03",
            title: "The models and services",
            text: "model_router.py is the traffic controller. It uses Groq to understand and write replies, and calls our destination, review, and budget code or image search when needed."
        },
        {
            number: "04",
            title: "Files and saved chats",
            text: "The project data is stored in CSV files, and trained models load from .pkl files. Firebase handles sign-in and Firestore keeps chat history for signed-in users."
        }
    ];

    return (
        <main className="about-page">
            <div className="about-content">
                <section className="about-hero">
                    <div className="about-intro">
                        <h1>About Traivo</h1>
                        <p>
                            We made Traivo for our college project. We wanted trip planning to feel
                            like a conversation: tell it what kind of trip you have in mind, and it
                            can help you think through destinations, reviews, and an approximate budget.
                        </p>
                    </div>
                    <figure className="about-workflow-image">
                        <img src="/traivo-workflow.png" alt="A traveler asks Traivo for help, and the assistant combines destination, budget, and review information into a travel response." />
                        <figcaption>A quick look at what happens after you send a message.</figcaption>
                    </figure>
                </section>

                <section className="about-section">
                    <div className="about-section-heading">
                        <h2>Travel planning can start with a question</h2>
                    </div>
                    <p className="about-section-copy">
                        We wanted to try combining a chatbot with models we trained ourselves. You
                        can ask for destination ideas, ask what people liked or disliked about a
                        place, or get a rough trip budget. The answer depends on what you ask, so
                        images and review details are only added when they make sense.
                    </p>
                    <div className="about-feature-grid">
                        <article className="about-feature-card">
                            <h3>Destination ideas</h3>
                            <p>Tell it your budget, group, or the kind of trip you like to get matching places.</p>
                        </article>
                        <article className="about-feature-card">
                            <h3>Approximate budgets</h3>
                            <p>Ask about cost to get a rough estimate based on the trip details and training data.</p>
                        </article>
                        <article className="about-feature-card">
                            <h3>Reviews and pictures</h3>
                            <p>Ask about reviews, or get a picture when seeing the destination helps.</p>
                        </article>
                    </div>
                </section>

                <section className="about-section">
                    <div className="about-section-heading">
                        <h2>From prompt to response</h2>
                    </div>
                    <div className="about-steps">
                        {steps.map((step, index) => (
                            <article className="about-step" key={step.title}>
                                <span className="about-step-number">{index + 1}</span>
                                <div>
                                    <h3>{step.title}</h3>
                                    <p>{step.text}</p>
                                </div>
                            </article>
                        ))}
                    </div>
                </section>

                <section className="about-section">
                    <div className="about-section-heading">
                        <h2>How the app is put together</h2>
                    </div>
                    <p className="about-section-copy">
                        The browser and Python backend have separate jobs. The browser collects your
                        message and shows the reply; the backend works out which tools to use and
                        sends the result back.
                    </p>
                    <div className="about-architecture">
                        {architecture.map((part) => (
                            <article className="about-architecture-card" key={part.number}>
                                <span className="about-architecture-number">{part.number}</span>
                                <div>
                                    <h3>{part.title}</h3>
                                    <p>{part.text}</p>
                                </div>
                            </article>
                        ))}
                    </div>
                    <p className="about-architecture-flow">
                        React app <span>→</span> Flask backend <span>→</span> models and data <span>→</span> reply in chat
                    </p>
                </section>

                <section className="about-section about-team-section">
                    <div className="about-section-heading">
                        <h2>Our team</h2>
                    </div>
                    <div className="about-team-grid">
                        {team.map((member) => (
                            <article className="about-team-card" key={member.name}>
                                <h3>{member.name}</h3>
                                <p>{member.role}</p>
                            </article>
                        ))}
                    </div>
                </section>

                <footer className="about-footer">
                    We built Traivo as a college project to learn how a chatbot, a Python backend, and trained models can work together.
                </footer>
            </div>
        </main>
    );
}

export default About;
