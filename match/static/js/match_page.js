document.addEventListener("DOMContentLoaded", () => {
    const slider = document.getElementById("arenaguideSlider");
    const slides = slider ? Array.from(slider.querySelectorAll(".arenaguide-slide")) : [];
    const prevBtn = slider ? slider.querySelector(".arenaguide-slider-btn.prev") : null;
    const nextBtn = slider ? slider.querySelector(".arenaguide-slider-btn.next") : null;
    const dotsContainer = slider ? slider.querySelector(".arenaguide-slider-dots") : null;

    let currentSlide = 0;
    let sliderInterval = null;

    function showSlide(index) {
        if (!slides.length) return;

        currentSlide = (index + slides.length) % slides.length;
        slides.forEach((slide, slideIndex) => {
            slide.classList.toggle("is-active", slideIndex === currentSlide);
        });

        const dots = dotsContainer ? dotsContainer.querySelectorAll("button") : [];
        dots.forEach((dot, dotIndex) => {
            dot.classList.toggle("is-active", dotIndex === currentSlide);
        });
    }

    function stopSlider() {
        if (sliderInterval) {
            clearInterval(sliderInterval);
            sliderInterval = null;
        }
    }

    function startSlider() {
        if (slides.length <= 1) return;

        stopSlider();

        sliderInterval = setInterval(() => {
            showSlide(currentSlide + 1);
        }, 5000);
    }

    if (slider && slides.length) {
        if (dotsContainer && !dotsContainer.children.length) {
            slides.forEach((_, index) => {
                const dot = document.createElement("button");
                dot.type = "button";
                dot.setAttribute("aria-label", `Go to slide ${index + 1}`);
                dot.addEventListener("click", () => {
                    showSlide(index);
                    startSlider();
                });
                dotsContainer.appendChild(dot);
            });
        }

        showSlide(0);
        startSlider();

        if (prevBtn) {
            prevBtn.addEventListener("click", () => {
                showSlide(currentSlide - 1);
                startSlider();
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener("click", () => {
                showSlide(currentSlide + 1);
                startSlider();
            });
        }

        slider.addEventListener("mouseenter", stopSlider);
        slider.addEventListener("mouseleave", startSlider);
    }

    const filterButtons = document.querySelectorAll(".arenaguide-ticket-filter button");
    const ticketDropdown = document.querySelector(".arenaguide-ticket-dropdown");
    const ticketCards = document.querySelectorAll(".arenaguide-booking-card[data-match-card]");

    function filterTickets(filter) {
        ticketCards.forEach((card) => {
            const cardTypes = (card.dataset.matchCard || "").split(/\s+/);
            const shouldShow = filter === "all" || cardTypes.includes(filter);

            card.hidden = !shouldShow;
        });

        filterButtons.forEach((button) => {
            button.classList.toggle("is-active", button.dataset.filter === filter);
        });

        if (ticketDropdown) {
            ticketDropdown.value = filter;
        }
    }

    filterButtons.forEach((button) => {
        button.addEventListener("click", () => {
            filterTickets(button.dataset.filter || "all");
        });
    });

    if (ticketDropdown) {
        ticketDropdown.addEventListener("change", () => {
            filterTickets(ticketDropdown.value || "all");
        });
    }

    const revealItems = document.querySelectorAll(".arenaguide-reveal");

    if ("IntersectionObserver" in window) {
        const revealObserver = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("arenaguide-show");
                        revealObserver.unobserve(entry.target);
                    }
                });
            },
            {threshold: 0.1,
            }
        );

        revealItems.forEach((item) => {
            revealObserver.observe(item);
        });
    } else {
        revealItems.forEach((item) => {
            item.classList.add("arenaguide-show");
        });
    }
});  