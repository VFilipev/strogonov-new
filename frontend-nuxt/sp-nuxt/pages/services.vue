<script setup>
import { RulerDimensionLine, Users } from "lucide-vue-next";
import FooterSection from "~/components/sections/FooterSection.vue";
import SiteHeaderNavigation from "~/components/sections/SiteHeaderNavigation.vue";

const config = useRuntimeConfig();
const siteUrl = config.public.siteUrl;

const priceSections = [
  {
    title: "Банкетный / конференц зал",
    highlightStats: [
      { icon: Users, label: "80 мест" },
      { icon: RulerDimensionLine, label: "170 м²" },
    ],
    items: [
      {
        name: "Аренда банкетного зала",
        details: "пт-вс / праздничные дни / 10 часов",
        price: "50 000 ₽",
      },
      {
        name: "Аренда банкетного зала",
        details: "будни / от 10 часов",
        price: "35 000 ₽",
      },
      {
        name: "Аренда конференц зала",
        details: "пт-вс / праздничные дни / 1 час",
        price: "5 000 ₽",
      },
      {
        name: "Аренда конференц зала",
        details: "будни / 1 час",
        price: "3 000 ₽",
      },
      {
        name: "Технический час",
        details: "монтаж / демонтаж",
        price: "1 000 ₽",
      },
      {
        name: "Клининг",
        price: "1 500 ₽",
      },
    ],
  },
  {
    title: "Прокат техники",
    items: [
      {
        name: "Аренда квадроцикла / снегохода",
        details: "1 час",
        price: "5 000 ₽",
      },
      {
        name: "Экипировка",
        details: "шлем, балаклава, защитный костюм",
        price: "бесплатно",
      },
      {
        name: "Аренда снегохода",
        details: "30 мин",
        price: "3 000 ₽",
      },
      {
        name: "Экипировка",
        details: "шлем, балаклава",
        price: "бесплатно",
      },
      {
        name: "Катание на банане",
        details: "снегоход / 10 мин",
        price: "500 ₽/чел",
      },
    ],
  },
  {
    title: "Аренда инвентаря",
    items: [
      {
        name: "Настольный теннис",
        price: "бесплатно",
      },
      {
        name: "Бадминтон",
        price: "бесплатно",
      },
      {
        name: "Мяч футбольный / волейбольный",
        price: "бесплатно",
      },
      {
        name: "Настольные игры",
        price: "бесплатно",
      },
      {
        name: "Коврик для йоги / пилатеса",
        details: "2 часа",
        price: "200 ₽",
      },
      {
        name: "Велосипед",
        details: "1 час",
        price: "200 ₽",
      },
    ],
  },
  {
    title: "Прокат",
    items: [
      {
        name: "Катамаран",
        details: "1 час / 2 человека",
        price: "600 ₽",
      },
      {
        name: "Катамаран",
        details: "1 час / 4 человека",
        price: "800 ₽",
      },
      {
        name: "Лодка весельная",
        details: "1 час / 2 человека",
        price: "400 ₽",
      },
      {
        name: "Sup-борд",
        details: "1 час / 1 человек",
        price: "800 ₽",
      },
      {
        name: "Sup-борд",
        details: "сутки / 1 человек",
        price: "2 000 ₽",
      },
      {
        name: "Спуск водной техники",
        details: "гидроцикл, лодка моторная, катер",
        price: "600 ₽",
      },
    ],
  },
  {
    title: "Зимний прокат",
    items: [
      {
        name: "Беговые лыжи",
        details: "1 час",
        price: "250 ₽",
      },
      {
        name: "Коньки",
        details: "1 час",
        price: "250 ₽",
      },
      {
        name: "Сноутюб",
        price: "бесплатно",
      },
      {
        name: "Клюшка для игры в хоккей",
        price: "150 ₽",
      },
    ],
  },
  {
    title: "Барбекю",
    items: [
      {
        name: "Гриль решетка",
        price: "150 ₽",
      },
      {
        name: "Казан",
        details: "3 литра",
        price: "250 ₽",
      },
      {
        name: "Казан",
        details: "8 литров",
        price: "450 ₽",
      },
      {
        name: "Шампуры",
        details: "6 штук",
        price: "150 ₽",
      },
      {
        name: "Розжиг / уголь для мангала / щепка",
        price: "уточнять на ресепшн",
      },
    ],
  },
];

const additionalServices = [
  {
    name: "Входной билет",
    price: "400 ₽",
  },
  {
    name: "Посещение контактного зоопарка",
    price: "бесплатно",
  },
  {
    name: "Детский комплекс",
    details: "батут, игровая площадка, веревочный парк",
    price: "бесплатно",
  },
  {
    name: "Услуги парковки автомобильного транспорта",
    price: "бесплатно",
  },
  {
    name: "Услуги прачечной",
    details: "1 кг",
    price: "150 ₽",
  },
];

const allSections = computed(() => [
  ...priceSections,
  {
    title: "Дополнительные услуги",
    items: additionalServices,
  },
]);

