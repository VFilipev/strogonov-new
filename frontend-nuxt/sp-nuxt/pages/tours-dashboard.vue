<script setup>
import {
  AlertCircle,
  Bike,
  CalendarDays,
  ChevronLeft,
  ChevronRight,
  Clock3,
  Gauge,
  LoaderCircle,
  RefreshCw,
  Route,
  ShieldCheck,
  UserCheck,
  Users,
} from "lucide-vue-next";
import { AdminStatusApi, ToursRoutesApi, ToursScheduleApi, resolveRuntimeApiBase } from "~/utils/api";
import { normalizeListResponse } from "~/utils/apiHelpers";

const DAY_MS = 86_400_000;
const statusLabels = {
  forming: "Набор",
  confirmed: "Подтвержден",
  cancelled: "Отменен",
  done: "Завершен",
};
const typeLabels = {
  route: "Маршрут",
  weekend_tour: "Тур выходного дня",
};

const authPending = ref(true);
const isAuthorized = ref(false);
const adminName = ref("");
const authError = ref("");
const schedulePending = ref(false);
const scheduleError = ref("");
const viewMode = ref("week");
const anchorDate = ref(toDateInputValue(new Date()));
const periodDateInput = ref(null);
const schedule = ref(null);
const routes = ref([]);
const adminLoginUrl = computed(() => {
  const apiBase = String(resolveRuntimeApiBase() || "").replace(/\/api\/?$/, "");
  return `${apiBase || ""}/admin/`;
});

const period = computed(() => {
  const anchor = parseDateInput(anchorDate.value);
  if (viewMode.value === "day") {
    return { from: anchor, to: anchor };
  }
  const day = anchor.getDay() || 7;
  const monday = addDays(anchor, 1 - day);
  return { from: monday, to: addDays(monday, 6) };
});

const periodLabel = computed(() => {
  if (viewMode.value === "day") return formatDateLong(period.value.from);
  return `${formatDateShort(period.value.from)} - ${formatDateShort(period.value.to)}`;
});
const periodInputLabel = computed(() => {
  if (viewMode.value === "day") return formatDateNumeric(period.value.from);
  return `${formatDateNumeric(period.value.from)} - ${formatDateNumeric(period.value.to)}`;
});

const days = computed(() => {
  const result = [];
  let cursor = period.value.from;
  while (cursor <= period.value.to) {
    result.push(new Date(cursor));
    cursor = addDays(cursor, 1);
  }
  return result;
});

const timeSlots = computed(() => {
  const start = schedule.value?.work_day_start || "09:00:00";
  const end = schedule.value?.work_day_end || "19:00:00";
  const step = Number(schedule.value?.slot_step_minutes || 30);
  const slots = [];
  let cursor = timeToMinutes(start);
  const endMinutes = timeToMinutes(end);
  while (cursor < endMinutes) {
    slots.push(cursor);
    cursor += step;
  }
  return slots;
});
const scheduleGridStyle = computed(() => ({
  gridTemplateColumns: `96px repeat(${days.value.length}, minmax(160px, 1fr))`,
  gridTemplateRows: `repeat(${timeSlots.value.length}, minmax(44px, auto))`,
}));

const outings = computed(() => schedule.value?.outings || []);
const activeOutings = computed(() => outings.value.filter((outing) => outing.status !== "cancelled"));
const bookings = computed(() => outings.value.flatMap((outing) => outing.bookings || []));
const activeBookings = computed(() => bookings.value.filter((booking) => booking.status !== "cancelled"));
const totalVehicles = computed(() =>
  activeOutings.value.reduce((sum, outing) => sum + Number(outing.total_vehicles || 0), 0),
);
const totalPeople = computed(() =>
  activeOutings.value.reduce((sum, outing) => sum + Number(outing.total_people || 0), 0),
);
const overCapacityCount = computed(() =>
  activeBookings.value.filter((booking) => booking.over_capacity).length,
);
const formingCount = computed(() =>
  activeOutings.value.filter((outing) => !outing.meets_minimum).length,
);
const weekendOutingsCount = computed(() =>
  activeOutings.value.filter((outing) => outing.booking_type === "weekend_tour").length,
);
const routeOutingsCount = computed(() =>
  activeOutings.value.filter((outing) => outing.booking_type === "route").length,
);
const routeCount = computed(() => routes.value.length);
const weekendRouteCount = computed(() => routes.value.filter((route) => route.available_for_tour).length);

