import { api } from "./api.js";
import { flash, getSession } from "./auth.js";

function updateCreatedUser(user) {
  const state = document.querySelector("#created-user-state");
  const details = document.querySelector("#created-user-details");
  const name = document.querySelector("#created-user-name");
  const email = document.querySelector("#created-user-email");
  const id = document.querySelector("#created-user-id");
  const role = document.querySelector("#created-user-role");

  if (!state || !details || !name || !email || !id || !role) {
    return;
  }

  state.hidden = true;
  details.hidden = false;
  name.textContent = `${user.first_name} ${user.last_name}`;
  email.textContent = user.email;
  id.textContent = user.id;
  role.textContent = user.is_admin ? "Administrator" : "Standard user";
}

async function handleCreateUser(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const formData = new FormData(form);
  const payload = {
    first_name: String(formData.get("first_name") || "").trim(),
    last_name: String(formData.get("last_name") || "").trim(),
    email: String(formData.get("email") || "").trim(),
    password: String(formData.get("password") || ""),
    is_admin: formData.get("is_admin") === "on",
  };

  try {
    const user = await api.post("/api/users", payload);
    updateCreatedUser(user);
    form.reset();
    flash(`Created ${user.first_name} ${user.last_name}`);
  } catch (error) {
    flash(error.message);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const form = document.querySelector("#admin-user-form");
  if (!form) {
    return;
  }

  try {
    const session = await getSession(true);
    if (!session.logged_in || !session.is_admin) {
      window.location.href = "/index.html";
      return;
    }

    form.addEventListener("submit", handleCreateUser);
  } catch (error) {
    flash(error.message);
    window.location.href = "/index.html";
  }
});
