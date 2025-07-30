document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const errorDiv = document.getElementById("loginError") || document.getElementById("registerError");

    function handleAuthSuccess(data) {
        console.log("API response:", data);

        const userId = data.user?.id || data.user_id || data.id;
        if (!userId) {
            alert("User ID missing from server response. Cannot continue.");
            return;
        }

        localStorage.setItem("user_id", userId);
        console.log("Logged in user_id:", userId);
        window.location.href = "/dashboard";
    }

    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();

            try {
                const response = await fetch("/api/v1/users/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    handleAuthSuccess(data);
                } else {
                    errorDiv.textContent = data.error || "Login failed.";
                }
            } catch (error) {
                errorDiv.textContent = "Network error. Try again.";
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
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, email, password, phone, age })
            });

            const data = await response.json();
            console.log("API response:", data);

            const userId = data.user_id || data.user?.id;

            if (!userId) {
                console.error("User ID missing from server response. Cannot continue.");
                return;
            }

            localStorage.setItem("user_id", userId);
            window.location.href = "/dashboard";
        } catch (error) {
            errorDiv.textContent = "Network error. Try again.";
        }
    });
}


    const track = document.querySelector('.slider-track');
    const slides = document.querySelectorAll('.slide');

    if (track && slides.length > 0) {
        track.innerHTML += track.innerHTML;

        const container = document.querySelector('.slider-container');
        if (container) {
            container.addEventListener('mouseenter', () => {
                track.style.animationPlayState = 'paused';
            });
            container.addEventListener('mouseleave', () => {
                track.style.animationPlayState = 'running';
            });
        }
    }
});
