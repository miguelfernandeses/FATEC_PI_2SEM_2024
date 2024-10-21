document.addEventListener('DOMContentLoaded', function() {
    const userButton = document.getElementById('user-menu-button');
    const sidebarMenu = document.getElementById('sidebar-menu');

    userButton.addEventListener('click', function(event) {
        event.preventDefault(); // Impede o link de ser seguido
        sidebarMenu.style.display = (sidebarMenu.style.display === 'block') ? 'none' : 'block';
    });

    // Fechar o menu se o usuário clicar fora dele
    document.addEventListener('click', function(event) {
        if (!userButton.contains(event.target) && !sidebarMenu.contains(event.target)) {
            sidebarMenu.style.display = 'none';
        }
    });
});
