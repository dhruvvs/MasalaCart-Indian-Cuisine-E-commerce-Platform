document.addEventListener('DOMContentLoaded', () => {
    const table = document.querySelector('.table');

    if (table) {
        table.addEventListener('click', (event) => {
            if (event.target.classList.contains('increment-btn')) {
                handleQuantityChange(event.target.closest('tr'), 1);
            } else if (event.target.classList.contains('decrement-btn')) {
                handleQuantityChange(event.target.closest('tr'), -1);
            }
        });
    }

    function handleQuantityChange(row, change) {
        const quantityElement = row.querySelector('.quantity-val');
        const productId = row.getAttribute('data-item-id');
        let newQuantity = parseInt(quantityElement.textContent) + change;
        if (newQuantity < 0) return;

        quantityElement.textContent = newQuantity;
        updateCartTotals();

        if (newQuantity === 0) {
            removeItemFromCart(row);
        }

        sendCartUpdate(productId, change);
    }

    function updateCartTotals() {
        let totalQuantity = 0;
        let totalPrice = 0;

        document.querySelectorAll('.table tbody tr').forEach(row => {
            const quantity = parseInt(row.querySelector('.quantity-val').textContent);
            const pricePerUnit = parseFloat(row.querySelector('.price-val-per-quantity').textContent.replace('$', ''));

            totalQuantity += quantity;
            totalPrice += quantity * pricePerUnit;
        });

        document.getElementById('total-quantity').innerHTML = `<strong>Total Quantity:</strong> ${totalQuantity}`;
        document.getElementById('total-price').innerHTML = `<strong>Total Price: $</strong>${totalPrice.toFixed(2)}`;
    }

    function removeItemFromCart(row) {
        row.remove();
        if (document.querySelectorAll('.table tbody tr').length === 0) {
            document.querySelector('.alert')?.classList.remove('d-none');
        }
    }

    function sendCartUpdate(productId, quantityChange) {
        const formData = new FormData();
        formData.append('product_id', productId);
        formData.append('quantity', quantityChange);

        fetch(updateCartURL, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.cart_empty) {
                    document.querySelector('.alert')?.classList.remove('d-none');
                }
            })
            .catch(error => console.error('Error updating cart:', error));
    }
});
