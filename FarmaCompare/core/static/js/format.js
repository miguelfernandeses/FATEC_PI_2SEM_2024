document.addEventListener('DOMContentLoaded', () => {
    const cnpjInput = document.querySelector('input[name="cnpj"]');
    const telefoneInput = document.querySelector('input[name="telefone"]');

    if (cnpjInput) {
        cnpjInput.addEventListener('input', () => {
            let cnpj = cnpjInput.value.replace(/\D/g, ''); 
            if (cnpj.length > 14) cnpj = cnpj.slice(0, 14);  // Limita a 14 caracteres
            cnpjInput.value = cnpj.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, "$1.$2.$3/$4-$5");  // Formata CNPJ
        });
    }

    if (telefoneInput) {
        telefoneInput.addEventListener('input', () => {
            let telefone = telefoneInput.value.replace(/\D/g, '');  // Remove caracteres não numéricos
            if (telefone.length > 11) telefone = telefone.slice(0, 11);  // Limita a 11 caracteres
            telefoneInput.value = telefone.replace(/^(\d{2})(\d{5})(\d{4})$/, "($1) $2-$3");  // Formata telefone
        });
    }
});

