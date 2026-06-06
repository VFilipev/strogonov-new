<script setup>
const formatPrice = (value) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;

const includedItems = [
  "Аренда бани на 4 часа",
  "Веники: дуб, берёза, пихта",
  "Коллективное бесконтактное парение веером и контактное парение вениками",
  "2 индивидуальные процедуры на выбор",
  "Полезный перекус: орехи, сухофрукты, мёд с ягодами",
  "Безлимитный травяной чай",
  "Банный комплект: полотенце, простыня, шапочка, шампунь, гель для душа",
];

const programs = [
  {
    title: "Русская банька с пармастером",
    subtitle: "программа 4 часа",
    prices: [
      { guests: "2-3 человека", value: 20000 },
      { guests: "4-6 человек", value: 25000 },
    ],
  },
  {
    title: "SPA-баня с пармастером",
    subtitle: "программа 4 часа",
    prices: [
      { guests: "2-3 человека", value: 25000 },
      { guests: "4-6 человек", value: 30000 },
    ],
  },
];

const additionalServices = [
  {
    title: "Каждый последующий час",
    price: `${formatPrice(2500)}/час`,
  },
  {
    title: "Пихтовое одеяло",
    price: formatPrice(5000),
  },
  {
    title: "Сибирский чан горячий",
    description: "с цитрусовыми дольками и ветками пихты",
    price: formatPrice(5000),
  },
  {
    title: "Японская ванна Фурако",
    description: "с цитрусовыми дольками и ветками пихты",
    price: formatPrice(5000),
  },
];

const procedures = [
  "Индивидуальное парение",
  "Солевое выкатывание",
  "Выкатывание горячими апельсинами",
  "Мыльно-веничный массаж",
];
</script>

<template>
  <section id="sauna-price" class="border-b border-border bg-muted/30 py-16 md:py-24">
    <div class="container mx-auto px-6 md:px-8">
      <div class="mx-auto max-w-3xl text-center">
        <p class="mb-3 text-sm font-semibold uppercase tracking-[0.28em] text-primary/70">
          Прайс
        </p>
        <h2 class="font-serif text-4xl text-primary md:text-5xl">
          Расслабление под ключ
        </h2>
        <p class="mt-5 text-lg leading-relaxed text-muted-foreground">
          Программы на 4 часа для русской бани и SPA-бани с пармастером,
          банным комплектом, чаепитием и процедурами на выбор.
        </p>
      </div>

      <div class="mt-12 grid gap-6 lg:grid-cols-[1.08fr_0.92fr]">
        <div class="space-y-6">
          <div class="grid gap-6 md:grid-cols-2">
            <article
              v-for="program in programs"
              :key="program.title"
              class="rounded-2xl border border-border bg-card p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
            >
              <div class="flex h-full flex-col">
                <div>
                  <p class="text-sm font-medium uppercase tracking-[0.18em] text-primary/60">
                    {{ program.subtitle }}
                  </p>
                  <h3 class="mt-3 font-serif text-2xl text-primary">
                    {{ program.title }}
                  </h3>
                </div>

                <div class="mt-auto space-y-3 pt-8">
                  <div
                    v-for="price in program.prices"
                    :key="`${program.title}-${price.guests}`"
                    class="flex items-center justify-between gap-4 rounded-xl border border-border/70 bg-background/70 px-4 py-3"
                  >
                    <span class="text-sm text-muted-foreground">{{ price.guests }}</span>
                    <span class="whitespace-nowrap text-lg font-semibold text-primary">
                      {{ formatPrice(price.value) }}
                    </span>
                  </div>
                </div>
              </div>
            </article>
          </div>

          <div class="rounded-2xl border border-border bg-card p-6 shadow-sm">
            <h3 class="font-serif text-2xl text-primary">
              В программу входит
            </h3>
            <div class="mt-5 grid gap-3 sm:grid-cols-2">
              <div
                v-for="item in includedItems"
                :key="item"
                class="flex items-start gap-3 text-sm leading-relaxed text-foreground/75"
              >
                <span class="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" />
                <span>{{ item }}</span>
              </div>
            </div>
          </div>

          <div class="rounded-2xl border border-primary/20 bg-card p-6 shadow-sm">
            <div class="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
              <div>
                <p class="text-sm font-semibold uppercase tracking-[0.2em] text-primary/60">
                  Бронирование
                </p>
                <h3 class="mt-2 font-serif text-2xl text-primary">
                  Выберите удобное время для отдыха
                </h3>
                <p class="mt-3 max-w-xl text-sm leading-relaxed text-muted-foreground">
                  Перейдите к услугам, чтобы посмотреть доступное время и оформить бронь.
                </p>
              </div>
              <a
                href="https://bronirui.online/stroganovskie-prostory/uslugi"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex shrink-0 items-center justify-center rounded-xl bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90"
              >
                Забронировать
              </a>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <div class="rounded-2xl border border-border bg-card p-6 shadow-sm">
            <h3 class="font-serif text-2xl text-primary">
              Дополнительно
            </h3>
            <div class="mt-5 divide-y divide-border/70">
              <div
                v-for="service in additionalServices"
                :key="service.title"
                class="flex items-start justify-between gap-4 py-4 first:pt-0 last:pb-0"
              >
                <div>
                  <p class="font-medium text-foreground">{{ service.title }}</p>
                  <p v-if="service.description" class="mt-1 text-sm leading-relaxed text-muted-foreground">
                    {{ service.description }}
                  </p>
                </div>
                <span class="whitespace-nowrap font-semibold text-primary">
                  {{ service.price }}
                </span>
              </div>
            </div>
          </div>

          <div class="overflow-hidden rounded-2xl border border-primary/20 bg-primary text-primary-foreground shadow-sm">
            <div class="p-6">
              <div class="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p class="text-sm font-semibold uppercase tracking-[0.2em] text-primary-foreground/70">
                    Индивидуально
                  </p>
                  <h3 class="mt-3 font-serif text-2xl">
                    Процедуры
                  </h3>
                </div>
                <span class="rounded-full bg-primary-foreground/15 px-4 py-2 text-sm text-primary-foreground/90">
                  2 входят в стоимость
                </span>
              </div>

              <div class="mt-6 space-y-3">
                <div
                  v-for="procedure in procedures"
                  :key="procedure"
                  class="rounded-xl border border-primary-foreground/15 bg-primary-foreground/10 p-4"
                >
                  <div class="flex items-start justify-between gap-4">
                    <div>
                      <p class="font-medium">{{ procedure }}</p>
                      <p class="mt-1 text-sm text-primary-foreground/70">20 минут</p>
                    </div>
                    <span class="whitespace-nowrap font-semibold">
                      {{ formatPrice(3000) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
