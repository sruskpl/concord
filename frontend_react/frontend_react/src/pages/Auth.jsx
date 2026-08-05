import "../styling/style.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Auth() {

    const navigate = useNavigate();

    const [showRegisterForm, setShowRegisterForm] = useState(false);
    const [loginEmail, setLoginEmail] = useState("");
    const [loginPassword, setLoginPassword] = useState("");
    const [employeeId, setEmployeeId] = useState("");
    const [fullName, setFullName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showLoginPassword, setShowLoginPassword] = useState(false);
    const [showRegisterPassword, setShowRegisterPassword] = useState(false);

    async function loginUser() {

    try {

        const response = await fetch(
            "http://localhost:5000/login",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email: loginEmail,
                    password: loginPassword
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

    localStorage.setItem(
        "access_token",
        data.access_token
    );

    localStorage.setItem(
        "role",
        data.role
    );

    alert("Login Successful!");

    if (data.role === "operator") {

        navigate("/operator");

    }

    else if (data.role === "reviewer") {

        navigate("/reviewer");

    }

    else {

        navigate("/admin");

    }

}

        else {

            alert(data.detail);

        }

    }

    catch (error) {

        console.error(error);

        alert("Unable to connect to backend.");

    }

}

    function showLogin() {
        setShowRegisterForm(false);
    }

    function showRegister() {
        setShowRegisterForm(true);
    }

    async function registerUser() {

    try {

        const response = await fetch(
            "http://localhost:5000/register",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    employee_id: employeeId,

                    full_name: fullName,

                    email: email,

                    password: password

                })

            }
        );

        const data = await response.json();

        if (response.ok) {

            alert("Registration Successful!");

            showLogin();

        }

        else {

            alert(data.detail);

        }

    }

    catch (error) {

        console.error(error);

        alert("Unable to connect to backend.");

    }

}
    return(
    <>
    <div className="auth-page">
        <div className="user-details">
            {!showRegisterForm && (
            <div id="login">
                <div className="auth-heading">
                    <h1>Concord</h1>
                    <h2>Sign in</h2>
                </div>
                <label>Email:</label>
                <input type="text" value={loginEmail} onChange={(e)=>setLoginEmail(e.target.value)} />
                <label>Password:</label>
                <div className="password-box">
                <input type={showLoginPassword ? "text" : "password"} value={loginPassword} onChange={(e)=>setLoginPassword(e.target.value)} />
                <span className="eye" onClick={() => setShowLoginPassword(!showLoginPassword)}></span>
                </div>
                <button className="btn1" id="loginuser" onClick={loginUser}>Login</button>
                <button className="newBtn" onClick={showRegister}>New user? Register</button>
            </div>
            )}
            {showRegisterForm && (
            <div id="register">
                <div className="auth-heading">
                    <h1>Concord</h1>
                    <h2>Create your account</h2>
                </div>
                <label>Employee ID:</label>
                <input type="text" value={employeeId} onChange={(e)=>setEmployeeId(e.target.value.toUpperCase())} autoComplete="off" spellCheck="false" style={{ textTransform: "uppercase" }} />
                <label>Full Name:</label>
                <input type="text" value={fullName} onChange={(e) => setFullName(e.target.value)} />
                <label>Email:</label>
                <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
                <label>Password:</label>
                <div className="password-box">
                <input type={showRegisterPassword ? "text" : "password"} value={password} onChange={(e) => setPassword(e.target.value)} />
                <span className="eye" onClick={() => setShowRegisterPassword(!showRegisterPassword)}></span>
                </div>
                <button className="btn1" id="registeruser" onClick={registerUser}>Register</button>
                <button className="newBtn" onClick={showLogin}>Already have an account? Login</button>
            </div>
            )}
        </div>
    </div>
    </>
    );
}

export default Auth;