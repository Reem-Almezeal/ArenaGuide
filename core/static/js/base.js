document.addEventListener("DOMContentLoaded", () => {
    const body = document.body;
    const header = document.getElementById("arenaHeader");
    const searchBtn = document.getElementById("arenaSearchBtn");
    const searchInline = document.getElementById("arenaSearchInline");
    const searchInput = searchInline ? searchInline.querySelector("input") : null;
    const accountBtn = document.getElementById("arenaAccountBtn");
    const accountMenu = document.getElementById("arenaAccountMenu");
    const menuBtn = document.getElementById("arenaMenuBtn");
    const mainMenu = document.getElementById("arenaMainMenu");
    const themeBtn = document.getElementById("arenaThemeBtn");
    const savedTheme = localStorage.getItem("arenaTheme");
    
    if (savedTheme === "dark") {
        body.classList.add("is-dark");
    }

    function updateHeader() {
        if (!header) return;
        header.classList.toggle("is-scrolled", window.scrollY > 20);
    }

    function closeMenus(except = null) {
        if (except !== "search") searchInline?.classList.remove("is-open");
        if (except !== "account") accountMenu?.classList.remove("is-open");
        if (except !== "menu") mainMenu?.classList.remove("is-open");
    }

    updateHeader();
    window.addEventListener("scroll", updateHeader);

    searchBtn?.addEventListener("click", (event) => {
        event.stopPropagation();

        const isOpen = searchInline.classList.contains("is-open");
        closeMenus("search");
        searchInline.classList.toggle("is-open", !isOpen);

        if (!isOpen) {
            setTimeout(() => searchInput?.focus(), 80);
        }
    });

    accountBtn?.addEventListener("click", (event) => {
        event.stopPropagation();

        const isOpen = accountMenu.classList.contains("is-open");
        closeMenus("account");
        accountMenu.classList.toggle("is-open", !isOpen);
    });

    menuBtn?.addEventListener("click", (event) => {
        event.stopPropagation();

        const isOpen = mainMenu.classList.contains("is-open");
        closeMenus("menu");
        mainMenu.classList.toggle("is-open", !isOpen);
    });

    themeBtn?.addEventListener("click", () => {
        body.classList.toggle("is-dark");

        const isDark = body.classList.contains("is-dark");
        localStorage.setItem("arenaTheme", isDark ? "dark" : "light");

        const icon = themeBtn.querySelector("i");
        if (icon) {
            icon.className = isDark ? "bi bi-sun-fill" : "bi bi-moon-stars-fill";
        }
    });

    const icon = themeBtn?.querySelector("i");
    if (icon && body.classList.contains("is-dark")) {
        icon.className = "bi bi-sun-fill";
    }

    document.addEventListener("click", (event) => {
        if (
            !event.target.closest("#arenaSearchInline") &&
            !event.target.closest("#arenaAccountMenu") &&
            !event.target.closest("#arenaMainMenu") &&
            !event.target.closest("#arenaAccountBtn") &&
            !event.target.closest("#arenaMenuBtn")
        ) {
            closeMenus();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeMenus();
        }
    });
});