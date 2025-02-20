document.addEventListener('DOMContentLoaded', function () {
    // Rolar até a seção de Informações Pessoais
    document.getElementById('btn-info').addEventListener('click', function (e) {
        e.preventDefault(); // Evita o comportamento padrão do link
        document.getElementById('informacoes-pessoais').scrollIntoView({ behavior: 'smooth' });
    });

    // Rolar até a seção de Minhas Casas
    document.getElementById('btn-casas').addEventListener('click', function (e) {
        e.preventDefault(); // Evita o comportamento padrão do link
        document.getElementById('minhas-casas').scrollIntoView({ behavior: 'smooth' });
    });
});