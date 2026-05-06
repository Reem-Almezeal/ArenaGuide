document.addEventListener("DOMContentLoaded", () => {
    const revealItems = document.querySelectorAll(".about-reveal");

    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("about-show");
                    revealObserver.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.16 }
    );

    revealItems.forEach((item) => revealObserver.observe(item));

    const counters = document.querySelectorAll("[data-about-count]");

    const counterObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;

                const counter = entry.target;
                const target = Number(counter.dataset.aboutCount);
                let current = 0;
                const duration = 1400;
                const start = performance.now();

                function animateCounter(time) {
                    const progress = Math.min((time - start) / duration, 1);
                    current = Math.floor(target * progress);
                    counter.textContent = current.toLocaleString();

                    if (progress < 1) {
                        requestAnimationFrame(animateCounter);
                    } else {
                        counter.textContent = target.toLocaleString();
                    }
                }

                requestAnimationFrame(animateCounter);
                counterObserver.unobserve(counter);
            });
        },
        { threshold: 0.5 }
    );

    counters.forEach((counter) => counterObserver.observe(counter));
});