import "../styles/Table.css";
import { useNavigate } from "react-router-dom";

function SessionTable({ sessions, latest = false }) {
    const navigate = useNavigate();
    sessions = sessions ?? [];

    return (

        <div className="table-card">

            <div className="table-header">

    <h2>

        {latest ? "Sessions" : "All Sessions"}

    </h2>

    <div className="table-header-right">

        <span className="table-info">

            {latest
                ? `Showing latest ${sessions.length} sessions`
                : `Total Sessions: ${sessions.length}`}

        </span>

        {latest && (

            <button
                className="view-all-btn"
                onClick={() => navigate("/operator/sessions")}
            >
                View All →
            </button>

        )}

    </div>

</div>

            <table className="exception-table">

                <thead>

                    <tr>

                        <th>ID</th>

                        <th>Business Date</th>

                        <th>Status</th>

                        <th>Matched</th>

                        <th>Exceptions</th>

                    </tr>

                </thead>

                <tbody>

                    {sessions.map((session)=>(

                        <tr key={session.id}>

                            <td>{session.id}</td>

                            <td>{session.business_date}</td>

                            <td>

                                <span
className={`status-pill ${
session.status === "READY"
? "ready"
: session.status === "COMPLETED"
? "completed"
: session.status === "IN_PROGRESS"
? "progress"
: "open"
}`}
>

                                    {session.status}

                                </span>

                            </td>

                            <td>{session.matched_transactions ?? 0}</td>

                            <td>{session.exception_count ?? 0}</td>

                        </tr>

                    ))}

                </tbody>

            </table>

        </div>

    );

}

export default SessionTable;