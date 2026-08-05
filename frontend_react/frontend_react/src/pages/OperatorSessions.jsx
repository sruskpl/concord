import { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";

import SessionTable from "../components/SessionTable";

function OperatorSessions() {

    const [sessions, setSessions] = useState([]);

    async function fetchSessions() {

        const response = await fetch(

            "http://localhost:5000/sessions"

        );

        const data = await response.json();

        setSessions(data);

    }

    useEffect(() => {

        fetchSessions();

    }, []);

    return (

        <DashboardLayout role="operator">

            <div className="dashboard-header">

    <h1>

        Sessions

    </h1>

    <p>

        View all reconciliation sessions.

    </p>

</div>

<SessionTable

    sessions={sessions}

/>

        </DashboardLayout>

    );

}

export default OperatorSessions;