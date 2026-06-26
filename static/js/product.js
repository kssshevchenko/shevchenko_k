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

    const base = parseFloat(priceBlock.dataset.basePrice);
    const surcharge = parseFloat(priceBlock.dataset.surcharge || 0);

    let finalPrice = base;

    const embroidery = document.querySelector('[name="choices_embroidery"]:checked');

    if (embroidery && (embroidery.value === "YES" || embroidery.value === "True" || embroidery.value === "1")) {
        finalPrice += surcharge;
    }

    priceBlock.innerText = `${finalPrice} грн`;
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

function renderStickers() {

    document.querySelectorAll(".sticker-option").forEach(el => {
        el.style.border = "2px solid transparent";
    });

    selectedStickers.forEach(id => {

        const el = document.querySelector(`.sticker-option[data-id="${id}"]`);

        if (el) {
            el.style.border = "2px solid black";
        }
    });

    toggleResetButton();
    updateStickersCounter();
}

function resetStickers() {

    selectedStickers = [];

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

    if (e.target.classList.contains("sticker-option")) {

        const id = e.target.dataset.id;
        const max = getMaxStickers();

        if (!max) return;

        selectedStickers.push(id);

        if (selectedStickers.length > max) {
            selectedStickers.pop();
        }

        renderStickers();
    }
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

function showError(message) {

    let errorDiv = document.getElementById("cartError");

    if (!errorDiv) {

        errorDiv = document.createElement("div");

        errorDiv.id = "cartError";
        errorDiv.style.color = "red";
        errorDiv.style.marginTop = "10px";

        document.getElementById("productForm").appendChild(errorDiv);
    }

    errorDiv.innerText = message;
}

function clearError() {

    const errorDiv = document.getElementById("cartError");

    if (errorDiv) {
        errorDiv.innerText = "";
    }
}

// =========================
// ADD TO CART
// =========================

function addToCart(url) {

    clearError();

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

        showError(error.error || "Щось пішло не так. Спробуй ще раз.");
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