
import '../CSS/Navbar.css';
import { useNavigate } from 'react-router-dom';

function Navbar() {
    const navigator = useNavigate();

    function navigate(path) {
        navigator(path);
    }

    return (
        <nav className="navbar">
            <ul>
                <li>
                    <button onClick={() => navigate('/home')}>
                        Chatbot
                    </button>
                </li>

                <li>
                    <button onClick={() => navigate('/about')}>
                        About
                    </button>
                </li>
            </ul>
        </nav>
    );
}

export default Navbar;
