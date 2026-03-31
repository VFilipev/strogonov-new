<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { ChevronDown, Menu, Phone, X } from "lucide-vue-next";
import logo from "~/assets/resort/logo.webp";
import nac from "~/assets/resort/nac.webp";
import heroImage from "~/assets/resort/preview.webp";

const props = defineProps({
  title: {
    type: String,
    default: "Снегоходные маршруты",
  },
  intro: {
    type: String,
    default: "",
  },
});

const { showServicesNav, showToursNav } = useNavVisibility();

const parallaxLayerRef = ref(null);
const parallaxEnabled = ref(false);
const mobileMenuOpen = ref(false);

const applyParallaxTransform = () => {
  const el = parallaxLayerRef.value;
  if (!el) return;
  if (!parallaxEnabled.value) {
    el.style.transform = "translate3d(0, 0, 0) scale(1.05)";
    el.style.willChange = "auto";
    return;
  }
  const y = window.scrollY * 0.5;
  el.style.transform = `translate3d(0, ${y}px, 0) scale(1.1)`;
  el.style.willChange = "transform";
};

let parallaxRafId = null;
const handleScroll = () => {
  if (!parallaxEnabled.value) return;
  if (parallaxRafId != null) return;
  parallaxRafId = requestAnimationFrame(() => {
    parallaxRafId = null;
    applyParallaxTransform();
  });
};

const closeMobileMenu = () => {
  mobileMenuOpen.value = false;
};

const scrollToContentBelow = () => {
  if (!import.meta.client) return;
  const viewportHeight = window.innerHeight || 0;
  const targetTop = Math.max(viewportHeight - 80, 0);
  window.scrollTo({
    top: targetTop,
    behavior: "smooth",
  });
};

watch(mobileMenuOpen, (isOpen) => {
  if (!import.meta.client) return;
  document.body.style.overflow = isOpen ? "hidden" : "";
});

const handleWindowKeydown = (event) => {
  if (event.key === "Escape") {
    closeMobileMenu();
  }
};

onMounted(async () => {
  if (!import.meta.client) return;

  const prefersReducedMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
  const isDesktop = window.matchMedia?.("(min-width: 768px)").matches;

  parallaxEnabled.value = !prefersReducedMotion && isDesktop;

  await nextTick();
  if (parallaxEnabled.value) {
    window.addEventListener("scroll", handleScroll, { passive: true });
  }
  applyParallaxTransform();
  window.addEventListener("keydown", handleWindowKeydown);
});

onBeforeUnmount(() => {
  closeMobileMenu();
  if (import.meta.client) {
    document.body.style.overflow = "";
    window.removeEventListener("keydown", handleWindowKeydown);
    if (parallaxRafId != null) {
      cancelAnimationFrame(parallaxRafId);
      parallaxRafId = null;
    }
  }
  if (parallaxEnabled.value && import.meta.client) {
    window.removeEventListener("scroll", handleScroll);
  }
});
</script>

