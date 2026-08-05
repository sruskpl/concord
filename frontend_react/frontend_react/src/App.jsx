import { Routes, Route } from "react-router-dom";
import OperatorDashboard from "./pages/OperatorDashboard";
import ReviewerDashboard from "./pages/ReviewerDashboard";
import ExceptionDetails from "./pages/ExceptionDetails";
import AdminAuditLogs from "./pages/AdminAuditLogs";
import OperatorAuditLogs from "./pages/OperatorAuditLogs";
import ReviewerAuditLogs from "./pages/ReviewerAuditLogs";
import Reports from "./pages/Reports";
import AdminDashboard from "./pages/AdminDashboard";
import ExceptionQueue from "./pages/ExceptionQueue";
import ReviewerExceptions from "./pages/ReviewerExceptions";
import SessionTable from "./components/SessionTable";
import OperatorSessions from "./pages/OperatorSessions";
import AdminUsers from "./pages/AdminUsers";
import AdminReports from "./pages/AdminReports";
import Auth from "./pages/Auth";
import Concord from "./pages/Concord";
import Home from "./pages/Home";

function App() {

    return (

            <Routes>

                <Route
                    path="/operator"
                    element={<OperatorDashboard />}
                />

                <Route
    path="/reviewer"
    element={<ReviewerDashboard />}
/>

                <Route
                    path="/reviewer/exception/:id"
                    element={<ExceptionDetails />}
                />

                <Route
    path="/operator/audit"
    element={<OperatorAuditLogs />}
 />

<Route
    path="/reviewer/audit"
    element={<ReviewerAuditLogs />}
 />

<Route
    path="/admin/audit"
    element={<AdminAuditLogs />}
 />

                <Route path="/reports" element={<Reports />} />

                <Route path="/admin" element={<AdminDashboard/>}/>

                <Route

path="/admin/users"

element={<AdminUsers />}

/>

<Route

path="/admin/reports"

element={<AdminReports />}

/>

                <Route
                    path="/reviewer/exceptions"
                    element={<ExceptionQueue />}
                />

                <Route

                    path="/operator/sessions"

                    element={<OperatorSessions />}

                />

                <Route

path="/reviewer/reports"

element={<Reports/>}

/>

<Route
    path="/"
    element={<Home />}
 />

<Route
    path="/auth"
    element={<Auth />}
 />

 <Route path="/concord" element={<Concord />} />

            </Routes>

    );

}

export default App; 