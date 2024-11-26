document.addEventListener('DOMContentLoaded', () => {
    let currentPage = 1; // Página inicial
    const query = "{{ query }}"; // A query do usuário
    const productsList = document.getElementById('products-list');
    const loadMoreButton = document.getElementById('load-more');

    function loadProducts() {
        fetch(`/busca/?q=${encodeURIComponent(query)}&page=${currentPage}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest' // Identifica a requisição como AJAX
            }
        })
        .then(response => response.json())
        .then(data => {
            data.produtos.forEach(produto => {
                const productItem = document.createElement('div');
                productItem.className = 'product-item';
                productItem.innerHTML = `
                    <img src="${product.images}" alt="${product.name}">
                    <h2>${product.name}</h2>
                    <p>Preço: R$ ${produto.price}</p>
                    <a href="/produto/${encodeURIComponent(product.name)}/">Ver Produto</a>
                `;
                productsList.appendChild(productItem);
            });

            if (data.has_more) {
                loadMoreButton.style.display = 'block'; // Exibe o botão "Ver mais"
            } else {
                loadMoreButton.style.display = 'none'; // Oculta o botão "Ver mais"
            }
        })
        .catch(error => console.error('Erro ao carregar os produtos:', error));
    }

    loadMoreButton.addEventListener('click', () => {
        currentPage++;
        loadProducts();
    });

    // Carrega a primeira página automaticamente
    loadProducts();
});
