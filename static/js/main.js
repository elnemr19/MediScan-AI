function appendMessage(message, role) {
    const container = document.getElementById("chat-container");
    const div = document.createElement("div");
    div.className = role + "-message";
    div.textContent = message;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById("user-message");
    const text = input.value;
    if (text) {
        appendMessage(text, "user");
        input.value = "";

        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: text })
        })
        .then(res => res.json())
        .then(data => {
            appendMessage(data.response, "assistant");
        })
        .catch(err => {
            console.error("Error:", err);
            appendMessage("Error occurred. Try again.", "assistant");
        });
    }
}
