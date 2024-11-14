let debounceTimer;

function searchProducts(event) {
    event.preventDefault(); 

    const query = document.getElementById('search-input').value.trim().toLowerCase(); 
    const resultsContainer = document.getElementById('search-results-container');

    if (query.length === 0) {
        resultsContainer.style.display = 'none';
        resultsContainer.innerHTML = ''; 
        document.getElementById('clear-search').style.display = 'none'; 
        return;
    }

    resultsContainer.style.display = 'block';
    resultsContainer.innerHTML = '<p>Carregando...</p>';

    clearTimeout(debounceTimer);

    debounceTimer = setTimeout(() => {
        fetch(`/search/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = ''; 

                if (data.products.length === 0) {
                    resultsContainer.innerHTML = '<p>Nenhum produto encontrado.</p>';
                } else {
                    data.products.forEach(product => {
                        const resultItem = document.createElement('div');
                        resultItem.classList.add('search-result');
                        resultItem.innerHTML = `
                            <div class="product-info">
                                <img src="${product.image}"> 
                                <p><strong>${product.name}</strong></p>
                            </div>
                        `;
                        resultsContainer.appendChild(resultItem);
                    });
                }
            })
            .catch(error => {
                console.error('Erro ao buscar produtos:', error);
                resultsContainer.innerHTML = '<p>Erro ao buscar produtos, tente novamente.</p>';
            });
    }, 550);

    if (query.length > 0) {
        document.getElementById('clear-search').style.display = 'block';
    }
}

function clearSearch() {
    const searchInput = document.getElementById('search-input');
    searchInput.value = ''; 
    document.getElementById('clear-search').style.display = 'none';
    searchInput.focus(); 
    document.getElementById('search-results-container').style.display = 'none'; 
}
