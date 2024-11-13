document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("#login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            const username = document.querySelector("#uname").value.trim();
            const password = document.querySelector("#pass").value.trim();

            if (!username || !password) {
                alert("Both fields are required!");
                event.preventDefault();  // Prevent form from submitting if fields are empty
            }
        });
    }
});
