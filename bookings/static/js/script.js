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
const filterBtn = document.getElementById('filter-btn');
        const sidebar = document.getElementById('sidebar');
        
        filterBtn.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });