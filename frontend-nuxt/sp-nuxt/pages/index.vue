<script setup>
import FooterSection from "~/components/sections/FooterSection.vue";

const {
  isAdmin,
  adminName,
  isEditMode,
  pending: adminStatusPending,
  toggleEditMode,
} = useAdminEditMode();

const { data: siteSettings } = useSiteSettings();
const siteIsActive = computed(() => siteSettings.value?.site_active !== false);
const showNewsOnHomepage = computed(
  () => siteSettings.value?.homepage_show_news !== false,
);

const config = useRuntimeConfig();
const siteUrl = config.public.siteUrl;
const apiBase = config.public.apiBase;

useHead({
  link: [
    { rel: "preconnect", href: apiBase },
    { rel: "dns-prefetch", href: apiBase },
  ],
});

const homeTitle =
  "База отдыха в Пермском крае — коттеджи и глэмпинг у Камского моря";
const homeDescription =
  "База отдыха «Строгановские Просторы» в Пермском крае: уютные коттеджи и глэмпинг на берегу Камского моря, баня с чаном, квадротуры и активный отдых под Пермью.";

useHead({
  link: [{ rel: "canonical", href: siteUrl }],
});

useSeoMeta({
  title: homeTitle,
  description: homeDescription,
  ogTitle: "База отдыха «Строгановские Просторы» — Пермский край",
  ogDescription: homeDescription,
  ogImage: `${siteUrl}/images/hero-cottages.jpg`,
  ogUrl: siteUrl,
  ogType: "website",
  ogLocale: "ru_RU",
  twitterCard: "summary_large_image",
  twitterTitle: "База отдыха «Строгановские Просторы» — Пермский край",
  twitterDescription: homeDescription,
  twitterImage: `${siteUrl}/images/hero-cottages.jpg`,
});

useStructuredData({
  "@context": "https://schema.org",
  "@type": "Resort",
  name: "База отдыха «Строгановские Просторы»",
  description: homeDescription,
  url: siteUrl,
  image: `${siteUrl}/images/hero-cottages.jpg`,
  telephone: "+79026439294",
  email: "stroganovprostor@gmail.com",
  priceRange: "₽₽",
  address: {
    "@type": "PostalAddress",
    addressCountry: "RU",
    addressRegion: "Пермский край",
    addressLocality: "Ильинский район, п. Ильинский, с. Дмитриевское",
  },
  areaServed: ["Пермь", "Пермский край"],
  sameAs: [
    "https://yandex.ru/maps/org/stroganovskiye_prostory/1277179994/",
  ],
});

const znmsWidgetOptions = {
  moduleId: 6826,
  index: 0,
  widget: {
    zindex: 2000,
    position: {
      top: "100px",
    },
    mobile: {
      absolute: false,
      color: undefined,
      position: {
        top: "100px",
      },
    },
  },
  button: {
    position: {
      bottom: "50px",
      left: "50px",
      right: "50px",
    },
  },
};

// Виджет бронирования подтягивает тяжёлый шрифт (~240 КБ) и блокирует
// критический путь, раздувая LCP. Грузим его скрипт отложенно — после
// простоя браузера, когда первый экран уже отрисован.
const initWidgetWhenReady = () => {
  let n = 0;
  const t = setInterval(() => {
    n += 1;
    const w = typeof window !== "undefined" ? window.znmsWidget : null;
    if (w?.init) {
      clearInterval(t);
      w.init("#znms-widget-1", znmsWidgetOptions);
    } else if (n >= 300) {
      clearInterval(t);
    }
  }, 50);
};

const loadBookingWidget = () => {
  if (document.getElementById("znms-widget-script")) return;
  const s = document.createElement("script");
  s.id = "znms-widget-script";
  s.src = "https://widget.bronirui-online.ru/js/app.js";
  s.async = true;
  s.onload = initWidgetWhenReady;
  document.body.appendChild(s);
};

onMounted(() => {
  if (!siteIsActive.value) return;
  if ("requestIdleCallback" in window) {
    requestIdleCallback(loadBookingWidget, { timeout: 3000 });
  } else {
    setTimeout(loadBookingWidget, 1500);
  }
});
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <div
      v-if="isAdmin"
      class="fixed right-4 top-4 z-[60] flex items-center gap-2 rounded-full border border-primary/20 bg-background/95 p-1 shadow-lg backdrop-blur"
    >
      <span class="px-2 text-xs text-muted-foreground">
        {{ adminName ? `Админ: ${adminName}` : "Админ" }}
      </span>
      <button
        class="rounded-full px-3 py-2 text-xs font-semibold transition-colors"
        :class="
          isEditMode
            ? 'bg-primary text-primary-foreground'
            : 'bg-muted text-foreground hover:bg-muted/80'
        "
        :disabled="adminStatusPending"
        @click="toggleEditMode"
      >
        {{
          isEditMode
            ? "Режим редактирования: ВКЛ"
            : "Режим редактирования: ВЫКЛ"
        }}
      </button>
    </div>

    <!-- Критичные компоненты для первого рендера - загружаются сразу -->
    <HeroSection :edit-mode="isEditMode" :hide-navigation="!siteIsActive" />

    <div v-if="siteIsActive" id="znms-widget-1" />

    <template v-if="siteIsActive">
      <ClientOnly>
        <GalleryStatsSection :edit-mode="isEditMode" />
        <template #fallback>
          <div
            class="min-h-[min(85vh,960px)] bg-[hsl(36_18%_91%)]"
            aria-hidden="true"
          />
        </template>
      </ClientOnly>

      <ClientOnly>
        <LazyLodgeSection />
        <LazyPeacefulRestSection />
        <LazyActiveRestSection />
        <LazyEventsSection />
        <LazyRestaurantSection />
        <LazyNewsSection v-if="showNewsOnHomepage" />
        <LazyGuestReviewsSection />
        <template #fallback>
          <div
            class="min-h-[min(200vh,3000px)] bg-background"
            aria-hidden="true"
          />
        </template>
      </ClientOnly>
    </template>

    <SiteMaintenanceSection v-else />

    <ClientOnly>
      <ScrollToTopButton />
    </ClientOnly>

    <FooterSection />
  </div>
</template>
