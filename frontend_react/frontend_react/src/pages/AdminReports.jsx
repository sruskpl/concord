import { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";

import "../styles/Table.css";

import SummaryCard from "../components/SummaryCard";

function AdminReports() {

    const [report, setReport] = useState({});

    useEffect(() => {

        async function fetchReport() {

    const response = await fetch(

        "http://127.0.0.1:5000/admin/reports",

        {

            headers: {

                Authorization:
                    `Bearer ${localStorage.getItem("access_token")}`

            }

        }

    );

    if (!response.ok) {

        console.error(await response.text());

        return;

    }

    const data = await response.json();

    setReport(data);

}

        fetchReport();

    }, []);

    return (

        <DashboardLayout role="admin">

            <div className="dashboard-header">

                <h1>

                    Reports

                </h1>

                <p>

                    Enterprise reconciliation overview

                </p>

            </div>

            <div className="summary-grid">

                <SummaryCard

                    title="Employees"

                    value={report.total_users}

                />

                <SummaryCard

                    title="Completed Sessions"

                    value={report.completed_sessions}

                />

                <SummaryCard

                    title="Overall Match Rate"

                    value={`${report.match_rate}%`}

                />

                <SummaryCard

                    title="Total Exceptions Recorded"

                    value={report.exceptions}

                />

            </div>

        </DashboardLayout>

    );

}

export default AdminReports;