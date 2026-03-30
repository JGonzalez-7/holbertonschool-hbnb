import { api } from "./api.js";

let allPlaces = [];

function renderPlaces(places) {
  const list = document.querySelector("#places-list");
  if (!list) {
    return;
  }

  if (!places.length) {
    list.innerHTML = '<p class="muted">No places match the selected price filter.</p>';
    return;
  }

  list.innerHTML = "";

  places.forEach((place) => {
    const card = document.createElement("article");
    card.className = "place-card";
    card.dataset.price = String(place.price);

    const ratingLabel =
      place.average_rating === null || place.average_rating === undefined
        ? "No ratings yet"
        : `${place.average_rating.toFixed(1)} / 5`;

    card.innerHTML = `
      <header>
        <div>
          <h3>${place.name}</h3>
          <p class="muted">${place.description || "No description provided."}</p>
        </div>
        <span class="price-badge">$${place.price.toFixed(2)} per night</span>
      </header>
      <div class="detail-meta">
        <span class="rating-badge">${ratingLabel}</span>
        <span class="muted">${place.reviews.length} review(s)</span>
      </div>
      <p class="muted">Lat ${place.latitude}, Lng ${place.longitude}</p>
      <p><a class="details-button" href="/place.html?id=${place.id}">View Details</a></p>
    `;

    list.appendChild(card);
  });
}

function applyFilters() {
  const selectedValue = document.querySelector("#price-filter")?.value || "all";
  const cards = document.querySelectorAll("#places-list .place-card");

  cards.forEach((card) => {
    const price = Number.parseFloat(card.dataset.price || "0");
    const matches = selectedValue === "all" || price <= Number.parseFloat(selectedValue);
    card.style.display = matches ? "" : "none";
  });
}

async function loadPageData() {
  const places = await api.get("/api/places");
  allPlaces = places;
  renderPlaces(allPlaces);
  applyFilters();
}

document.addEventListener("DOMContentLoaded", () => {
  const page = document.querySelector("#places-page");
  if (!page) {
    return;
  }

  document.querySelector("#price-filter")?.addEventListener("change", applyFilters);

  loadPageData().catch((error) => {
    const list = document.querySelector("#places-list");
    if (list) {
      list.innerHTML = `<p class="muted">${error.message}</p>`;
    }
  });
});