<template>
  <section
    class="relative flex min-h-screen items-center justify-center overflow-hidden"
  >
    <div class="absolute inset-0 z-0 overflow-hidden">
      <div
        ref="parallaxLayerRef"
        class="absolute inset-0 [backface-visibility:hidden]"
      >
        <NuxtImg
          :src="heroImage"
          alt="Снегоход на зимнем маршруте, Строгановские Просторы"
          width="1410"
          height="940"
          :quality="80"
          class="h-full w-full object-cover [backface-visibility:hidden]"
          loading="eager"
          decoding="async"
          fetchpriority="high"
          sizes="100vw"
          format="webp"
        />
      </div>
      <div
        class="absolute inset-0 bg-gradient-to-b from-primary/75 via-primary/55 to-primary/75"
      />
    </div>

    <nav class="animate-fade-in absolute left-0 right-0 top-0 z-20 p-4 md:p-8">
      <div class="container mx-auto flex items-center justify-between">
        <div class="flex items-center gap-4 md:gap-8">
          <div class="flex items-center">
            <NuxtLink to="/" class="inline-flex items-center">
              <NuxtImg
                :src="logo"
                alt="Строгановские Просторы"
                class="h-10 transition-transform duration-300 hover:scale-105 md:h-16"
                fetchpriority="high"
                decoding="async"
                sizes="140px"
              />
            </NuxtLink>
            <div class="mx-[0.6rem] h-16 w-px bg-white md:mx-[0.8rem] md:h-24" />
            <NuxtImg
              :src="nac"
              fetchpriority="high"
              alt="национальные проекты"
              class="h-16 md:h-24"
              decoding="async"
              sizes="150px"
            />
          </div>
          <div class="hidden items-center gap-8 md:flex">
            <NuxtLink
              class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
              to="/complain"
              >ваше мнение</NuxtLink
            >
            <a
              class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
              href="/lodge"
              >дома</a
            >
            <NuxtLink
              v-if="showToursNav"
              class="font-semibold text-primary-foreground underline decoration-primary-foreground/50 underline-offset-4"
              to="/tours"
              >туры</NuxtLink
            >
            <a
              v-if="showServicesNav"
              class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
              href="/#active"
              >услуги</a
            >
            <a
              class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
              href="/event-calculator"
              >афиша и мероприятия</a
            >
          </div>
        </div>
        <div class="hidden items-center gap-4 md:flex">
          <a
            href="tel:+73422333332"
            class="transition-transform duration-300 text-primary-foreground hover:scale-110 hover:text-primary-foreground/80"
          >
            <Phone class="h-5 w-5" />
          </a>
          <a
            href="#request"
            class="rounded-full border border-primary-foreground bg-transparent px-6 py-2 text-sm font-semibold uppercase tracking-wide text-primary-foreground transition-all duration-300 hover:scale-105 hover:bg-primary-foreground hover:text-primary"
          >
            забронировать
          </a>
        </div>
        <div class="flex items-center gap-2 md:hidden">
          <button
            class="flex h-10 w-10 items-center justify-center rounded-full border border-primary-foreground/70 bg-black/20 text-primary-foreground backdrop-blur-sm transition-colors hover:bg-primary-foreground/15"
            :aria-label="mobileMenuOpen ? 'Закрыть меню' : 'Открыть меню'"
            :aria-expanded="mobileMenuOpen"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <X v-if="mobileMenuOpen" class="h-5 w-5" />
            <Menu v-else class="h-5 w-5" />
          </button>
        </div>
      </div>
      <div
        v-if="mobileMenuOpen"
        class="mt-3 ml-auto w-full max-w-[360px] rounded-2xl border border-white/20 bg-primary/85 p-4 shadow-xl backdrop-blur-md md:hidden"
      >
        <div class="flex flex-col gap-3 text-primary-foreground">
          <NuxtLink
            class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
            to="/complain"
            @click="closeMobileMenu"
            >ваше мнение</NuxtLink
          >
          <a
            class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
            href="/lodge"
            @click="closeMobileMenu"
            >дома</a
          >
          <NuxtLink
            v-if="showToursNav"
            class="font-semibold"
            to="/tours"
            @click="closeMobileMenu"
            >туры</NuxtLink
          >
          <a
            v-if="showServicesNav"
            class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
            href="/#active"
            @click="closeMobileMenu"
            >услуги</a
          >
          <a
            class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
            href="/event-calculator"
            @click="closeMobileMenu"
            >мероприятия</a
          >
          <a
            href="tel:+73422333332"
            class="mt-2 inline-flex w-fit items-center gap-2 transition-transform duration-300 text-primary-foreground hover:scale-105 hover:text-primary-foreground/80"
            @click="closeMobileMenu"
          >
            <Phone class="h-5 w-5" />
            <span>+7 (342) 2-33-33-32</span>
          </a>
        </div>
      </div>
    </nav>

    <div class="absolute bottom-0 left-0 right-0 z-10 pb-12 md:pb-16">
      <div class="container mx-auto px-6 md:px-8">
        <div class="grid items-end gap-8 md:grid-cols-2">
          <div
            class="animate-fade-in"
            style="
              animation-delay: 0.3s;
              opacity: 0;
              animation-fill-mode: forwards;
            "
          >
            <h1
              class="text-2xl font-light leading-relaxed text-primary-foreground md:text-3xl lg:text-4xl"
            >
              {{ title }}
            </h1>
          </div>

          <div
            class="animate-slide-in-right rounded-2xl border border-primary-foreground/20 bg-primary-foreground/10 p-6 backdrop-blur-md transition-all duration-500 hover:bg-primary-foreground/15 md:p-8"
            style="
              animation-delay: 0.6s;
              opacity: 0;
              animation-fill-mode: forwards;
            "
          >
            <p class="text-base leading-relaxed text-primary-foreground md:text-lg">
              {{ intro }}
            </p>
          </div>
        </div>
        <div class="mt-6 flex justify-center md:hidden">
          <a
            href="#request"
            class="rounded-full border border-primary-foreground bg-primary-foreground/10 px-8 py-3 text-sm font-semibold uppercase tracking-wide text-primary-foreground backdrop-blur-sm transition-all duration-300 hover:bg-primary-foreground hover:text-primary"
          >
            забронировать
          </a>
        </div>
        <div class="mt-6 flex justify-center md:mt-8">
          <button
            type="button"
            class="group flex flex-col items-center rounded-full border border-primary-foreground/20 bg-primary-foreground/5 p-2 text-primary-foreground/85 shadow-sm backdrop-blur-sm transition-all duration-300 hover:border-primary-foreground/35 hover:bg-primary-foreground/12 hover:text-primary-foreground focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-foreground/80 motion-safe:animate-hero-scroll-hint"
            aria-label="Прокрутить к контенту ниже"
            @click="scrollToContentBelow"
          >
            <ChevronDown
              class="h-6 w-6 transition-transform duration-300 group-hover:translate-y-0.5 md:h-7 md:w-7"
              aria-hidden="true"
              stroke-width="2"
            />
          </button>
        </div>
      </div>
    </div>
  </section>
</template>
