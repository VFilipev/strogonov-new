<script setup>
const visible = ref(false);

function updateVisible() {
  if (typeof window === "undefined") return;
  visible.value = window.scrollY >= window.innerHeight * 2;
}

function scrollToTop() {
  if (typeof window === "undefined") return;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

onMounted(() => {
  updateVisible();
  window.addEventListener("scroll", updateVisible, { passive: true });
  window.addEventListener("resize", updateVisible, { passive: true });
});

onBeforeUnmount(() => {
  if (typeof window === "undefined") return;
  window.removeEventListener("scroll", updateVisible);
  window.removeEventListener("resize", updateVisible);
});
</script>

<template>
  <button
    type="button"
    class="fixed bottom-[134px] right-[50px] z-[1900] mr-[11px] hidden h-12 w-12 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-lg outline-none transition-opacity duration-300 ease-out hover:bg-primary/90 focus:outline-none focus:ring-0 focus:ring-offset-0 focus-visible:outline-none focus-visible:ring-0 lg:flex"
    :class="visible ? 'pointer-events-auto opacity-100' : 'pointer-events-none opacity-0'"
    aria-label="Прокрутить страницу в начало"
    @click="scrollToTop"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      aria-hidden="true"
    >
      <path d="m18 15-6-6-6 6" />
    </svg>
  </button>
</template>
