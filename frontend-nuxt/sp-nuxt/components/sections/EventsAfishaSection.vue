<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from "vue";
import { Info } from "lucide-vue-next";

const { mainEvents, masterclasses, pending, error } = useAfisha({
  server: true,
});

function formatRub(value) {
  if (value == null || Number.isNaN(value)) return "";
  return `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
}

const isVisible = ref(false);
const sectionRef = ref(null);
let sectionObserver = null;

const selected = ref(null);

function openItem(item) {
  selected.value = item;
}

function closeModal() {
  selected.value = null;
}

function onKeydown(e) {
  if (e.key === "Escape") closeModal();
}

watch(selected, (v) => {
  if (!import.meta.client) return;
  document.body.style.overflow = v ? "hidden" : "";
});

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
    { threshold: 0.08, rootMargin: "0px 0px -5%" }
  );

  if (sectionRef.value) {
    sectionObserver.observe(sectionRef.value);
  }

  window.addEventListener("keydown", onKeydown);
});

onBeforeUnmount(() => {
  if (sectionObserver) {
    sectionObserver.disconnect();
    sectionObserver = null;
  }
  window.removeEventListener("keydown", onKeydown);
  if (import.meta.client) {
    document.body.style.overflow = "";
  }
});
</script>

<template>
  <section
    id="afisha"
    ref="sectionRef"
    class="border-t border-border/40 bg-background"
  >
    <div class="container mx-auto px-6 py-20 md:px-8">
      <div class="mb-12 text-center">
        <h2
          class="mb-4 font-serif text-3xl text-primary transition-[opacity,transform] duration-700 md:text-4xl"
          :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'"
        >
          Главные события этого года
        </h2>
        <p
          class="mx-auto max-w-2xl text-lg text-muted-foreground transition-[opacity,transform] duration-700 delay-100"
          :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'"
        >
          Афиша праздников и мастер-классов на территории базы — следите за датами и присоединяйтесь к программам.
        </p>
        <p
          v-if="error"
          class="mx-auto mt-4 max-w-2xl text-center text-sm text-destructive"
          role="alert"
        >
          Не удалось загрузить афишу. Попробуйте обновить страницу позже.
        </p>
        <p
          v-else-if="pending && mainEvents.length === 0 && masterclasses.length === 0"
          class="mx-auto mt-4 max-w-2xl text-center text-sm text-muted-foreground"
        >
          Загрузка…
        </p>
      </div>

      <!-- Главные события -->
      <div class="mb-14">
        <h3
          class="mb-6 font-serif text-2xl text-primary md:text-3xl transition-[opacity,transform] duration-700 delay-150"
          :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'"
        >
          Список событий
        </h3>
        <div class="flex flex-col gap-4 sm:gap-5">
          <button
            v-for="(ev, index) in mainEvents"
            :key="ev.id"
            type="button"
            class="group grid w-full grid-cols-1 overflow-hidden rounded-2xl border border-border/50 bg-card text-left shadow-sm transition-[opacity,transform,box-shadow] duration-500 hover:border-primary/30 hover:shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-primary sm:grid-cols-[minmax(240px,260px)_minmax(0,1fr)]"
            :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'"
            :style="{
              transitionDelay: isVisible ? `${180 + index * 45}ms` : '0ms',
            }"
            @click="openItem(ev)"
          >
            <div
              class="relative min-h-40 w-full overflow-hidden sm:h-full"
            >
              <NuxtImg
                :src="ev.image"
                :alt="ev.title"
                width="400"
                height="250"
                class="absolute inset-0 h-full w-full object-cover object-center transition-transform duration-500 group-hover:scale-[1.02] rounded-t-2xl sm:rounded-l-2xl sm:rounded-tr-none"
                sizes="(max-width:640px) 100vw, 280px"
                loading="lazy"
              />
            </div>
            <div
              class="flex min-h-[10rem] min-w-0 flex-col gap-2 p-4 text-left sm:min-h-0 sm:py-5 sm:pl-5 sm:pr-6"
            >
              <div class="flex shrink-0 items-start justify-between gap-3">
                <h4
                  class="font-serif text-base font-semibold leading-snug text-foreground group-hover:text-primary sm:text-lg md:text-xl"
                >
                  {{ ev.title }}
                </h4>
              </div>
              <p
                class="min-h-0 flex-1 text-sm leading-relaxed text-muted-foreground line-clamp-3 sm:line-clamp-2 md:line-clamp-4"
              >
                {{ ev.shortDescription }}
              </p>
              <div
                v-if="ev.pricePerGuest != null"
                class="flex flex-wrap items-baseline gap-x-3 gap-y-0.5 text-sm"
              >
                <span class="font-semibold tabular-nums text-foreground">
                  {{ formatRub(ev.pricePerGuest) }} за гостя
                </span>
              </div>
              <div
                class="flex shrink-0 flex-wrap items-end justify-between gap-x-4 gap-y-2 pt-3"
              >
                <time
                  :datetime="ev.sortKey"
                  class="text-sm italic text-[#0b4134]"
                >
                  {{ ev.dateLabel }}
                </time>
                <span
                  class="inline-flex shrink-0 items-center justify-center rounded-full border border-primary bg-transparent px-5 py-2 text-sm font-medium text-primary transition-colors group-hover:bg-primary/5"
                >
                  Подробнее
                </span>
              </div>
            </div>
          </button>
        </div>
        <p
          v-if="!error && !pending && mainEvents.length === 0"
          class="rounded-2xl border border-dashed border-border/60 bg-muted/30 px-6 py-10 text-center text-base leading-relaxed text-muted-foreground transition-[opacity,transform] duration-700"
          :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'"
        >
          Сейчас список событий пуст. Следите за обновлениями — готовим для вас увлекательные мероприятия.
        </p>
      </div>

      <!-- Мастер-классы -->
      <div>
        <h3
          class="mb-6 font-serif text-2xl text-primary md:text-3xl transition-[opacity,transform] duration-700 delay-150"
          :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'"
        >
          Мастер-классы
        </h3>
        <div class="flex flex-col gap-4 sm:gap-5">
          <button
            v-for="(ev, index) in masterclasses"
            :key="ev.id"
            type="button"
            class="group grid w-full grid-cols-1 overflow-hidden rounded-2xl border border-border/50 bg-card text-left shadow-sm transition-[opacity,transform,box-shadow] duration-500 hover:border-primary/30 hover:shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-primary sm:grid-cols-[minmax(240px,260px)_minmax(0,1fr)]"
            :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'"
            :style="{
              transitionDelay: isVisible ? `${400 + index * 35}ms` : '0ms',
            }"
            @click="openItem(ev)"
          >
            <div
              class="relative min-h-40 w-full overflow-hidden sm:h-full"
            >
              <NuxtImg
                :src="ev.image"
                :alt="ev.title"
                width="400"
                height="250"
                class="absolute inset-0 h-full w-full object-cover object-center transition-transform duration-500 group-hover:scale-[1.02] rounded-t-2xl sm:rounded-l-2xl sm:rounded-tr-none"
                sizes="(max-width:640px) 100vw, 280px"
                loading="lazy"
              />
            </div>
            <div
              class="flex min-h-[10rem] min-w-0 flex-col gap-2 p-4 text-left sm:min-h-0 sm:py-5 sm:pl-5 sm:pr-6"
            >
              <div class="flex shrink-0 items-start justify-between gap-3">
                <h4
                  class="font-serif text-base font-semibold leading-snug text-foreground group-hover:text-primary sm:text-lg md:text-xl"
                >
                  {{ ev.title }}
                </h4>
                <span
                  class="inline-flex shrink-0 rounded-full bg-primary/10 p-1.5 text-primary"
                  aria-hidden="true"
                >
                  <Info class="h-4 w-4 md:h-5 md:w-5" stroke-width="2" />
                </span>
              </div>
              <p
                class="min-h-0 flex-1 text-sm leading-relaxed text-muted-foreground line-clamp-3 sm:line-clamp-2 md:line-clamp-4"
              >
                {{ ev.shortDescription }}
              </p>
              <div
                v-if="ev.pricePerGuest != null"
                class="flex flex-wrap items-baseline gap-x-3 gap-y-0.5 text-sm"
              >
                <span class="font-semibold tabular-nums text-foreground">
                  {{ formatRub(ev.pricePerGuest) }} за гостя
                </span>
              </div>
              <div
                class="flex shrink-0 flex-wrap items-end justify-between gap-x-4 gap-y-2 pt-3"
              >
                <time
                  :datetime="ev.sortKey"
                  class="text-sm italic text-[#0b4134]"
                >
                  {{ ev.dateLabel }}
                </time>
                <span
                  class="inline-flex shrink-0 items-center justify-center rounded-full border border-primary bg-transparent px-5 py-2 text-sm font-medium text-primary transition-colors group-hover:bg-primary/5"
                >
                  Подробнее
                </span>
              </div>
            </div>
          </button>
        </div>
        <p
          v-if="!error && !pending && masterclasses.length === 0"
          class="rounded-2xl border border-dashed border-border/60 bg-muted/30 px-6 py-10 text-center text-base leading-relaxed text-muted-foreground transition-[opacity,transform] duration-700"
          :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'"
        >
          Программа мастер-классов скоро появится здесь. Следите за обновлениями — для вас готовим новые встречи и занятия.
        </p>
      </div>
    </div>

    <Teleport to="body">
      <div
        v-if="selected"
        class="fixed inset-0 z-[100] flex items-end justify-center sm:items-center sm:p-4"
        role="presentation"
      >
        <div
          class="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity"
          aria-hidden="true"
          @click="closeModal"
        />
        <div
          role="dialog"
          aria-modal="true"
          :aria-labelledby="selected ? 'afisha-modal-title' : undefined"
          class="relative z-[101] flex max-h-[90vh] w-full max-w-lg flex-col overflow-hidden rounded-t-2xl bg-background shadow-2xl sm:rounded-2xl"
          @click.stop
        >
          <div class="relative aspect-[16/9] shrink-0 sm:aspect-[2/1]">
            <NuxtImg
              :src="selected.image"
              :alt="selected.title"
              width="800"
              height="450"
              class="h-full w-full object-cover"
              sizes="100vw"
            />
            <button
              type="button"
              class="absolute right-3 top-3 flex h-10 w-10 items-center justify-center rounded-full bg-background/90 text-foreground shadow-md transition-colors hover:bg-background"
              aria-label="Закрыть"
              @click="closeModal"
            >
              <span class="text-xl leading-none" aria-hidden="true">×</span>
            </button>
          </div>
          <div class="min-h-0 flex-1 overflow-y-auto p-6">
            <p class="mb-2 text-sm italic text-[#0b4134]">
              {{ selected.dateLabel }}
            </p>
            <h3
              id="afisha-modal-title"
              class="mb-4 font-serif text-2xl text-foreground md:text-3xl"
            >
              {{ selected.title }}
            </h3>
            <div
              v-if="selected.pricePerGuest != null"
              class="mb-4 border-b border-border/40 pb-4 text-base"
            >
              <p class="tabular-nums">
                <span class="text-muted-foreground">За гостя: </span>
                <span class="font-semibold text-foreground">{{ formatRub(selected.pricePerGuest) }}</span>
              </p>
            </div>
            <p class="whitespace-pre-line text-base leading-relaxed text-muted-foreground">
              {{ selected.fullDescription }}
            </p>
            <button
              type="button"
              class="mt-6 w-full rounded-xl border border-primary bg-primary px-4 py-3 text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90 sm:w-auto"
              @click="closeModal"
            >
              Закрыть
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </section>
</template>
