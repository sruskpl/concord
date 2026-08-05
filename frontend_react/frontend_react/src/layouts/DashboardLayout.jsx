import "./DashboardLayout.css";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function DashboardLayout({ role, children }) {
    return (
        <div className="dashboard-layout">

            <Navbar />

            <div className="dashboard-body">

                <Sidebar role={role} />

                <main className="dashboard-content">
                    {children}
                </main>

            </div>

        </div>
    );
}

export default DashboardLayout;