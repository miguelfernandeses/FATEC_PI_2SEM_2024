document.addEventListener("DOMContentLoaded", () => {
    const loadMoreBtn = document.getElementById("load-more");
    const productsContainer = document.getElementById("products-container");

    if (loadMoreBtn) {
        loadMoreBtn.addEventListener("click", () => {
            const nextPage = loadMoreBtn.getAttribute("data-page");
            const query = new URLSearchParams(window.location.search).get("q");

            fetch(`/busca/?q=${encodeURIComponent(query)}&page=${nextPage}`, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    data.produtos.forEach((produto) => {
                        const productItem = document.createElement("div");
                        productItem.classList.add("product-item");

                        productItem.innerHTML = `
                            <img src="${produto.images}" alt="${produto.name}">
                            <h2>${produto.name}</h2>
                            <p>Preço: R$ ${produto.price}</p>
                            <a href="/produto/${produto.id}/" class="view-product-link">Ver Produto</a>
                        `;

                        productsContainer.appendChild(productItem);
                    });

                    if (data.has_next) {
                        loadMoreBtn.setAttribute("data-page", parseInt(nextPage) + 1);
                    } else {
                        loadMoreBtn.style.display = "none";
                    }
                })
                .catch((error) => console.error("Erro ao carregar mais produtos:", error));
        });
    }
});