const isGreenCard = (index) => {
  const row = Math.floor(index / 2);
  const col = index % 2;
  return (row + col) % 2 === 1;
};

useHead({
  title: "Прайс услуг — Строгановские Просторы",
  meta: [
    {
      name: "description",
      content:
        "Прайс на услуги базы отдыха Строгановские Просторы: аренда залов, прокат техники, инвентаря, барбекю и дополнительные услуги.",
    },
  ],
  link: [{ rel: "canonical", href: `${siteUrl}/services` }],
});
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <SiteHeaderNavigation active-page="services" />

    <main>
      <section class="bg-gradient-to-b from-primary/10 to-background px-3 pb-12 pt-32 md:px-6 md:pb-16">
        <div class="container mx-auto px-0">
          <div class="mx-auto max-w-3xl text-center">
            <h1 class="text-4xl font-serif font-light leading-tight text-primary">
              Прайс на услуги
            </h1>
            <p class="mt-4 max-w-prose mx-auto text-base leading-relaxed text-muted-foreground md:text-base">
              Актуальные цены на аренду залов, прокат техники, инвентаря,
              барбекю и дополнительные услуги на территории базы отдыха.
            </p>
          </div>
        </div>
      </section>

      <section class="px-3 pb-16 md:px-6 md:pb-20">
        <div class="container mx-auto px-0">
          <div class="grid gap-6 lg:grid-cols-2">
            <article
              v-for="(section, index) in allSections"
              :key="section.title"
              class="overflow-hidden rounded-3xl border shadow-sm"
              :class="
                isGreenCard(index)
                  ? 'border-primary/25 bg-primary text-primary-foreground'
                  : 'border-border bg-card text-foreground'
              "
            >
              <div
                class="border-b p-5 md:p-6"
                :class="
                  isGreenCard(index)
                    ? 'border-primary-foreground/15 bg-primary/90'
                    : 'border-border/70 bg-muted/30'
                "
              >
                <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
                  <div class="min-w-0">
                    <h2
                      class="text-2xl font-serif font-normal leading-snug"
                      :class="
                        isGreenCard(index) ? 'text-primary-foreground' : 'text-primary'
                      "
                    >
                      {{ section.title }}
                    </h2>
                    <div
                      v-if="section.highlightStats?.length"
                      class="mt-2 flex flex-wrap gap-1.5"
                    >
                      <span
                        v-for="stat in section.highlightStats"
                        :key="stat.label"
                        class="inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[0.6rem] font-medium leading-tight tracking-normal md:text-[0.7rem]"
                        :class="
                          isGreenCard(index)
                            ? 'border-primary-foreground/30 text-primary-foreground'
                            : 'border-primary/25 text-primary'
                        "
                      >
                        <component
                          :is="stat.icon"
                          class="h-[0.7rem] w-[0.7rem] shrink-0 opacity-90 md:h-[0.8rem] md:w-[0.8rem]"
                          aria-hidden="true"
                          stroke-width="2"
                        />
                        {{ stat.label }}
                      </span>
                    </div>
                    <p
                      v-if="section.subtitle"
                      class="mt-2 text-sm font-medium uppercase tracking-[0.14em]"
                      :class="isGreenCard(index) ? 'text-primary-foreground/80' : 'text-primary/70'"
                    >
                      {{ section.subtitle }}
                    </p>
                  </div>
                  <div
                    v-if="section.meta?.length"
                    class="flex flex-wrap gap-2 text-xs font-medium uppercase tracking-[0.14em]"
                    :class="isGreenCard(index) ? 'text-primary-foreground/80' : 'text-primary/70'"
                  >
                    <span
                      v-for="metaItem in section.meta"
                      :key="metaItem"
                      class="rounded-full border px-3 py-1"
                      :class="isGreenCard(index) ? 'border-primary-foreground/30' : 'border-primary/20'"
                    >
                      {{ metaItem }}
                    </span>
                  </div>
                </div>
              </div>

              <div :class="isGreenCard(index) ? 'divide-y divide-primary-foreground/15 px-5 md:px-6' : 'divide-y divide-border/70 px-5 md:px-6'">
                <div
                  v-for="item in section.items"
                  :key="`${section.title}-${item.name}-${item.details || item.price}`"
                  class="flex flex-col gap-1.5 py-3 sm:flex-row sm:items-start sm:justify-between"
                >
                  <div>
                    <h3 class="text-sm font-medium leading-snug md:text-base">
                      {{ item.name }}
                    </h3>
                    <p
                      v-if="item.details"
                      class="mt-1 text-xs leading-relaxed md:text-sm"
                      :class="isGreenCard(index) ? 'text-primary-foreground/75' : 'text-muted-foreground'"
                    >
                      {{ item.details }}
                    </p>
                  </div>
                  <p class="shrink-0 text-sm font-semibold tabular-nums sm:text-right md:text-base">
                    {{ item.price }}
                  </p>
                </div>
              </div>
            </article>
          </div>
        </div>
      </section>
    </main>

    <FooterSection />
  </div>
</template>
