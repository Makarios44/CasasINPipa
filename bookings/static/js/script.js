//Calendario
document.addEventListener("DOMContentLoaded", function() {
    // Inicializa o Flatpickr nos campos de data
    flatpickr("#checkin", {
        minDate: "today", // Impede a seleção de datas passadas
        dateFormat: "Y-m-d", // Formato da data
    });
    flatpickr("#checkout", {
        minDate: "today", // Impede a seleção de datas passadas
        dateFormat: "Y-m-d", // Formato da data
    });

    // Evento de busca
    document.querySelector(".search-btn").addEventListener("click", function() {
        const checkin = document.getElementById("checkin").value;
        const checkout = document.getElementById("checkout").value;
        const guests = document.getElementById("guests").value;

        if (!checkin || !checkout || !guests) {
            alert("Por favor, preencha todas as informações!");
            return;
        }

        // Chama a função para verificar a disponibilidade das casas
        searchAvailableHouses(checkin, checkout, guests);
    });
});

// Função para buscar casas disponíveis
function searchAvailableHouses(checkin, checkout, guests) {
    // Simulação de casas disponíveis (substitua com lógica real)
    const houses = [
        { id: 1, name: "Casa 1", availableFrom: "2025-01-10", availableTo: "2025-01-15", maxGuests: 4 },
        { id: 2, name: "Casa 2", availableFrom: "2025-01-20", availableTo: "2025-01-25", maxGuests: 6 }
    ];

    const availableHouses = houses.filter(house => {
        return (checkin >= house.availableFrom && checkout <= house.availableTo) && (guests <= house.maxGuests);
    });

    if (availableHouses.length > 0) {
        displayAvailableHouses(availableHouses);
    } else {
        document.getElementById("results").innerHTML = "Desculpe, não há casas disponíveis para essas datas.";
    }
}

// Função para exibir as casas disponíveis
function displayAvailableHouses(houses) {
    let output = '<h2>Casas Disponíveis:</h2><ul>';
    houses.forEach(house => {
        output += `<li>${house.name} (Máximo de ${house.maxGuests} hóspedes)</li>`;
    });
    output += '</ul>';
    document.getElementById("results").innerHTML = output;
}

//Sidebar

const myCarouselElement = document.querySelector('#myCarousel')

const carousel = new bootstrap.Carousel(myCarouselElement, {
  interval: 1000,
  touch: false
})

