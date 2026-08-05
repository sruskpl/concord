import { useEffect, useMemo, useState } from "react";
import DashboardLayout from "../layouts/DashboardLayout";
import ExceptionTable from "../components/ExceptionTable";
import "./ReviewerExceptions.css";

function ReviewerExceptions() {

    const [exceptions, setExceptions] = useState([]);

    const [search, setSearch] = useState("");

    const [status, setStatus] = useState("ALL");

    const [severity, setSeverity] = useState("ALL");

    async function fetchExceptions() {

        headers:{

    Authorization:
        `Bearer ${localStorage.getItem("access_token")}`

}

        const data = await response.json();

        setExceptions(data);

    }

    useEffect(() => {

        fetchExceptions();

    }, []);

    const filteredExceptions = useMemo(() => {

        return exceptions

            .filter((exception) => {

                const searchMatch =

                    exception.exception_type
                        .toLowerCase()
                        .includes(search.toLowerCase())

                    ||

                    exception.id
                        .toString()
                        .includes(search);

                const statusMatch =

                    status === "ALL"

                    ||

                    exception.status === status;

                const severityMatch =

                    severity === "ALL"

                    ||

                    exception.severity === severity;

                return (

                    searchMatch

                    &&

                    statusMatch

                    &&

                    severityMatch

                );

            })

            .sort((a, b) => b.id - a.id);

    }, [exceptions, search, status, severity]);

    return (

        <DashboardLayout role="reviewer">

            <h1 className="page-title">

                Exception Queue

            </h1>

            <div className="filters">

                <input

                    placeholder="Search by ID or Type"

                    value={search}

                    onChange={(e)=>setSearch(e.target.value)}

                />

                <select

                    value={status}

                    onChange={(e)=>setStatus(e.target.value)}

                >

                    <option value="ALL">All Status</option>

                    <option value="OPEN">Open</option>

                    <option value="RESOLVED">Resolved</option>

                    <option value="ESCALATED">Escalated</option>

                </select>

                <select

                    value={severity}

                    onChange={(e)=>setSeverity(e.target.value)}

                >

                    <option value="ALL">All Severity</option>

                    <option value="HIGH">High</option>

                    <option value="MEDIUM">Medium</option>

                    <option value="LOW">Low</option>

                </select>

            </div>

            <ExceptionTable

                exceptions={filteredExceptions}

                latest={false}

            />

        </DashboardLayout>

    );

}

export default ReviewerExceptions;