<script setup>
const STORAGE_KEY = "sp-personal-data-consent";
const UNLOCK_SESSION_KEY = "sp-personal-data-banner-unlocked";

const route = useRoute();

const consentKnown = ref(false);
const hasConsent = ref(false);
const bannerUnlocked = ref(false);

let removeScroll = null;
let removeResize = null;

function readStorage() {
  if (typeof window === "undefined") return;
  hasConsent.value = window.localStorage.getItem(STORAGE_KEY) === "1";
  consentKnown.value = true;
}

function readUnlockSession() {
  if (typeof window === "undefined") return;
  bannerUnlocked.value =
    window.sessionStorage.getItem(UNLOCK_SESSION_KEY) === "1";
}

function tryUnlockFromHomeScroll() {
  if (typeof window === "undefined") return;
  if (route.path !== "/") return;
  if (window.scrollY <= window.innerHeight) return;
  if (bannerUnlocked.value) return;
  bannerUnlocked.value = true;
  window.sessionStorage.setItem(UNLOCK_SESSION_KEY, "1");
}

function accept() {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(STORAGE_KEY, "1");
  window.sessionStorage.removeItem(UNLOCK_SESSION_KEY);
  hasConsent.value = true;
}

onMounted(() => {
  readStorage();
  readUnlockSession();
  if (hasConsent.value) return;
  tryUnlockFromHomeScroll();
  const onScroll = () => tryUnlockFromHomeScroll();
  const onResize = () => tryUnlockFromHomeScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onResize, { passive: true });
  removeScroll = () => window.removeEventListener("scroll", onScroll);
  removeResize = () => window.removeEventListener("resize", onResize);
});

watch(
  () => route.path,
  () => {
    tryUnlockFromHomeScroll();
  },
);

onBeforeUnmount(() => {
  removeScroll?.();
  removeResize?.();
});

const isVisible = computed(
  () => consentKnown.value && !hasConsent.value && bannerUnlocked.value,
);
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="translate-y-full opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="translate-y-full opacity-0"
    >
      <div
        v-if="isVisible"
        class="pointer-events-none fixed inset-x-0 bottom-0 z-[1880] flex justify-center px-4 pb-5 pt-2 sm:px-6"
        role="dialog"
        aria-labelledby="privacy-consent-title"
        aria-describedby="privacy-consent-desc"
      >
        <div
          class="pointer-events-auto flex max-w-5xl flex-col gap-4 rounded-2xl border border-border bg-card/95 px-5 py-4 shadow-lg backdrop-blur-sm sm:flex-row sm:items-center sm:gap-6 sm:py-5 sm:pl-6 sm:pr-5 lg:mr-24"
        >
          <p
            id="privacy-consent-desc"
            class="text-sm font-sans leading-relaxed text-foreground sm:flex-1 sm:text-base"
          >
            <span id="privacy-consent-title" class="sr-only">
              Согласие на использование cookie
            </span>
            Для обеспечения удобства пользователей и анализа трафика наш сайт
            использует файлы cookie. Продолжая просмотр, вы соглашаетесь с их
            использованием. Подробнее — в
            <NuxtLink
              to="/privacy"
              target="_blank"
              rel="noopener noreferrer"
              class="font-medium text-secondary underline decoration-secondary/40 underline-offset-2 transition-colors hover:text-secondary/80"
            >
              Политике обработки персональных данных
            </NuxtLink>
            .
          </p>
          <button
            type="button"
            class="shrink-0 self-stretch rounded-xl border border-border bg-transparent px-6 py-3 font-sans text-sm font-semibold text-secondary transition-colors hover:bg-muted/50 sm:self-center sm:py-2.5"
            @click="accept"
          >
            Согласен
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
