<script setup>
import PhotoViewer from "~/components/lodge/PhotoViewer.vue";
import { restaurantMenuImages } from "~/utils/restaurantMenuImages";

definePageMeta({
  ssr: false,
});

const route = useRoute();
const menuOpen = ref(true);

const initialSlide = computed(() => {
  const raw = route.query.slide;
  if (raw === undefined || raw === null || raw === "") return 0;
  const n = Number(Array.isArray(raw) ? raw[0] : raw);
  if (!Number.isFinite(n)) return 0;
  const i = Math.floor(n);
  if (i < 0 || i >= restaurantMenuImages.length) return 0;
  return i;
});

function onClose() {
  navigateTo("/");
}

useHead({
  title: "Меню ресторана",
  meta: [
    {
      name: "description",
      content: "Меню ресторана базы отдыха Строгановские Просторы.",
    },
  ],
});
</script>

<template>
  <PhotoViewer
    :open="menuOpen"
    :images="restaurantMenuImages"
    :initial-index="initialSlide"
    @close="onClose"
  />
</template>
