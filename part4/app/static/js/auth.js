import { api } from "./api.js";
import { getCookie } from "./utils.js";

let sessionState = null;

function setTokenCookie(token) {
  document.cookie = `token=${encodeURIComponent(token)}; path=/; SameSite=Lax`;
}

function clearTokenCookie() {
  document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Lax";
}

function flash(message) {
  const element = document.querySelector("#flash-message");
  if (!element) {
    return;
  }

  element.textContent = message;
  element.hidden = false;

  window.clearTimeout(flash.timeoutId);
  flash.timeoutId = window.setTimeout(() => {
    element.hidden = true;
  }, 3200);
}

function updateNavigation(session) {
  const adminLink = document.querySelector("#admin-link");
  const loginLink = document.querySelector("#login-link");
  const logoutButton = document.querySelector("#logout-button");
  const authStatus = document.querySelector("#auth-status");

  if (!loginLink || !logoutButton || !authStatus || !adminLink) {
    return;
  }

  if (session && session.logged_in) {
    adminLink.hidden = !session.is_admin;
    loginLink.hidden = true;
    logoutButton.hidden = false;
    authStatus.textContent = session.is_admin
      ? `Signed in as administrator (${session.user_id})`
      : `Signed in (${session.user_id})`;
    return;
  }

  adminLink.hidden = true;
  loginLink.hidden = false;
  logoutButton.hidden = true;
  authStatus.textContent = "Browsing as guest";
}

function updateNavigationFromCookie() {
  const token = getCookie("token");
  updateNavigation(
    token
      ? { logged_in: true, user_id: "Authenticated user", is_admin: false }
      : { logged_in: false, user_id: null, is_admin: false },
  );
}

export async function getSession(forceRefresh = false) {
  if (sessionState && !forceRefresh) {
    return sessionState;
  }

  sessionState = await api.get("/api/session");
  updateNavigation(sessionState);
  return sessionState;
}

async function handleLogout() {
  await api.post("/api/session/logout", {});
  clearTokenCookie();
  sessionState = { logged_in: false, user_id: null, is_admin: false };
  updateNavigation(sessionState);
  flash("Logged out");

  if (window.location.pathname === "/login") {
    return;
  }
}

async function handleLoginSubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const formData = new FormData(form);

  const payload = {
    email: String(formData.get("email") || "").trim(),
    password: String(formData.get("password") || ""),
  };

  try {
    const response = await api.post("/api/session/login", payload);
    setTokenCookie(response.access_token);
    sessionState = {
      logged_in: true,
      user_id: response.user_id,
      is_admin: response.is_admin,
    };
    updateNavigation(sessionState);
    window.location.href = "/index.html";
  } catch (error) {
    clearTokenCookie();
    flash(error.message);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const logoutButton = document.querySelector("#logout-button");
  const loginForm = document.querySelector("#login-form");
  const pageName = document.body.dataset.page;

  if (logoutButton) {
    logoutButton.addEventListener("click", () => {
      handleLogout().catch((error) => flash(error.message));
    });
  }

  if (loginForm) {
    loginForm.addEventListener("submit", handleLoginSubmit);
  }

  updateNavigationFromCookie();

  try {
    const session = await getSession(true);
    if (pageName === "login" && session.logged_in) {
      window.location.href = "/";
    }
  } catch (error) {
    clearTokenCookie();
    updateNavigation(null);
    flash(error.message);
  }
});

export { flash, getCookie };
