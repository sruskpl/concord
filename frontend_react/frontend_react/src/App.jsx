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
import ProtectedRoutes from "./components/ProtectedRoutes";

function App() {

    return (

            <Routes>

                <Route
    path="/operator"
    element={
        <ProtectedRoutes allowedRoles={["operator"]}>
            <OperatorDashboard />
        </ProtectedRoutes>
    }
/>

                <Route
    path="/reviewer"
    element={
        <ProtectedRoutes allowedRoles={["reviewer"]}>
            <ReviewerDashboard />
        </ProtectedRoutes>
    }
/>

                <Route
    path="/reviewer/exception/:id"
    element={
        <ProtectedRoutes allowedRoles={["reviewer"]}>
            <ExceptionDetails />
        </ProtectedRoutes>
    }
/>

                <Route
    path="/operator/audit"
    element={
        <ProtectedRoutes allowedRoles={["operator"]}>
            <OperatorAuditLogs />
        </ProtectedRoutes>
    }
/>

<Route
    path="/reviewer/audit"
    element={
        <ProtectedRoutes allowedRoles={["reviewer"]}>
            <ReviewerAuditLogs />
        </ProtectedRoutes>
    }
/>

<Route
    path="/admin/audit"
    element={
        <ProtectedRoutes allowedRoles={["admin"]}>
            <AdminAuditLogs />
        </ProtectedRoutes>
    }
/>

                <Route
    path="/reports"
    element={
        <ProtectedRoutes allowedRoles={["reviewer"]}>
            <Reports />
        </ProtectedRoutes>
    }
/>

                <Route
    path="/admin"
    element={
        <ProtectedRoutes allowedRoles={["admin"]}>
            <AdminDashboard />
        </ProtectedRoutes>
    }
/>

                <Route
    path="/admin/users"
    element={
        <ProtectedRoutes allowedRoles={["admin"]}>
            <AdminUsers />
        </ProtectedRoutes>
    }
/>

<Route
    path="/admin/reports"
    element={
        <ProtectedRoutes allowedRoles={["admin"]}>
            <AdminReports />
        </ProtectedRoutes>
    }
/>

                <Route
    path="/reviewer/exceptions"
    element={
        <ProtectedRoutes allowedRoles={["reviewer"]}>
            <ExceptionQueue />
        </ProtectedRoutes>
    }
/>

                <Route
    path="/operator/sessions"
    element={
        <ProtectedRoutes allowedRoles={["operator"]}>
            <OperatorSessions />
        </ProtectedRoutes>
    }
/>

                <Route
    path="/reviewer/reports"
    element={
        <ProtectedRoutes allowedRoles={["reviewer"]}>
            <Reports />
        </ProtectedRoutes>
    }
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