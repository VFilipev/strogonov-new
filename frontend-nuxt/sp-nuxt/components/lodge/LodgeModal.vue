<script setup>
import { ChevronDown } from "lucide-vue-next";
import { computed, onBeforeUnmount, ref, watch } from "vue";
import { useRouter } from "vue-router";
import ImageCarousel from "./ImageCarousel.vue";

const props = defineProps({
  open: { type: Boolean, default: false },
  isClosing: { type: Boolean, default: false },
  showContent: { type: Boolean, default: false },
  meta: {
    type: Object,
    default: () => ({}),
  },
  items: {
    type: Array,
    default: () => [],
  },
  categories: {
    type: Array,
    default: () => [],
  },
  loadingItems: { type: Boolean, default: false },
});

const emit = defineEmits(["close", "category-change"]);

const router = useRouter();
const selectedCategory = ref(null);
const selectedCapacity = ref("all");
const categorySelect = ref(null);
const capacitySelect = ref(null);

const copyToastVisible = ref(false);
const copyToastHideTimer = ref(null);

const LONG_PRESS_MS = 550;
let longPressConsumed = false;

const pressTrack = ref({ item: null, start: 0, ptrId: null });

const resetPressTrack = () => {
  pressTrack.value = { item: null, start: 0, ptrId: null };
};

const getHouseRouteLocation = (item) => {
  if (item.id && item.houseType) {
    return {
      path: "/doma",
      query: {
        houseId: item.id,
        houseType: item.houseType,
      },
    };
  }
  if (item.slug) {
    return `/doma/${item.slug}`;
  }
  return { path: "/doma" };
};

const buildHouseShareUrl = (item) => {
  const loc = getHouseRouteLocation(item);
  const resolved = router.resolve(loc);
  return `${window.location.origin}${resolved.fullPath}`;
};

const showCopyToast = () => {
  if (copyToastHideTimer.value) {
    clearTimeout(copyToastHideTimer.value);
    copyToastHideTimer.value = null;
  }
  copyToastVisible.value = true;
  copyToastHideTimer.value = window.setTimeout(() => {
    copyToastVisible.value = false;
    copyToastHideTimer.value = null;
  }, 2600);
};

const copyTextToClipboardSync = (text) => {
  try {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    ta.style.top = "0";
    ta.style.fontSize = "16px";
    document.body.appendChild(ta);
    ta.focus({ preventScroll: true });
    ta.select();
    try {
      ta.setSelectionRange(0, text.length);
    } catch {
    }
    const ok = document.execCommand("copy");
    document.body.removeChild(ta);
    return ok;
  } catch {
    return false;
  }
};

const tryCopyHouseAfterLongPress = (item) => {
  const url = buildHouseShareUrl(item);
  if (navigator.clipboard?.writeText) {
    navigator.clipboard
      .writeText(url)
      .then(() => {
        showCopyToast();
      })
      .catch(() => {
        const ok = copyTextToClipboardSync(url);
        if (ok) {
          showCopyToast();
        } else {
          longPressConsumed = false;
        }
      });
    return;
  }
  const ok = copyTextToClipboardSync(url);
  if (ok) {
    showCopyToast();
  } else {
    longPressConsumed = false;
  }
};

const onHouseCardPointerDown = (item, e) => {
  if (!import.meta.client) return;
  if (e.button != null && e.button !== 0) return;
  longPressConsumed = false;
  pressTrack.value = { item, start: Date.now(), ptrId: e.pointerId };
  const el = e.currentTarget;
  if (el?.setPointerCapture) {
    try {
      el.setPointerCapture(e.pointerId);
    } catch {
    }
  }
};

const onHouseCardPointerEnd = (e) => {
  const { item, start, ptrId } = pressTrack.value;
  const elapsed = Date.now() - start;
  resetPressTrack();
  elReleasePointerSafe(e);
  if (!item || ptrId !== e.pointerId) return;
  if (elapsed < LONG_PRESS_MS) return;
  longPressConsumed = true;
  tryCopyHouseAfterLongPress(item);
};

