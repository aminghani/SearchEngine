document.addEventListener("DOMContentLoaded", () => {
    const searchForm = document.getElementById("searchForm");
    const searchInput = document.getElementById("searchInput");
    const imageResults = document.getElementById("imageResults");
    const loading = document.getElementById("loading");

    searchForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const query = searchInput.value.trim();
        if (query) {
            showLoading();
            try {
                const response = await fetch(`/search_images?query=${encodeURIComponent(query)}`);
                const data = await response.json();
                displayImages(data.images);
            } catch (error) {
                console.error("Error fetching images:", error);
            } finally {
                hideLoading();
            }
        }
    });

    function displayImages(images) {
        imageResults.innerHTML = "";
        images.forEach((image) => {
            const imgContainer = document.createElement("div");
            imgContainer.className = "image-container";

            const imgElement = document.createElement("img");
            imgElement.src = image.image_url;
            imgElement.alt = "Search result";

            const nameElement = document.createElement("h3");
            nameElement.textContent = image.name;

            const captionElement = document.createElement("p");
            captionElement.textContent = image.caption;

            imgContainer.appendChild(imgElement);
            imgContainer.appendChild(nameElement);
            imgContainer.appendChild(captionElement);

            imageResults.appendChild(imgContainer);
        });
    }

    function showLoading() {
        loading.style.display = "block";
        imageResults.innerHTML = "";
    }

    function hideLoading() {
        loading.style.display = "none";
    }
});