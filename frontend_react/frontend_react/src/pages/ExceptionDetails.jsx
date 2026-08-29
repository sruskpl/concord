import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "./ExceptionDetails.css";

import DashboardLayout from "../layouts/DashboardLayout";

function ExceptionDetails() {

    const { id } = useParams();

    const navigate = useNavigate();

    const [exception, setException] = useState(null);

    const [comment, setComment] = useState("");

    useEffect(() => {

        openException();

    }, []);

    async function openException() {

    const response = await fetch(

        `http://localhost:5000/exceptions/${id}`,

        {

            headers: {

                Authorization:
                    `Bearer ${localStorage.getItem("access_token")}`

            }

        }

    );

    const data = await response.json();

    if (!response.ok) {

        alert("Unable to load exception.");

        return;

    }

    if (data.status === "OPEN") {

        const statusResponse = await fetch(

            `http://localhost:5000/exceptions/${id}/status`,

            {

                method: "PATCH",

                headers: {

                    "Content-Type": "application/json",

                    Authorization:
                        `Bearer ${localStorage.getItem("access_token")}`

                },

                body: JSON.stringify({

                    status: "UNDER REVIEW"

                })

            }

        );

        if (!statusResponse.ok) {

            alert("Unable to start exception review.");

            return;

        }

    }

    await fetchException();

}
    async function fetchException() {

    const response = await fetch(
        `http://localhost:5000/exceptions/${id}`,
        {
            headers:{
                Authorization:
                    `Bearer ${localStorage.getItem("access_token")}`
            }
        }
    );

    const data = await response.json();

    setException(data);
}

    async function addComment(event){

    event.preventDefault();

    const response = await fetch(

        `http://localhost:5000/exceptions/${id}/comments`,

        {

            method:"POST",

            headers:{
                "Content-Type":"application/json",
                Authorization:
                    `Bearer ${localStorage.getItem("access_token")}`
            },

            body:JSON.stringify({

                comment:comment

            })

        }

    );

    if(response.ok){

        setComment("");

        fetchException();

    }

}

async function updateStatus(status) {

    const response = await fetch(

        `http://localhost:5000/exceptions/${id}/status`,

        {

            method: "PATCH",

            headers: {

                "Content-Type": "application/json",

                Authorization:
                    `Bearer ${localStorage.getItem("access_token")}`

            },

            body: JSON.stringify({

                status

            })

        }

    );

    if (!response.ok) {

        alert("Unable to update exception.");

        return;

    }

    await fetchException();

    alert(`Exception marked as ${status}.`);

}

    if (!exception) {

        return (
            <DashboardLayout role="reviewer">
                <h2>Loading...</h2>
            </DashboardLayout>
        );

    }

    return (

        <DashboardLayout role="reviewer">

            <h1>Exception #{exception.exception_id}</h1>

            <div className="details-card">

                <h2>Exception Information</h2>

                <p>
                    <strong>Type:</strong>
                    {" "}
                    {exception.exception_type}
                </p>

                <p>
                    <strong>Status:</strong>
                    {" "}
                    {exception.status}
                </p>

                <p>
                    <strong>Severity:</strong>
                    {" "}
                    {exception.severity}
                </p>

                <p>
                    <strong>Description:</strong>
                    {" "}
                    {exception.description}
                </p>

            </div>

            <div className="details-card">

                <h2>Transaction</h2>

                <div className="details-card">

    <h2>Source Comparison</h2>

    <table className="exception-table">

        <thead>

            <tr>

                <th>Source</th>

                <th>Amount</th>

                <th>Currency</th>

                <th>Date</th>

                <th>Status</th>

            </tr>

        </thead>

        <tbody>

            {

                exception.related_transactions.map((transaction,index)=>(

                    <tr key={index}>

                        <td>{transaction.source}</td>

                        <td>{transaction.amount}</td>

                        <td>{transaction.currency}</td>

                        <td>{transaction.date}</td>

                        <td>{transaction.status}</td>

                    </tr>

                ))

            }

        </tbody>

    </table>

</div>

                <p>
                    <strong>Reference:</strong>
                    {" "}
                    {exception.transaction.transaction_reference}
                </p>

                <p>
                    <strong>Customer:</strong>
                    {" "}
                    {exception.transaction.customer_id}
                </p>

                <p>
                    <strong>Amount:</strong>
                    {" "}
                    {exception.transaction.amount}
                </p>

                <p>
                    <strong>Currency:</strong>
                    {" "}
                    {exception.transaction.currency}
                </p>

                <p>
                    <strong>Date:</strong>
                    {" "}
                    {exception.transaction.transaction_date}
                </p>

            </div>

            <div className="details-card">

    <h2>
        Investigation Comments
    </h2>

    {

        exception.comments.length === 0 ?

        (

            <p>
                No comments yet.
            </p>

        )

        :

        (

            exception.comments.map((comment) => (

                <div
                    key={comment.id}
                    className="comment-card"
                >

                    <strong>

                        {comment.employee_id}

                    </strong>

                    <p>

                        {comment.comment}

                    </p>

                </div>

            ))

        )

    }

</div>

        <div className="details-card">

    <h2>

        Add Comment

    </h2>

    <textarea

        value={comment}

        onChange={(event)=>

            setComment(event.target.value)

        }

        rows="4"

        className="comment-box"

    />

    <button

        type="button"

        className="comment-btn"

        onClick={addComment}

    >

        Submit Comment

    </button>

    <div className="action-buttons">

    <button
        className="resolve-btn"
        onClick={() => updateStatus("RESOLVED")}
    >
        Resolve
    </button>

<button
    className="keep-open-btn"
    onClick={() => updateStatus("OPEN")}
>
    Keep Open
</button>

<button
    className="escalate-btn"
    onClick={() => updateStatus("ESCALATED")}
>
    Escalate
</button>

</div>

</div>

        </DashboardLayout>

    );

}

export default ExceptionDetails;