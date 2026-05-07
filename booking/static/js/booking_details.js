document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".visitor-form");
    const submitBtn = document.getElementById("detailsSubmitBtn");

    if (!form) return;

    form.addEventListener("submit", (event) => {
        const email = document.getElementById("email").value.trim();
        const phone = document.getElementById("phone").value.trim();
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const phonePattern = /^05\d{8}$/;
        const idPattern = /^\d{4}$/;

        if (!emailPattern.test(email)) {
            event.preventDefault();
            alert("Please enter a valid email address.");
            return;
        }

        if (!phonePattern.test(phone)) {
            event.preventDefault();
            alert("Please enter a valid Saudi phone number starting with 05.");
            return;
        }

        const holderCards = document.querySelectorAll(".ticket-holder-card");

        for (let index = 0; index < holderCards.length; index++) {
            const card = holderCards[index];
            const ticketNumber = index + 1;
            const fullNameInput = card.querySelector(`input[name="full_name_${ticketNumber}"]`);
            const idLast4Input = card.querySelector(`input[name="id_last4_${ticketNumber}"]`);
            const dobInput = card.querySelector(`input[name="date_of_birth_${ticketNumber}"]`);
            const idDocumentInput = card.querySelector(`input[name="id_document_${ticketNumber}"]`);
            const fullName = fullNameInput.value.trim();
            const idLast4 = idLast4Input.value.trim();
            const dateOfBirth = dobInput.value;

            if (fullName.length < 5 || fullName.split(" ").length < 2) {
                event.preventDefault();
                alert(`Please enter the full name for Ticket ${ticketNumber}.`);
                fullNameInput.focus();
                return;
            }

            if (!dateOfBirth) {
                event.preventDefault();
                alert(`Please enter the date of birth for Ticket ${ticketNumber}.`);
                dobInput.focus();
                return;
            }

            if (!idPattern.test(idLast4)) {
                event.preventDefault();
                alert(`Please enter exactly 4 ID/passport digits for Ticket ${ticketNumber}.`);
                idLast4Input.focus();
                return;
            }

            if (idDocumentInput && idDocumentInput.files.length) {
                const file = idDocumentInput.files[0];
                const allowedTypes = ["image/jpeg", "image/png", "image/jpg"];
                const maxSize = 5 * 1024 * 1024;

                if (!allowedTypes.includes(file.type)) {
                    event.preventDefault();
                    alert(`ID document for Ticket ${ticketNumber} must be JPG or PNG.`);
                    return;
                }

                if (file.size > maxSize) {
                    event.preventDefault();
                    alert(`ID document for Ticket ${ticketNumber} must be less than 5MB.`);
                    return;
                }
            }
        }

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = "Verifying...";
        }
    });
        setTimeout(() => {
        const toasts = document.querySelectorAll('.toast-message');
        toasts.forEach(toast => {
            toast.classList.add('toast-hide');
        })},3000);
});