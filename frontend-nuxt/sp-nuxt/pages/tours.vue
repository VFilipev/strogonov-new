<script setup>
import { ArrowRight, Clock3, Gauge, MapPinned, ShieldCheck, Users } from "lucide-vue-next";
import ToursHero from "~/components/sections/ToursHero.vue";

import tourCardImage1 from "~/assets/resort/tour1.jpeg";
import tourCardImage2 from "~/assets/resort/tour2.jpeg";
import tourCardImage3 from "~/assets/resort/tour3.jpg";
import tourCardImage4 from "~/assets/resort/tour4.jpeg";
import tourCardImage from "~/assets/resort/123.webp";
import galleryHero from "~/assets/tours/hero.webp";
import galleryHero6 from "~/assets/tours/hero6.webp";
import galleryHero7 from "~/assets/tours/hero7.webp";
import galleryHero8 from "~/assets/tours/hero8.webp";
import galleryHero9 from "~/assets/tours/hero9.webp";
import galleryHero10 from "~/assets/tours/hero10.webp";
import galleryHero11 from "~/assets/tours/hero11.webp";

const config = useRuntimeConfig();
const siteUrl = config.public.siteUrl;
const bookingPhone = "+7 (342) 233-33-32";
const bookingTel = "tel:+73422333332";

const heroIntro =
  "Незабываемые туры на квадроциклах в Пермском крае: премиальная техника TGB, сопровождение гида и полный комплект экипировки.";

const formatRub = (value) => `${new Intl.NumberFormat("ru-RU").format(value)} руб`;

const quadTours = [
  {
    id: "oznakomitelnyy",
    title: "Ознакомительный",
    duration: "60 минут",
    group: "от 3 квадроциклов",
    difficulty: "легкая",
    price: 5000,
    photo: tourCardImage1,
  },
  {
    id: "bobrovaya-plitina",
    title: "Бобровая плотина",
    duration: "2,5 - 3 часа",
    group: "от 3 квадроциклов",
    difficulty: "средняя",
    price: 14000,
    photo: tourCardImage2,
  },
  {
    id: "pchelodey",
    title: "Пчеловод",
    duration: "3 - 4 часа",
    group: "от 4 квадроциклов",
    difficulty: "средняя",
    price: 17000,
    photo: tourCardImage3,
  },
  {
    id: "vedmin-krug",
    title: "Чермоз",
    duration: "10 часов",
    group: "от 4 квадроциклов",
    difficulty: "тяжелая",
    price: 35000,
    photo: tourCardImage4,
  },
];

const includedItems = [
  {
    title: "Аренда премиальной техники",
    text: "Квадроцикл TGB Blade LTX EPS с двигателем 600 куб.см и 45 л.с.",
  },
  {
    title: "Квалифицированный инструктаж",
    text: "По технике безопасности и эксплуатации мотовездехода.",
  },
  {
    title: "Комплект профессиональной экипировки",
    text: "Для защиты вашего здоровья и повседневной одежды.",
  },
  {
    title: "Сопровождение гида",
    text: "И помощь на всё время проведения тура.",
  },
  {
    title: "Фото и видеосъемка",
    text: "С дальнейшим монтажем и отправкой материалов.",
  },
  {
    title: "Запрет на алкоголь",
    text: "Для всех участников мероприятия.",
  },
];

const tourGallery = [
  { src: galleryHero11, alt: "Участник тура на квадроцикле" },
  { src: galleryHero8, alt: "Квадроцикл и маршрут в лесу" },
  { src: galleryHero, alt: "Квадроцикл на маршруте" },
  { src: galleryHero9, alt: "Поездка по лесной дороге" },
  { src: galleryHero6, alt: "Участник тура на водной преграде" },
  { src: galleryHero10, alt: "Квадроцикл на пересеченной местности" },
  { src: galleryHero7, alt: "Квадроцикл в динамике" },
];

