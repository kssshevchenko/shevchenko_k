function addToCart(url) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error("Помилка додавання товару");
            }
            return response.json().catch(() => ({}));
        })
        .then(() => {
            // даємо невеликий “буфер”, щоб cart.js точно вже був у window
            setTimeout(() => {
                if (window.openCart) {
                    window.openCart();
                }
            }, 50);
        })
        .catch(error => console.error("AddToCart error:", error));
}
window.addToCart = addToCart;