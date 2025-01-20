
    document.getElementById('registrationForm').addEventListener('submit', function(event) {
        // Verificar se o checkbox dos termos está marcado
        var termsChecked = document.getElementById('terms').checked;

        if (!termsChecked) {
            // Prevenir o envio do formulário se os termos não foram aceitos
            event.preventDefault();
            alert('Você precisa aceitar os Termos de Uso para continuar.');
        }
    });

    // Função para abrir o modal
    function openModal() {
        var modal = document.getElementById('termsModal');
        modal.style.display = 'block';
    }

    // Função para fechar o modal
    function closeModal() {
        var modal = document.getElementById('termsModal');
        modal.style.display = 'none';
    }

