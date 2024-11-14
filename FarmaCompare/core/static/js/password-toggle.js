document.getElementById("eye-icon").addEventListener("click", function() {
    var passwordField = document.getElementById("password");

    if (passwordField.type === "password") {
        passwordField.type = "text"; // Torna a senha visível
        this.classList.replace("fa-eye", "fa-eye-slash"); // Troca o ícone para "fa-eye-slash"
    } else {
        passwordField.type = "password"; // Torna a senha invisível novamente
        this.classList.replace("fa-eye-slash", "fa-eye"); // Troca o ícone de volta para "fa-eye"
    }
});
