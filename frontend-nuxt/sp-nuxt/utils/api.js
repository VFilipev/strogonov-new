import axios from "axios";
import { toURLParams } from "./apiHelpers.js";

function appendSlash(url) {
  return url.endsWith("/") ? url : `${url}/`;
}

function joinUrl(baseUrl, path) {
  if (!baseUrl) return path;
  if (!path) return baseUrl;

  const normalizedBase = baseUrl.endsWith("/") ? baseUrl.slice(0, -1) : baseUrl;
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;

  return `${normalizedBase}${normalizedPath}`;
}

export function resolveRuntimeApiBase() {
  const configuredBase = useRuntimeConfig().public.apiBase;
  if (typeof window === "undefined") return configuredBase;

  try {
    const url = new URL(configuredBase);
    const localHosts = ["localhost", "127.0.0.1"];
    if (localHosts.includes(url.hostname) && localHosts.includes(window.location.hostname)) {
      url.hostname = window.location.hostname;
      return url.toString().replace(/\/$/, "");
    }
  } catch {
    return configuredBase;
  }

  return configuredBase;
}

async function _save(url, obj, config = {}) {
  const payload = obj ?? {};
  const id = payload instanceof FormData ? payload.get("id") : payload.id;
  const normalizedUrl = appendSlash(url);

  const response = id
    ? await axios.patch(`${normalizedUrl}${id}/`, payload, config)
    : await axios.post(normalizedUrl, payload, config);

  return response.data;
}

async function _delete(url, obj, config = {}) {
  const id = obj?.id;
  if (!id) return null;

  const normalizedUrl = appendSlash(url);
  return axios.delete(`${normalizedUrl}${id}/`, {
    ...config,
    data: obj,
  });
}

async function _getList(url, filter = {}, config = {}) {
  const normalizedUrl = appendSlash(url);
  const query = toURLParams(filter);
  const endpoint = query ? `${normalizedUrl}?${query}` : normalizedUrl;
  const response = await axios.get(endpoint, config);
  return response.data;
}

async function _getById(url, id, config = {}) {
  const normalizedUrl = appendSlash(url);
  const response = await axios.get(`${normalizedUrl}${id}/`, config);
  return response.data;
}

export function apiConstructor(apiUrl) {
  const normalizedUrl = appendSlash(apiUrl);

  return {
    async save(obj, config = {}) {
      return _save(normalizedUrl, obj, config);
    },
    async getById(id, config = {}) {
      return _getById(normalizedUrl, id, config);
    },
    async getList(filter = {}, config = {}) {
      return _getList(normalizedUrl, filter, config);
    },
    async delete(obj, config = {}) {
      return _delete(normalizedUrl, obj, config);
    },
  };
}

export function createApi(baseUrl, apiPath) {
  return apiConstructor(joinUrl(baseUrl, apiPath));
}

function createRuntimeApi(apiPath) {
  const normalizedPath = appendSlash(apiPath);
  const baseUrl = () => joinUrl(resolveRuntimeApiBase(), normalizedPath);

  return {
    async save(obj, config = {}) {
      return _save(baseUrl(), obj, config);
    },
    async getById(id, config = {}) {
      return _getById(baseUrl(), id, config);
    },
    async getList(filter = {}, config = {}) {
      return _getList(baseUrl(), filter, config);
    },
    async delete(obj, config = {}) {
      return _delete(baseUrl(), obj, config);
    },
  };
}

export const ActivitiesApi = createRuntimeApi("/activities/");
export const AfishaApi = createRuntimeApi("/afisha/");
export const SiteSettingsApi = createRuntimeApi("/site-settings/");
export const NewsApi = createRuntimeApi("/news/");
export const EventTypesApi = createRuntimeApi("/events/types/");
export const LodgesApi = createRuntimeApi("/lodges/");
export const LodgeTypesApi = createRuntimeApi("/lodges/types/");
export const LodgeCategoriesApi = createRuntimeApi("/lodges/categories/");
export const StatisticsApi = createRuntimeApi("/statistics/");
export const GalleryApi = createRuntimeApi("/gallery/");
export const HeroApi = createRuntimeApi("/hero/");
export const AdminStatusApi = createRuntimeApi("/auth/admin-status/");
export const RestaurantApi = createRuntimeApi("/restaurant/");
export const RestaurantImagesApi = createRuntimeApi("/restaurant/images/");
export const MealTypesApi = createRuntimeApi("/restaurant/meal-types/");
export const BenefitsApi = createRuntimeApi("/restaurant/benefits/");
export const EventCalculatorRequestsApi = createRuntimeApi("/events/requests/");
export const ToursRoutesApi = createRuntimeApi("/tours/routes/");
export const ToursWeekendApi = createRuntimeApi("/tours/weekend/");
export const ToursAvailabilityApi = createRuntimeApi("/tours/availability/");
export const ToursWeekendAvailabilityApi = createRuntimeApi("/tours/weekend-availability/");
export const ToursBookingsApi = createRuntimeApi("/tours/bookings/");
export const ToursScheduleApi = createRuntimeApi("/tours/schedule/");
