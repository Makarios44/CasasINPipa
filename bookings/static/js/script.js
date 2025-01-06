document.addEventListener("DOMContentLoaded", () => {
    flatpickr("#checkin", {
        dateFormat: "d M",
        minDate: "today",
    });
    flatpickr("#checkout", {
        dateFormat: "d M",
        minDate: "today",
    });
});
