document.addEventListener("DOMContentLoaded", function () {
    const openBtn = document.getElementById("openLogoutModal");
    const closeBtn = document.getElementById("closeLogoutModal");
    const modal = document.getElementById("logoutModal");

    if (openBtn) {
        openBtn.addEventListener("click", () => {
            modal.classList.add("show");
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            modal.classList.remove("show");
        });
    }

    if (modal) {
        modal.addEventListener("click", (e) => {
            if (e.target === modal) {
                modal.classList.remove("show");
            }
        });
    }
});