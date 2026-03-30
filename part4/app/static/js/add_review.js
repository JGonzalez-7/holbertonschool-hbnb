import { api } from "./api.js";
import { flash, getCookie } from "./auth.js";

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

function checkAuthentication() {
  const token = getCookie("token");
  if (!token) {
    window.location.href = "/index.html";
    return null;
  }

  return token;
}

function updateBackLink(placeId) {
  const backLink = document.querySelector("#back-to-place");
  if (!backLink || !placeId) {
    return;
  }

  backLink.href = `/place.html?id=${placeId}`;
}

async function submitReview(token, placeId, rating, reviewText) {
  return api.post("/api/reviews", {
    place_id: placeId,
    rating,
    comment: reviewText,
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const reviewForm = document.querySelector("#review-form");
  if (!reviewForm) {
    return;
  }

  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();

  if (!token) {
    return;
  }

  if (!placeId) {
    window.location.href = "/index.html";
    return;
  }

  updateBackLink(placeId);

  reviewForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(reviewForm);
    const reviewText = String(formData.get("comment") || "").trim();
    const rating = Number.parseInt(String(formData.get("rating") || ""), 10);

    try {
      await submitReview(token, placeId, rating, reviewText);
      reviewForm.reset();
      flash("Review submitted successfully!");
    } catch (error) {
      flash(error.message || "Failed to submit review");
    }
  });
});
