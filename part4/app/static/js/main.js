import { api } from "./api.js";

let allPlaces = [];

function formatRating(value) {
  if (Number.isInteger(value)) {
    return String(value);
  }

  return value.toFixed(1);
}

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
        : `${formatRating(place.average_rating)} / 5`;
    const demoLabel = place.is_demo
      ? '<span class="muted demo-label">Demo listing</span>'
      : "";
    const imageMarkup = place.image_url
      ? `
        <div class="property-media">
          <img src="${place.image_url}" alt="${place.name}">
        </div>
      `
      : "";

    card.innerHTML = `
      ${imageMarkup}
      <header>
        <div>
          <h3>${place.name}</h3>
          <p class="muted">${place.description || "No description provided."}</p>
        </div>
        <span class="price-text">$${place.price.toFixed(2)} per night</span>
      </header>
      <div class="detail-meta">
        <span class="rating-badge">${ratingLabel}</span>
        <span class="muted">${place.reviews.length} review(s)</span>
      </div>
      <p class="muted">Lat ${place.latitude}, Lng ${place.longitude}</p>
      ${demoLabel}
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
  allPlaces = [...places].sort((left, right) => {
    const priceDelta = Number(left.price || 0) - Number(right.price || 0);
    if (priceDelta !== 0) {
      return priceDelta;
    }

    return String(left.name || "").localeCompare(String(right.name || ""));
  });
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
