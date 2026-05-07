document.addEventListener("DOMContentLoaded", () => {
    const seats = document.querySelectorAll(".seat:not(.booked)");
    const seatInput = document.getElementById("seatInput");
    const selectedSeatBox = document.getElementById("selectedSeat");
    const nextBtn = document.getElementById("nextBtn");
    const addParking = document.getElementById("addParking");
    const parkingCards = document.getElementById("parkingCards");
    const parkingInput = document.getElementById("parkingInput");
    const parkingCardItems = document.querySelectorAll(".parking-card");

    let selectedSeats = [];

    function updateParkingInfo() {
        const parkingInfo = document.getElementById("parkingInfo");
        const selectedParking = document.querySelector(".parking-card.selected");
        if (parkingInfo && selectedParking) {
            const parkingName = selectedParking.dataset.parkingName || "Parking";
            parkingInfo.innerHTML = `Parking: ${parkingName}`;
        }
    }

    function updateSummary() {
        if (!selectedSeats.length) {
            seatInput.value = "";
            selectedSeatBox.innerHTML = `<p>No seat selected</p>`;

            if (nextBtn) {
                nextBtn.disabled = true;
                nextBtn.classList.remove("ready");
            }

            return;
        }

        seatInput.value = selectedSeats.map((item) => item.id).join(",");

        const totalPrice = selectedSeats.reduce((sum, item) => {
            return sum + Number(item.price);
        }, 0);

        selectedSeatBox.innerHTML = `
            <div class="selected-seat-card">
                <span>Selected Seats</span>
                <h5>${selectedSeats.length} seat(s) selected</h5>

                <div class="selected-seats-list">
                    ${selectedSeats.map((item) => `
                        <div class="selected-seat-row">
                        <br>
                            <p>Section ${item.section} • Row ${item.row} • Seat ${item.number}</p>
                            <small>Gate: ${item.gate} • View: ${item.viewQuality}</small>
                            <b>${Number(item.price).toFixed(2)} SAR</b>
                        </div>
                    `).join("")}
                </div>

                <div class="seat-price-row">
                    <small>Total Ticket Price</small>
                    <strong>${totalPrice.toFixed(2)} SAR</strong>
                </div>

                <div id="parkingInfo" class="parking-info"></div>
            </div>
        `;

        updateParkingInfo();

        if (nextBtn) {
            nextBtn.disabled = false;
            nextBtn.classList.add("ready");
        }
    }

    seats.forEach((seat) => {
        seat.addEventListener("click", () => {
            const seatId = seat.dataset.seatId;
            const existingSeat = selectedSeats.find((item) => item.id === seatId);

            if (existingSeat) {
                selectedSeats = selectedSeats.filter((item) => item.id !== seatId);
                seat.classList.remove("selected");
            } else {
                selectedSeats.push({
                    id: seatId,
                    price: seat.dataset.price || "0",
                    section: seat.dataset.section || "-",
                    row: seat.dataset.row || "-",
                    number: seat.dataset.number || "-",
                    gate: seat.dataset.gate || "Not assigned",
                    viewQuality: seat.dataset.viewQuality || "Good",
                    shaded: seat.dataset.shaded === "True" ? "Yes" : "No",
                    sunExposure: seat.dataset.sunExposure || "Medium",
                    notes: seat.dataset.notes || "No extra notes",
                });

                seat.classList.add("selected");
            }

            updateSummary();
        });
    });

    if (addParking && parkingCards && parkingInput) {
        addParking.addEventListener("change", () => {
            parkingCards.classList.toggle("is-active", addParking.checked);

            if (!addParking.checked) {
                parkingInput.value = "";
                parkingCardItems.forEach((card) => card.classList.remove("selected"));

                const parkingInfo = document.getElementById("parkingInfo");
                if (parkingInfo) parkingInfo.innerHTML = "";
            }
        });

        parkingCardItems.forEach((card) => {
            card.addEventListener("click", () => {
                if (!addParking.checked) {
                    addParking.checked = true;
                    parkingCards.classList.add("is-active");
                }

                parkingCardItems.forEach((item) => item.classList.remove("selected"));
                card.classList.add("selected");

                parkingInput.value = card.dataset.parkingId || "";
                updateParkingInfo();
            });
        });
    }

    const form = document.querySelector(".booking-summary form");

    if (form) {
        form.addEventListener("submit", (event) => {
            if (!seatInput.value) {
                event.preventDefault();
                alert("Please select at least one seat.");
                return;
            }

            if (addParking && addParking.checked && !parkingInput.value) {
                event.preventDefault();
                alert("Please select a parking area or uncheck Add Parking.");
            }
        });
    }
});