const elReleasePointerSafe = (e) => {
  const el = e.currentTarget;
  if (!el?.releasePointerCapture) return;
  try {
    if (typeof el.hasPointerCapture !== "function" || el.hasPointerCapture(e.pointerId)) {
      el.releasePointerCapture(e.pointerId);
    }
  } catch {
  }
};

const onHouseCardPointerCancel = (e) => {
  resetPressTrack();
  elReleasePointerSafe(e);
};

const onHouseCardClickCapture = (e) => {
  if (!longPressConsumed) return;
  e.preventDefault();
  e.stopPropagation();
  queueMicrotask(() => {
    longPressConsumed = false;
  });
};

onBeforeUnmount(() => {
  if (copyToastHideTimer.value) {
    clearTimeout(copyToastHideTimer.value);
  }
});

const formatPrice = (value) =>
  Number(value || 0).toLocaleString("ru-RU");

const formatHouseQuantity = (value) => {
  const count = Number(value || 0);
  if (!count) return "";
  const mod10 = count % 10;
  const mod100 = count % 100;
  if (mod10 === 1 && mod100 !== 11) return `${count} дом`;
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return `${count} дома`;
  return `${count} домов`;
};

const isModularModal = computed(() => {
  const title = String(props.meta?.title || "").toLowerCase();
  return title.includes("модуль");
});

const categoryCards = computed(() => {
  if (!isModularModal.value || !props.categories.length) return [];

  return props.categories.map((c, index) => {
    const capacity = Number(c.capacity_max ?? 0);
    const priceFrom = Number(c.price_from_min ?? 0);
    const slug = c.slug ? String(c.slug) : String(c.id ?? index);
    return {
      id: slug,
      title: c.name,
      description: c.description || "",
      image: c.image_url || null,
      capacityLabel: capacity > 0 ? `до ${capacity} чел` : "до 0 чел",
      priceLabel: `от ₽ ${formatPrice(priceFrom)}`,
    };
  });
});

const showCategoryStep = computed(
  () =>
    isModularModal.value &&
    !selectedCategory.value &&
    (props.categories.length > 0 || props.loadingItems),
);

const selectedCategoryValue = computed({
  get: () => selectedCategory.value || categoryCards.value[0]?.id || "",
  set: (value) => {
    selectedCategory.value = value;
  },
});

const usesServerCategories = computed(
  () => isModularModal.value && props.categories.length > 0,
);

const filteredItems = computed(() => {
  if (!isModularModal.value || selectedCapacity.value === "all") {
    return props.items;
  }

  const need = Number(selectedCapacity.value);
  if (!need) {
    return props.items;
  }

  const list = props.items.filter(
    (item) => Number(item.capacityNum || 0) >= need,
  );

  return [...list].sort((a, b) => {
    const ca = Number(a.capacityNum || 0);
    const cb = Number(b.capacityNum || 0);
    const tierA = ca === need ? 0 : 1;
    const tierB = cb === need ? 0 : 1;
    if (tierA !== tierB) return tierA - tierB;
    return ca - cb;
  });
});

const lodgeCategoryCoverStyle = (src) =>
  src ? { backgroundImage: `url("${String(src)}")` } : {};

const handleClose = () => emit("close");

const handleCategorySelect = (categoryId) => {
  selectedCategory.value = categoryId;
};

const openSelect = (select) => {
  if (!select) return;
  if (typeof select.focus === "function") {
    select.focus();
  }
  if (typeof select.showPicker === "function") {
    select.showPicker();
  }
};

const handleDetailsClick = (item) => {
  router.push(getHouseRouteLocation(item));
};

watch(
  () => props.open,
  (isOpen) => {
    if (!isOpen) {
      selectedCategory.value = null;
      selectedCapacity.value = "all";
    }
  },
);

