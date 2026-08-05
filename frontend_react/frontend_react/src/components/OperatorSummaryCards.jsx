import "./OperatorSummaryCards.css";

function SummaryCards({

    matched,

    exceptions,

    pending,

    matchRate

}) {

    return (

        <div className="summary-grid">

            <div className="summary-card">

                <p>Matched</p>

                <h2>{matched}</h2>

            </div>

            <div className="summary-card">

                <p>Exceptions</p>

                <h2>{exceptions}</h2>

            </div>

            <div className="summary-card">

                <p>Pending Review</p>

                <h2>{pending}</h2>

            </div>

            <div className="summary-card">

                <p>Match Rate</p>

                <h2>{Number(matchRate).toFixed(2)}%</h2>

            </div>

        </div>

    );

}

export default SummaryCards;