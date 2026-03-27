const getCookieValue = (name) => {
  if (!import.meta.client) return null;
  const cookie = document.cookie.split("; ").find((row) => row.startsWith(`${name}=`));
  return cookie ? decodeURIComponent(cookie.split("=")[1]) : null;
};

export const useAdminContentApi = () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;

  const ensureCsrf = async () => {
    await $fetch(`${apiBase}/auth/csrf/`, {
      method: "GET",
      credentials: "include",
    });
  };

  const csrfHeaders = (json = true) => {
    const csrfToken = getCookieValue("csrftoken");
    return {
      ...(csrfToken ? { "X-CSRFToken": csrfToken } : {}),
      ...(json ? { "Content-Type": "application/json" } : {}),
    };
  };

  const fetchWithCsrf = async (method, endpoint, body) => {
    await ensureCsrf();
    return await $fetch(`${apiBase}${endpoint}`, {
      method,
      body,
      credentials: "include",
      headers: csrfHeaders(true),
    });
  };

  const sendForm = async (method, endpoint, formData) => {
    await ensureCsrf();
    const csrfToken = getCookieValue("csrftoken");
    return await $fetch(`${apiBase}${endpoint}`, {
      method,
      body: formData,
      credentials: "include",
      headers: {
        ...(csrfToken ? { "X-CSRFToken": csrfToken } : {}),
      },
    });
  };

  const get = async (endpoint) => {
    await ensureCsrf();
    return await $fetch(`${apiBase}${endpoint}`, {
      method: "GET",
      credentials: "include",
    });
  };

  const patch = (endpoint, payload) => fetchWithCsrf("PATCH", endpoint, payload);
  const post = (endpoint, payload) => fetchWithCsrf("POST", endpoint, payload);
  const patchForm = (endpoint, formData) => sendForm("PATCH", endpoint, formData);
  const postForm = (endpoint, formData) => sendForm("POST", endpoint, formData);

  return { get, patch, patchForm, post, postForm };
};
