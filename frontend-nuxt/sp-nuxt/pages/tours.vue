<script setup>
import {
  ArrowRight,
  CalendarDays,
  Clock3,
  LoaderCircle,
  Gauge,
  PackageCheck,
  ShieldCheck,
  Users,
  X,
} from "lucide-vue-next";
import ToursHero from "~/components/sections/ToursHero.vue";
import {
  createTourBooking,
  getRouteAvailability,
  getWeekendAvailability,
  useToursPageData,
} from "~/composables/useTours";

import tourCardImage1 from "~/assets/resort/tour1.jpeg";
import tourCardImage2 from "~/assets/resort/tour2.jpeg";
import tourCardImage3 from "~/assets/resort/tour3.jpg";
import tourCardImage4 from "~/assets/resort/tour4.jpeg";
import galleryHero from "~/assets/tours/hero.webp";
import galleryHero6 from "~/assets/tours/hero6.webp";
import galleryHero7 from "~/assets/tours/hero7.webp";
import galleryHero8 from "~/assets/tours/hero8.webp";
import galleryHero9 from "~/assets/tours/hero9.webp";
import galleryHero10 from "~/assets/tours/hero10.webp";
import galleryHero11 from "~/assets/tours/hero11.webp";
import weekendFoodImage from "~/assets/restoran/menu3.webp";
import weekendRelaxImage from "~/assets/resort/sauna.jpg";
import weekendStayImage from "~/assets/resort/stay.jpg";

const config = useRuntimeConfig();
const siteUrl = config.public.siteUrl;
const bookingPhone = "+7 (342) 233-33-32";
const bookingTel = "tel:+73422333332";

const heroIntro =
  "Незабываемые туры на квадроциклах в Пермском крае: премиальная техника TGB, сопровождение гида и полный комплект экипировки.";

const formatRub = (value) => `${new Intl.NumberFormat("ru-RU").format(value)} руб`;

const includedItems = [
  {
    title: "Аренда премиальной техники",
    text: "Квадроцикл TGB Blade LTX EPS с двигателем 600 куб.см и 45 л.с.",
  },
  {
    title: "Квалифицированный инструктаж",
    text: "По технике безопасности и эксплуатации мотовездехода.",
  },
  {
    title: "Комплект профессиональной экипировки",
    text: "Для защиты вашего здоровья и повседневной одежды.",
  },
  {
    title: "Сопровождение гида",
    text: "И помощь на всё время проведения тура.",
  },
  {
    title: "Фото и видеосъемка",
    text: "С дальнейшим монтажем и отправкой материалов.",
  },
  {
    title: "Запрет на алкоголь",
    text: "Для всех участников мероприятия.",
  },
];

const coverStyle = (src) =>
  src ? { backgroundImage: `url("${String(src)}")` } : {};

const fallbackRoutePhotos = {
  oznakomitelnyy: tourCardImage1,
  "bobrovaya-plotina": tourCardImage2,
  pchelovod: tourCardImage3,
  pcheloved: tourCardImage3,
  "vedmin-krug": tourCardImage4,
  chermoz: tourCardImage4,
};

const fallbackWeekendExperienceMedia = [
  { id: "food", photo: weekendFoodImage, photoAlt: "Питание на базе отдыха" },
  { id: "quad", photo: galleryHero11, photoAlt: "Квадроцикл на маршруте выходного дня" },
  { id: "relax", photo: weekendRelaxImage, photoAlt: "Банный комплекс для отдыха после тура" },
  { id: "stay", photo: weekendStayImage, photoAlt: "Дом для проживания на базе отдыха" },
];

const {
  routes,
  weekendProgram,
  weekendRoutes,
  pending: toursPending,
  error: toursError,
} = useToursPageData();

const quadTours = computed(() =>
  routes.value.map((tour, index) => ({
    id: tour.id,
    title: tour.title,
    duration: tour.duration_label || `${tour.duration_minutes} минут`,
    group: tour.group_label || `от ${tour.min_vehicles || 1} квадроциклов`,
    difficulty: (tour.difficulty_display || tour.difficulty || "").toLowerCase(),
    price: Number(tour.price || 0),
    photo:
      tour.image_variants?.card ||
      tour.photo_url ||
      fallbackRoutePhotos[tour.slug] ||
      [tourCardImage1, tourCardImage2, tourCardImage3, tourCardImage4][index % 4],
  })),
);

const weekendTourBenefits = computed(() => weekendProgram.value?.benefits || []);

const weekendTourOptions = computed(() =>
  weekendRoutes.value.map((route, index) => ({
    id: route.id,
    title: route.title,
    description: route.tour_description || route.description || "Маршрут выходного дня.",
    difficulty: route.difficulty_display || route.difficulty || "",
    price: Number(route.tour_price ?? route.price ?? 0),
    oldPrice: route.tour_old_price == null ? null : Number(route.tour_old_price),
    photo:
      route.image_variants?.card ||
      route.photo_url ||
      fallbackRoutePhotos[route.slug] ||
      [tourCardImage2, tourCardImage3, tourCardImage1, tourCardImage4][index % 4],
    photoAlt: `Маршрут ${route.title}`,
  })),
);

const weekendSchedule = computed(() => weekendProgram.value?.schedule || []);
const weekendIncludedItems = computed(() => weekendProgram.value?.included_items || []);
const weekendExperienceItems = computed(() =>
  (weekendProgram.value?.experience_items || []).map((item, index) => {
    const media =
      fallbackWeekendExperienceMedia.find((entry) => entry.id === item.id) ||
      fallbackWeekendExperienceMedia[index % fallbackWeekendExperienceMedia.length];
    return {
      ...item,
      photo: media.photo,
      photoAlt: media.photoAlt,
    };
  }),
);

