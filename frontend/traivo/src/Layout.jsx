
import Navbar from "./Components/Navbar";
import AccountSideBar from "./Components/AccountSideBar";
import { Outlet } from "react-router-dom";

function Layout() {
  return (
    <div className="app-shell">
      <Navbar />
      <AccountSideBar />

      <main className="app-content">
        <Outlet />
      </main>
    </div>
  );
}

export default Layout;