useHead({
  title: "Туры на квадроциклах — Строгановские Просторы",
  meta: [
    {
      name: "description",
      content:
        "Квадротуры в Пермском крае: маршруты разной сложности, сопровождение гида, экипировка, фото и видео отчет.",
    },
  ],
  link: [{ rel: "canonical", href: `${siteUrl}/tours` }],
});
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <ToursHero
      title="Незабываемые туры на квадроциклах"
      :intro="heroIntro"
    />

    <section id="tours-list" class="scroll-mt-24 border-b border-border bg-background py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <h2 class="font-serif text-3xl text-primary md:text-4xl">
          Маршруты
        </h2>

        <div class="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-4">
          <article
            v-for="tour in quadTours"
            :key="tour.id"
            class="group flex flex-col overflow-hidden rounded-2xl border border-border bg-card shadow-sm transition-all duration-300"
          >
            <div class="relative min-h-[170px] overflow-hidden bg-primary/95 px-5 py-6 text-primary-foreground">
              <NuxtImg
                :src="tour.photo"
                alt=""
                class="absolute inset-0 h-full w-full object-cover opacity-95"
                loading="lazy"
                decoding="async"
              />
              <div class="absolute inset-0 bg-gradient-to-b from-black/15 via-black/35 to-black/35" />
              <h3 class="relative mt-auto font-serif text-2xl text-primary-foreground">
                {{ tour.title }}
              </h3>
            </div>

            <div class="flex flex-1 flex-col px-5 py-5">
              <dl class="space-y-2 text-sm">
                <div class="flex items-start gap-2">
                  <Clock3 class="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                  <div>
                    <dt class="text-muted-foreground">Продолжительность:</dt>
                    <dd class="font-semibold text-foreground">{{ tour.duration }}</dd>
                  </div>
                </div>
                <div class="flex items-start gap-2">
                  <Users class="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                  <div>
                    <dt class="text-muted-foreground">Группа:</dt>
                    <dd class="font-semibold text-foreground">{{ tour.group }}</dd>
                  </div>
                </div>
                <div class="flex items-start gap-2">
                  <Gauge class="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                  <div>
                    <dt class="text-muted-foreground">Сложность:</dt>
                    <dd class="font-semibold text-foreground">{{ tour.difficulty }}</dd>
                  </div>
                </div>
              </dl>

              <p class="mt-6 font-serif text-3xl font-semibold text-primary">
                {{ formatRub(tour.price) }}
              </p>

              <a
                href="#request"
                class="mt-5 inline-flex items-center justify-center gap-2 rounded-full border border-primary bg-primary px-5 py-2.5 text-sm font-semibold uppercase tracking-wide text-primary-foreground transition-colors hover:bg-primary/90"
              >
                Забронировать
                <ArrowRight class="h-4 w-4" aria-hidden="true" />
              </a>
            </div>
          </article>
        </div>

        <p class="mt-8 text-sm leading-relaxed text-muted-foreground">
          * Стоимость указана за 1 человека, который будет управлять квадроциклом, возможность и цена размещения пассажира обговаривается отдельно и зависит от конкретного маршрута. Бронирование квадротуров происходит через оператора с внесением предоплаты в размере 20% от стоимости тура, в стоимость услуги не входит доставка клиента до точки проведения туристического мероприятия и обратный трансфер.
        </p>
      </div>
    </section>

    <section class="border-b border-border bg-muted/30 py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <h2 class="font-serif text-3xl text-primary md:text-4xl">
          Что входит в каждый тур
        </h2>

        <div class="mt-10 rounded-3xl border-2 border-dashed border-primary/70 bg-card/80 p-5 md:p-8">
          <div class="grid gap-4 md:grid-cols-2">
            <article
              v-for="(item, index) in includedItems"
              :key="item.title"
              class="relative rounded-2xl border border-border bg-background px-5 py-4"
            >
              <div
                class="absolute -left-3 -top-3 flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold text-primary-foreground"
                :class="item.title === 'Запрет на алкоголь' ? 'bg-red-600' : 'bg-primary'"
              >
                {{ index + 1 }}
              </div>
              <h3 class="font-semibold text-foreground">
                {{ item.title }}
              </h3>
              <p class="mt-1 text-sm leading-relaxed text-muted-foreground">
                {{ item.text }}
              </p>
            </article>
          </div>
        </div>

        <p class="mt-6 text-sm leading-relaxed text-muted-foreground">
          В состав длительных и индивидуальных туров могут входить дополнительные услуги: рыбалка, сбор ягод и грибов, а также приготовление пищи в походных условиях.
        </p>
      </div>
    </section>

    <section class="border-b border-border bg-background py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <h2 class="text-center font-serif text-3xl text-primary md:text-4xl">
          Фото и видео отчеты
        </h2>
        <div class="mt-10 grid grid-cols-1 gap-4 md:grid-cols-3">
          <div class="grid gap-4">
            <article class="h-[240px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm md:h-[250px]">
              <NuxtImg
                :src="tourGallery[0].src"
                :alt="tourGallery[0].alt"
                class="h-full w-full object-cover transition-transform duration-500"
                loading="lazy"
                decoding="async"
                sizes="(max-width: 768px) 100vw, 33vw"
              />
            </article>
            <article class="h-[240px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm md:h-[285px]">
              <NuxtImg
                :src="tourGallery[4].src"
                :alt="tourGallery[4].alt"
                class="h-full w-full object-cover transition-transform duration-500"
                loading="lazy"
                decoding="async"
                sizes="(max-width: 768px) 100vw, 33vw"
              />
            </article>
          </div>

          <div class="grid gap-4">
            <article class="h-[170px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
              <NuxtImg
                :src="tourGallery[1].src"
                :alt="tourGallery[1].alt"
                class="h-full w-full object-cover transition-transform duration-500"
                loading="lazy"
                decoding="async"
                sizes="(max-width: 768px) 100vw, 33vw"
              />
            </article>
            <article class="h-[170px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
              <NuxtImg
                :src="tourGallery[3].src"
                :alt="tourGallery[3].alt"
                class="h-full w-full object-cover transition-transform duration-500"
                loading="lazy"
                decoding="async"
                sizes="(max-width: 768px) 100vw, 33vw"
              />
            </article>
            <article class="h-[170px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
              <NuxtImg
                :src="tourGallery[5].src"
                :alt="tourGallery[5].alt"
                class="h-full w-full object-cover transition-transform duration-500"
                loading="lazy"
                decoding="async"
                sizes="(max-width: 768px) 100vw, 33vw"
              />
            </article>
          </div>

          <div class="grid gap-4">
            <article class="h-[240px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm md:h-[250px]">
              <NuxtImg
                :src="tourGallery[2].src"
                :alt="tourGallery[2].alt"
                class="h-full w-full object-cover transition-transform duration-500"
                loading="lazy"
                decoding="async"
                sizes="(max-width: 768px) 100vw, 33vw"
              />
            </article>
            <article class="h-[240px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm md:h-[285px]">
              <NuxtImg
                :src="tourGallery[6].src"
                :alt="tourGallery[6].alt"
                class="h-full w-full object-cover transition-transform duration-500"
                loading="lazy"
                decoding="async"
                sizes="(max-width: 768px) 100vw, 33vw"
              />
            </article>
          </div>
        </div>
      </div>
    </section>

    <section class="border-b border-border bg-muted/20 py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <div class="grid items-center gap-8 lg:grid-cols-[1fr_1.4fr]">
          <div>
            <h2 class="font-serif text-3xl text-primary md:text-4xl">
              Как к нам добраться
            </h2>
            <p class="mt-5 max-w-xl leading-relaxed text-muted-foreground">
              Наши квадроциклы, как и начальная точка всех маршрутов, находятся на базе отдыха «Строгановские Просторы» в Ильинском районе Пермского края. Это примерно в двух часах езды от iMall Эспланада в центре Перми.
            </p>
          </div>
          <div style="position:relative;overflow:hidden;"><a href="https://yandex.com/maps?utm_medium=mapframe&utm_source=maps" style="color:#eee;font-size:12px;position:absolute;top:0px;">Яндекс Карты</a><a href="https://yandex.com/maps/?from=mapframe&ll=55.923443%2C58.318195&mode=routes&rtext=58.011576%2C56.227308~58.614132%2C55.722128&rtt=auto&ruri=ymapsbm1%3A%2F%2Forg%3Foid%3D117771901434~ymapsbm1%3A%2F%2Forg%3Foid%3D1277179994&source=mapframe&utm_medium=mapframe&utm_source=maps&z=8" style="color:#eee;font-size:12px;position:absolute;top:14px;">Строгановские просторы: как доехать на автомобиле, общественным транспортом или пешком – Яндекс Карты</a><iframe src="https://yandex.com/map-widget/v1/?from=mapframe&ll=55.923443%2C58.318195&mode=routes&rtext=58.011576%2C56.227308~58.614132%2C55.722128&rtt=auto&ruri=ymapsbm1%3A%2F%2Forg%3Foid%3D117771901434~ymapsbm1%3A%2F%2Forg%3Foid%3D1277179994&source=mapframe&utm_source=mapframe&z=8" width="560" height="400" frameborder="1" allowfullscreen="true" style="position:relative;"></iframe></div>
        </div>
      </div>
    </section>

    <section id="request" class="scroll-mt-24 bg-background py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <div class="mx-auto max-w-3xl rounded-3xl border border-primary/20 bg-gradient-to-br from-primary/10 via-primary/5 to-transparent p-8 text-center md:p-10">
          <ShieldCheck class="mx-auto h-10 w-10 text-primary" aria-hidden="true" />
          <h2 class="mt-4 font-serif text-3xl text-primary md:text-4xl">
            Забронировать тур
          </h2>
          <p class="mt-4 leading-relaxed text-muted-foreground">
            Бронирование происходит через оператора. Позвоните нам или перейдите к маршрутам и оставьте заявку на подходящий тур.
          </p>
          <div class="mt-8 flex flex-wrap items-center justify-center gap-3">
            <a
              :href="bookingTel"
              class="inline-flex items-center justify-center rounded-full border border-primary bg-primary px-7 py-3 text-sm font-semibold uppercase tracking-wide text-primary-foreground transition-colors hover:bg-primary/90"
            >
              {{ bookingPhone }}
            </a>
            <a
              href="#tours-list"
              class="inline-flex items-center justify-center gap-2 rounded-full border border-primary/40 px-7 py-3 text-sm font-semibold uppercase tracking-wide text-primary transition-colors hover:border-primary/80 hover:bg-primary/5"
            >
              Выбрать маршрут
              <ArrowRight class="h-4 w-4" aria-hidden="true" />
            </a>
          </div>
        </div>
      </div>
    </section>

    <LazyFooterSection />
  </div>
</template>
