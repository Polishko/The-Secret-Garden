/* Main purpose: asynchronously fetching related products on product detail pages and saving scroller position
* when navigating to related product detail page */
document.addEventListener('DOMContentLoaded', async () => {
    const relatedDiv = document.getElementById('related-products');
    const productType = relatedDiv.dataset.type;

    const savedScrollPosition = localStorage.getItem('scrollPosition');
    if (savedScrollPosition) {
        window.scrollTo(0, parseInt(savedScrollPosition, 10));
        localStorage.removeItem('scrollPosition');
    }

    try {
        const response = await fetch(`/api/related-products/${productType}/`);
        if (response.ok) {
            const data = await response.json();

            const sliderContainer = document.createElement('div');
            sliderContainer.className = 'slider-container overflow-hidden';

            const slider = document.createElement('ul');
            slider.className = 'slider';

            data.products.forEach(product => {
                const listItem = document.createElement('li');
                listItem.className = 'slider-item';

                const detailUrl = productType === 'plant'
                    ? `/flowers/${product.slug}/detail/`
                    : `/gifts/${product.slug}/detail/`;

                listItem.innerHTML = `
                    <a href="${detailUrl}" class="text-decoration-none text-dark related-product-link">
                        <div class="d-flex justify-content-center align-items-center">
                            <span class="me-3">${product.name}</span>
                            <img src="${product.image}" alt="${product.name}" 
                                 class="img-thumbnail me-3" 
                                 style="width: 50px; height: 50px; object-fit: cover;">
                            <span class="badge bg-success">${parseFloat(product.price).toFixed(2)} EUR</span>
                        </div>
                    </a>
                `;
                slider.appendChild(listItem);
            });

            sliderContainer.appendChild(slider);
            relatedDiv.appendChild(sliderContainer);

            const links = document.querySelectorAll('.related-product-link');
            links.forEach(link => {
                link.addEventListener('click', () => {
                    localStorage.setItem('scrollPosition', window.scrollY);
                });
            });
        }
    } catch (error) {
        console.error('Error fetching related products:', error);
    }
});
