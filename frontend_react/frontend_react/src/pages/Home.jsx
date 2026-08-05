import { useNavigate } from "react-router-dom";
import "../styling/style.css";

function Home() {

    const navigate = useNavigate();

    return(
    <>
    <div className="hero">
        <div className="top-actions">
            <button id="transitionButton"
                onClick={() => navigate("/auth")}>
                Login / Register →
            </button>
        </div>
        <h1 id="welcome">Concord</h1>
        <h2 id="sub-title">
            Enterprise Reconciliation Platform  
        </h2>
        <div id="tagline">
            <p>Reconcile with confidence.</p>
            <p>Every transaction. Every decision. Fully auditable.</p>
        </div>
            <div id="why-link"
                onClick={() => navigate("/concord")}>
                <h4>Why Concord →</h4>
    </div>
    </div>
    </>
    );
}

export default Home;
