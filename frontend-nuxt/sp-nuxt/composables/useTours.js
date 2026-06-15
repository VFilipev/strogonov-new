import { computed } from "vue";
import {
  ToursAvailabilityApi,
  ToursBookingsApi,
  ToursRoutesApi,
  ToursWeekendApi,
  ToursWeekendAvailabilityApi,
} from "~/utils/api";
import { normalizeListResponse } from "~/utils/apiHelpers";

function parseNumber(value, fallback = 0) {
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

export function useToursPageData() {
  const { data: routesData, pending: routesPending, error: routesError, refresh: refreshRoutes } =
    useAsyncData(
      "tours-routes",
      () => ToursRoutesApi.getList(),
      { default: () => [], server: true },
    );

  const { data: weekendData, pending: weekendPending, error: weekendError, refresh: refreshWeekend } =
    useAsyncData(
      "tours-weekend-program",
      () => ToursWeekendApi.getList(),
      { default: () => null, server: true },
    );

  const routes = computed(() =>
    normalizeListResponse(routesData.value).map((item) => ({
      ...item,
      price: parseNumber(item.price),
      tour_price: item.tour_price == null ? null : parseNumber(item.tour_price),
      tour_old_price: item.tour_old_price == null ? null : parseNumber(item.tour_old_price),
      min_vehicles: Number(item.min_vehicles || 1),
    })),
  );

  const weekendProgram = computed(() => weekendData.value || null);
  const weekendRoutes = computed(() =>
    normalizeListResponse(weekendProgram.value?.routes).map((item) => ({
      ...item,
      price: parseNumber(item.price),
      tour_price: item.tour_price == null ? null : parseNumber(item.tour_price),
      tour_old_price: item.tour_old_price == null ? null : parseNumber(item.tour_old_price),
      min_vehicles: Number(item.min_vehicles || 1),
    })),
  );

  const pending = computed(() => routesPending.value || weekendPending.value);
  const error = computed(() => routesError.value || weekendError.value);

  const refresh = async () => {
    await Promise.all([refreshRoutes(), refreshWeekend()]);
  };

  return {
    routes,
    weekendProgram,
    weekendRoutes,
    routesPending,
    weekendPending,
    pending,
    error,
    refresh,
  };
}

export async function getRouteAvailability(routeId, date) {
  return ToursAvailabilityApi.getList({ route: routeId, date });
}

export async function getWeekendAvailability(routeId, checkinDate) {
  return ToursWeekendAvailabilityApi.getList({ route: routeId, checkin_date: checkinDate });
}

export async function createTourBooking(payload) {
  return ToursBookingsApi.save(payload);
}
