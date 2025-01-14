// Abertura do modal
var modal = document.getElementById("myModal");
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
    modal.style.display = "block"; // Exibe o modal
}

// Fechar o modal ao clicar no "X"
span.onclick = function() {
    modal.style.display = "none"; // Fecha o modal
}

// Fechar o modal se clicar fora dele
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
