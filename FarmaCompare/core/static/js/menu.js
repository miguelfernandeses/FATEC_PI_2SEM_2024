document.addEventListener("DOMContentLoaded", function() {
    const mobileMenu = document.getElementById('mobile-menu');
    const navLinks = document.getElementById('nav-links');

    // Adiciona um evento de clique
    mobileMenu.addEventListener('click', () => {
        navLinks.classList.toggle('active'); // Alterna a classe 'active'
    });
});
