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

                content.innerHTML = `
                    <div class="empty-cart">
                        <p>🛍</p>
                        <p>Ваш кошик поки порожній.</p>
                    </div>
                `;

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
                    embroideryText = `
                        <p>
                            <span>Вишивка:</span>
                            Так
                        </p>
                    `;
                } else if (item.embroidery === "NO") {
                    embroideryText = `
                        <p>
                            <span>Вишивка:</span>
                            Ні
                        </p>
                    `;
                }

                let stickersText = "";

                if (item.stickers_count) {
                    stickersText = `
                        <p>
                            <span>Кількість принтів:</span>
                            ${item.stickers_count}
                        </p>
                    `;
                }

                content.innerHTML += `

                    <div class="cart-item">

                        <div class="cart-image">

                            <img src="${item.image}" alt="${item.name}">

                        </div>

                        <div class="cart-info">

                            <h2 class="cart-product-title">
                                ${item.name}
                            </h2>

                            <div class="cart-options">

                                ${item.size ? `
                                    <p>
                                        <span>Розмір:</span>
                                        ${item.size}
                                    </p>
                                ` : ""}

                                ${item.color ? `
                                    <p>
                                        <span>Колір:</span>
                                        ${item.color}
                                    </p>
                                ` : ""}

                                ${item.print_position ? `
                                    <p>
                                        <span>Розміщення принта:</span>
                                        ${printPositionText}
                                    </p>
                                ` : ""}

                                ${embroideryText}

                                ${stickersText}

                            </div>

                            <div class="cart-price">

                                ${item.subtotal} грн

                            </div>

                            <div class="cart-controls">

                                <button onclick="updateCart('/cart/decrease/${item.key}/')">
                                    −
                                </button>

                                <span class="cart-quantity">
                                    ${item.quantity}
                                </span>

                                <button onclick="updateCart('/cart/increase/${item.key}/')">
                                    +
                                </button>

                                <button
                                    class="delete-btn"
                                    onclick="updateCart('/cart/delete/${item.key}/')">

                                    🗑

                                </button>

                            </div>

                        </div>



                    </div>

                `;
            });

            total.innerText = data.total_price + " грн";

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