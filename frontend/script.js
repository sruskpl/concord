function showLogin() {
    document.getElementById("register").style.display = "none";
    document.getElementById("login").style.display = "flex";
}

function showRegister() {
    document.getElementById("login").style.display = "none";
    document.getElementById("register").style.display = "flex";
}

function togglePassword(id){

    const passwordInput =
        document.getElementById(id);

    if(passwordInput.type === "password"){
        passwordInput.type = "text";
    }
    else{
        passwordInput.type = "password";
    }
}

const API_BASE_URL = "http://127.0.0.1:5000";

async function registerUser() {

    const employeeId = document.getElementById("registerEmployeeId").value;
    const username = document.getElementById("registerUsername").value;
    const email = document.getElementById("registerEmail").value;
    const password = document.getElementById("registerPassword").value;

    const response = await fetch(`${API_BASE_URL}/register`, {

        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            employee_id: employeeId,
            username: username,
            email: email,
            password: password
        })
    });

    const data = await response.json();

    if (response.ok) {
        alert("Registration Successful!");
        showLogin();
    }
    else {
        alert(data.detail);
    }
}

async function loginUser() {

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    const response = await fetch(`${API_BASE_URL}/login`, {

        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("role", data.role);
        window.location.href = "dashboard.html";
    }
    else {
        alert(data.detail);
    }
}

function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("role");
    window.location.href = "auth.html";
}

function saveToken(token) {
    localStorage.setItem("access_token", token);
}

function getToken() {
    return localStorage.getItem("access_token");
}

function removeToken() {
    localStorage.removeItem("access_token");
}