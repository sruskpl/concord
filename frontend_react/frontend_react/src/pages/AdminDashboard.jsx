import { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";

import "./AdminDashboard.css";

function AdminDashboard() {

    const [dashboard, setDashboard] = useState({

        total_users: 0,

        active_sessions: 0,

        open_exceptions: 0,

        recent_users: []

    });

    async function fetchDashboard() {

    const response = await fetch(

        "http://localhost:5000/admin/dashboard",

        {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
        }

    );

    const data = await response.json();

    setDashboard(data);

}

    useEffect(() => {

        fetchDashboard();

    }, []);

    return (

        <DashboardLayout role="admin">

            <div className="dashboard-header">

                <h1>

                    Admin Control Center

                </h1>

                <p>

                    Monitor users, sessions and platform activity.

                </p>

            </div>

            <div className="summary-grid">

                <div className="summary-card">

                    <h3>Total Users</h3>

                    <h1>{dashboard.total_users}</h1>

                </div>

                <div className="summary-card">

                    <h3>Active Sessions</h3>

                    <h1>{dashboard.active_sessions}</h1>

                </div>

                <div className="summary-card">

                    <h3>Open Exceptions</h3>

                    <h1>{dashboard.open_exceptions}</h1>

                </div>

            </div>

            <div className="table-card">

                <div className="table-header">

                    <h2>

                        Recent User Registrations

                    </h2>

                </div>

                <table className="exception-table">

                    <thead>

                        <tr>

                            <th>Employee ID</th>

                            <th>Name</th>

                            <th>Email</th>

                            <th>Role</th>

                            <th>Created</th>

                        </tr>

                    </thead>

                    <tbody>

                        {

                            dashboard.recent_users.map(user => (

                                <tr key={user.id}>

                                    <td>{user.employee_id}</td>

                                    <td>{user.full_name}</td>

                                    <td>{user.email}</td>

                                    <td>{user.role}</td>

                                    <td>

{

new Date(user.created_at).toLocaleDateString(

"en-IN",

{

day:"2-digit",

month:"short",

year:"numeric"

}

)

}

</td>

                                </tr>

                            ))

                        }

                    </tbody>

                </table>

            </div>

        </DashboardLayout>

    );

}

export default AdminDashboard;