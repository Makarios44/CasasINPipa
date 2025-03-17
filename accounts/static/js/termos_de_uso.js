// Código para privacy_policy.js e terms_of_use.js

document.addEventListener('DOMContentLoaded', function() {
    // Adicionar botão "Voltar ao topo"
    const body = document.querySelector('body');
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '↑';
    backToTopButton.setAttribute('title', 'Voltar ao topo');
    backToTopButton.style.position = 'fixed';
    backToTopButton.style.bottom = '20px';
    backToTopButton.style.right = '20px';
    backToTopButton.style.height = '40px';
    backToTopButton.style.width = '40px';
    backToTopButton.style.fontSize = '20px';
    backToTopButton.style.background = '#1e88e5';
    backToTopButton.style.color = 'white';
    backToTopButton.style.border = 'none';
    backToTopButton.style.borderRadius = '50%';
    backToTopButton.style.cursor = 'pointer';
    backToTopButton.style.display = 'none';
    backToTopButton.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
    
    body.appendChild(backToTopButton);
    
    // Mostrar/ocultar botão baseado na posição de rolagem
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });
    
    // Funcionalidade de voltar ao topo
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Adicionar links de navegação interna para seções principais
    const sections = document.querySelectorAll('.modal-content p strong');
    const navigationDiv = document.createElement('div');
    navigationDiv.className = 'navigation-links';
    navigationDiv.style.margin = '20px 0';
    navigationDiv.style.padding = '15px';
    navigationDiv.style.backgroundColor = '#f0f8ff';
    navigationDiv.style.borderRadius = '5px';
    
    const navTitle = document.createElement('p');
    navTitle.innerHTML = '<strong>Índice:</strong>';
    navigationDiv.appendChild(navTitle);
    
    const navList = document.createElement('ul');
    navList.style.listStyleType = 'none';
    navList.style.paddingLeft = '10px';
    
    // Criar ID único para cada seção
    sections.forEach((section, index) => {
        // Verificar se o texto do strong é um título de seção (contém um número)
        const text = section.textContent;
        if (/\d+\./.test(text)) {
            const sectionId = 'section-' + index;
            section.parentElement.id = sectionId;
            
            const listItem = document.createElement('li');
            listItem.style.margin = '5px 0';
            
            const link = document.createElement('a');
            link.href = '#' + sectionId;
            link.textContent = text;
            link.style.textDecoration = 'none';
            link.style.color = '#0d47a1';
            
            listItem.appendChild(link);
            navList.appendChild(listItem);
        }
    });
    
    navigationDiv.appendChild(navList);
    
    // Inserir a navegação logo após o título principal
    const title = document.querySelector('h2');
    title.parentNode.insertBefore(navigationDiv, title.nextSibling.nextSibling);
});