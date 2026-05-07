document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("dashboardThemeToggle");
    const body = document.body;

    if (localStorage.getItem("dashboardTheme") === "dark") {
        body.classList.add("dashboard-dark");
    }

    if (toggle) {
        toggle.addEventListener("click", function () {
            body.classList.toggle("dashboard-dark");

            if (body.classList.contains("dashboard-dark")) {
                localStorage.setItem("dashboardTheme", "dark");
            } else {
                localStorage.setItem("dashboardTheme", "light");
            }
        });
    }
const menuBtn = document.getElementById("mobileMenuBtn");
const sidebar = document.querySelector(".dashboard-sidebar");

if (menuBtn && sidebar) {
    menuBtn.addEventListener("click", () => {
        sidebar.classList.toggle("show-sidebar");
    });
}
});