import { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";

import ExceptionTable from "../components/ExceptionTable";

function ExceptionQueue(){

const [exceptions, setExceptions] = useState([]);

const [sessionId, setSessionId] = useState(null);

useEffect(() => {

    fetch("http://localhost:5000/exceptions/session-info")

        .then(r => r.json())

        .then(data => {

            setSessionId(data.session_id);

            if (data.session_id) {

                fetch(`http://localhost:5000/exceptions/session/${data.session_id}`)

                    .then(r => r.json())

                    .then(exceptionData => {

                        setExceptions(exceptionData);

                    });

            }

        });

}, []);

return(

<DashboardLayout role="reviewer">

<h1>Exception Queue</h1>

<p>

Review all reconciliation exceptions.

</p>

<ExceptionTable

    exceptions={exceptions}

    sessionId={sessionId}

/>

</DashboardLayout>

);

}

export default ExceptionQueue;