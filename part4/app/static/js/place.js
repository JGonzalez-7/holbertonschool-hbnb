import { api } from "./api.js";
import { flash, getCookie } from "./auth.js";

let currentPlace = null;
let currentToken = null;

function formatRating(value) {
  if (Number.isInteger(value)) {
    return String(value);
  }

  return value.toFixed(1);
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

function renderPlace(place) {
  const container = document.querySelector("#place-details");
  if (!container) {
    return;
  }

  const amenities = (place.amenities || [])
    .map((amenity) => `<span class="pill">${amenity.name}</span>`)
    .join("");
  const ratingLabel =
    place.average_rating === null || place.average_rating === undefined
      ? "No ratings yet"
      : `${formatRating(place.average_rating)} / 5`;

  container.innerHTML = `
    <p class="eyebrow">Place</p>
    <h1>${place.name}</h1>
    ${
      place.image_url
        ? `
          <div class="property-hero">
            <img src="${place.image_url}" alt="${place.name}">
          </div>
        `
        : ""
    }
    <div class="place-info">
      <p class="intro">${place.description || "No description provided."}</p>
      <div class="detail-meta">
        <span class="price-badge">$${place.price.toFixed(2)} / night</span>
        <span class="rating-badge">${ratingLabel}</span>
      </div>
      <p><strong>Host:</strong> ${place.owner?.first_name || ""} ${place.owner?.last_name || ""}</p>
      <p><strong>Email:</strong> ${place.owner?.email || "Unknown"}</p>
      <p><strong>Coordinates:</strong> ${place.latitude}, ${place.longitude}</p>
      <h2>Amenities</h2>
      <div class="amenity-pills">${amenities || '<span class="muted">No amenities</span>'}</div>
    </div>
  `;
}

function renderReviews(reviews, usersById = {}) {
  const list = document.querySelector("#reviews");
  if (!list) {
    return;
  }

  if (!reviews.length) {
    list.innerHTML = '<p class="muted">No reviews yet.</p>';
    return;
  }

  list.innerHTML = reviews
    .map(
      (review) => `
        <article class="review-card">
          <header>
            <strong>${usersById[review.user_id] || `User ${review.user_id}`}</strong>
            <span class="rating-badge">${review.rating} / 5</span>
          </header>
          <p>${review.comment}</p>
        </article>
      `,
    )
    .join("");
}

function updateReviewAccess(place) {
  const addReviewSection = document.querySelector("#add-review");
  const note = document.querySelector("#review-form-note");
  if (!addReviewSection || !note) {
    return;
  }

  if (!currentToken) {
    addReviewSection.hidden = true;
    note.textContent = "Sign in to leave a review.";
    return;
  }

  if (place.owner_id === place.current_user_id) {
    addReviewSection.hidden = true;
    note.textContent = "Owners cannot review their own places.";
    return;
  }

  addReviewSection.hidden = false;
  note.textContent = "Submit your review below.";
}

async function resolveReviewUsers(reviews) {
  const uniqueUserIds = [...new Set(reviews.map((review) => review.user_id))];
  const usersById = {};

  await Promise.all(
    uniqueUserIds.map(async (userId) => {
      try {
        const user = await api.get(`/api/users/${userId}`);
        usersById[userId] = `${user.first_name} ${user.last_name}`.trim();
      } catch (_error) {
        usersById[userId] = `User ${userId}`;
      }
    }),
  );

  return usersById;
}

async function fetchPlaceDetails() {
  const placeId = getPlaceIdFromURL();
  if (!placeId) {
    throw new Error("Missing place id in URL");
  }

  currentToken = getCookie("token");
  const place = await api.get(`/api/places/${placeId}`);
  const reviews = place.reviews || [];
  const usersById = await resolveReviewUsers(reviews);

  if (currentToken) {
    try {
      const session = await api.get("/api/session");
      place.current_user_id = session.user_id;
    } catch (_error) {
      place.current_user_id = null;
    }
  } else {
    place.current_user_id = null;
  }

  currentPlace = place;
  renderPlace(place);
  renderReviews(reviews, usersById);
  updateReviewAccess(place);
}

async function handleReviewSubmit(event) {
  event.preventDefault();
  if (!currentPlace) {
    flash("Place details are not loaded yet");
    return;
  }

  const form = event.currentTarget;
  const formData = new FormData(form);

  try {
    await api.post("/api/reviews", {
      place_id: currentPlace.id,
      rating: Number.parseInt(String(formData.get("rating")), 10),
      comment: String(formData.get("comment") || "").trim(),
    });
    form.reset();
    await fetchPlaceDetails();
    flash("Review submitted");
  } catch (error) {
    flash(error.message);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const page = document.querySelector("#place-page");
  if (!page) {
    return;
  }

  document.querySelector("#review-form")?.addEventListener("submit", handleReviewSubmit);

  fetchPlaceDetails().catch((error) => {
    const container = document.querySelector("#place-details");
    if (container) {
      container.innerHTML = `<p class="muted">${error.message}</p>`;
    }
  });
});
