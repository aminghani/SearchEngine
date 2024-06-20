document.addEventListener("DOMContentLoaded", () => {
    const searchForm = document.getElementById("searchForm");
    const searchInput = document.getElementById("searchInput");
    const priceRangeMin = document.getElementById("priceRangeMin");
    const priceRangeMax = document.getElementById("priceRangeMax");
    const priceMinValue = document.getElementById("priceMinValue");
    const priceMaxValue = document.getElementById("priceMaxValue");
    const imageResults = document.getElementById("imageResults");
    const loading = document.getElementById("loading");

    priceRangeMin.addEventListener("input", () => {
        if (parseInt(priceRangeMin.value) > parseInt(priceRangeMax.value)) {
            priceRangeMax.value = priceRangeMin.value;
        }
        priceMinValue.textContent = priceRangeMin.value;
    });

    priceRangeMax.addEventListener("input", () => {
        if (parseInt(priceRangeMax.value) < parseInt(priceRangeMin.value)) {
            priceRangeMin.value = priceRangeMax.value;
        }
        priceMaxValue.textContent = priceRangeMax.value;
    });

    searchForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const query = searchInput.value.trim();
        const minPrice = priceRangeMin.value;
        const maxPrice = priceRangeMax.value;
        if (query) {
            showLoading();
            try {
                const response = await fetch(`/search_images?query=${encodeURIComponent(query)}&min_price=${encodeURIComponent(minPrice)}&max_price=${encodeURIComponent(maxPrice)}`);
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

            const priceElement = document.createElement("p");
            priceElement.textContent = `Price: $${image.price}`;

            const captionElement = document.createElement("p");
            captionElement.textContent = image.caption;

            imgContainer.appendChild(imgElement);
            imgContainer.appendChild(nameElement);
            imgContainer.appendChild(priceElement);
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