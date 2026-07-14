let selectedStickers = [];

// csrf
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
}

// =========================
// КОЛЬОРИ
// =========================

function initColorSelection() {

    const colorInputs = document.querySelectorAll(".color-input");

    colorInputs.forEach(input => {

        input.addEventListener("change", function () {

            document.querySelectorAll(".color-option").forEach(option => {
                option.classList.remove("active");
            });

            const selectedOption = this.closest(".color-option");

            if (selectedOption) {
                selectedOption.classList.add("active");
                clearFieldError("colorError");
            }
        });
    });

    const checked = document.querySelector(".color-input:checked");

    if (checked) {
        const option = checked.closest(".color-option");

        if (option) {
            option.classList.add("active");
        }
    }
}

// =========================
// ЦІНА (НОВЕ)
// =========================

function updatePrice() {

    const priceBlock = document.querySelector(".price");
    if (!priceBlock) return;

    const finalPriceElement = document.getElementById("finalPrice");
    const originalPriceElement = document.getElementById("originalPrice");

    const basePrice = parseFloat(priceBlock.dataset.basePrice);
    const originalPrice = parseFloat(priceBlock.dataset.originalPrice);
    const surcharge = parseFloat(priceBlock.dataset.surcharge || 0);

    let finalPrice = basePrice;
    let oldPrice = originalPrice;

    const embroidery = document.querySelector(
        '[name="choices_embroidery"]:checked'
    );

    if (
        embroidery &&
        (embroidery.value === "YES" ||
         embroidery.value === "True" ||
         embroidery.value === "1")
    ) {
        finalPrice += surcharge;
        oldPrice += surcharge;
    }

    if (finalPriceElement) {
        finalPriceElement.innerText = `${finalPrice.toFixed(2)} грн`;
    }

    if (originalPriceElement) {

        if (oldPrice > finalPrice) {

            originalPriceElement.style.display = "inline";
            originalPriceElement.innerText = `${oldPrice.toFixed(2)} грн`;

        } else {

            originalPriceElement.style.display = "none";

        }
    }
}

// =========================
// НАЛІПКИ
// =========================

function getMaxStickers() {
    const selected = document.querySelector('[name="choices_count_sticker"]:checked');
    return selected ? parseInt(selected.value) : 0;
}

function toggleResetButton() {
    const btn = document.querySelector(".reset-stickers-btn");
    if (!btn) return;

    btn.style.display = selectedStickers.length > 0 ? "inline-block" : "none";
}

function updateStickersCounter() {

    const counter = document.getElementById("stickersCounter");
    if (!counter) return;

    const max = getMaxStickers();

    counter.innerText = `${selectedStickers.length} з ${max}`;
}
function updateStickerCounts() {

    // очищаємо всі лічильники
    document.querySelectorAll(".sticker-count").forEach(el => {
        el.innerText = "";
    });

    // рахуємо кількість кожної наліпки
    const counts = {};

    selectedStickers.forEach(id => {
        counts[id] = (counts[id] || 0) + 1;
    });

    // записуємо кількість у картки
    Object.keys(counts).forEach(id => {

        const sticker = document.querySelector(
            `.sticker-option[data-id="${id}"]`
        );

        if (!sticker) return;

        const counter = sticker.querySelector(".sticker-count");

        if (counter) {
            counter.innerText = counts[id];
        }
    });
}
function renderStickers() {
    if(selectedStickers.length>0){
        clearFieldError("stickersError");
    }
    document.querySelectorAll(".sticker-option").forEach(el => {
        el.style.border = "2px solid transparent";
    });

    selectedStickers.forEach(id => {

        const el = document.querySelector(`.sticker-option[data-id="${id}"]`);

        if (el) {
            el.style.border = "2px solid black";
        }
    });
    updateStickerCounts();
    toggleResetButton();
    updateStickersCounter();
}

function resetStickers() {

    selectedStickers = [];
    updateStickerCounts();

    document.querySelectorAll(".sticker-option").forEach(el => {
        el.style.border = "2px solid transparent";
    });

    toggleResetButton();
    updateStickersCounter();
}

// =========================
// ВИБІР НАЛІПОК
// =========================

document.addEventListener("click", function (e) {

    const sticker = e.target.closest(".sticker-option");

    if (!sticker) return;

    const id = sticker.dataset.id;
    const max = getMaxStickers();

    if (!max) return;

    selectedStickers.push(id);

    if (selectedStickers.length > max) {
        selectedStickers.shift();
    }

    renderStickers();
});
// =========================
// ЗМІНА КІЛЬКОСТІ НАЛІПОК
// =========================

document.addEventListener("change", function (e) {

    if (e.target.name === "choices_count_sticker") {
        resetStickers();
        renderStickers();
    }

    if (e.target.name === "choices_embroidery") {
        updatePrice();
    }
});

// =========================
// ПОМИЛКИ
// =========================

function showFieldError(id, message){

    const error=document.getElementById(id);

    if(!error) return;

    error.innerHTML="⚠ " + message;
    error.classList.add("show");
}

function clearFieldError(id){

    const error=document.getElementById(id);

    if(!error) return;

    error.innerHTML="";
    error.classList.remove("show");
}

// =========================
// ADD TO CART
// =========================

function addToCart(url) {

    clearFieldError("colorError");
    clearFieldError("stickersError");

    const form = document.getElementById("productForm");
    const formData = new FormData(form);

    selectedStickers.forEach(id => {
        formData.append("sticker_id", id);
    });

    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCSRFToken(),
        },
        body: formData
    })
    .then(async response => {

        const data = await response.json();

        if (!response.ok) throw data;

        return data;
    })
    .then(() => {

        resetStickers();
        renderStickers();
        updatePrice();

        if (typeof window.openCart === "function") {
            window.openCart();
        }
    })
    .catch(error => {

        console.error("AddToCart error:", error);

        if (error.error?.toLowerCase().includes("колір")) {

            showFieldError("colorError", error.error);

        }
        else if (
            error.error?.toLowerCase().includes("наліп")
        ) {

            showFieldError("stickersError", error.error);

        }
        else {

            alert(error.error || "Щось пішло не так.");

        }

    });
}

// =========================
// INIT
// =========================

document.addEventListener("DOMContentLoaded", function () {

    initColorSelection();
    updateStickersCounter();
    toggleResetButton();
    updatePrice();
});