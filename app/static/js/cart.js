// app/static/js/cart.js
document.addEventListener('DOMContentLoaded', function() {
    // Update cart count from session
    function updateCartCount() {
        fetch('/orders/cart_count')
            .then(response => response.json())
            .then(data => {
                const cartCountElement = document.getElementById('cart-count');
                if (cartCountElement) {
                    cartCountElement.textContent = data.count;
                }
            });
    }
    
    // Call on page load
    updateCartCount();
    
    // Add to cart functionality
    const addToCartForms = document.querySelectorAll('form[action*="add_to_cart"]');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const productId = this.action.split('/').pop();
            
            fetch(this.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    const alertHTML = `
                        <div class="alert alert-success alert-dismissible fade show">
                            ${data.message}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    `;
                    document.querySelector('main').insertAdjacentHTML('afterbegin', alertHTML);
                    
                    // Update cart count
                    updateCartCount();
                }
            });
        });
    });
});