watch(selectedCategory, (val) => {
  if (!val || !usesServerCategories.value) return;
  emit("category-change", val);
});
</script>

<template>
  <Teleport to="body">
    <div v-if="open">
      <div
        class="fixed inset-0 z-40 bg-black/70 transition-opacity duration-700"
        :class="showContent && !isClosing ? 'opacity-100' : 'opacity-0'"
        @click="handleClose"
      />

      <div
        class="fixed z-50 overflow-hidden rounded-2xl bg-background shadow-2xl"
        :class="[
          isClosing ? 'lodge-popup-collapsing' : showContent ? 'lodge-popup-expanded' : 'lodge-popup-expanding',
        ]"
      >
        <div v-if="!showContent || isClosing" class="absolute inset-0">
          <NuxtImg
            :src="meta.heroImage"
            :alt="meta.title"
            :width="1410"
            :height="940"
            :quality="80"
            loading="eager"
            sizes="1410px"
            class="h-full w-full object-cover"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
          <div class="absolute inset-0 flex flex-col justify-end p-8">
            <h3 class="mb-3 text-3xl font-serif text-white md:text-4xl">
              {{ meta.title }}
            </h3>
            <p class="text-lg text-white/90">
              {{ meta.subtitle }}
            </p>
          </div>
        </div>
        <div v-else class="absolute inset-0 bg-background" />

        <div v-if="showContent && !isClosing" class="relative flex h-full min-h-0 w-full flex-col">
          <div class="flex shrink-0 items-center justify-between gap-3 border-b border-border/50 bg-background/95 p-4 backdrop-blur">
            <div class="flex items-center gap-3">
              <h3 class="text-2xl font-serif text-primary md:text-3xl">
                {{ meta.title }}
              </h3>
            </div>
            <button class="rounded-full p-2 transition-colors hover:bg-secondary/80" @click="handleClose">
              <span class="sr-only">Закрыть</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 6l12 12M18 6L6 18" />
              </svg>
            </button>
          </div>

          <div
            class="min-h-0 flex-1"
            :class="
              showCategoryStep ? 'flex min-h-0 flex-col overflow-hidden' : 'overflow-y-auto overscroll-contain'
            "
          >
            <div
              v-if="showCategoryStep && loadingItems && !categoryCards.length"
              class="flex min-h-[40vh] flex-1 items-center justify-center p-8 md:min-h-0"
            >
              <span class="text-sm font-medium text-muted-foreground">Загрузка...</span>
            </div>
            <div
              v-else-if="showCategoryStep"
              class="flex min-h-0 flex-1 flex-col gap-3 p-3 md:gap-3 md:p-4"
            >
              <div
                class="grid min-h-0 flex-1 grid-cols-1 grid-rows-4 gap-3 md:grid-cols-2 md:grid-rows-2 md:gap-3"
              >
              <article
                v-for="card in categoryCards"
                :key="card.id"
                class="group relative flex min-h-0 min-w-0 cursor-pointer flex-col overflow-hidden rounded-2xl"
                @click="handleCategorySelect(card.id)"
              >
                <div
                  v-if="card.image"
                  class="relative min-h-0 w-full flex-1 overflow-hidden"
                >
                  <div
                    class="lodge-category-cover absolute inset-0 transition-transform duration-700 group-hover:scale-105"
                    aria-hidden="true"
                    :style="lodgeCategoryCoverStyle(card.image)"
                  />
                </div>
                <div
                  v-else
                  class="relative min-h-0 w-full flex-1 bg-gradient-to-br from-secondary to-secondary/60 transition-opacity duration-700 group-hover:opacity-90"
                />
                <div class="pointer-events-none absolute inset-0 flex flex-col justify-end bg-gradient-to-t from-black/80 via-black/35 to-transparent p-4 md:p-5">
                  <h4 class="mb-1 line-clamp-2 text-xl font-serif text-white md:mb-1.5 md:text-3xl">{{ card.title }}</h4>
                  <p class="line-clamp-2 text-xs leading-snug text-white/90 md:text-sm">{{ card.description }}</p>
                  <div class="mt-2 flex flex-wrap items-center gap-2 text-xs text-white/95 md:mt-2.5 md:text-sm">
                    <span class="rounded-full bg-black/30 px-3 py-1">{{ card.capacityLabel }}</span>
                    <span class="rounded-full bg-black/30 px-3 py-1">{{ card.priceLabel }}</span>
                  </div>
                </div>
              </article>
              </div>
            </div>

            <div v-else class="relative px-6 pb-6 pt-3">
              <div
                v-if="loadingItems"
                class="absolute inset-0 z-10 flex items-start justify-center rounded-2xl bg-background/70 pt-24 backdrop-blur-sm"
              >
                <span class="text-sm font-medium text-muted-foreground">Загрузка...</span>
              </div>
              <div v-if="isModularModal" class="mb-4 grid gap-2.5 md:grid-cols-2">
                <div
                  v-if="categoryCards.length"
                  class="flex items-center justify-between gap-4 rounded-xl border border-border/40 bg-muted/20 px-3 py-2 transition-[border-color,background-color,box-shadow] hover:border-border/55 hover:bg-muted/30 focus-within:border-primary/30 focus-within:ring-1 focus-within:ring-primary/15 md:gap-5"
                >
                  <label
                    for="lodge-modal-category-filter"
                    class="cursor-pointer shrink-0 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
                    @click.prevent="openSelect(categorySelect)"
                  >
                    Категория
                  </label>
                  <div class="relative max-w-[min(210px,calc(100%-7rem))] flex-1">
                    <select
                      id="lodge-modal-category-filter"
                      ref="categorySelect"
                      v-model="selectedCategoryValue"
                      class="h-10 w-full cursor-pointer appearance-none rounded-md border border-transparent bg-transparent py-2 pl-2 pr-10 text-right text-sm text-foreground transition-colors hover:text-primary focus-visible:border-transparent focus-visible:outline-none focus-visible:ring-0"
                    >
                      <option v-for="card in categoryCards" :key="card.id" :value="card.id">
                        {{ card.title }}
                      </option>
                    </select>
                    <ChevronDown
                      class="pointer-events-none absolute right-1.5 top-1/2 h-4 w-4 shrink-0 -translate-y-1/2 opacity-55"
                      aria-hidden="true"
                      stroke-width="1.75"
                    />
                  </div>
                </div>

                <div
                  class="flex items-center justify-between gap-4 rounded-xl border border-border/40 bg-muted/20 px-3 py-2 transition-[border-color,background-color,box-shadow] hover:border-border/55 hover:bg-muted/30 focus-within:border-primary/30 focus-within:ring-1 focus-within:ring-primary/15 md:gap-5"
                >
                  <label
                    for="lodge-modal-capacity-filter"
                    class="cursor-pointer text-sm font-medium leading-snug text-muted-foreground transition-colors hover:text-foreground"
                    @click.prevent="openSelect(capacitySelect)"
                  >
                    Количество проживающих
                  </label>
                  <div class="relative max-w-[min(210px,calc(100%-11rem))] flex-1 shrink-0">
                    <select
                      id="lodge-modal-capacity-filter"
                      ref="capacitySelect"
                      v-model="selectedCapacity"
                      class="h-10 w-full cursor-pointer appearance-none rounded-md border border-transparent bg-transparent py-2 pl-2 pr-10 text-right text-sm text-foreground transition-colors hover:text-primary focus-visible:border-transparent focus-visible:outline-none focus-visible:ring-0"
                    >
                      <option value="all">Любое количество</option>
                      <option value="2">до 2 чел</option>
                      <option value="4">до 4 чел</option>
                    </select>
                    <ChevronDown
                      class="pointer-events-none absolute right-1.5 top-1/2 h-4 w-4 shrink-0 -translate-y-1/2 opacity-55"
                      aria-hidden="true"
                      stroke-width="1.75"
                    />
                  </div>
                </div>
              </div>

              <div class="grid gap-6 md:grid-cols-3" :class="loadingItems ? 'pointer-events-none opacity-60' : ''">
                <article
                  v-for="item in filteredItems"
                  :key="item.id || item.slug || item.name"
                  class="overflow-hidden rounded-2xl border-0 bg-[#f5f2ed] shadow-sm transition-all duration-300 hover:shadow-xl"
                >
                  <div
                    class="touch-manipulation select-none"
                    @pointerdown.capture="onHouseCardPointerDown(item, $event)"
                    @pointerup.capture="onHouseCardPointerEnd"
                    @pointercancel.capture="onHouseCardPointerCancel"
                    @click.capture="onHouseCardClickCapture"
                  >
                    <ImageCarousel :images="item.images" />

                    <div class="px-4 pb-4">
                      <p v-if="item.category" class="mb-1 text-xs font-medium uppercase tracking-wide text-primary/80">
                        {{ item.category }}
                      </p>
                      <div class="mb-3 flex items-baseline justify-between gap-3">
                        <h4 class="line-clamp-2 text-lg font-semibold text-foreground">{{ item.name }}</h4>
                        <div class="flex shrink-0 gap-2 whitespace-nowrap text-xs md:text-sm items-center">
                          <span class="font-medium text-foreground">₽ {{ Number(item.priceFrom || 0).toLocaleString('ru-RU') }}</span>
                          <div class="flex items-center gap-1 whitespace-nowrap text-muted-foreground">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 12c2.485 0 4.5-2.015 4.5-4.5S14.485 3 12 3 7.5 5.015 7.5 7.5 9.515 12 12 12zM5.25 20.25a6.75 6.75 0 1 1 13.5 0" />
                            </svg>
                            <span>до {{ item.capacityNum }} чел</span>
                          </div>
                        </div>
                      </div>

                      <p class="mb-0 line-clamp-3 text-sm leading-relaxed text-muted-foreground">
                        {{ item.description }}
                      </p>
                    </div>
                  </div>

                  <div class="mt-4 flex items-center justify-between gap-3 px-4 pb-4">
                    <div
                      v-if="item.quantity"
                      class="flex items-center gap-1.5 whitespace-nowrap text-xs font-medium text-muted-foreground md:text-sm"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3.75 20.25h16.5M5.25 20.25V8.25l7.5-4.5 6 3.6v12.9M9 20.25v-4.5h3v4.5" />
                      </svg>
                      <span>{{ formatHouseQuantity(item.quantity) }}</span>
                    </div>
                    <div v-else />
                    <button
                      class="rounded-full border border-primary px-5 py-2 text-sm font-medium text-primary transition-colors hover:bg-primary hover:text-primary-foreground"
                      @click="handleDetailsClick(item)"
                    >
                      подробнее
                    </button>
                  </div>
                </article>
              </div>

              <div
                v-if="!filteredItems.length"
                class="rounded-2xl border border-dashed border-border/70 bg-secondary/30 px-6 py-8 text-center text-sm text-muted-foreground"
              >
                По выбранным параметрам размещения пока нет доступных вариантов
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>

  <Teleport to="body">
    <div
      v-show="copyToastVisible"
      class="pointer-events-none fixed bottom-8 left-1/2 z-[100] max-w-[min(90vw,20rem)] -translate-x-1/2 rounded-full border border-border/60 bg-background/95 px-4 py-2.5 text-center text-sm font-medium text-foreground shadow-lg backdrop-blur-md transition-opacity duration-300"
      role="status"
      aria-live="polite"
    >
      Ссылка на дом скопирована
    </div>
  </Teleport>
</template>

<style scoped>
.lodge-category-cover {
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
</style>