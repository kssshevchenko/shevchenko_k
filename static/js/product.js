let selectedStickers = [];

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
}

// отримати максимальну кількість наліпок
function getMaxStickers() {
    const selected = document.querySelector('[name="choices_count_sticker"]:checked');
    return selected ? parseInt(selected.value) : 0;
}

// 🔥 кнопка reset
function toggleResetButton() {
    const btn = document.querySelector(".reset-stickers-btn");
    if (!btn) return;

    btn.style.display = selectedStickers.length > 0 ? "inline-block" : "none";
}

// 🔥 лічильник наліпок
function updateStickersCounter() {
    const counter = document.getElementById("stickersCounter");
    if (!counter) return;

    const max = getMaxStickers();
    const current = selectedStickers.length;

    counter.innerText = `${current} з ${max}`;
}

// перемалювати вибір
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
}

// reset
function resetStickers() {
    selectedStickers = [];

    document.querySelectorAll(".sticker-option").forEach(el => {
        el.style.border = "2px solid transparent";
    });

    toggleResetButton();
    updateStickersCounter();
}

// вибір наліпок
document.addEventListener("click", function (e) {
    if (e.target.classList.contains("sticker-option")) {

        const id = e.target.dataset.id;
        const max = getMaxStickers();

        if (!max) return;

        selectedStickers.push(id);

        if (selectedStickers.length > max) {
            selectedStickers = selectedStickers.slice(-max);
        }

        renderStickers();
        updateStickersCounter();
    }
});

// зміна кількості наліпок
document.addEventListener("change", function (e) {
    if (e.target.name === "choices_count_sticker") {
        resetStickers();
        renderStickers();
        updateStickersCounter();
    }
});

// показ помилки
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
    if (errorDiv) errorDiv.innerText = "";
}

// додати в кошик
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
        updateStickersCounter();

        if (typeof window.openCart === "function") {
            window.openCart();
        }
    })
    .catch(error => {
        console.error("AddToCart error:", error);
        showError(error.error || "Щось пішло не так. Спробуй ще раз.");
    });
}

// ініціалізація
document.addEventListener("DOMContentLoaded", function () {
    toggleResetButton();
    updateStickersCounter();
});