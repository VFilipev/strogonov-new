<script setup>
import { ref, computed } from "vue";
import {
  ArrowRight,
  Check,
  Compass,
  Mountain,
  Shield,
  Sparkles,
  Wrench,
} from "lucide-vue-next";
import ToursHero from "~/components/sections/ToursHero.vue";

const config = useRuntimeConfig();
const siteUrl = config.public.siteUrl;

const heroIntro =
  "Устали от города? Пришло время сменить декорации. Садитесь за руль мощного снегохода и рвите с привычной реальностью.";

const {
  freedomPoints,
  whyUs,
  tours,
  instructors,
  preparationItems,
  equipmentItems,
} = useSnowmobileToursPage();

const formatRub = (value) =>
  `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;

const summaryStats = computed(() => {
  if (!tours.length) {
    return [
      { label: "Маршрутов", value: "0" },
      { label: "Макс. дистанция", value: "0 км" },
      { label: "Стоимость", value: "по запросу" },
    ];
  }

  const maxDistance = Math.max(...tours.map((tour) => tour.distanceKm));
  const minPrice = Math.min(...tours.map((tour) => tour.priceRub));

  return [
    { label: "Маршрутов", value: String(tours.length) },
    { label: "Макс. дистанция", value: `${maxDistance} км` },
    { label: "Стоимость", value: `от ${formatRub(minPrice)}` },
  ];
});

const requestName = ref("");
const requestPhone = ref("");
const requestTourId = ref("");
const requestMessage = ref("");
const requestSent = ref(false);

const tourOptions = computed(() => [
  { value: "", label: "Выберите маршрут" },
  ...tours.map((t) => ({ value: t.id, label: `${t.title} (${t.distanceKm} км)` })),
]);

function submitRequest(e) {
  e.preventDefault();
  requestSent.value = true;
}

useHead({
  title: "Снегоходные маршруты — Строгановские Просторы",
  meta: [
    {
      name: "description",
      content:
        "Снегоходные туры по Пермскому краю: маршруты для новичков и опытных, сопровождение гида, техника и экипировка. База отдыха Строгановские Просторы.",
    },
  ],
  link: [{ rel: "canonical", href: `${siteUrl}/tours` }],
});
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <ToursHero :intro="heroIntro" />

    <section class="border-b border-border bg-background py-10 md:py-14">
      <div class="container mx-auto px-6 md:px-8">
        <div
          class="rounded-3xl border border-border bg-card/90 p-6 shadow-sm md:p-8 lg:p-10"
        >
          <div class="grid gap-8 lg:grid-cols-[1.15fr_0.85fr] lg:items-center">
            <div>
              <p
                class="text-xs font-semibold uppercase tracking-[0.2em] text-primary/90"
              >
                Ваш не забываемый уикенд
              </p>
              <h2 class="mt-3 font-serif text-2xl text-primary md:text-3xl">
                Все ключевое о турах за 30 секунд
              </h2>
              <p class="mt-4 max-w-2xl text-pretty leading-relaxed text-muted-foreground">
                Выбирайте сценарий под настроение: спокойная прогулка по лесу или
                насыщенный маршрут с обзорными точками и сопровождением инструктора.
              </p>
              <div class="mt-6 flex flex-wrap gap-3">
                <a
                  href="#tours-list"
                  class="inline-flex items-center gap-2 rounded-full border border-primary bg-primary px-5 py-2.5 text-sm font-semibold uppercase tracking-wide text-primary-foreground transition-colors hover:bg-primary/90"
                >
                  Смотреть маршруты
                  <ArrowRight class="h-4 w-4" aria-hidden="true" />
                </a>
                <a
                  href="#request"
                  class="inline-flex items-center rounded-full border border-primary/30 px-5 py-2.5 text-sm font-semibold uppercase tracking-wide text-primary transition-colors hover:border-primary/60 hover:bg-primary/5"
                >
                  Забронировать дату
                </a>
              </div>
            </div>

            <div class="grid gap-3 sm:grid-cols-3 lg:grid-cols-1">
              <article
                v-for="item in summaryStats"
                :key="item.label"
                class="rounded-2xl border border-border bg-muted/30 p-4 text-center lg:text-left"
              >
                <p class="text-xs font-medium uppercase tracking-[0.18em] text-muted-foreground">
                  {{ item.label }}
                </p>
                <p class="mt-2 font-serif text-2xl text-primary md:text-3xl">
                  {{ item.value }}
                </p>
              </article>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="border-b border-border bg-muted/40 py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <h2
          class="mx-auto max-w-3xl text-center font-serif text-2xl uppercase leading-snug tracking-[0.12em] text-primary md:text-3xl md:tracking-[0.16em]"
        >
          Почувствуйте настоящую свободу
        </h2>
        <div class="mt-12 grid gap-8 md:grid-cols-3">
          <article
            v-for="(item, index) in freedomPoints"
            :key="item.title"
            class="group relative overflow-hidden rounded-2xl border border-border/80 bg-card p-8 shadow-sm transition-shadow hover:shadow-md"
          >
            <span
              class="absolute right-4 top-4 font-serif text-5xl font-light text-primary/10 transition-colors group-hover:text-primary/15"
              aria-hidden="true"
              >{{ index + 1 }}</span
            >
            <Mountain
              class="mb-4 h-8 w-8 text-primary"
              aria-hidden="true"
            />
            <h3 class="mb-3 font-serif text-xl text-primary">
              {{ item.title }}
            </h3>
            <p class="text-pretty leading-relaxed text-muted-foreground">
              {{ item.text }}
            </p>
          </article>
        </div>
      </div>
    </section>

    <section class="py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <h2
          class="mb-10 text-center font-serif text-3xl text-primary md:text-4xl"
        >
          Почему выбирают нас?
        </h2>
        <ul
          class="mx-auto grid max-w-4xl gap-4 md:grid-cols-3"
          role="list"
        >
          <li
            v-for="(line, i) in whyUs"
            :key="i"
            class="flex gap-3 rounded-xl border border-border bg-card p-5 shadow-sm"
          >
            <span
              class="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary"
            >
              <Check class="h-4 w-4" aria-hidden="true" />
            </span>
            <span class="leading-relaxed text-foreground">{{ line }}</span>
          </li>
        </ul>
      </div>
    </section>

    <section
      id="tours-list"
      class="scroll-mt-24 border-y border-border bg-muted/30 py-16 md:py-24"
    >
      <div class="container mx-auto px-6 md:px-8">
        <div class="mb-12 flex flex-col items-start justify-between gap-4 md:flex-row md:items-end">
          <div>
            <p
              class="text-xs font-semibold uppercase tracking-[0.2em] text-primary/90"
            >
              Туры
            </p>
            <h2 class="mt-2 font-serif text-3xl text-primary md:text-4xl">
              Выберите маршрут
            </h2>
          </div>
          <p class="max-w-xl text-pretty text-muted-foreground">
            Два готовых сценария — от спокойного часа в лесу до насыщенного дня с
            переходом к бобровой плотине.
          </p>
        </div>

        <div class="grid gap-8 lg:grid-cols-2">
          <article
            v-for="tour in tours"
            :key="tour.id"
            class="group flex flex-col overflow-hidden rounded-3xl border border-border bg-card shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg"
          >
            <div
              class="border-b border-border bg-gradient-to-br from-primary/8 via-primary/5 to-transparent px-6 py-6 md:px-8 md:flex md:items-baseline md:justify-between"
            >
              <div>
                <p
                  class="inline-flex items-center gap-1.5 rounded-full border border-primary/20 bg-primary/5 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-primary/90"
                >
                  <Compass class="h-3.5 w-3.5" aria-hidden="true" />
                  Маршрут
                </p>
                <h3 class="mt-3 font-serif text-2xl text-primary md:text-3xl">
                  {{ tour.title }}
                </h3>
              </div>
              <p class="mt-3 text-sm font-medium uppercase tracking-wide text-muted-foreground md:mt-0">
                {{ tour.distanceKm }} км
              </p>
            </div>
            <div class="flex flex-1 flex-col px-6 py-6 md:px-8">
              <p class="flex-1 text-pretty leading-relaxed text-muted-foreground">
                {{ tour.description }}
              </p>
              <dl
                class="mt-6 grid grid-cols-2 gap-3 border-t border-border pt-6 text-sm"
              >
                <div class="rounded-xl border border-border bg-muted/30 p-3">
                  <dt class="text-xs uppercase tracking-wide text-muted-foreground">Возраст</dt>
                  <dd class="mt-1 text-sm font-medium text-foreground">{{ tour.age }}</dd>
                </div>
                <div class="rounded-xl border border-border bg-muted/30 p-3">
                  <dt class="text-xs uppercase tracking-wide text-muted-foreground">Посадка</dt>
                  <dd class="mt-1 text-sm font-medium text-foreground">{{ tour.seats }}</dd>
                </div>
              </dl>
              <p
                class="mt-6 font-serif text-3xl font-semibold text-primary"
              >
                {{ formatRub(tour.priceRub) }}
              </p>
              <a
                href="#request"
                class="mt-6 inline-flex w-full items-center justify-center gap-2 rounded-full border border-primary bg-primary px-6 py-3 text-center text-sm font-semibold uppercase tracking-wide text-primary-foreground transition-colors hover:bg-primary/90"
              >
                Оставить заявку
                <ArrowRight
                  class="h-4 w-4 transition-transform group-hover:translate-x-0.5"
                  aria-hidden="true"
                />
              </a>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <h2
          class="mb-12 text-center font-serif text-3xl text-primary md:text-4xl"
        >
          Инструкторы
        </h2>
        <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
          <article
            v-for="person in instructors"
            :key="person.id"
            class="rounded-2xl border border-border bg-card p-6 text-center shadow-sm"
          >
            <div
              class="mx-auto mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-primary/20 to-primary/5 font-serif text-2xl text-primary"
              aria-hidden="true"
            >
              {{ person.name.charAt(0) }}
            </div>
            <h3 class="font-serif text-xl text-primary">
              {{ person.name }}
            </h3>
            <p class="mt-1 text-sm font-medium text-primary/80">
              {{ person.role }}
            </p>
            <p class="mt-3 text-pretty text-sm leading-relaxed text-muted-foreground">
              {{ person.bio }}
            </p>
          </article>
        </div>
      </div>
    </section>

    <section class="border-t border-border bg-muted/40 py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <div class="grid gap-12 lg:grid-cols-2">
          <div>
            <div class="flex items-center gap-3">
              <Sparkles class="h-8 w-8 text-primary" aria-hidden="true" />
              <h2 class="font-serif text-2xl text-primary md:text-3xl">
                Подготовка к путешествию
              </h2>
            </div>
            <ul class="mt-6 space-y-4" role="list">
              <li
                v-for="(item, idx) in preparationItems"
                :key="idx"
                class="flex gap-3 text-pretty leading-relaxed text-muted-foreground"
              >
                <span class="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                {{ item }}
              </li>
            </ul>
          </div>
          <div>
            <div class="flex items-center gap-3">
              <Wrench class="h-8 w-8 text-primary" aria-hidden="true" />
              <h2 class="font-serif text-2xl text-primary md:text-3xl">
                Наша техника
              </h2>
            </div>
            <ul class="mt-6 space-y-4" role="list">
              <li
                v-for="(item, idx) in equipmentItems"
                :key="idx"
                class="flex gap-3 text-pretty leading-relaxed text-muted-foreground"
              >
                <Shield
                  class="mt-0.5 h-5 w-5 shrink-0 text-primary"
                  aria-hidden="true"
                />
                {{ item }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="border-t border-border bg-background py-14 md:py-20">
      <div class="container mx-auto px-6 md:px-8">
        <div
          class="overflow-hidden rounded-3xl border border-primary/20 bg-gradient-to-br from-primary/10 via-primary/5 to-transparent p-8 md:p-10"
        >
          <div class="grid gap-8 lg:grid-cols-[1fr_auto] lg:items-center">
            <div>
              <p class="text-xs font-semibold uppercase tracking-[0.2em] text-primary/90">
                Готовы к старту
              </p>
              <h2 class="mt-3 font-serif text-2xl text-primary md:text-3xl">
                Выберите маршрут и зафиксируйте удобную дату
              </h2>
              <p class="mt-4 max-w-2xl text-pretty leading-relaxed text-muted-foreground">
                После заявки мы свяжемся с вами, поможем подобрать оптимальный
                формат тура и дадим рекомендации по подготовке.
              </p>
            </div>
            <a
              href="#request"
              class="inline-flex items-center justify-center gap-2 rounded-full border border-primary bg-primary px-8 py-3 text-sm font-semibold uppercase tracking-wide text-primary-foreground transition-colors hover:bg-primary/90"
            >
              Перейти к заявке
              <ArrowRight class="h-4 w-4" aria-hidden="true" />
            </a>
          </div>
        </div>
      </div>
    </section>

    <section
      id="request"
      class="scroll-mt-24 border-t border-border py-16 md:py-24"
    >
      <div class="container mx-auto max-w-lg px-6 md:px-8">
        <h2
          class="mb-2 text-center font-serif text-3xl text-primary md:text-4xl"
        >
          Оставить заявку
        </h2>
        <p class="mb-10 text-center text-pretty text-muted-foreground">
          Заполните форму — мы свяжемся с вами для уточнения даты и состава
          группы. Сейчас данные не отправляются на сервер (демо-режим).
        </p>

        <div
          v-if="requestSent"
          class="rounded-2xl border border-primary/20 bg-card p-8 text-center shadow-sm"
          role="status"
        >
          <p class="font-medium text-primary">Заявка принята (демо)</p>
          <p class="mt-2 text-sm text-muted-foreground">
            Для реального бронирования позвоните нам или напишите на почту из
            подвала сайта.
          </p>
          <button
            type="button"
            class="mt-6 text-sm font-semibold text-primary underline underline-offset-4"
            @click="requestSent = false"
          >
            Отправить ещё одну
          </button>
        </div>

        <form
          v-else
          class="rounded-2xl border border-border bg-card p-6 shadow-sm md:p-10"
          @submit="submitRequest"
        >
          <div class="space-y-5">
            <div>
              <label
                for="tour-request-name"
                class="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-muted-foreground"
                >Имя</label
              >
              <input
                id="tour-request-name"
                v-model="requestName"
                type="text"
                autocomplete="name"
                class="w-full rounded-md border border-input bg-background px-3 py-2.5 text-foreground shadow-sm focus:border-ring focus:outline-none focus:ring-2 focus:ring-ring/30"
                placeholder="Как к вам обращаться"
              />
            </div>
            <div>
              <label
                for="tour-request-phone"
                class="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-muted-foreground"
                >Телефон</label
              >
              <input
                id="tour-request-phone"
                v-model="requestPhone"
                type="tel"
                autocomplete="tel"
                class="w-full rounded-md border border-input bg-background px-3 py-2.5 text-foreground shadow-sm focus:border-ring focus:outline-none focus:ring-2 focus:ring-ring/30"
                placeholder="+7 …"
              />
            </div>
            <div>
              <label
                for="tour-request-tour"
                class="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-muted-foreground"
                >Маршрут</label
              >
              <select
                id="tour-request-tour"
                v-model="requestTourId"
                class="w-full rounded-md border border-input bg-background px-3 py-2.5 text-foreground shadow-sm focus:border-ring focus:outline-none focus:ring-2 focus:ring-ring/30"
              >
                <option
                  v-for="opt in tourOptions"
                  :key="String(opt.value)"
                  :value="opt.value"
                >
                  {{ opt.label }}
                </option>
              </select>
            </div>
            <div>
              <label
                for="tour-request-msg"
                class="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-muted-foreground"
                >Комментарий</label
              >
              <textarea
                id="tour-request-msg"
                v-model="requestMessage"
                rows="4"
                class="w-full rounded-md border border-input bg-background px-3 py-2.5 text-foreground shadow-sm focus:border-ring focus:outline-none focus:ring-2 focus:ring-ring/30"
                placeholder="Дата, количество человек, пожелания"
              />
            </div>
            <button
              type="submit"
              class="w-full rounded-full border border-primary bg-primary py-3 text-sm font-semibold uppercase tracking-wide text-primary-foreground transition-colors hover:bg-primary/90"
            >
              Отправить заявку
            </button>
          </div>
        </form>
      </div>
    </section>

    <LazyFooterSection />
  </div>
</template>
