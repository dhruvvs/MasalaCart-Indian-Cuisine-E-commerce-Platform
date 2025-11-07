let cartCount = 0;
let originalCards = [];

function changeQuantity(productId, change) {
    const quantityElement = document.getElementById(`quantity-${productId}`);
    const hiddenQuantityElement = document.getElementById(`hidden-quantity-${productId}`);
    if (!quantityElement || !hiddenQuantityElement) return;

    let quantity = parseInt(quantityElement.innerText);
    quantity = isNaN(quantity) ? 0 : Math.max(0, quantity + change);

    quantityElement.innerText = quantity;
    hiddenQuantityElement.value = quantity;

    updateCartCount();
}

function changeQuantityFromButton(button, change) {
    const productId = button.getAttribute('data-product-id');
    changeQuantity(productId, change);
}

function updateCartCount() {
    cartCount = Array.from(document.querySelectorAll("[id^=quantity-]"))
        .map(el => parseInt(el.innerText) || 0)
        .reduce((sum, qty) => sum + qty, 0);

    document.getElementById("cartButton").innerText = `Cart (${cartCount})`;
}

function searchProducts() {
    const searchTerm = document.getElementById("searchBar").value.toLowerCase();
    const productCards = document.querySelectorAll(".product");

    productCards.forEach(card => {
        const productName = card.querySelector("h5").innerText.toLowerCase();
        card.style.display = productName.includes(searchTerm) ? "block" : "none";
    });
}

function filterProducts() {
    const categoryFilter = document.getElementById("categoryFilter").value;
    const sortFilter = document.getElementById("sortFilter").value;
    const container = document.querySelector("#productListing");

    // Cache all cards only once
    if (originalCards.length === 0) {
        originalCards = Array.from(container.children).map(card => card.cloneNode(true));
    }

    let filtered = originalCards.map(card => card.cloneNode(true));

    filtered = filtered.filter(card => {
        const category = card.querySelector(".product").getAttribute("data-category");
        return categoryFilter === "all" || category === categoryFilter;
    });

    if (sortFilter === "priceLowHigh") {
        filtered.sort((a, b) => {
            const priceA = parseFloat(a.querySelector(".price").innerText.replace("$", ""));
            const priceB = parseFloat(b.querySelector(".price").innerText.replace("$", ""));
            return priceA - priceB;
        });
    } else if (sortFilter === "priceHighLow") {
        filtered.sort((a, b) => {
            const priceA = parseFloat(a.querySelector(".price").innerText.replace("$", ""));
            const priceB = parseFloat(b.querySelector(".price").innerText.replace("$", ""));
            return priceB - priceA;
        });
    }

    container.innerHTML = "";
    filtered.forEach(card => container.appendChild(card));

    // Reattach quantity button events after DOM update
    filtered.forEach(card => {
        const productId = card.querySelector(".product").getAttribute("data-product-id");

        const plusBtn = card.querySelector(".btn-success[data-product-id]");
        const minusBtn = card.querySelector(".btn-danger[data-product-id]");

        if (plusBtn) {
            plusBtn.onclick = () => changeQuantity(productId, 1);
        }
        if (minusBtn) {
            minusBtn.onclick = () => changeQuantity(productId, -1);
        }
    });
}