const statCards = computed(() => [
  {
    title: "Квадроциклы",
    value: schedule.value?.fleet_size ? `${totalVehicles.value}/${schedule.value.fleet_size}` : totalVehicles.value,
    caption: schedule.value?.fleet_size ? "занято в заявках / парк" : "лимит парка не задан",
    icon: Bike,
  },
  {
    title: "Инструкторы",
    value: schedule.value?.instructor_capacity ?? 0,
    caption: "доступно одновременно",
    icon: UserCheck,
  },
  {
    title: "Заявки",
    value: activeBookings.value.length,
    caption: `${totalPeople.value} чел. в периоде`,
    icon: Users,
  },
  {
    title: "Выезды",
    value: activeOutings.value.length,
    caption: `${routeOutingsCount.value} маршрутов, ${weekendOutingsCount.value} уикенд`,
    icon: Route,
  },
]);

const signalCards = computed(() => [
  {
    label: "Маршруты",
    value: routeCount.value,
    caption: `${weekendRouteCount.value} для тура выходного дня`,
  },
  {
    label: "Набор группы",
    value: formingCount.value,
    caption: "выездов ниже минимума",
  },
  {
    label: "Сверх емкости",
    value: overCapacityCount.value,
    caption: "заявок в лайт-режиме",
  },
]);

function parseDateInput(value) {
  const [year, month, day] = String(value || toDateInputValue(new Date())).split("-").map(Number);
  return new Date(year, month - 1, day);
}

function toDateInputValue(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function addDays(date, amount) {
  return new Date(date.getTime() + amount * DAY_MS);
}

function dateKey(date) {
  return toDateInputValue(date);
}

function timeToMinutes(value) {
  const [hours, minutes] = String(value || "00:00").split(":").map(Number);
  return hours * 60 + minutes;
}

function formatMinutes(minutes) {
  const hours = String(Math.floor(minutes / 60)).padStart(2, "0");
  const mins = String(minutes % 60).padStart(2, "0");
  return `${hours}:${mins}`;
}

function formatDateShort(date) {
  return new Intl.DateTimeFormat("ru-RU", { day: "2-digit", month: "2-digit" }).format(date);
}

function formatDateLong(date) {
  return new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(date);
}

function formatDateNumeric(date) {
  return new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "2-digit",
    year: "numeric",
  }).format(date);
}

function formatWeekday(date) {
  return new Intl.DateTimeFormat("ru-RU", { weekday: "short" }).format(date);
}

