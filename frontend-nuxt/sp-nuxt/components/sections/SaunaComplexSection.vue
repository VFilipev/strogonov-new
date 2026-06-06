<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import PhotoViewer from "~/components/lodge/PhotoViewer.vue";

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  highlights: {
    type: Array,
    default: () => [],
  },
  images: {
    type: Array,
    default: () => [],
  },
  reverse: {
    type: Boolean,
    default: false,
  },
});

const isVisible = ref(false);
const activeIndex = ref(0);
const galleryOpen = ref(false);
const viewerInitialIndex = ref(0);
const sectionRef = ref(null);
const containerRef = ref(null);

let sectionObserver = null;

const validImages = computed(() =>
  Array.isArray(props.images) && props.images.length ? props.images : []
);

const coverStyle = (src) =>
  src ? { backgroundImage: `url("${String(src)}")` } : {};

const handleMouseMove = (event) => {
  if (!containerRef.value || validImages.value.length <= 1) return;

  const rect = containerRef.value.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const sectionWidth = rect.width / validImages.value.length;
  const nextIndex = Math.min(
    Math.floor(x / sectionWidth),
    validImages.value.length - 1
  );

  if (nextIndex !== activeIndex.value) {
    activeIndex.value = nextIndex;
  }
};

const handleMouseLeave = () => {
  activeIndex.value = 0;
};

function openGallery() {
  if (!validImages.value.length) return;
  viewerInitialIndex.value = activeIndex.value;
  galleryOpen.value = true;
}

function closeGallery() {
  galleryOpen.value = false;
}

onMounted(() => {
  let revealRaf = null;
  sectionObserver = new IntersectionObserver(
    ([entry]) => {
      if (!entry.isIntersecting) return;
      if (revealRaf != null) return;
      revealRaf = requestAnimationFrame(() => {
        revealRaf = null;
        isVisible.value = true;
      });
    },
    { threshold: 0.1, rootMargin: "0px 0px -5%" }
  );

  if (sectionRef.value) {
    sectionObserver.observe(sectionRef.value);
  }
});

onBeforeUnmount(() => {
  if (sectionObserver) {
    sectionObserver.disconnect();
    sectionObserver = null;
  }
});
</script>

<template>
  <section ref="sectionRef" class="py-12 md:py-16">
    <div
      class="grid items-center gap-8 transition-[opacity,transform] duration-700 lg:grid-cols-2 lg:gap-12"
      :class="[
        reverse ? 'lg:[&>*:first-child]:order-2 lg:[&>*:last-child]:order-1' : '',
        isVisible ? 'opacity-100' : 'opacity-0',
      ]"
    >
      <div class="relative overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
        <div class="gallery-aspect">
          <div
            ref="containerRef"
            class="gallery-frame cursor-pointer"
            role="button"
            tabindex="0"
            @mousemove="handleMouseMove"
            @mouseleave="handleMouseLeave"
            @click="openGallery"
            @keydown.enter.prevent="openGallery"
            @keydown.space.prevent="openGallery"
          >
            <div
              v-for="(img, index) in validImages"
              :key="`${title}-${index}`"
              class="gallery-cover absolute inset-0 transition-opacity duration-300"
              :class="index === activeIndex ? 'opacity-100' : 'opacity-0'"
              role="img"
              :aria-label="`${title} ${index + 1}`"
              :style="coverStyle(img)"
            />
            <div
              v-if="validImages.length > 1"
              class="absolute bottom-3 left-1/2 flex -translate-x-1/2 gap-1.5"
              @click.stop
            >
              <button
                v-for="(_, index) in validImages"
                :key="`dot-${title}-${index}`"
                type="button"
                class="h-1 rounded-full transition-all duration-300"
                :class="index === activeIndex ? 'w-4 bg-white' : 'w-1.5 bg-white/50'"
                :aria-label="`Показать фото ${index + 1}`"
                @click="activeIndex = index"
              />
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div>
          <h2 class="font-serif text-3xl text-primary md:text-4xl">
            {{ title }}
          </h2>
          <p class="mt-4 text-lg leading-relaxed text-foreground/80">
            {{ description }}
          </p>
        </div>

        <ul class="space-y-3">
          <li
            v-for="(item, index) in highlights"
            :key="`${title}-${index}`"
            class="flex items-start gap-3"
          >
            <span class="mt-2.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" />
            <span class="text-foreground/70">{{ item }}</span>
          </li>
        </ul>
      </div>
    </div>

    <PhotoViewer
      :open="galleryOpen"
      :images="validImages"
      :initial-index="viewerInitialIndex"
      @close="closeGallery"
    />
  </section>
</template>

<style scoped>
.gallery-aspect {
  position: relative;
  width: 100%;
}

.gallery-aspect::before {
  content: "";
  display: block;
  padding-top: 75%;
}

.gallery-frame {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.gallery-cover {
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
</style>
