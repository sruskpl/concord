import { useEffect, useState } from "react";
import DashboardLayout from "../layouts/DashboardLayout";
import "../styles/Table.css";

function ReviewerAuditLogs() {

    const [logs, setLogs] = useState([]);

    useEffect(() => {

        async function fetchLogs() {

    const response = await fetch(

        "http://127.0.0.1:5000/audit-logs/reviewer",

        {

            headers: {

                Authorization:
                    `Bearer ${localStorage.getItem("access_token")}`

            }

        }

    );

    if (!response.ok) {

        return;

    }

    const data = await response.json();

    setLogs(data);

}

        fetchLogs();

    }, []);

    return (

        <DashboardLayout role="reviewer">

            <div className="dashboard-header">

                <h1>Audit Logs</h1>

                <p>Operational activity history</p>

            </div>

            <table className="exception-table">

                <thead>

                    <tr>

                        <th>Time</th>

                        <th>Employee</th>

                        <th>Action</th>

                        <th>Description</th>

                    </tr>

                </thead>

                <tbody>

                    {logs.map(log => (

                        <tr key={log.id}>

                            <td>

{new Date(log.created_at).toLocaleString()}

</td>

                            <td>

👤 {log.created_by}

</td>

                            <td>

<span className="status-pill completed">

{log.action.replaceAll("_"," ")}

</span>

</td>

                            <td>{log.description}</td>

                        </tr>

                    ))}

                </tbody>

            </table>

        </DashboardLayout>

    );

}

export default ReviewerAuditLogs;