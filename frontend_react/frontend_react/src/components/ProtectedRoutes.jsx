import { Navigate } from "react-router-dom";

function ProtectedRoutes({ allowedRoles, children }) {

    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");

    // User is not logged in
    if (!token) {

        return (
            <Navigate
                to="/auth"
                replace
            />
        );

    }

    // User is logged in but does not have permission
    if (!allowedRoles.includes(role)) {

        if (role === "operator") {

            return (
                <Navigate
                    to="/operator"
                    replace
                />
            );

        }

        if (role === "reviewer") {

            return (
                <Navigate
                    to="/reviewer"
                    replace
                />
            );

        }

        if (role === "admin") {

            return (
                <Navigate
                    to="/admin"
                    replace
                />
            );

        }

        return (
            <Navigate
                to="/auth"
                replace
            />
        );

    }

    return children;

}

export default ProtectedRoutes;