import "./ReviewerSummaryCards.css";

function SummaryCards({ exceptions }) {

    const total = exceptions.length;

    const open = exceptions.filter(
        (e) => e.status === "OPEN"
    ).length;

    const resolved = exceptions.filter(
        (e) => e.status === "RESOLVED"
    ).length;

    const high = exceptions.filter(
        (e) => e.severity === "HIGH"
    ).length;

    return (

        <section className="summary-grid">

            <div className="summary-card">

                <p>Total Exceptions</p>

                <h2>{total}</h2>

            </div>

            <div className="summary-card">

                <p>Open</p>

                <h2>{open}</h2>

            </div>

            <div className="summary-card">

                <p>Resolved</p>

                <h2 className="resolved-number">
                    {resolved}
                </h2>

            </div>

            <div className="summary-card">

                <p>High Severity</p>

                <h2 className="danger-number">
                    {high}
                </h2>

            </div>

        </section>

    );

}

export default SummaryCards;