const weekendIntro = computed(
  () =>
    weekendProgram.value?.intro ||
    "Формат для тех, кто хочет приехать на базу на весь уикенд: выбрать квадромаршрут, переночевать в комфортном доме и отдохнуть после активной поездки.",
);

const bookingModalOpen = ref(false);
const bookingType = ref("route");
const selectedRouteId = ref(null);
const selectedRouteDate = ref("");
const selectedCheckinDate = ref("");
const selectedStartTime = ref("");
const selectedJoinOuting = ref(null);
const vehiclesCount = ref(1);
const peopleCount = ref(null);
const contactName = ref("");
const contactPhone = ref("");
const contactEmail = ref("");
const comment = ref("");
const bookingSubmitError = ref("");
const bookingSubmitSuccess = ref("");
const consentAccepted = ref(false);
const availabilityError = ref("");
const availabilityPending = ref(false);
const routeAvailability = ref(null);
const weekendAvailability = ref(null);
const isSubmittingBooking = ref(false);
const previousBodyOverflow = ref("");

const bookingRoutes = computed(() =>
  bookingType.value === "weekend_tour" ? weekendRoutes.value : routes.value,
);
const availableSlots = computed(() => routeAvailability.value?.slots || []);
const availableFormingOutings = computed(() => routeAvailability.value?.forming_outings || []);

const formatIsoTime = (isoString) => {
  if (!isoString) return "";
  const date = new Date(isoString);
  return new Intl.DateTimeFormat("ru-RU", { hour: "2-digit", minute: "2-digit" }).format(date);
};

