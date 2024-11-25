document.addEventListener('DOMContentLoaded', function () {
    const loadMoreButton = document.getElementById('load-more-button');
    const productsList = document.getElementById('products-list');
    const query = "{{ query }}";

    loadMoreButton.addEventListener('click', function () {
        const offset = parseInt(loadMoreButton.getAttribute('data-offset'));

        fetch(`/search-results/?query=${encodeURIComponent(query)}&offset=${offset}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            data.produtos.forEach(produto => {
                const productItem = document.createElement('div');
                productItem.classList.add('product-item');
                productItem.innerHTML = `
                    <img src="${produto.images}">
                    <h2>${produto.name}</h2>
                    <p>Preço: R$ ${produto.price}</p>
                    <a href="/produto/${encodeURIComponent(produto.name)}/" class="view-product-button">Ver Produto</a>
                `;
                productsList.appendChild(productItem);
            });

            // Atualiza o offset
            loadMoreButton.setAttribute('data-offset', offset + 50);

            // Remove o botão se não houver mais produtos
            if (data.produtos.length < 50) {
                loadMoreButton.style.display = 'none';
            }
        })
        .catch(error => console.error('Erro ao carregar mais produtos:', error));
    });
});
