function openCart() {
    const drawer = document.getElementById("cartDrawer");
    const overlay = document.getElementById("overlay");

    if (!drawer || !overlay) return;

    drawer.classList.add("active");
    overlay.classList.add("active");

    loadCart();
}

function closeCart() {
    const drawer = document.getElementById("cartDrawer");
    const overlay = document.getElementById("overlay");

    if (!drawer || !overlay) return;

    drawer.classList.remove("active");
    overlay.classList.remove("active");
}

function loadCart() {
    fetch("/cart/cart_data/")
        .then(response => response.json())
        .then(data => {
            const content = document.getElementById("cartContent");
            const total = document.getElementById("totalPrice");

            if (!content || !total) return;

            content.innerHTML = "";

            if (data.cart_items.length === 0) {
                content.innerHTML = "<p>Кошик порожній</p>";
                total.innerText = "";
                return;
            }

            data.cart_items.forEach(item => {
                content.innerHTML += `
                    <div class="cart-item">
                        <strong>${item.name}</strong><br>
                        Кількість: ${item.quantity}<br>
                        Сума: ${item.subtotal}

                        <div class="qty-controls">
                            <button onclick="updateCart('/cart/increase/${item.id}/')">+</button>
                            <button onclick="updateCart('/cart/decrease/${item.id}/')">-</button>
                            <button onclick="updateCart('/cart/delete/${item.id}/')">✕</button>
                        </div>
                    </div>
                `;
            });

            total.innerText = "Загальна сума: " + data.total_price;
        })
        .catch(error => console.error("Error:", error));
}

function updateCart(url) {
    fetch(url).then(() => loadCart());
}

window.openCart = openCart;
window.closeCart = closeCart;
window.loadCart = loadCart;
window.updateCart = updateCart;