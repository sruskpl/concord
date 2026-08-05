import ReviewerHeader from "../components/ReviewerHeader";
import ReviewerSummaryCards from "../components/ReviewerSummaryCards";
import DashboardLayout from "../layouts/DashboardLayout";
import ExceptionTable from "../components/ExceptionTable";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import "./ReviewerDashboard.css";

function ReviewerDashboard() {

    const navigate=useNavigate();

    const [exceptions, setExceptions] = useState([]);

    async function fetchExceptions() {

    // Get latest completed reconciliation session

    const sessionResponse = await fetch(
        "http://localhost:5000/exceptions/session-info"
    );

    const sessionData = await sessionResponse.json();

    if (!sessionData.session_id) {

        setExceptions([]);

        return;

    }

    // Get exceptions of that session

    const response = await fetch(
        `http://localhost:5000/exceptions/session/${sessionData.session_id}`
    );

    if (!response.ok) {

        return;

    }

    const data = await response.json();

    setExceptions(data);

}

    useEffect(() => {

        fetchExceptions();

    }, []);

    return (

        <DashboardLayout role="reviewer">

            <ReviewerHeader />

            <ReviewerSummaryCards
                exceptions={exceptions}
            />

            <ExceptionTable
    exceptions={
        exceptions
            .filter(e => e.status === "OPEN")
            .slice(0, 5)
    }
    latest={true}
/>
        </DashboardLayout>

    );

}

export default ReviewerDashboard;