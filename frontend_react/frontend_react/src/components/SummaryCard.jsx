import "./SummaryCard.css";

function SummaryCard({ title, value }) {
    return (
        <div className="summary-card">
            <h3>{title}</h3>
            <h2>{value}</h2>
        </div>
    );
}

export default SummaryCard;