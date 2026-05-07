const verifyForm = document.getElementById("verifyForm");
const identityInput = document.getElementById("identity_number");

if (verifyForm && identityInput) {

    verifyForm.addEventListener("submit", function (event) {
        const value = identityInput.value.trim();

        if (!value || value.length !== 10) {
            event.preventDefault();

            identityInput.classList.add("input-error");
            identityInput.focus();
        }
    });

    identityInput.addEventListener("input", function () {

        this.value = this.value.replace(/\D/g, "").slice(0, 10);

        if (this.value.length === 10) {
            this.classList.remove("input-error");
        }
    });

    identityInput.addEventListener("blur", function () {

        if (this.value.length > 0 && this.value.length < 10) {
            this.classList.add("input-error");
        } else {
            this.classList.remove("input-error");
        }
    });
}