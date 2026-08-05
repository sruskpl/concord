import "./Sidebar.css";

import { useLocation, useNavigate } from "react-router-dom";

function Sidebar({ role }) {

    const navigate = useNavigate();

    const location = useLocation();
    return (

        <aside className="sidebar">

            <div className="sidebar-logo">

                Workspace

            </div>

            <nav className="sidebar-nav">

                {role === "operator" && (

                    <>

                        <button
    className={`sidebar-item ${
        location.pathname === "/operator" ? "active" : ""
    }`}
    onClick={() => navigate("/operator")}
>
    Dashboard
</button>

                        <button
    className={`sidebar-item ${
        location.pathname === "/operator/sessions" ? "active" : ""
    }`}
    onClick={() => navigate("/operator/sessions")}
>
    Sessions
</button>

                        <button
    className={`sidebar-item ${
        location.pathname === "/operator/audit"
            ? "active"
            : ""
    }`}
    onClick={() => navigate("/operator/audit")}
>
    Audit Logs
</button>

                        <button
    className="sidebar-item"
    onClick={() => {

        localStorage.removeItem("access_token");
localStorage.removeItem("role");

        window.location.href =
"http://localhost:5173/";

    }}
>
    Logout
</button>

                    </>

                )}

                {role === "reviewer" && (

                    <>

                        <button
    className={`sidebar-item ${
    location.pathname === "/reviewer"
        ? "active"
        : ""
}`}
    onClick={() => navigate("/reviewer")}
>
    Dashboard
</button>

                        <button
    className={`sidebar-item ${
        location.pathname.startsWith("/reviewer/exceptions") ||
        location.pathname.startsWith("/reviewer/exception")
            ? "active"
            : ""
    }`}
    onClick={() => navigate("/reviewer/exceptions")}
>
    Exception Queue
</button>

                        <button
    className={`sidebar-item ${
        location.pathname === "/reviewer/audit"
            ? "active"
            : ""
    }`}
    onClick={() => navigate("/reviewer/audit")}
>
    Audit Logs
</button>

                        <button
className={`sidebar-item ${
location.pathname==="/reviewer/reports"
? "active"
: ""
}`}
onClick={()=>navigate("/reviewer/reports")}
>

Reports

</button>

                        <button
    className="sidebar-item"
    onClick={() => {

        localStorage.removeItem("access_token");
localStorage.removeItem("role");

        window.location.href =
"http://localhost:5173/";
    }}
>
    Logout
</button>
                    </>

                )}

                {role === "admin" && (

                    <>

                        <button
    className={`sidebar-item ${
        location.pathname === "/admin"
            ? "active"
            : ""
    }`}
    onClick={() => navigate("/admin")}
>
    Dashboard
</button>

                        <button

className={`sidebar-item ${

location.pathname === "/admin/users"

? "active"

: ""

}`}

onClick={() => navigate("/admin/users")}

>

Users

</button>
                        <button
    className={`sidebar-item ${
        location.pathname === "/admin/audit"
            ? "active"
            : ""
    }`}
    onClick={() => navigate("/admin/audit")}
>
    Audit Logs
</button>

                        <button

className={`sidebar-item ${

location.pathname === "/admin/reports"

? "active"

: ""

}`}

onClick={() => navigate("/admin/reports")}

>

Reports

</button>
                        <button
    className="sidebar-item"
    onClick={() => {

        localStorage.removeItem("access_token");
localStorage.removeItem("role");

       window.location.href =
"http://localhost:5173/";

    }}
>
    Logout
</button>

                    </>

                )}

            </nav>

        </aside>

    );

}

export default Sidebar;