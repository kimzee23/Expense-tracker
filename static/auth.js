document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const errorDiv = document.getElementById("loginError") || document.getElementById("registerError");

    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();

            try {
                const response = await fetch("/api/v1/users/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    localStorage.setItem("user", JSON.stringify(data));
                    window.location.href = "/dashboard";
                } else {
                    errorDiv.textContent = data.error || "Login failed.";
                    errorDiv.style.color = "red";
                }
            } catch (error) {
                errorDiv.textContent = "Network error. Try again.";
                errorDiv.style.color = "red";
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const name = document.getElementById("name").value.trim();
            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();
            const phone = document.getElementById("phone").value.trim();
            const age = parseInt(document.getElementById("age").value.trim());

            try {
                const response = await fetch("/api/v1/users/register", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ name, email, password, phone, age })
                });

                const data = await response.json();

                if (response.ok) {
                    localStorage.setItem("user", JSON.stringify(data));
                    window.location.href = "/dashboard";

                } else {
                    errorDiv.textContent = data.error || "Registration failed.";
                    errorDiv.style.color = "red";
                }
            } catch (error) {
                errorDiv.textContent = "Network error. Try again.";
                errorDiv.style.color = "red";
            }
        });
    }
});
