//Calendario
document.addEventListener("DOMContentLoaded", () => {
    // Inicializando o Flatpickr para os campos de datas
    flatpickr("#checkin", {
        dateFormat: "d M Y", // Formato de exibição da data
        minDate: "today", // Data mínima disponível para seleção
        onChange: function(selectedDates, dateStr, instance) {
            // Garantir que a data de check-out seja sempre após o check-in
            const checkoutInput = document.getElementById("checkout");
            const checkoutDate = new Date(selectedDates[0].getTime() + 86400000); // Adiciona 1 dia à data de check-in
            flatpickr(checkoutInput, {
                dateFormat: "d M Y",
                minDate: checkoutDate, // Define o mínimo para o campo de checkout
            });
        }
    });

    flatpickr("#checkout", {
        dateFormat: "d M Y",
        minDate: "today", // A data mínima de checkout é a de hoje, por padrão
    });

    // Estrutura de dados simulada das casas
    const houses = [
        { name: "Casa de Praia", maxGuests: 4, availableDates: { checkin: "2025-01-20", checkout: "2025-01-25" } },
        { name: "Apartamento Moderno", maxGuests: 2, availableDates: { checkin: "2025-01-10", checkout: "2025-01-15" } },
        { name: "Chalé na Montanha", maxGuests: 6, availableDates: { checkin: "2025-02-01", checkout: "2025-02-10" } },
        { name: "Sítio Verde", maxGuests: 5, availableDates: { checkin: "2025-01-15", checkout: "2025-01-20" } },
    ];

    // Evento para o envio do formulário de busca
    document.getElementById("searchForm").addEventListener("submit", (e) => {
        e.preventDefault(); // Evitar o reload da página

        // Obter os valores dos campos
        const checkin = document.getElementById("checkin").value;
        const checkout = document.getElementById("checkout").value;
        const guests = parseInt(document.getElementById("guests").value);

        // Validar se os campos estão preenchidos corretamente
        if (!checkin || !checkout || isNaN(guests) || guests <= 0) {
            alert("Por favor, preencha todos os campos corretamente.");
            return;
        }

        // Converter as datas para o formato Date para comparação
        const checkinDate = new Date(checkin);
        const checkoutDate = new Date(checkout);

        // Filtrar as casas que atendem aos critérios
        const filteredHouses = houses.filter(house => {
            const houseCheckinDate = new Date(house.availableDates.checkin);
            const houseCheckoutDate = new Date(house.availableDates.checkout);

            // Verificar a quantidade de hóspedes
            const guestsMatch = guests <= house.maxGuests;

            // Verificar se as datas de reserva da casa não colidem com as datas selecionadas
            const datesMatch = checkinDate >= houseCheckinDate && checkoutDate <= houseCheckoutDate;

            return guestsMatch && datesMatch;
        });

        // Exibir os resultados filtrados
        const resultsContainer = document.getElementById("searchResults");
        if (filteredHouses.length > 0) {
            resultsContainer.innerHTML = `<ul>${filteredHouses.map(house => `<li>${house.name} - Max Hóspedes: ${house.maxGuests} | Disponível: ${house.availableDates.checkin} a ${house.availableDates.checkout}</li>`).join("")}</ul>`;
        } else {
            resultsContainer.textContent = "Nenhuma casa encontrada com os critérios informados.";
        }
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

const myCarouselElement = document.querySelector('#myCarousel')

const carousel = new bootstrap.Carousel(myCarouselElement, {
  interval: 1000,
  touch: false
})
