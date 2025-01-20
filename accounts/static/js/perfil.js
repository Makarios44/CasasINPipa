// Selecionando os botões do menu
const btnInfo = document.getElementById("btn-info");
const btnReservas = document.getElementById("btn-reservas");
const btnCasas = document.getElementById("btn-casas");

// Selecionando as seções
const infoSection = document.getElementById("info-section");
const reservasSection = document.getElementById("reservas-section");
const casasSection = document.getElementById("casas-section");

// Função para alternar visibilidade das seções
function showSection(sectionToShow) {
    // Ocultar todas as seções
    infoSection.classList.add("hidden");
    reservasSection.classList.add("hidden");
    casasSection.classList.add("hidden");

    // Mostrar a seção específica
    sectionToShow.classList.remove("hidden");
}

// Adicionando eventos de clique nos botões
btnInfo.addEventListener("click", () => showSection(infoSection));
btnReservas.addEventListener("click", () => showSection(reservasSection));
btnCasas.addEventListener("click", () => showSection(casasSection));

// Função para alternar a visibilidade do formulário de edição
function toggleEditForm() {
    const form = document.getElementById("edit-form");
    const isFormVisible = form.style.display === "block";
    form.style.display = isFormVisible ? "none" : "block";  // Alterna a visibilidade do formulário
}

// Função para cancelar a edição (simplesmente oculta o campo de edição)

function cancelEditForm() {
    const form = document.getElementById("edit-form");
    form.style.display = "none";  // Esconde o formulário de edição
}


