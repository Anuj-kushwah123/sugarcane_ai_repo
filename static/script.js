document.querySelectorAll(".menu a").forEach(link => {
    link.addEventListener("click", function (e) {
        e.preventDefault();
        let target = this.getAttribute("href");
        let section = document.querySelector(target);

        if (section) {
            section.scrollIntoView({ behavior: "smooth" });
        }
    });
});

//Image Preview
let imageInput = document.getElementById("leaf_image");
let previewImage = document.getElementById("preview");

if (imageInput && previewImage) {
    imageInput.addEventListener("change", function () {
        let file = this.files[0];

        if (file) {
            previewImage.src = URL.createObjectURL(file); 
            previewImage.style.display = "block";
        }
    });
}

// Fetch API (async/await)
async function detectDisease(event) {
    event.preventDefault();

    let file = document.getElementById("leaf_image").files[0];
    if (!file) return alert("Please upload image");

    // Loading state
    document.getElementById("disease").innerText = "Detecting...";
    document.getElementById("confidence").innerText = "...";
    document.getElementById("solution").innerText = "...";

    let formData = new FormData();
    formData.append("leaf_image", file);

    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try{
        let response = await fetch("/predict/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        if (!response.ok) throw new Error("Server error");
        let data = await response.json();
        // result show
        document.getElementById("disease").innerText = data.disease;
        document.getElementById("confidence").innerText = data.confidence + "%";
        document.getElementById("solution").innerText = data.solution;
        // scroll to result
        document.getElementById("result-section").scrollIntoView({
            behavior: "smooth"
        });
    } catch (err) {
        console.error(err); // debug ke liye
        alert("Server error. Please try again.");
    }
}
document.querySelector("form").addEventListener("submit", detectDisease);
