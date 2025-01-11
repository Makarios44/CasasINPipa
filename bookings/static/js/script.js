//Calendario
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
//Calendario

//Sidebar
const sidebar = document.querySelector('.sidebar');
const filterBtn = document.getElementById('filter-btn');


filterBtn.addEventListener('click', () => {
    sidebar.classList.add('active');
});


document.addEventListener('click', (event) => {

    if (!sidebar.contains(event.target) && event.target !== filterBtn) {
        sidebar.classList.remove('active');
    }
});
//Sidebar