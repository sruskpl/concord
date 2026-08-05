import { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";

import "./Reports.css";

function Reports() {

    const [report, setReport] = useState({

    total:0,

    resolution_rate:0,

    backlog:0,

    escalated:0,

    most_common:"N/A",

    high_share:0

});

    async function fetchReport() {

    const response = await fetch(

        "http://localhost:5000/reviewer/reports",

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

    setReport(data);

}

    useEffect(() => {

        fetchReport();

    }, []);

    return (

        <DashboardLayout role="reviewer">

            <div className="dashboard-header">

                <h1>

                    Review Analytics

                </h1>

                <p>

                    Operational summary of today's review work.

                </p>

            </div>

            <div className="reports-grid">

<div className="report-card">

<h3>Total Investigations</h3>

<h1>{report.total}</h1>

</div>

<div className="report-card">

<h3>Resolution Rate</h3>

<h1>{report.resolution_rate}%</h1>

</div>

<div className="report-card">

<h3>Escalated Cases</h3>

<h1>{report.escalated}</h1>

</div>

<div className="report-card">

    <h3>Average Resolution Time</h3>

    <h1>

        {report.average_resolution_time}

        <span className="minutes">
            mins
        </span>

    </h1>

</div>

<div className="report-card">

<h3>Most Common Exception</h3>

<h2>{report.most_common}</h2>

</div>

<div className="report-card">

<h3>High Priority Share</h3>

<h1>{report.high_share}%</h1>

</div>

</div>

        </DashboardLayout>

    );

}

export default Reports;