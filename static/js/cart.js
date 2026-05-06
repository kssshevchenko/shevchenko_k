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

                let printPositionText = "";
                if (item.print_position === "FRONT") {
                    printPositionText = "Спереду";
                } else if (item.print_position === "BACK") {
                    printPositionText = "Ззаду";
                }

                let embroideryText = "";
                if (item.embroidery === "YES") {
                    embroideryText = "Вишивка: так<br>";
                } else if (item.embroidery === "NO") {
                    embroideryText = "Вишивка: ні<br>";
                }

                let stickersText = "";
                if (item.stickers_count) {
                    stickersText = `Кількість принтів: ${item.stickers_count}<br>`;
                }

                content.innerHTML += `
                    <div class="cart-item">
                        <strong>${item.name}</strong><br>

                        ${item.size ? `Розмір: ${item.size}<br>` : ""}
                        ${item.color ? `Колір: ${item.color}<br>` : ""}
                        ${item.print_position ? `Розміщення принта: ${printPositionText}<br>` : ""}
                        ${item.embroidery ? embroideryText : ""}
                        ${stickersText}

                        Кількість: ${item.quantity}<br>
                        Сума: ${item.subtotal}

                        <div class="qty-controls">
                            <button onclick="updateCart('/cart/increase/${item.key}/')">+</button>
                            <button onclick="updateCart('/cart/decrease/${item.key}/')">-</button>
                            <button onclick="updateCart('/cart/delete/${item.key}/')">✕</button>
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