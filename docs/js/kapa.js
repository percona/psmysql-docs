(function () {
    function createAIButton() {
        if (document.getElementById("ask-percona-ai")) {
            return;
        }

        // The Algolia search container in the header (partials/header.html)
        const container = document.querySelector("#docsearch");

        if (!container) {
            return;
        }

        const button = document.createElement("button");

        button.id = "ask-percona-ai";
        button.type = "button";

        button.innerHTML = `
            <span class="percona-star">✨</span>
            <span class="percona-text">Ask Percona AI</span>
        `;

        button.addEventListener("click", function (event) {
            event.preventDefault();
            if (window.Kapa && typeof window.Kapa.open === "function") {
                window.Kapa.open();
            }
        });

        container.appendChild(button);
    }

    createAIButton();
})();

