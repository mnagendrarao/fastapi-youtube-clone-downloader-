document.getElementById("downloadForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const link = document.getElementById("link").value;
    const quality = document.getElementById("quality").value;

    const payload = {
        link: link,
        quality: quality
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/download", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        document.getElementById("result").innerHTML = `<p>${result.message}</p>`;
    } catch (error) {
        document.getElementById("result").innerHTML = `<p>Error: ${error.message}</p>`;
    }
});
