import { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";

import "../styles/Table.css";

function AdminUsers() {

    const [users, setUsers] = useState([]);

    useEffect(() => {

        async function fetchUsers() {

    const response = await fetch(

        "http://127.0.0.1:5000/admin/users",

        {
            headers: {
                Authorization:
                    `Bearer ${localStorage.getItem("access_token")}`
            }
        }

    );

    const data = await response.json();

    setUsers(data);

}

        fetchUsers();

    }, []);

    return (

        <DashboardLayout role="admin">

            <div className="dashboard-header">

                <h1>

                    User Management

                </h1>

                <p>

                    Registered employees

                </p>

            </div>

            <div className="table-card">

                <table className="exception-table">

                    <thead>

                        <tr>

                            <th>Employee</th>

                            <th>Name</th>

                            <th>Email</th>

                            <th>Role</th>

                            <th>Created</th>

                            <th>Last Login</th>

                        </tr>

                    </thead>

                    <tbody>

                        {users.map(user => (

                            <tr key={user.employee_id}>

                                <td>{user.employee_id}</td>

                                <td>{user.full_name}</td>

                                <td>{user.email}</td>

                                <td>

                                    <span className="status-pill completed">

                                        {user.role}

                                    </span>

                                </td>

                                <td>
    {new Date(user.created_at).toLocaleDateString(
        "en-IN",
        {
            day: "2-digit",
            month: "short",
            year: "numeric"
        }
    )}
</td>

                                <td>

    {

        user.last_login

        ?

        new Date(user.last_login).toLocaleString(

            "en-IN",

            {

                day: "2-digit",
                month: "short",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit"

            }

        )

        :

        "--"

    }

</td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </DashboardLayout>

    );

}

export default AdminUsers;