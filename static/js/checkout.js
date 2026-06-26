const checkoutForm = document.getElementById("checkoutForm");

if (checkoutForm) {

    checkoutForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const formData = new FormData(checkoutForm);

        const errorBlock = document.getElementById("formError");

        errorBlock.innerText = "";

        try {

            const response = await fetch(checkoutForm.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            const data = await response.json();

            if (!response.ok) {

                errorBlock.innerText = data.error;

                return;
            }

            if (data.success_url) {
                window.location.href = data.success_url;
            }

        } catch(error) {

            errorBlock.innerText = "Помилка сервера";

            console.error(error);
        }

    });

}
