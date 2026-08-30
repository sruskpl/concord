import "./SessionCard.css";

function SessionCard(props) {
    return (
        <section className="session-card">

            <h2>Today's Reconciliation Session</h2>

            <div className="session-details">

            <div className="detail-row">
                <span>Business Date</span>
                <strong>{props.businessDate || "--"}</strong>
            </div>

            <div className="detail-row">
    <span>Session Status</span>

    <strong>
        {props.status === "COMPLETED"
            ? "NOT STARTED"
            : props.status || "NOT STARTED"}
    </strong>
</div>

            <div className="detail-row">
                <span>Today's Sessions</span>
                <strong>{props.todaysSessions}</strong>
            </div>

            <div className="detail-row">
                <span>Total Sessions</span>
                <strong>{props.totalSessions}</strong>
            </div>

            </div>

    <div className="button-row">

{props.status === "" && (

<button
    className="start-session-btn"
    onClick={props.onStartSession}
>
    Start Session
</button>

)}

{props.status === "UPLOADING" && (

<button
    className="upload-btn"
    onClick={props.onUploadClick}
>
    Upload CSV
</button>

)}

{props.status === "READY" && (

<button
    className="reconcile-btn"
    onClick={props.onReconcile}
>
    Run Reconciliation
</button>

)}

{props.status === "COMPLETED" && (

<button
    className="start-session-btn"
    onClick={props.onStartSession}
>
    Start Session
</button>

)}

</div>
            <div className="source-container">

    <div className="source-card">

        <p>Uploaded Sources:</p>

        <ul>

            {props.status === "COMPLETED" ? (

                <li>Start a new reconciliation session.</li>

            ) : (

                (props.uploadedSources ?? []).map((source) => (

                    <li key={source}>
                        {source}
                    </li>

                ))

            )}

        </ul>

    </div>


    <div className="source-card">

        <p>Missing Sources:</p>

        <ul>

            {!props.sessionStarted || props.status === "COMPLETED" ? (

                <li>Start a reconciliation session.</li>

            ) : props.missingSources.length === 0 ? (

                <li>✅ No Missing Sources</li>

            ) : (

                props.missingSources.map((source) => (

                    <li key={source}>
                        {source}
                    </li>

                ))

            )}

        </ul>

    </div>

</div>
        </section>
    );
}

export default SessionCard;