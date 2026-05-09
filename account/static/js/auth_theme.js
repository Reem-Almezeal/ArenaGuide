document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("arenaTheme");

    if (savedTheme === "dark") {
        document.body.classList.add("is-dark");
    } else {
        document.body.classList.remove("is-dark");
    }
});