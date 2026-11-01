import '../CSS/Navbar.css';
import { useNavigate, useLocation } from 'react-router-dom';

function Navbar() {
    const navigator = useNavigate();
    const location = useLocation();
    let status = "closed";

    function navigate(path) {
        if (path === "/about") {
            window.loadAccountChats = null;
            window.accountChatHistoryLoaded = false;
        }
        navigator(path);
    }

    function setActiveStyle(path) {
        return location.pathname === path
            ? "0 4px 15px rgba(125, 128, 131, 0.35)"
            : "none";
    }
    function moveSidebar() {
        if (window.loadAccountChats) window.loadAccountChats(window.traivoUser || null);
        let sidebar = document.querySelector(".sidebar");

        if (status === "closed") {
            sidebar.style.left = "0%";

            status = "displayed";
        } else {
            sidebar.style.left = "-60%";
            status = "closed";
        }
    }

    function moveAccountSidebar() {
        if (window.loadAccountChats) window.loadAccountChats(window.traivoUser || null);
        let sidebar = document.querySelector(".account-sidebar");

        if (sidebar.dataset.open === "true") {
            sidebar.style.right = "-350px";
            sidebar.dataset.open = "false";
        } else {
            sidebar.style.right = "0";
            sidebar.dataset.open = "true";
        }
    }

    return (
        <nav className="navbar">
            <div className="corner-left">
                 <button id="sidebar-btn" onClick={moveSidebar}>
                    <img src="sidebar.png" alt="sidebar" />
                </button>
            </div>
            <div className="nav-buttons">
                    <button
                        onClick={() => navigate('/')}
                        style={{ boxShadow: setActiveStyle('/') }}
                    >
                        Chatbot
                    </button>
     

   
                    <button
                        onClick={() => navigate('/about')}
                        style={{ boxShadow: setActiveStyle('/about') }}
                    >
                        About
                    </button>
            </div>
     

            <div className="corner-right">
                <div className='traivo-logo'>
                    <img src="traivo-logo.png" alt="Traivo" />

                </div>
                <button id="account" onClick={moveAccountSidebar} aria-label="Open account menu" title="Account">
                    <img src="user.png" alt="Account" />
                </button>
            </div>
        </nav>
    );
}

export default Navbar;
