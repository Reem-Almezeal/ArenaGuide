document.addEventListener("DOMContentLoaded", () => {
    const forms = document.querySelectorAll(".gate-form");

    forms.forEach((form) => {
        const statusSelect = form.querySelector(".gate-status-select");
        const messageInput = form.querySelector("textarea[name='message']");

        function updateMessagePlaceholder() {
            const status = statusSelect.value;

            if (status === "closed") {
                messageInput.placeholder = "This gate is closed. Please proceed to the alternative gate.";
            } else if (status === "crowded") {
                messageInput.placeholder = "This gate is crowded. Please use the suggested alternative gate.";
            } else if (status === "emergency") {
                messageInput.placeholder = "Emergency reported at this gate. Please follow organizer instructions.";
            } else if (status === "maintenance") {
                messageInput.placeholder = "This gate is under maintenance. Please use another gate.";
            } else {
                messageInput.placeholder = "Gate is open and operating normally.";
            }
        }

        statusSelect.addEventListener("change", updateMessagePlaceholder);
        updateMessagePlaceholder();
    });
});