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
        images.forEach((imageURL) => {
            const imgElement = document.createElement("img");
            imgElement.src = imageURL;
            imgElement.alt = "Search result";
            imageResults.appendChild(imgElement);
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