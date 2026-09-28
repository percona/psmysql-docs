// "Ask Percona AI" button for Percona Server docs.
// The Kapa widget itself (with all its data-* config) is loaded from
// main.html as a markup <script data-osano="ESSENTIAL">, so Osano doesn't
// block it. This file only creates the button and opens the widget via
// Kapa's JS API, so it works no matter which one loads first.
(function () {
    function createAIButton() {
        if (document.getElementById("ask-percona-ai")) {
            return;
        }

        const search = document.querySelector(".md-search");

        if (!search || !search.parentNode) {
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
            } else {
                console.warn("Kapa widget not loaded yet (blocked or still loading).");
            }
        });

        // Place button AFTER search component
        search.parentNode.insertBefore(button, search.nextSibling);
    }

    createAIButton();
})();