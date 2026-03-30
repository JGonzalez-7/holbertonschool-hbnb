import { getCookie } from "./utils.js";

async function parseResponse(response) {
  const contentType = response.headers.get("content-type") || "";

  if (contentType.includes("application/json")) {
    return response.json();
  }

  return response.text();
}

async function request(path, options = {}) {
  const token = getCookie("token");
  const fetchOptions = {
    method: options.method || "GET",
    headers: {
      Accept: "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.json ? { "Content-Type": "application/json" } : {}),
      ...(options.headers || {}),
    },
    credentials: "same-origin",
  };

  if (options.json) {
    fetchOptions.body = JSON.stringify(options.json);
  }

  const response = await fetch(path, fetchOptions);
  const payload = await parseResponse(response);

  if (!response.ok) {
    const message =
      (payload && typeof payload === "object" && payload.message) ||
      (typeof payload === "string" && payload) ||
      response.statusText ||
      "Request failed";
    throw new Error(message);
  }

  return payload;
}

export const api = {
  get(path) {
    return request(path);
  },
  post(path, json) {
    return request(path, { method: "POST", json });
  },
};