const formatIsoDateTime = (isoString) => {
  if (!isoString) return "";
  const date = new Date(isoString);
  return new Intl.DateTimeFormat("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
};

const parseApiError = (error) => {
  const fallbackMessage = "Не удалось выполнить запрос. Попробуйте ещё раз.";
  const data = error?.response?.data;
  if (!data) return fallbackMessage;
  if (typeof data.detail === "string") return data.detail;
  if (typeof data === "string") return data;
  if (Array.isArray(data.non_field_errors) && data.non_field_errors[0]) {
    return data.non_field_errors[0];
  }
  const firstKey = Object.keys(data)[0];
  if (!firstKey) return fallbackMessage;
  const firstValue = data[firstKey];
  if (Array.isArray(firstValue) && firstValue[0]) return `${firstKey}: ${firstValue[0]}`;
  if (typeof firstValue === "string") return `${firstKey}: ${firstValue}`;
  return fallbackMessage;
};

const openNativeDatePicker = (event) => {
  const input = event?.currentTarget;
  if (typeof input?.showPicker !== "function") return;
  try {
    input.showPicker();
  } catch {
    // showPicker can be blocked outside a direct user gesture.
  }
};

const isFridayIsoDate = (dateString) => {
  if (!dateString) return false;
  return new Date(`${dateString}T00:00:00`).getDay() === 5;
};

const handleWeekendDateChange = () => {
  if (!selectedCheckinDate.value || isFridayIsoDate(selectedCheckinDate.value)) return;
  selectedCheckinDate.value = "";
  weekendAvailability.value = null;
  availabilityError.value = "Для тура выходного дня выберите пятницу.";
};

const resetBookingForm = () => {
  selectedRouteDate.value = "";
  selectedCheckinDate.value = "";
  selectedStartTime.value = "";
  selectedJoinOuting.value = null;
  vehiclesCount.value = 1;
  peopleCount.value = null;
  contactName.value = "";
  contactPhone.value = "";
  contactEmail.value = "";
  comment.value = "";
  bookingSubmitError.value = "";
  bookingSubmitSuccess.value = "";
  consentAccepted.value = false;
  availabilityError.value = "";
  routeAvailability.value = null;
  weekendAvailability.value = null;
};

const openBookingModal = (type, routeId = null) => {
  bookingType.value = type;
  selectedRouteId.value =
    routeId ||
    bookingRoutes.value?.[0]?.id ||
    null;
  resetBookingForm();
  bookingModalOpen.value = true;
};

const closeBookingModal = () => {
  bookingModalOpen.value = false;
  bookingSubmitError.value = "";
  bookingSubmitSuccess.value = "";
};

watch([bookingType, selectedRouteId, selectedRouteDate], async ([type, routeId, routeDate]) => {
  if (type !== "route") return;
  routeAvailability.value = null;
  availabilityError.value = "";
  selectedStartTime.value = "";
  selectedJoinOuting.value = null;
  if (!routeId || !routeDate) return;
  availabilityPending.value = true;
  try {
    routeAvailability.value = await getRouteAvailability(routeId, routeDate);
  } catch (error) {
    availabilityError.value = parseApiError(error);
  } finally {
    availabilityPending.value = false;
  }
});

watch([bookingType, selectedRouteId, selectedCheckinDate], async ([type, routeId, checkinDate]) => {
  if (type !== "weekend_tour") return;
  weekendAvailability.value = null;
  availabilityError.value = "";
  if (!routeId || !checkinDate) return;
  availabilityPending.value = true;
  try {
    weekendAvailability.value = await getWeekendAvailability(routeId, checkinDate);
  } catch (error) {
    availabilityError.value = parseApiError(error);
  } finally {
    availabilityPending.value = false;
  }
});

watch([bookingType, selectedRouteId], ([type, routeId]) => {
  if (!routeId) return;
  if (type === "route") {
    selectedCheckinDate.value = "";
    weekendAvailability.value = null;
  } else {
    selectedRouteDate.value = "";
    routeAvailability.value = null;
    selectedStartTime.value = "";
    selectedJoinOuting.value = null;
  }
});

watch(bookingType, (type) => {
  const list = type === "weekend_tour" ? weekendRoutes.value : routes.value;
  if (!list.some((item) => Number(item.id) === Number(selectedRouteId.value))) {
    selectedRouteId.value = list[0]?.id || null;
  }
});

const submitBooking = async () => {
  bookingSubmitError.value = "";
  bookingSubmitSuccess.value = "";
  if (!selectedRouteId.value) {
    bookingSubmitError.value = "Выберите маршрут.";
    return;
  }
  if (!contactName.value.trim()) {
    bookingSubmitError.value = "Укажите имя для обратной связи.";
    return;
  }
  const phoneDigits = (contactPhone.value || "").replace(/\D/g, "");
  if (!contactEmail.value.trim() && phoneDigits.length < 10) {
    bookingSubmitError.value = "Укажите телефон или email для связи.";
    return;
  }
  if (!consentAccepted.value) {
    bookingSubmitError.value = "Подтвердите согласие на обработку персональных данных.";
    return;
  }

  const payload = {
    booking_type: bookingType.value,
    route: Number(selectedRouteId.value),
    vehicles_count: Number(vehiclesCount.value || 1),
    people_count: peopleCount.value ? Number(peopleCount.value) : null,
    contact_name: contactName.value.trim(),
    contact_phone: contactPhone.value.trim(),
    contact_email: contactEmail.value.trim(),
    comment: comment.value.trim(),
  };

  if (bookingType.value === "route") {
    if (!selectedRouteDate.value) {
      bookingSubmitError.value = "Укажите дату выезда.";
      return;
    }
    if (!selectedStartTime.value && !selectedJoinOuting.value) {
      bookingSubmitError.value = "Выберите время или присоединение к группе.";
      return;
    }
    payload.date = selectedRouteDate.value;
    if (selectedJoinOuting.value) {
      payload.join_outing = Number(selectedJoinOuting.value);
    } else {
      payload.start_time = selectedStartTime.value;
    }
  } else {
    if (!selectedCheckinDate.value) {
      bookingSubmitError.value = "Укажите дату заезда.";
      return;
    }
    if (!isFridayIsoDate(selectedCheckinDate.value)) {
      bookingSubmitError.value = "Для тура выходного дня выберите пятницу.";
      return;
    }
    payload.checkin_date = selectedCheckinDate.value;
  }

  isSubmittingBooking.value = true;
  try {
    const result = await createTourBooking(payload);
    bookingSubmitSuccess.value = result?.message || "Заявка успешно отправлена.";
    bookingSubmitError.value = "";
  } catch (error) {
    bookingSubmitError.value = parseApiError(error);
  } finally {
    isSubmittingBooking.value = false;
  }
};

watch(bookingModalOpen, (isOpen) => {
  if (typeof document === "undefined") return;
  if (isOpen) {
    previousBodyOverflow.value = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return;
  }
  document.body.style.overflow = previousBodyOverflow.value;
});

onBeforeUnmount(() => {
  if (typeof document !== "undefined") {
    document.body.style.overflow = previousBodyOverflow.value;
  }
});

const tourGallery = [
  { src: galleryHero11, alt: "Участник тура на квадроцикле" },
  { src: galleryHero8, alt: "Квадроцикл и маршрут в лесу" },
  { src: galleryHero, alt: "Квадроцикл на маршруте" },
  { src: galleryHero9, alt: "Поездка по лесной дороге" },
  { src: galleryHero6, alt: "Участник тура на водной преграде" },
  { src: galleryHero10, alt: "Квадроцикл на пересеченной местности" },
  { src: galleryHero7, alt: "Квадроцикл в динамике" },
];

// Бренд добавляется глобальным titleTemplate, в title его не дублируем.
const toursTitle = "Квадротуры в Перми и Пермском крае — маршруты и цены";
const toursDescription =
  "Квадротуры в Перми и Пермском крае на базе отдыха «Строгановские Просторы»: прокат квадроциклов, маршруты разной сложности, сопровождение гида, экипировка, фото и видео отчёт.";

useSeoMeta({
  title: toursTitle,
  description: toursDescription,
  ogTitle: "Квадротуры в Пермском крае — Строгановские Просторы",
  ogDescription: toursDescription,
  ogType: "website",
  ogLocale: "ru_RU",
});

useHead({
  link: [{ rel: "canonical", href: `${siteUrl}/tours` }],
});

useStructuredData({
  "@context": "https://schema.org",
  "@type": "Service",
  serviceType: "Квадротуры на квадроциклах",
  name: "Квадротуры в Пермском крае",
  description: toursDescription,
  url: `${siteUrl}/tours`,
  areaServed: ["Пермь", "Пермский край"],
  provider: {
    "@type": "Resort",
    name: "База отдыха «Строгановские Просторы»",
    url: siteUrl,
    telephone: "+79026439294",
    address: {
      "@type": "PostalAddress",
      addressCountry: "RU",
      addressRegion: "Пермский край",
      addressLocality: "Ильинский район, п. Ильинский, с. Дмитриевское",
    },
  },
});

useBreadcrumbs([{ name: "Квадротуры", path: "/tours" }]);
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <ToursHero
      title="Квадротуры в Пермском крае"
      :intro="heroIntro"
    />

    <section id="tours-list" class="scroll-mt-24 border-b border-border bg-background py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <h2 class="font-serif text-3xl text-primary md:text-4xl">
          Маршруты
        </h2>

        <p
          v-if="toursError"
          class="mt-6 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
        >
          Не удалось загрузить маршруты. Обновите страницу или попробуйте позже.
        </p>

        <div
          v-else-if="toursPending && quadTours.length === 0"
          class="mt-8 flex items-center gap-3 text-sm text-muted-foreground"
        >
          <LoaderCircle class="h-4 w-4 animate-spin" aria-hidden="true" />
          Загрузка маршрутов...
        </div>

        <div
          v-else-if="quadTours.length > 0"
          class="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-4"
        >
          <article
            v-for="tour in quadTours"
            :key="tour.id"
            class="group flex flex-col overflow-hidden rounded-2xl border border-border bg-card shadow-sm transition-all duration-300"
          >
            <div class="relative min-h-[170px] overflow-hidden bg-primary/95 px-5 py-6 text-primary-foreground">
              <div
                class="cover-bg absolute inset-0 opacity-95"
                role="img"
                :aria-label="tour.title"
                :style="coverStyle(tour.photo)"
              />
              <div class="absolute inset-0 bg-gradient-to-b from-black/15 via-black/35 to-black/35" />
              <h3 class="relative mt-auto font-serif text-2xl text-primary-foreground">
                {{ tour.title }}
              </h3>
            </div>

            <div class="flex flex-1 flex-col px-5 py-5">
              <dl class="space-y-2 text-sm">
                <div class="flex items-start gap-2">
                  <Clock3 class="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                  <div>
                    <dt class="text-muted-foreground">Продолжительность:</dt>
                    <dd class="font-semibold text-foreground">{{ tour.duration }}</dd>
                  </div>
                </div>
                <div class="flex items-start gap-2">
                  <Users class="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                  <div>
                    <dt class="text-muted-foreground">Группа:</dt>
                    <dd class="font-semibold text-foreground">{{ tour.group }}</dd>
                  </div>
                </div>
                <div class="flex items-start gap-2">
                  <Gauge class="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                  <div>
                    <dt class="text-muted-foreground">Сложность:</dt>
                    <dd class="font-semibold text-foreground">{{ tour.difficulty }}</dd>
                  </div>
                </div>
              </dl>

              <p class="mt-6 font-serif text-3xl font-semibold text-primary">
                {{ formatRub(tour.price) }}
              </p>

              <button
                type="button"
                @click="openBookingModal('route', tour.id)"
                class="mt-5 inline-flex items-center justify-center gap-2 rounded-full border border-primary bg-primary px-5 py-2.5 text-sm font-semibold uppercase tracking-wide text-primary-foreground transition-colors hover:bg-primary/90"
              >
                Забронировать
                <ArrowRight class="h-4 w-4" aria-hidden="true" />
              </button>
            </div>
          </article>
        </div>

        <p
          v-else
          class="mt-6 rounded-2xl border border-border bg-card px-4 py-3 text-sm text-muted-foreground"
        >
          Сейчас нет доступных маршрутов.
        </p>

        <p class="mt-8 text-sm leading-relaxed text-muted-foreground">
          * Стоимость указана за 1 человека, который будет управлять квадроциклом, возможность и цена размещения пассажира обговаривается отдельно и зависит от конкретного маршрута. Бронирование квадротуров происходит через оператора с внесением предоплаты в размере 20% от стоимости тура, в стоимость услуги не входит доставка клиента до точки проведения туристического мероприятия и обратный трансфер.
        </p>
      </div>
    </section>

    <section class="border-b border-border bg-muted/30 py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <h2 class="font-serif text-3xl text-primary md:text-4xl">
          Что входит в стоимость
        </h2>

        <div class="mt-10 rounded-3xl border-2 border-dashed border-primary/70 bg-card/80 p-5 md:p-8">
          <div class="grid gap-4 md:grid-cols-2">
            <article
              v-for="(item, index) in includedItems"
              :key="item.title"
              class="relative rounded-2xl border border-border bg-background px-5 py-4"
            >
              <div
                class="absolute -left-3 -top-3 flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold text-primary-foreground"
                :class="item.title === 'Запрет на алкоголь' ? 'bg-red-600' : 'bg-primary'"
              >
                {{ index + 1 }}
              </div>
              <h3 class="font-semibold text-foreground">
                {{ item.title }}
              </h3>
              <p class="mt-1 text-sm leading-relaxed text-muted-foreground">
                {{ item.text }}
              </p>
            </article>
          </div>
        </div>

        <p class="mt-6 text-sm leading-relaxed text-muted-foreground">
          В состав длительных и индивидуальных туров могут входить дополнительные услуги: рыбалка, сбор ягод и грибов, а также приготовление пищи в походных условиях.
        </p>
      </div>
    </section>

    <section class="border-b border-border bg-background py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <div class="grid gap-8 lg:grid-cols-[0.95fr_1.05fr] lg:items-start">
          <div class="rounded-3xl border border-primary/20 bg-gradient-to-br from-primary/10 via-primary/5 to-transparent p-6 md:p-8">
            <span class="inline-flex items-center gap-2 rounded-full bg-primary px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] text-primary-foreground">
              <CalendarDays class="h-4 w-4" aria-hidden="true" />
              Тур выходного дня
            </span>
            <h2 class="mt-6 font-serif text-3xl text-primary md:text-4xl">
              Маршрут, проживание и отдых в одном предложении
            </h2>
            <p class="mt-5 text-base leading-relaxed text-muted-foreground md:text-lg">
              {{ weekendIntro }}
            </p>


            <div class="mt-8 grid gap-4">
              <article
                v-for="benefit in weekendTourBenefits"
                :key="benefit.title"
                class="rounded-2xl border border-border bg-card/90 p-5 shadow-sm"
              >
                <h3 class="font-semibold text-foreground">
                  {{ benefit.title }}
                </h3>
                <p class="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {{ benefit.text }}
                </p>
              </article>
            </div>
          </div>

          <div class="grid gap-5">
            <article
              v-for="option in weekendTourOptions"
              :key="option.id"
              class="overflow-hidden rounded-3xl border border-border bg-card shadow-sm"
            >
              <div class="grid gap-0 md:grid-cols-[180px_1fr_auto]">
                <div class="relative min-h-[190px] overflow-hidden bg-primary/10 md:min-h-full">
                  <div
                    class="cover-bg absolute inset-0"
                    role="img"
                    :aria-label="option.photoAlt"
                    :style="coverStyle(option.photo)"
                  />
                  <div class="absolute inset-0 bg-gradient-to-t from-black/45 via-transparent to-transparent" />
                </div>
                <div class="p-6 md:p-7">
                  <div
                    v-if="option.difficulty"
                    class="mb-3 inline-flex items-center gap-1.5 text-xs font-medium text-muted-foreground"
                  >
                    <Gauge class="h-3.5 w-3.5 text-primary/70" aria-hidden="true" />
                    <span>{{ option.difficulty }}</span>
                  </div>
                  <h3 class="font-serif text-2xl text-primary md:text-3xl">
                    {{ option.title }}
                  </h3>
                  <p class="mt-3 text-sm leading-relaxed text-muted-foreground">
                    {{ option.description }}
                  </p>
                </div>

                <div class="flex min-w-[210px] flex-col justify-center border-t border-border bg-primary/5 p-6 md:border-l md:border-t-0 md:p-7">
                  <p class="text-sm text-muted-foreground">
                    Стоимость тура
                  </p>
                  <p class="mt-2 font-serif text-3xl font-semibold text-primary">
                    {{ formatRub(option.price) }}
                  </p>
                  <p
                    v-if="option.oldPrice"
                    class="mt-2 text-sm text-muted-foreground"
                  >
                    Обычная цена
                    <span class="ml-1 text-base font-semibold text-foreground line-through">
                      {{ formatRub(option.oldPrice) }}
                    </span>
                  </p>
                  <button
                    type="button"
                    @click="openBookingModal('weekend_tour', option.id)"
                    class="mt-5 inline-flex items-center justify-center gap-2 rounded-full border border-primary bg-primary px-5 py-2.5 text-xs font-semibold uppercase tracking-wide text-primary-foreground transition-colors hover:bg-primary/90"
                  >
                    Забронировать тур
                    <ArrowRight class="h-4 w-4" aria-hidden="true" />
                  </button>
                </div>
              </div>
            </article>
          </div>
        </div>

        <div class="mt-8 rounded-3xl border border-border bg-card p-5 shadow-sm md:p-8">
          <h3 class="font-serif text-2xl text-primary md:text-3xl">
            Все для готового уикенда
          </h3>
          <p class="mt-2 max-w-3xl text-sm leading-relaxed text-muted-foreground md:text-base">
            В туре уже закрыты ключевые потребности отдыха: питание, активный маршрут, восстановление и проживание.
          </p>

          <div class="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <article
              v-for="item in weekendExperienceItems"
              :key="item.id"
              class="overflow-hidden rounded-2xl border border-border bg-background"
            >
              <div class="relative h-40 overflow-hidden">
                <div
                  class="cover-bg absolute inset-0"
                  role="img"
                  :aria-label="item.photoAlt"
                  :style="coverStyle(item.photo)"
                />
                <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />
              </div>
              <div class="p-4">
                <h4 class="font-semibold text-foreground">
                  {{ item.title }}
                </h4>
                <p class="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {{ item.text }}
                </p>
              </div>
            </article>
          </div>
        </div>

        <div class="mt-10 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <div class="rounded-3xl border border-border bg-card p-5 shadow-sm md:p-8">
            <div class="flex items-center gap-3">
              <Clock3 class="h-6 w-6 text-primary" aria-hidden="true" />
              <h3 class="font-serif text-2xl text-primary md:text-3xl">
                Программа тура
              </h3>
            </div>

            <div class="mt-6 grid gap-4 md:grid-cols-3">
              <article
                v-for="day in weekendSchedule"
                :key="day.day"
                class="rounded-2xl border border-primary/20 bg-background p-5"
              >
                <h4 class="font-serif text-xl text-primary">
                  {{ day.day }}
                </h4>
                <ul class="mt-4 space-y-3 text-sm leading-relaxed text-muted-foreground">
                  <li
                    v-for="item in day.items"
                    :key="item"
                    class="flex gap-2"
                  >
                    <span class="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" aria-hidden="true" />
                    <span>{{ item }}</span>
                  </li>
                </ul>
              </article>
            </div>

          </div>

          <div class="rounded-3xl border-2 border-dashed border-primary/70 bg-card/80 p-5 md:p-8">
            <div class="flex items-center gap-3">
              <PackageCheck class="h-6 w-6 text-primary" aria-hidden="true" />
              <h3 class="font-serif text-2xl text-primary md:text-3xl">
                Включено в тур
              </h3>
            </div>

            <div class="mt-6 grid gap-3">
              <div
                v-for="item in weekendIncludedItems"
                :key="item.title"
                class="flex items-start gap-3 rounded-2xl border border-border bg-background px-4 py-3 text-sm leading-relaxed text-foreground"
              >
                <ShieldCheck class="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                <span>
                  <span class="block font-semibold">{{ item.title }}</span>
                  <span
                    v-if="item.text"
                    class="mt-1 block text-muted-foreground"
                  >
                    {{ item.text }}
                  </span>
                </span>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-8 flex flex-wrap items-center justify-between gap-4 rounded-3xl border border-primary/20 bg-primary px-6 py-5 text-primary-foreground md:px-8">
          <p class="max-w-2xl text-sm leading-relaxed md:text-base">
            Итоговая стоимость зависит от выбранного маршрута. Сейчас для тура выходного дня доступны два направления.
          </p>
          <button
            type="button"
            @click="openBookingModal('weekend_tour', weekendTourOptions[0]?.id || null)"
            class="inline-flex items-center justify-center gap-2 rounded-full border border-primary-foreground/80 px-6 py-3 text-sm font-semibold uppercase tracking-wide transition-colors hover:bg-primary-foreground hover:text-primary"
          >
            Забронировать уикенд
            <ArrowRight class="h-4 w-4" aria-hidden="true" />
          </button>
        </div>
      </div>
    </section>

    <section class="border-b border-border bg-background py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <h2 class="text-center font-serif text-3xl text-primary md:text-4xl">
          Фото и видео отчеты
        </h2>
        <div class="mt-10 grid grid-cols-1 gap-4 md:grid-cols-3">
          <div class="grid gap-4">
            <article class="relative h-[240px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm md:h-[250px]">
              <div
                class="cover-bg absolute inset-0"
                role="img"
                :aria-label="tourGallery[0].alt"
                :style="coverStyle(tourGallery[0].src)"
              />
            </article>
            <article class="relative h-[240px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm md:h-[285px]">
              <div
                class="cover-bg absolute inset-0"
                role="img"
                :aria-label="tourGallery[4].alt"
                :style="coverStyle(tourGallery[4].src)"
              />
            </article>
          </div>

          <div class="grid gap-4">
            <article class="relative h-[170px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
              <div
                class="cover-bg absolute inset-0"
                role="img"
                :aria-label="tourGallery[1].alt"
                :style="coverStyle(tourGallery[1].src)"
              />
            </article>
            <article class="relative h-[170px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
              <div
                class="cover-bg absolute inset-0"
                role="img"
                :aria-label="tourGallery[3].alt"
                :style="coverStyle(tourGallery[3].src)"
              />
            </article>
            <article class="relative h-[170px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
              <div
                class="cover-bg absolute inset-0"
                role="img"
                :aria-label="tourGallery[5].alt"
                :style="coverStyle(tourGallery[5].src)"
              />
            </article>
          </div>

          <div class="grid gap-4">
            <article class="relative h-[240px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm md:h-[250px]">
              <div
                class="cover-bg absolute inset-0"
                role="img"
                :aria-label="tourGallery[2].alt"
                :style="coverStyle(tourGallery[2].src)"
              />
            </article>
            <article class="relative h-[240px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm md:h-[285px]">
              <div
                class="cover-bg absolute inset-0"
                role="img"
                :aria-label="tourGallery[6].alt"
                :style="coverStyle(tourGallery[6].src)"
              />
            </article>
          </div>
        </div>
      </div>
    </section>

    <section class="border-b border-border bg-muted/20 py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <div class="grid items-center gap-8 lg:grid-cols-[1fr_1.4fr]">
          <div>
            <h2 class="font-serif text-3xl text-primary md:text-4xl">
              Как к нам добраться
            </h2>
            <p class="mt-5 max-w-xl leading-relaxed text-muted-foreground">
              Наши квадроциклы, как и начальная точка всех маршрутов, находятся на базе отдыха «Строгановские Просторы» в Ильинском районе Пермского края. Это примерно в двух часах езды от iMall Эспланада в центре Перми.
            </p>
          </div>
          <div style="position:relative;overflow:hidden;"><a href="https://yandex.com/maps?utm_medium=mapframe&utm_source=maps" style="color:#eee;font-size:12px;position:absolute;top:0px;">Яндекс Карты</a><a href="https://yandex.com/maps/?from=mapframe&ll=55.923443%2C58.318195&mode=routes&rtext=58.011576%2C56.227308~58.614132%2C55.722128&rtt=auto&ruri=ymapsbm1%3A%2F%2Forg%3Foid%3D117771901434~ymapsbm1%3A%2F%2Forg%3Foid%3D1277179994&source=mapframe&utm_medium=mapframe&utm_source=maps&z=8" style="color:#eee;font-size:12px;position:absolute;top:14px;">Строгановские просторы: как доехать на автомобиле, общественным транспортом или пешком – Яндекс Карты</a><iframe src="https://yandex.com/map-widget/v1/?from=mapframe&ll=55.923443%2C58.318195&mode=routes&rtext=58.011576%2C56.227308~58.614132%2C55.722128&rtt=auto&ruri=ymapsbm1%3A%2F%2Forg%3Foid%3D117771901434~ymapsbm1%3A%2F%2Forg%3Foid%3D1277179994&source=mapframe&utm_source=mapframe&z=8" width="560" height="400" frameborder="1" allowfullscreen="true" style="position:relative;"></iframe></div>
        </div>
      </div>
    </section>

    <section id="request" class="scroll-mt-24 bg-background py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <div class="mx-auto max-w-3xl rounded-3xl border border-primary/20 bg-gradient-to-br from-primary/10 via-primary/5 to-transparent p-8 text-center md:p-10">
          <ShieldCheck class="mx-auto h-10 w-10 text-primary" aria-hidden="true" />
          <h2 class="mt-4 font-serif text-3xl text-primary md:text-4xl">
            Забронировать тур
          </h2>
          <p class="mt-4 leading-relaxed text-muted-foreground">
            Бронирование происходит через оператора. Позвоните нам или перейдите к маршрутам и оставьте заявку на подходящий тур.
          </p>
          <div class="mt-8 flex flex-wrap items-center justify-center gap-3">
            <a
              :href="bookingTel"
              class="inline-flex items-center justify-center rounded-full border border-primary bg-primary px-7 py-3 text-sm font-semibold uppercase tracking-wide text-primary-foreground transition-colors hover:bg-primary/90"
            >
              {{ bookingPhone }}
            </a>
            <button
              type="button"
              @click="openBookingModal('route', quadTours[0]?.id || null)"
              class="inline-flex items-center justify-center gap-2 rounded-full border border-primary/40 px-7 py-3 text-sm font-semibold uppercase tracking-wide text-primary transition-colors hover:border-primary/80 hover:bg-primary/5"
            >
              Выбрать маршрут
              <ArrowRight class="h-4 w-4" aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
    </section>

    <div
      v-if="bookingModalOpen"
      class="fixed inset-0 z-[70] flex items-center justify-center bg-black/50 px-4 py-8"
      @click.self="closeBookingModal"
    >
      <div class="flex max-h-[calc(100vh-4rem)] w-full max-w-2xl flex-col overflow-hidden rounded-3xl border border-border bg-background shadow-xl">
        <div class="flex shrink-0 items-start justify-between gap-4 border-b border-border/70 bg-background px-6 py-5 md:px-8">
          <div>
            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-primary">
              {{ bookingType === 'weekend_tour' ? 'Тур выходного дня' : 'Маршрут' }}
            </p>
            <h3 class="mt-2 font-serif text-2xl text-primary md:text-3xl">
              Бронирование
            </h3>
          </div>
          <button
            type="button"
            @click="closeBookingModal"
            class="inline-flex h-9 w-9 items-center justify-center rounded-full border border-border text-muted-foreground transition-colors hover:border-primary hover:text-primary"
            aria-label="Закрыть окно бронирования"
          >
            <X class="h-4 w-4" aria-hidden="true" />
          </button>
        </div>

        <div class="booking-modal-scroll grid gap-5 overflow-y-auto px-6 py-6 md:px-8">
          <label class="grid gap-2 text-sm">
            <span class="font-semibold text-foreground">Тип заявки</span>
            <select
              v-model="bookingType"
              class="rounded-xl border border-border bg-card px-3 py-2.5 text-foreground outline-none transition-colors focus:border-primary"
            >
              <option value="route">Маршрут</option>
              <option value="weekend_tour">Тур выходного дня</option>
            </select>
          </label>

          <label class="grid gap-2 text-sm">
            <span class="font-semibold text-foreground">Маршрут</span>
            <select
              v-model="selectedRouteId"
              class="rounded-xl border border-border bg-card px-3 py-2.5 text-foreground outline-none transition-colors focus:border-primary"
            >
              <option :value="null" disabled>Выберите маршрут</option>
              <option
                v-for="route in bookingRoutes"
                :key="route.id"
                :value="route.id"
              >
                {{ route.title }}
              </option>
            </select>
          </label>

          <div
            v-if="bookingType === 'route'"
            class="grid gap-4"
          >
            <label class="grid gap-2 text-sm">
              <span class="font-semibold text-foreground">Дата выезда</span>
              <input
                v-model="selectedRouteDate"
                type="date"
                @click="openNativeDatePicker"
                @focus="openNativeDatePicker"
                class="rounded-xl border border-border bg-card px-3 py-2.5 text-foreground outline-none transition-colors focus:border-primary"
              >
            </label>

            <div v-if="availabilityPending" class="flex items-center gap-2 text-sm text-muted-foreground">
              <LoaderCircle class="h-4 w-4 animate-spin" aria-hidden="true" />
              Проверяем доступность...
            </div>

            <div
              v-if="selectedRouteDate && routeAvailability"
              class="grid gap-4 rounded-2xl border border-border bg-card p-4"
            >
              <div v-if="availableSlots.length > 0" class="grid gap-2 text-sm">
                <span class="font-semibold text-foreground">Свободные слоты</span>
                <select
                  v-model="selectedStartTime"
                  @change="selectedJoinOuting = null"
                  class="rounded-xl border border-border bg-background px-3 py-2.5 text-foreground outline-none transition-colors focus:border-primary"
                >
                  <option value="">Выберите время</option>
                  <option
                    v-for="slot in availableSlots"
                    :key="slot"
                    :value="formatIsoTime(slot)"
                  >
                    {{ formatIsoDateTime(slot) }}
                  </option>
                </select>
              </div>

              <div v-if="availableFormingOutings.length > 0" class="grid gap-2 text-sm">
                <span class="font-semibold text-foreground">Или присоединиться к группе</span>
                <select
                  v-model="selectedJoinOuting"
                  @change="selectedStartTime = ''"
                  class="rounded-xl border border-border bg-background px-3 py-2.5 text-foreground outline-none transition-colors focus:border-primary"
                >
                  <option :value="null">Не присоединяться</option>
                  <option
                    v-for="outing in availableFormingOutings"
                    :key="outing.id"
                    :value="outing.id"
                  >
                    {{ formatIsoDateTime(outing.start_at) }} — в группе {{ outing.total_vehicles }} из {{ outing.min_vehicles }}
                  </option>
                </select>
              </div>

              <p
                v-if="availableSlots.length === 0 && availableFormingOutings.length === 0"
                class="text-sm text-muted-foreground"
              >
                На выбранную дату нет доступных слотов.
              </p>
            </div>
          </div>

          <div
            v-else
            class="grid gap-4"
          >
            <label class="grid gap-2 text-sm">
              <span class="font-semibold text-foreground">Дата заезда (пятница)</span>
              <input
                v-model="selectedCheckinDate"
                type="date"
                min="2024-01-05"
                step="7"
                @click="openNativeDatePicker"
                @focus="openNativeDatePicker"
                @change="handleWeekendDateChange"
                class="rounded-xl border border-border bg-card px-3 py-2.5 text-foreground outline-none transition-colors focus:border-primary"
              >
            </label>

            <div
              v-if="selectedCheckinDate && weekendAvailability"
              class="rounded-2xl border border-border bg-card p-4 text-sm"
            >
              <p class="text-foreground">
                Выезд:
                <span class="font-semibold">
                  {{ formatIsoDateTime(weekendAvailability.outing_start) }}
                </span>
              </p>
              <p class="mt-1 text-muted-foreground">
                Статус:
                <span class="font-semibold text-foreground">
                  {{ weekendAvailability.can_request ? 'можно отправить заявку' : 'временное ограничение по ресурсам' }}
                </span>
              </p>
            </div>
          </div>

          <div class="grid gap-4 md:grid-cols-2">
            <label class="grid gap-2 text-sm">
              <span class="font-semibold text-foreground">Квадроциклов</span>
              <input
                v-model.number="vehiclesCount"
                type="number"
                min="1"
                class="rounded-xl border border-border bg-card px-3 py-2.5 text-foreground outline-none transition-colors focus:border-primary"
              >
            </label>
            <label class="grid gap-2 text-sm">
              <span class="font-semibold text-foreground">Человек</span>
              <input
                v-model.number="peopleCount"
                type="number"
                min="1"
                class="rounded-xl border border-border bg-card px-3 py-2.5 text-foreground outline-none transition-colors focus:border-primary"
              >
            </label>
          </div>

          <div class="grid gap-4 md:grid-cols-2">
            <label class="grid gap-2 text-sm">
              <span class="font-semibold text-foreground">Имя</span>
              <input
                v-model="contactName"
                type="text"
                class="rounded-xl border border-border bg-card px-3 py-2.5 text-foreground outline-none transition-colors focus:border-primary"
              >
            </label>
            <label class="grid gap-2 text-sm">
              <span class="font-semibold text-foreground">Телефон</span>
              <input
                v-model="contactPhone"
                type="tel"
                class="rounded-xl border border-border bg-card px-3 py-2.5 text-foreground outline-none transition-colors focus:border-primary"
              >
            </label>
          </div>

          <label class="grid gap-2 text-sm">
            <span class="font-semibold text-foreground">E-mail</span>
            <input
              v-model="contactEmail"
              type="email"
              class="rounded-xl border border-border bg-card px-3 py-2.5 text-foreground outline-none transition-colors focus:border-primary"
            >
          </label>

          <label class="grid gap-2 text-sm">
            <span class="font-semibold text-foreground">Комментарий</span>
            <textarea
              v-model="comment"
              rows="3"
              class="rounded-xl border border-border bg-card px-3 py-2.5 text-foreground outline-none transition-colors focus:border-primary"
            ></textarea>
          </label>

          <div class="flex gap-3 text-left">
            <input
              id="tour-booking-consent"
              v-model="consentAccepted"
              type="checkbox"
              class="mt-0.5 h-4 w-4 shrink-0 rounded border border-input text-primary accent-primary"
            >
            <label for="tour-booking-consent" class="text-xs leading-relaxed text-muted-foreground">
              Я даю
              <NuxtLink
                href="/consent.pdf"
                target="_blank"
                rel="noopener noreferrer"
                class="text-primary underline underline-offset-2 hover:text-primary/90"
              >согласие</NuxtLink>
              на
              <a
                href="/privacy"
                target="_blank"
                rel="noopener noreferrer"
                class="text-primary underline underline-offset-2 hover:text-primary/90"
              >обработку персональных данных</a>.
            </label>
          </div>

          <p v-if="availabilityError" class="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {{ availabilityError }}
          </p>
          <p v-if="bookingSubmitError" class="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {{ bookingSubmitError }}
          </p>
          <p v-if="bookingSubmitSuccess" class="rounded-2xl border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
            {{ bookingSubmitSuccess }}
          </p>

          <div class="flex flex-wrap justify-end gap-3">
            <button
              type="button"
              @click="closeBookingModal"
              class="inline-flex items-center justify-center rounded-full border border-border px-6 py-2.5 text-sm font-semibold uppercase tracking-wide text-muted-foreground transition-colors hover:border-primary hover:text-primary"
            >
              Закрыть
            </button>
            <button
              type="button"
              :disabled="isSubmittingBooking || !consentAccepted"
              @click="submitBooking"
              class="inline-flex items-center justify-center gap-2 rounded-full border border-primary bg-primary px-6 py-2.5 text-sm font-semibold uppercase tracking-wide text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-60"
            >
              <LoaderCircle
                v-if="isSubmittingBooking"
                class="h-4 w-4 animate-spin"
                aria-hidden="true"
              />
              Отправить заявку
            </button>
          </div>
        </div>
      </div>
    </div>

    <LazyFooterSection />
  </div>
</template>

<style scoped>
.cover-bg {
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}

.booking-modal-scroll {
  scrollbar-color: rgba(16, 83, 69, 0.32) transparent;
  scrollbar-gutter: stable;
  scrollbar-width: thin;
}

.booking-modal-scroll::-webkit-scrollbar {
  width: 8px;
}

.booking-modal-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.booking-modal-scroll::-webkit-scrollbar-thumb {
  background-color: rgba(16, 83, 69, 0.28);
  border: 2px solid transparent;
  border-radius: 999px;
  background-clip: padding-box;
}

.booking-modal-scroll::-webkit-scrollbar-thumb:hover {
  background-color: rgba(16, 83, 69, 0.42);
}
</style>
