document.addEventListener("DOMContentLoaded", () => {
    const messageType = document.getElementById("messageType");
    const otherTypeField = document.getElementById("otherTypeField");
    const otherTypeInput = document.getElementById("otherTypeInput");

    function toggleOtherType() {
        if (!messageType || !otherTypeField) return;
        const isOther = messageType.value === "other";
        otherTypeField.classList.toggle("is-visible", isOther);
        if (otherTypeInput) {
            otherTypeInput.required = isOther;

            if (!isOther) {
                otherTypeInput.value = "";
            }
        }
    }

    toggleOtherType();
    if (messageType) {
        messageType.addEventListener("change", toggleOtherType);
    }
});