function formatTime(value) {
  if (!value) return "";
  return new Intl.DateTimeFormat("ru-RU", {
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

function getCellDateTime(day, minutes) {
  const date = new Date(day);
  date.setHours(Math.floor(minutes / 60), minutes % 60, 0, 0);
  return date;
}

function outingStartsInCell(outing, day, minutes) {
  const start = new Date(outing.start_at);
  const cellStart = getCellDateTime(day, minutes);
  const cellEnd = new Date(cellStart.getTime() + Number(schedule.value?.slot_step_minutes || 30) * 60_000);
  return start >= cellStart && start < cellEnd;
}

function outingsForCell(day, minutes) {
  return outings.value.filter((outing) => outingStartsInCell(outing, day, minutes));
}

function occupiedOutingsForCell(day, minutes) {
  const cellStart = getCellDateTime(day, minutes);
  const cellEnd = new Date(cellStart.getTime() + Number(schedule.value?.slot_step_minutes || 30) * 60_000);
  return outings.value.filter((outing) => {
    const start = new Date(outing.start_at);
    const end = new Date(outing.end_at);
    return start < cellEnd && end > cellStart;
  });
}

function continuingOutingsForCell(day, minutes) {
  return occupiedOutingsForCell(day, minutes).filter(
    (outing) => !outingStartsInCell(outing, day, minutes),
  );
}

function isCellOccupied(day, minutes) {
  return occupiedOutingsForCell(day, minutes).length > 0;
}

function getCellTone(day, minutes) {
  const cellOutings = occupiedOutingsForCell(day, minutes);
  if (cellOutings.length === 0) return "";
  if (cellOutings.some((outing) => outing.status === "cancelled")) return "bg-red-50/45";
  if (cellOutings.some((outing) => !outing.meets_minimum)) return "bg-amber-50/55";
  return "bg-emerald-50/55";
}

function outingsForDay(day) {
  const key = dateKey(day);
  return outings.value.filter((outing) => dateKey(new Date(outing.start_at)) === key);
}

function getOutingGridStyle(outing, dayIndex) {
  const step = Number(schedule.value?.slot_step_minutes || 30);
  const workStart = timeToMinutes(schedule.value?.work_day_start || "09:00:00");
  const workEnd = timeToMinutes(schedule.value?.work_day_end || "19:00:00");
  const start = new Date(outing.start_at);
  const end = new Date(outing.end_at);
  const startMinutes = start.getHours() * 60 + start.getMinutes();
  const endMinutes = end.getHours() * 60 + end.getMinutes();
  const rowStart = Math.max(1, Math.floor((startMinutes - workStart) / step) + 1);
  const rowEnd = Math.min(
    timeSlots.value.length + 1,
    Math.ceil((Math.min(endMinutes, workEnd) - workStart) / step) + 1,
  );

  return {
    gridColumn: `${dayIndex + 2}`,
    gridRow: `${rowStart} / ${Math.max(rowStart + 1, rowEnd)}`,
  };
}

function getOutingTone(outing) {
  if (outing.status === "cancelled") return "border-red-200 bg-red-50 text-red-900";
  if (outing.status === "done") return "border-slate-200 bg-slate-50 text-slate-700";
  if (outing.meets_minimum) return "border-emerald-200 bg-emerald-50 text-emerald-950";
  return "border-amber-200 bg-amber-50 text-amber-950";
}

async function loadAuth() {
  authPending.value = true;
  authError.value = "";
  try {
    const data = await AdminStatusApi.getList({}, { withCredentials: true });
    isAuthorized.value = Boolean(data?.is_authenticated);
    adminName.value = data?.username || "";
  } catch (error) {
    isAuthorized.value = false;
    authError.value =
      error?.response?.status === 401 || error?.response?.status === 403
        ? "Для просмотра дашборда необходимо войти в административную панель."
        : "Не удалось проверить авторизацию.";
  } finally {
    authPending.value = false;
  }
}

async function loadDashboard() {
  if (!isAuthorized.value) return;
  schedulePending.value = true;
  scheduleError.value = "";
  try {
    const [scheduleData, routesData] = await Promise.all([
      ToursScheduleApi.getList(
        {
          date_from: toDateInputValue(period.value.from),
          date_to: toDateInputValue(period.value.to),
        },
        { withCredentials: true },
      ),
      ToursRoutesApi.getList({}, { withCredentials: true }),
    ]);
    schedule.value = scheduleData;
    routes.value = normalizeListResponse(routesData);
  } catch (error) {
    scheduleError.value =
      error?.response?.status === 401 || error?.response?.status === 403
        ? "Нет доступа к шахматке. Войдите под учетной записью администратора или инструктора."
        : "Не удалось загрузить шахматку.";
  } finally {
    schedulePending.value = false;
  }
}

function shiftPeriod(direction) {
  const step = viewMode.value === "week" ? 7 : 1;
  anchorDate.value = toDateInputValue(addDays(parseDateInput(anchorDate.value), direction * step));
}

function openPeriodPicker() {
  const input = periodDateInput.value;
  if (!input) return;

  input.focus();
  try {
    if (typeof input.showPicker === "function") {
      input.showPicker();
    }
  } catch {
    input.focus();
  }
}

watch([viewMode, anchorDate], () => {
  loadDashboard();
});

onMounted(async () => {
  await loadAuth();
  await loadDashboard();
});

useHead({
  title: "Шахматка туров",
  meta: [
    {
      name: "robots",
      content: "noindex, nofollow",
    },
  ],
});
</script>

<template>
  <div class="min-h-screen bg-white text-foreground">
    <div class="container mx-auto px-4 py-6 md:px-8 md:py-8">
      <header class="flex flex-wrap items-center justify-between gap-4 border-b border-border pb-5">
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.18em] text-primary">
            Администрирование туров
          </p>
          <h1 class="mt-2 font-serif text-3xl text-primary md:text-4xl">
            Шахматка маршрутов
          </h1>
        </div>
        <NuxtLink
          to="/tours"
          class="inline-flex items-center justify-center rounded-full border border-primary/30 px-5 py-2.5 text-sm font-semibold text-primary transition-colors hover:border-primary hover:bg-primary/5"
        >
          На страницу туров
        </NuxtLink>
      </header>

      <div
        v-if="authPending"
        class="mt-8 flex items-center gap-3 rounded-xl border border-border bg-background px-5 py-4 text-sm text-muted-foreground"
      >
        <LoaderCircle class="h-4 w-4 animate-spin" aria-hidden="true" />
        Проверяем доступ...
      </div>

      <div
        v-else-if="!isAuthorized"
        class="mt-8 rounded-xl border border-amber-200 bg-amber-50 p-6 text-amber-950"
      >
        <div class="flex items-start gap-3">
          <AlertCircle class="mt-0.5 h-5 w-5 shrink-0" aria-hidden="true" />
          <div>
            <h2 class="font-semibold">Нужна авторизация</h2>
            <p class="mt-2 text-sm leading-relaxed">
              {{ authError || 'Войдите в административную панель, затем обновите эту страницу.' }}
            </p>
            <a
              :href="adminLoginUrl"
              class="mt-4 inline-flex rounded-full bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground"
            >
              Войти в админку
            </a>
          </div>
        </div>
      </div>

      <main v-else class="mt-6 space-y-6">
        <section class="flex flex-wrap items-center justify-between gap-4">
          <div class="text-sm text-muted-foreground">
            Пользователь:
            <span class="font-semibold text-foreground">{{ adminName }}</span>
          </div>

          <div class="flex flex-wrap items-center gap-2">
            <div class="inline-flex rounded-full border border-border bg-background p-1">
              <button
                type="button"
                class="rounded-full px-4 py-2 text-sm font-semibold transition-colors"
                :class="viewMode === 'day' ? 'bg-primary text-primary-foreground' : 'text-muted-foreground hover:text-primary'"
                @click="viewMode = 'day'"
              >
                День
              </button>
              <button
                type="button"
                class="rounded-full px-4 py-2 text-sm font-semibold transition-colors"
                :class="viewMode === 'week' ? 'bg-primary text-primary-foreground' : 'text-muted-foreground hover:text-primary'"
                @click="viewMode = 'week'"
              >
                Неделя
              </button>
            </div>
            <button
              type="button"
              class="inline-flex h-10 w-10 items-center justify-center rounded-full border border-border bg-background text-primary transition-colors hover:border-primary"
              aria-label="Предыдущий период"
              @click="shiftPeriod(-1)"
            >
              <ChevronLeft class="h-4 w-4" aria-hidden="true" />
            </button>
            <div
              class="relative h-10 min-w-[220px] cursor-pointer overflow-hidden rounded-full border border-border bg-background px-4 text-sm text-foreground transition-colors focus-within:border-primary"
              role="button"
              tabindex="0"
              aria-label="Выбрать дату периода"
              @click="openPeriodPicker"
              @keydown.enter.prevent="openPeriodPicker"
              @keydown.space.prevent="openPeriodPicker"
            >
              <span class="flex h-full items-center justify-between gap-3">
                <span>{{ periodInputLabel }}</span>
                <CalendarDays class="h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
              </span>
              <input
                ref="periodDateInput"
                v-model="anchorDate"
                type="date"
                class="pointer-events-none absolute inset-0 h-full w-full cursor-pointer opacity-0"
                aria-label="Выбрать дату периода"
              >
            </div>
            <button
              type="button"
              class="inline-flex h-10 w-10 items-center justify-center rounded-full border border-border bg-background text-primary transition-colors hover:border-primary"
              aria-label="Следующий период"
              @click="shiftPeriod(1)"
            >
              <ChevronRight class="h-4 w-4" aria-hidden="true" />
            </button>
            <button
              type="button"
              class="inline-flex h-10 items-center gap-2 rounded-full border border-primary/30 bg-background px-4 text-sm font-semibold text-primary transition-colors hover:border-primary"
              :disabled="schedulePending"
              @click="loadDashboard"
            >
              <RefreshCw class="h-4 w-4" :class="schedulePending ? 'animate-spin' : ''" aria-hidden="true" />
              Обновить
            </button>
          </div>
        </section>

        <section class="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          <article
            v-for="card in statCards"
            :key="card.title"
            class="rounded-xl border border-primary/15 bg-muted/20 p-5 shadow-sm"
          >
            <div class="flex items-start justify-between gap-4">
              <div>
                <p class="text-sm text-muted-foreground">{{ card.title }}</p>
                <p class="mt-2 text-3xl font-semibold text-primary">{{ card.value }}</p>
              </div>
              <component :is="card.icon" class="h-6 w-6 text-primary" aria-hidden="true" />
            </div>
            <p class="mt-3 text-xs text-muted-foreground">{{ card.caption }}</p>
          </article>
        </section>

        <section class="grid gap-3 md:grid-cols-3">
          <article
            v-for="card in signalCards"
            :key="card.label"
            class="flex items-center justify-between gap-4 rounded-xl border border-primary/15 bg-muted/20 px-5 py-4 shadow-sm"
          >
            <div>
              <p class="text-sm font-semibold text-foreground">{{ card.label }}</p>
              <p class="mt-1 text-xs text-muted-foreground">{{ card.caption }}</p>
            </div>
            <span class="text-2xl font-semibold text-primary">{{ card.value }}</span>
          </article>
        </section>

        <section class="rounded-xl border border-primary/15 bg-background shadow-sm">
          <div class="flex flex-wrap items-center justify-between gap-3 border-b border-border px-5 py-4">
            <div>
              <h2 class="font-serif text-2xl text-primary">Шахматка</h2>
              <p class="mt-1 text-sm text-muted-foreground">
                {{ periodLabel }} · {{ schedule?.work_day_start?.slice(0, 5) || '09:00' }}-{{ schedule?.work_day_end?.slice(0, 5) || '19:00' }}
              </p>
            </div>
            <div class="flex flex-wrap gap-2 text-xs">
              <span class="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-3 py-1 text-emerald-800">
                <ShieldCheck class="h-3.5 w-3.5" aria-hidden="true" />
                минимум набран
              </span>
              <span class="inline-flex items-center gap-1 rounded-full bg-amber-50 px-3 py-1 text-amber-800">
                <Gauge class="h-3.5 w-3.5" aria-hidden="true" />
                идет набор
              </span>
            </div>
          </div>

          <div
            v-if="scheduleError"
            class="m-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
          >
            {{ scheduleError }}
          </div>

          <div
            v-else-if="schedulePending"
            class="flex items-center gap-3 px-5 py-8 text-sm text-muted-foreground"
          >
            <LoaderCircle class="h-4 w-4 animate-spin" aria-hidden="true" />
            Загружаем шахматку...
          </div>

          <div v-else class="overflow-x-auto">
            <div class="min-w-[860px]">
              <div
                class="grid border-b border-border bg-primary/5"
                :style="{ gridTemplateColumns: `96px repeat(${days.length}, minmax(160px, 1fr))` }"
              >
                <div class="px-4 py-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                  Время
                </div>
                <div
                  v-for="day in days"
                  :key="dateKey(day)"
                  class="border-l border-border px-4 py-3"
                >
                  <p class="text-xs font-semibold uppercase text-muted-foreground">{{ formatWeekday(day) }}</p>
                  <p class="mt-1 font-semibold text-foreground">{{ formatDateShort(day) }}</p>
                </div>
              </div>

              <div class="grid" :style="scheduleGridStyle">
                <template
                  v-for="(minutes, rowIndex) in timeSlots"
                  :key="minutes"
                >
                  <div
                    class="min-h-[44px] border-b border-border px-4 py-2 text-sm font-semibold text-muted-foreground"
                    :style="{ gridColumn: '1', gridRow: rowIndex + 1 }"
                  >
                    {{ formatMinutes(minutes) }}
                  </div>
                  <div
                    v-for="(day, dayIndex) in days"
                    :key="`${dateKey(day)}-${minutes}`"
                    class="min-h-[44px] border-b border-l border-border transition-colors"
                    :class="getCellTone(day, minutes)"
                    :style="{ gridColumn: dayIndex + 2, gridRow: rowIndex + 1 }"
                  />
                </template>

                <template
                  v-for="(day, dayIndex) in days"
                  :key="`outings-${dateKey(day)}`"
                >
                  <article
                    v-for="outing in outingsForDay(day)"
                    :key="outing.id"
                    class="z-10 m-2 overflow-auto rounded-lg border px-3 py-2 text-xs shadow-sm"
                    :class="getOutingTone(outing)"
                    :style="getOutingGridStyle(outing, dayIndex)"
                  >
                    <div class="flex items-start justify-between gap-2">
                      <div>
                        <p class="font-semibold">{{ outing.route_title }}</p>
                        <p class="mt-1 opacity-80">
                          {{ formatTime(outing.start_at) }}-{{ formatTime(outing.end_at) }} · {{ typeLabels[outing.booking_type] || outing.booking_type }}
                        </p>
                      </div>
                      <span class="shrink-0 rounded-full bg-white/70 px-2 py-0.5 font-semibold">
                        {{ outing.total_vehicles }}/{{ outing.min_vehicles }}
                      </span>
                    </div>
                    <div class="mt-2 flex flex-wrap gap-1">
                      <span class="rounded-full bg-white/70 px-2 py-0.5">
                        {{ outing.total_people || 0 }} чел.
                      </span>
                      <span class="rounded-full bg-white/70 px-2 py-0.5">
                        {{ statusLabels[outing.status] || outing.status }}
                      </span>
                      <span
                        v-if="outing.instructor_name"
                        class="rounded-full bg-white/70 px-2 py-0.5"
                      >
                        {{ outing.instructor_name }}
                      </span>
                    </div>
                    <details v-if="outing.bookings?.length" class="mt-2">
                      <summary class="cursor-pointer text-[11px] font-semibold uppercase tracking-wide opacity-75">
                        Заявки: {{ outing.bookings.length }}
                      </summary>
                      <div class="mt-2 grid gap-1">
                        <p
                          v-for="booking in outing.bookings"
                          :key="booking.id"
                          class="rounded-md bg-white/70 px-2 py-1"
                        >
                          {{ booking.contact_name }} · {{ booking.vehicles_count }} квад. · {{ booking.people_count || 0 }} чел.
                        </p>
                      </div>
                    </details>
                  </article>
                </template>
              </div>

              <div
                v-if="outings.length === 0"
                class="px-5 py-8 text-center text-sm text-muted-foreground"
              >
                В выбранном периоде пока нет выездов.
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>
