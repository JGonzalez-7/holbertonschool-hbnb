export function getCookie(name) {
  const prefix = `${name}=`;
  const parts = document.cookie.split(";").map((part) => part.trim());

  for (const part of parts) {
    if (part.startsWith(prefix)) {
      return decodeURIComponent(part.slice(prefix.length));
    }
  }

  return null;
}
