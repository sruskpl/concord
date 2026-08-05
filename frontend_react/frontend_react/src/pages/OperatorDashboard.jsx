import { useEffect, useState } from "react";
import { useRef } from "react";
import { useNavigate } from "react-router-dom";
import SessionCard from "../components/SessionCard";
import DashboardLayout from "../layouts/DashboardLayout";
import OperatorSummaryCards from "../components/OperatorSummaryCards";
import SessionTable from "../components/SessionTable";

function OperatorDashboard() {

    const navigate=useNavigate();

    const [user, setUser] = useState(null);

    const [sessions,setSessions]=useState([]);

    async function fetchSessions() {

    try {

        const response = await fetch(

    "http://localhost:5000/sessions",

    {

        headers: {

            Authorization:
                `Bearer ${localStorage.getItem("access_token")}`

        }

    }

);

        const data = await response.json();

        setSessions(data);

    }

    catch (error) {

    }

}

    const [dashboard, setDashboard] = useState({
        sessionId: null,
        businessDate: "",
        todaysSessions: 0,
        totalSessions: 0,
        status: "",
        uploadedSources: [],
        missingSources: []
    });

    const fileInputRef = useRef(null);

    async function fetchDashboard() {

        try {

            const response = await fetch(

    "http://localhost:5000/dashboard/current",

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

            setDashboard({
                sessionId: data.session_id,
                businessDate: data.business_date,
                todaysSessions: data.todays_sessions,
                totalSessions: data.total_sessions,
                status: data.current_session_status,
                canStartSession: data.can_start_session,
                uploadedSources: data.uploaded_sources,
                missingSources: data.missing_sources,
                matchedTransactions: data.matched_transactions ?? 0,
                exceptionTransactions: data.exception_transactions ?? 0,
                pendingReview: data.pending_review ?? 0
            });

        } catch (error) {
                console.error("Fetch failed:");
                console.error(error);

            if (error instanceof Error) {
                console.error(error.message);
            }

        }

    }

    async function fetchCurrentUser() {

    const response = await fetch(
        "http://localhost:5000/me",
        {
            headers: {
                Authorization:
                    `Bearer ${localStorage.getItem("access_token")}`
            }
        }
    );

    const data = await response.json();

    setUser(data);

}

useEffect(() => {

    fetchDashboard();
    fetchSessions();
    fetchCurrentUser();

}, []);

async function startSession() {

    try {

        const token = localStorage.getItem("access_token");

const response = await fetch(
    "http://localhost:5000/sessions/start",
    {
        method: "POST",
        headers: {
            Authorization: `Bearer ${token}`
        }
    }
);

        const data = await response.json();

if (!response.ok) {
    alert(data.detail);
    return;
}

alert(data.message);

        await fetchDashboard();
        await fetchSessions();

    }

    catch (error) {
        console.error("Fetch failed:");
        console.error(error);
        if (error instanceof Error) {
                console.error(error.message);
            }
    }
}

function openFilePicker(){

    fileInputRef.current.click();

}

async function uploadFile(event){

    const file = event.target.files[0];

    if(!file)
        return;

    const formData = new FormData();

    formData.append(
    "file",
    file
);

const response = await fetch(

    "http://localhost:5000/upload",

    {

        method: "POST",

        headers: {

            Authorization:
                `Bearer ${localStorage.getItem("access_token")}`

        },

        body: formData

    }

);

const data = await response.json();

if (!response.ok) {
    alert(data.detail);
    return;
}

alert(data.message);

event.target.value = "";

await fetchDashboard();
await fetchSessions();

}

async function reconcile() {

    if (!dashboard.sessionId) {
        alert("No active session.");
        return;
    }

    const response = await fetch(

    `http://localhost:5000/reconcile/${dashboard.sessionId}`,

    {

        method: "POST",

        headers: {

            Authorization:
                `Bearer ${localStorage.getItem("access_token")}`

        }

    }

);

    const data = await response.json();

    if (!response.ok) {
    alert(data.detail);
    return;
    }

    alert("Reconciliation Complete");

    await fetchDashboard();
    await fetchSessions();

// force React to render latest state
    setTimeout(async () => {
        await fetchDashboard();
        await fetchSessions();
    }, 300);

}

const hour = new Date().getHours();

let greeting = "Good Evening";

if (hour < 12)
    greeting = "Good Morning";
else if (hour < 18)
    greeting = "Good Afternoon";

    return (

        <DashboardLayout role="operator">
        <div className="dashboard-header">

        <h1>
            {greeting}, {user?.full_name ?? "Operator"}
        </h1>

        <p>
            Ready to begin today's reconciliation.
        </p>

        </div>

        <OperatorSummaryCards

    matched={dashboard.matchedTransactions}

    exceptions={dashboard.exceptionTransactions}

    pending={dashboard.pendingReview}

    matchRate={

        dashboard.matchedTransactions +

        dashboard.exceptionTransactions === 0

            ? 0

            : (

                dashboard.matchedTransactions /

                (

                    dashboard.matchedTransactions +

                    dashboard.exceptionTransactions

                )

            ) * 100

    }

/>

    <SessionCard
        sessionId={dashboard.sessionId}
        businessDate={dashboard.businessDate}
        status={dashboard.status}
        todaysSessions={dashboard.todaysSessions}
        totalSessions={dashboard.totalSessions}
        uploadedSources={dashboard.uploadedSources}
        missingSources={dashboard.missingSources}
        onStartSession={startSession}
        onUploadClick={openFilePicker}
        onReconcile={reconcile}
        sessionStarted={dashboard.sessionId !== null}
        canStartSession={dashboard.canStartSession}
    />

    <input
        type="file"
        ref={fileInputRef}
        hidden
        accept=".csv"
        onChange={uploadFile}
    />

    <SessionTable

    sessions={sessions.slice(0,5)}

    latest={true}

/>

    </DashboardLayout>

);
}

export default OperatorDashboard;