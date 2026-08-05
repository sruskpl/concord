import { Link } from "react-router-dom";
import "./ExceptionTable.css";
import { useNavigate } from "react-router-dom";

function ExceptionTable({

    exceptions = [],

    sessionId,

    latest = false

}) {

    const navigate = useNavigate();

    function getStatusClass(status) {

        switch (status) {

            case "OPEN":
                return "status-open";

            case "RESOLVED":
                return "status-resolved";

            case "ESCALATED":
                return "status-escalated";

            default:
                return "";

        }

    }

    function getSeverityClass(severity) {

        switch (severity) {

            case "HIGH":
                return "severity-high";

            case "MEDIUM":
                return "severity-medium";

            case "LOW":
                return "severity-low";

            default:
                return "";

        }

    }

    return (

        <div className="table-card">

            <div className="table-header">

                <h2>

    {latest

        ? "Latest Exceptions"

        : `All Exceptions of Session #${sessionId}`}

</h2>

                <div className="table-header-right">

                    {latest && (

<span className="table-info">

    Showing latest {exceptions.length} exceptions

</span>

)}
                    {latest && (
            
                    <button
                        className="view-all-btn"
                        onClick={() => navigate("/reviewer/exceptions")}
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

                        <th>Type</th>

                        <th>Status</th>

                        <th>Severity</th>

                        <th>Action</th>

                    </tr>

                </thead>

                <tbody>

                    {exceptions.map((exception) => (

                        <tr key={exception.id}>

                            <td>{exception.id}</td>

                            <td>{exception.exception_type}</td>

                            <td>

<span
className={`status-pill ${exception.status.toLowerCase()}`}
>

{exception.status}

</span>

</td>

<td>

<span
className={`severity-pill ${exception.severity.toLowerCase()}`}
>

{exception.severity}

</span>

</td>
                            <td>

                                <Link
                                    className="details-btn"
                                    to={`/reviewer/exception/${exception.id}`}
                                >
                                    View Details
                                </Link>

                            </td>

                        </tr>

                    ))}

                </tbody>

            </table>

        </div>

    );

}

export default ExceptionTable;