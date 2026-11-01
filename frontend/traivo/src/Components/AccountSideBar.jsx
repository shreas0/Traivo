import "../CSS/AccountSideBar.css";
import { onAuthStateChanged, signInWithPopup, signOut } from "firebase/auth";
import { auth, googleProvider } from "../firebase";

let currentAccount = auth.currentUser;

if (localStorage.getItem("traivo-theme") === "dark") {
    document.body.classList.add("dark-mode");
}
if (localStorage.getItem("traivo-text-size") === "large") {
    document.body.classList.add("large-chat-text");
}

onAuthStateChanged(auth, (user) => {
    currentAccount = user;
    window.traivoUser = user;
    if (window.loadAccountChats) window.loadAccountChats(user);
    let name = document.querySelector("#account-profile-name");
    let email = document.querySelector("#account-profile-email");
    let loginButton = document.querySelector("#account-login");
    let logoutButton = document.querySelector("#account-logout");

    if (name && email) {
        name.innerText = user ? user.displayName || "Signed in" : "Guest";
        email.innerText = user ? user.email || "" : "Sign in to your account";
    }
    if (loginButton) {
        loginButton.style.display = user ? "none" : "block";
    }
    if (logoutButton) {
        logoutButton.style.display = user ? "block" : "none";
    }
});

function AccountSideBar() {
    async function login() {
        try {
            await signInWithPopup(auth, googleProvider);
        } catch (error) {
            alert("Google sign-in failed: " + error.message);
        }
    }

    async function logout() {
        await signOut(auth);
    }

    function showProfile() {
        let user = auth.currentUser;
        alert(user ? user.displayName + "\n" + user.email : "Please log in to view your profile.");
    }

    function showSettings() {
        document.querySelector(".account-menu").style.display = "none";
        document.querySelector(".account-settings").style.display = "block";
        document.querySelector(".account-sidebar-heading h3").innerText = "Settings";
    }

    function showAccountMenu() {
        document.querySelector(".account-menu").style.display = "flex";
        document.querySelector(".account-settings").style.display = "none";
        document.querySelector(".account-sidebar-heading h3").innerText = "Account";
    }

    function changeTheme(event) {
        document.body.classList.toggle("dark-mode", event.target.checked);
        localStorage.setItem("traivo-theme", event.target.checked ? "dark" : "light");
    }

    function changeTextSize(event) {
        document.body.classList.toggle("large-chat-text", event.target.value === "large");
        localStorage.setItem("traivo-text-size", event.target.value);
    }

    return (
        <div className="account-sidebar" data-open="false">
            <div className="account-sidebar-heading">
                <h3>Account</h3>
            </div>

            <div className="account-profile">
                <img src="/user.png" alt="Profile" />
                <div>
                    <strong id="account-profile-name">{currentAccount ? currentAccount.displayName || "Signed in" : "Guest"}</strong>
                    <span id="account-profile-email">{currentAccount ? currentAccount.email : "Sign in to your account"}</span>
                </div>
            </div>

            <div className="account-menu">
                <button type="button" onClick={showProfile}>Profile</button>
                <button type="button" onClick={showSettings}>Settings</button>
                <div className="account-menu-divider"></div>
                <button id="account-login" type="button" onClick={login} style={{ display: currentAccount ? "none" : "block" }}>Log in with Google</button>
                <button id="account-logout" type="button" onClick={logout} style={{ display: currentAccount ? "block" : "none" }}>Log out</button>
            </div>

            <div className="account-settings">
                <button className="settings-back" type="button" onClick={showAccountMenu}>← Back to account</button>
                <h4>Appearance</h4>
                <label className="setting-row" htmlFor="dark-mode-toggle">
                    <span>
                        <strong>Dark mode</strong>
                        <small>Use a darker look</small>
                    </span>
                    <input
                        id="dark-mode-toggle"
                        type="checkbox"
                        defaultChecked={localStorage.getItem("traivo-theme") === "dark"}
                        onChange={changeTheme}
                    />
                </label>
                <label className="setting-row" htmlFor="chat-text-size">
                    <span>
                        <strong>Text size</strong>
                        <small>Change chat response size</small>
                    </span>
                    <select
                        id="chat-text-size"
                        defaultValue={localStorage.getItem("traivo-text-size") || "normal"}
                        onChange={changeTextSize}
                    >
                        <option value="normal">Normal</option>
                        <option value="large">Large</option>
                    </select>
                </label>
                <p className="settings-note">These settings are saved on this device.</p>
            </div>
        </div>
    );
}

export default AccountSideBar;
