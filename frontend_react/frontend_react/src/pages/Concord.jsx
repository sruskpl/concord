import "../styling/style.css";
import { useNavigate } from "react-router-dom";

function Concord() {

    const navigate = useNavigate();

    return(
    <>
    <button
    id="backHomeBtn"
    onClick={() => navigate("/")}>
    ← Home
    </button>
    <div className="why-page">
        <h1 id="why-heading">Why Concord?</h1>
        <main>
            <div className="why-container">
                <section className="info-card">
                    <h2>The meaning behind the name</h2>
                    <p><b>Concord</b> means agreement, harmony, and consistency.
                    In financial reconciliation, every transaction should arrive at the same truth across accounts, systems, and reports. Concord embodies that principle by bringing records into alignment, reducing discrepancies, and providing a single, reliable view of financial data.
                    Because when systems agree, businesses can move forward with confidence.</p>
                </section>
                <section className="info-card">
                    <h2>Reconciliation without uncertainty</h2>
                    <p>Financial operations teams process thousands of transactions every day. Even a single mismatch can lead to delayed settlements, reporting errors, and hours of manual investigation.
                    Concord streamlines reconciliation by bringing transactions, validation, and exception management into one unified workspace.</p>
                </section>
                <section className="info-card">
                    <h2>Enterprise-grade workflow</h2>
                    <ul>
                        <li>Secure authentication and protected access</li>
                        <li>Centralized reconciliation sessions</li>
                        <li>Intelligent exception tracking</li>
                        <li>Real-time reconciliation metrics</li>
                        <li>Comprehensive audit visibility</li>   
                    </ul>
                </section>
                <section className="info-card">
                    <h2>Why it matters</h2>
                    <p>Operational efficiency isn't just about processing data faster—it's about making financial decisions with confidence.
                    By reducing manual effort and improving visibility, Concord helps teams focus on resolving meaningful exceptions instead of searching for them.</p>
                </section>
            </div>
        </main>
    </div>
    </>
    );
}

export default Concord;