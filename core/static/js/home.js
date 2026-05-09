document.addEventListener("DOMContentLoaded", () => {

    const revealItems = document.querySelectorAll(".ag-reveal");
    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("ag-show");
                    revealObserver.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.14 }
    );

    revealItems.forEach((item) => revealObserver.observe(item));

    const countdown = document.getElementById("worldCupCountdown");

    function updateCountdown() {
        if (!countdown) return;

        const target = new Date("2034-06-01T00:00:00").getTime();
        const now = Date.now();
        const diff = Math.max(0, target - now);
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));

        countdown.textContent = days.toLocaleString();
    }

    updateCountdown();
    setInterval(updateCountdown, 1000 * 60 * 60);

    const soldElement = document.getElementById("ticketsSold");
    const leftElement = document.getElementById("ticketsLeft");

    let ticketsSold = 128400;
    let ticketsLeft = 21600;

    function updateTickets() {
        const soldIncrease = Math.floor(Math.random() * 7) + 1;
        const leftDecrease = Math.floor(Math.random() * 4) + 1;

        ticketsSold += soldIncrease;
        ticketsLeft = Math.max(0, ticketsLeft - leftDecrease);

        if (soldElement) soldElement.textContent = ticketsSold.toLocaleString();
        if (leftElement) leftElement.textContent = ticketsLeft.toLocaleString();
    }

    setInterval(updateTickets, 2800);

    const slides = document.querySelectorAll(".hero-slide");
    const dots = document.querySelectorAll(".hero-dot");
    const nextBtn = document.querySelector(".hero-next");
    const prevBtn = document.querySelector(".hero-prev");

    let currentSlide = 0;
    let sliderTimer;

    function showSlide(index) {
        if (!slides.length) return;

        currentSlide = (index + slides.length) % slides.length;

        slides.forEach((slide, i) => {
            slide.classList.toggle("active", i === currentSlide);
        });

        dots.forEach((dot, i) => {
            dot.classList.toggle("active", i === currentSlide);
        });
    }

    function nextSlide() {
        showSlide(currentSlide + 1);
    }

    function prevSlide() {
        showSlide(currentSlide - 1);
    }

    function startSlider() {
        sliderTimer = setInterval(nextSlide, 5000);
    }

    function resetSlider() {
        clearInterval(sliderTimer);
        startSlider();
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", () => {
            nextSlide();
            resetSlider();
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener("click", () => {
            prevSlide();
            resetSlider();
        });
    }

    dots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
            showSlide(index);
            resetSlider();
        });
    });

    showSlide(0);
    startSlider();
});