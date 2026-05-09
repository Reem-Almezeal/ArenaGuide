document.addEventListener("DOMContentLoaded", () => {

    const revealItems = document.querySelectorAll(".ag-reveal");

    const observer = new IntersectionObserver((entries) => {

        entries.forEach((entry) => {

            if (entry.isIntersecting) {
                entry.target.classList.add("ag-show");
            }

        });

    }, {
        threshold: 0.15
    });

    revealItems.forEach((item) => observer.observe(item));

});