<script setup>
import {
  ArrowRight,
  BedDouble,
  CalendarDays,
  Clock3,
  Fish,
  Flame,
  Gauge,
  PackageCheck,
  ShieldCheck,
  Utensils,
  Users,
} from "lucide-vue-next";
import ToursHero from "~/components/sections/ToursHero.vue";

import tourCardImage1 from "~/assets/resort/tour1.jpeg";
import tourCardImage2 from "~/assets/resort/tour2.jpeg";
import tourCardImage3 from "~/assets/resort/tour3.jpg";
import tourCardImage4 from "~/assets/resort/tour4.jpeg";
import galleryHero from "~/assets/tours/hero.webp";
import galleryHero6 from "~/assets/tours/hero6.webp";
import galleryHero7 from "~/assets/tours/hero7.webp";
import galleryHero8 from "~/assets/tours/hero8.webp";
import galleryHero9 from "~/assets/tours/hero9.webp";
import galleryHero10 from "~/assets/tours/hero10.webp";
import galleryHero11 from "~/assets/tours/hero11.webp";
import weekendFoodImage from "~/assets/restoran/menu.webp";
import weekendRelaxImage from "~/assets/resort/sauna-hero.jpeg";
import weekendStayImage from "~/assets/resort/frame.webp";

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

const weekendTourBenefits = [
  {
    title: "Готовый план на выходные",
    text: "Не нужно собирать программу из отдельных услуг: заезд, проживание, питание, маршрут и отдых уже собраны в один сценарий.",
  },
  {
    title: "Два маршрута на выбор",
    text: "Для тура выходного дня доступны «Бобровая плотина» и «Пчеловод». В дальнейшем линейку можно расширить новыми направлениями.",
  },
  {
    title: "Отдых после маршрута",
    text: "После квадротура можно восстановиться в бане на дровах, порыбачить на форель и провести вечер на базе.",
  },
];

const weekendTourOptions = [
  {
    id: "weekend-bobrovaya-plotina",
    title: "Бобровая плотина",
    description:
      "Маршрут к природной локации для тех, кто хочет совместить драйв, лесные дороги и спокойный отдых на базе.",
    price: 32000,
    oldPrice: 41000,
    photo: tourCardImage2,
    photoAlt: "Квадроцикл на маршруте Бобровая плотина",
  },
  {
    id: "weekend-pcheloved",
    title: "Пчеловод",
    description:
      "Более насыщенная поездка по живописной дороге к пасеке с ощущением полноценного путешествия на выходные.",
    price: 37000,
    oldPrice: 43000,
    photo: tourCardImage3,
    photoAlt: "Квадроцикл на маршруте Пчеловод",
  },
];

const weekendSchedule = [
  {
    day: "Пятница",
    items: [
      "Заезд с 15:00 до 19:00",
      "Размещение в доме категории Комфорт без кухни",
      "Ужин с 18:00 до 20:00",
    ],
  },
  {
    day: "Суббота",
    items: [
      "Завтрак с 9:00 до 10:00",
      "Выезд на квадроцикле по выбранному маршруту",
      "Обед с 12:00 до 14:00",
      "Баня на дровах 2 часа",
      "Ужин с 18:00 до 20:00",
    ],
  },
  {
    day: "Воскресенье",
    items: [
      "Завтрак с 9:00 до 10:00",
      "Свободное время до 13:00",
      "Выезд",
    ],
  },
];

const weekendIncludedItems = [
  {
    title: "Все, что входит в стоимость выбранного квадромаршрута",
  },
  {
    title: "Проживание в доме класса Комфорт",
  },
  {
    title: "Питание по программе тура",
  },
  {
    title: "Рыбалка на форель",
    text: "Рыбалка входит в стоимость тура, улов оплачивается отдельно: 1 500 руб/кг.",
  },
  {
    title: "Баня на дровах",
  },
  {
    title: "Прокат инвентаря",
  },
];

const weekendExperienceItems = [
  {
    id: "food",
    title: "Питание без забот",
    text: "Блюда уже продуманы по программе тура, вам не нужно думать о меню и готовке.",
    photo: weekendFoodImage,
    photoAlt: "Блюдо из ресторана на базе отдыха",
  },
  {
    id: "quad",
    title: "Квадромаршрут и драйв",
    text: "Главное действие уикенда: насыщенная поездка на квадроциклах с эмоциями и красивыми локациями.",
    photo: galleryHero11,
    photoAlt: "Квадроцикл на маршруте выходного дня",
  },
  {
    id: "relax",
    title: "Баня и релакс",
    text: "После маршрута можно восстановиться в бане на дровах и перезагрузиться перед вечером.",
    photo: weekendRelaxImage,
    photoAlt: "Банный комплекс для отдыха после тура",
  },
  {
    id: "stay",
    title: "Проживание Комфорт",
    text: "Понятное размещение на базе: ночевка в доме класса Комфорт без лишних организационных вопросов.",
    photo: weekendStayImage,
    photoAlt: "Дом для проживания на базе отдыха",
  },
];

const coverStyle = (src) =>
  src ? { backgroundImage: `url("${String(src)}")` } : {};

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
              <div
                class="cover-bg absolute inset-0 opacity-95"
                role="img"
                :aria-label="tour.title"
                :style="coverStyle(tour.photo)"
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
          Что входит в стоимость
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
        <div class="grid gap-8 lg:grid-cols-[0.95fr_1.05fr] lg:items-start">
          <div class="rounded-3xl border border-primary/20 bg-gradient-to-br from-primary/10 via-primary/5 to-transparent p-6 md:p-8">
            <span class="inline-flex items-center gap-2 rounded-full bg-primary px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] text-primary-foreground">
              <CalendarDays class="h-4 w-4" aria-hidden="true" />
              Тур выходного дня
            </span>
            <h2 class="mt-6 font-serif text-3xl text-primary md:text-4xl">
              Маршрут, проживание и отдых в одном предложении
            </h2>
            <p class="mt-5 text-base leading-relaxed text-muted-foreground md:text-lg">
              Формат для тех, кто хочет приехать на базу на весь уикенд: выбрать квадромаршрут, переночевать в комфортном доме, поужинать без спешки и добавить спокойный отдых после активной поездки.
            </p>


            <div class="mt-8 grid gap-4">
              <article
                v-for="benefit in weekendTourBenefits"
                :key="benefit.title"
                class="rounded-2xl border border-border bg-card/90 p-5 shadow-sm"
              >
                <h3 class="font-semibold text-foreground">
                  {{ benefit.title }}
                </h3>
                <p class="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {{ benefit.text }}
                </p>
              </article>
            </div>
          </div>

          <div class="grid gap-5">
            <article
              v-for="option in weekendTourOptions"
              :key="option.id"
              class="overflow-hidden rounded-3xl border border-border bg-card shadow-sm"
            >
              <div class="grid gap-0 md:grid-cols-[180px_1fr_auto]">
                <div class="relative min-h-[190px] overflow-hidden bg-primary/10 md:min-h-full">
                  <div
                    class="cover-bg absolute inset-0"
                    role="img"
                    :aria-label="option.photoAlt"
                    :style="coverStyle(option.photo)"
                  />
                  <div class="absolute inset-0 bg-gradient-to-t from-black/45 via-transparent to-transparent" />
                </div>
                <div class="p-6 md:p-7">
                  <p class="text-xs font-semibold uppercase tracking-[0.18em] text-primary">
                    Выбранный маршрут
                  </p>
                  <h3 class="mt-3 font-serif text-2xl text-primary md:text-3xl">
                    {{ option.title }}
                  </h3>
                  <p class="mt-3 text-sm leading-relaxed text-muted-foreground">
                    {{ option.description }}
                  </p>
                </div>

                <div class="flex min-w-[210px] flex-col justify-center border-t border-border bg-primary/5 p-6 md:border-l md:border-t-0 md:p-7">
                  <p class="text-sm text-muted-foreground">
                    Стоимость тура
                  </p>
                  <p class="mt-2 font-serif text-3xl font-semibold text-primary">
                    {{ formatRub(option.price) }}
                  </p>
                  <p class="mt-2 text-sm text-muted-foreground">
                    Обычная цена
                    <span class="ml-1 text-base font-semibold text-foreground line-through">
                      {{ formatRub(option.oldPrice) }}
                    </span>
                  </p>
                </div>
              </div>
            </article>
          </div>
        </div>

        <div class="mt-8 rounded-3xl border border-border bg-card p-5 shadow-sm md:p-8">
          <h3 class="font-serif text-2xl text-primary md:text-3xl">
            Все для готового уикенда
          </h3>
          <p class="mt-2 max-w-3xl text-sm leading-relaxed text-muted-foreground md:text-base">
            В туре уже закрыты ключевые потребности отдыха: питание, активный маршрут, восстановление и проживание.
          </p>

          <div class="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <article
              v-for="item in weekendExperienceItems"
              :key="item.id"
              class="overflow-hidden rounded-2xl border border-border bg-background"
            >
              <div class="relative h-40 overflow-hidden">
                <div
                  class="cover-bg absolute inset-0"
                  role="img"
                  :aria-label="item.photoAlt"
                  :style="coverStyle(item.photo)"
                />
                <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />
              </div>
              <div class="p-4">
                <h4 class="font-semibold text-foreground">
                  {{ item.title }}
                </h4>
                <p class="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {{ item.text }}
                </p>
              </div>
            </article>
          </div>
        </div>

        <div class="mt-10 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <div class="rounded-3xl border border-border bg-card p-5 shadow-sm md:p-8">
            <div class="flex items-center gap-3">
              <Clock3 class="h-6 w-6 text-primary" aria-hidden="true" />
              <h3 class="font-serif text-2xl text-primary md:text-3xl">
                Программа тура
              </h3>
            </div>

            <div class="mt-6 grid gap-4 md:grid-cols-3">
              <article
                v-for="day in weekendSchedule"
                :key="day.day"
                class="rounded-2xl border border-primary/20 bg-background p-5"
              >
                <h4 class="font-serif text-xl text-primary">
                  {{ day.day }}
                </h4>
                <ul class="mt-4 space-y-3 text-sm leading-relaxed text-muted-foreground">
                  <li
                    v-for="item in day.items"
                    :key="item"
                    class="flex gap-2"
                  >
                    <span class="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" aria-hidden="true" />
                    <span>{{ item }}</span>
                  </li>
                </ul>
              </article>
            </div>

          </div>

          <div class="rounded-3xl border-2 border-dashed border-primary/70 bg-card/80 p-5 md:p-8">
            <div class="flex items-center gap-3">
              <PackageCheck class="h-6 w-6 text-primary" aria-hidden="true" />
              <h3 class="font-serif text-2xl text-primary md:text-3xl">
                Включено в тур
              </h3>
            </div>

            <div class="mt-6 grid gap-3">
              <div
                v-for="item in weekendIncludedItems"
                :key="item.title"
                class="flex items-start gap-3 rounded-2xl border border-border bg-background px-4 py-3 text-sm leading-relaxed text-foreground"
              >
                <ShieldCheck class="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                <span>
                  <span class="block font-semibold">{{ item.title }}</span>
                  <span
                    v-if="item.text"
                    class="mt-1 block text-muted-foreground"
                  >
                    {{ item.text }}
                  </span>
                </span>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-8 flex flex-wrap items-center justify-between gap-4 rounded-3xl border border-primary/20 bg-primary px-6 py-5 text-primary-foreground md:px-8">
          <p class="max-w-2xl text-sm leading-relaxed md:text-base">
            Итоговая стоимость зависит от выбранного маршрута. Сейчас для тура выходного дня доступны два направления, но формат рассчитан на расширение программы.
          </p>
          <a
            href="#request"
            class="inline-flex items-center justify-center gap-2 rounded-full border border-primary-foreground/80 px-6 py-3 text-sm font-semibold uppercase tracking-wide transition-colors hover:bg-primary-foreground hover:text-primary"
          >
            Забронировать уикенд
            <ArrowRight class="h-4 w-4" aria-hidden="true" />
          </a>
        </div>
      </div>
    </section>

    <section class="border-b border-border bg-background py-16 md:py-24">
      <div class="container mx-auto px-6 md:px-8">
        <h2 class="text-center font-serif text-3xl text-primary md:text-4xl">
          Фото и видео отчеты
        </h2>
        <div class="mt-10 grid grid-cols-1 gap-4 md:grid-cols-3">
          <div class="grid gap-4">
            <article class="relative h-[240px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm md:h-[250px]">
              <div
                class="cover-bg absolute inset-0"
                role="img"
                :aria-label="tourGallery[0].alt"
                :style="coverStyle(tourGallery[0].src)"
              />
            </article>
            <article class="relative h-[240px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm md:h-[285px]">
              <div
                class="cover-bg absolute inset-0"
                role="img"
                :aria-label="tourGallery[4].alt"
                :style="coverStyle(tourGallery[4].src)"
              />
            </article>
          </div>

          <div class="grid gap-4">
            <article class="relative h-[170px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
              <div
                class="cover-bg absolute inset-0"
                role="img"
                :aria-label="tourGallery[1].alt"
                :style="coverStyle(tourGallery[1].src)"
              />
            </article>
            <article class="relative h-[170px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
              <div
                class="cover-bg absolute inset-0"
                role="img"
                :aria-label="tourGallery[3].alt"
                :style="coverStyle(tourGallery[3].src)"
              />
            </article>
            <article class="relative h-[170px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
              <div
                class="cover-bg absolute inset-0"
                role="img"
                :aria-label="tourGallery[5].alt"
                :style="coverStyle(tourGallery[5].src)"
              />
            </article>
          </div>

          <div class="grid gap-4">
            <article class="relative h-[240px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm md:h-[250px]">
              <div
                class="cover-bg absolute inset-0"
                role="img"
                :aria-label="tourGallery[2].alt"
                :style="coverStyle(tourGallery[2].src)"
              />
            </article>
            <article class="relative h-[240px] overflow-hidden rounded-2xl border border-border bg-card shadow-sm md:h-[285px]">
              <div
                class="cover-bg absolute inset-0"
                role="img"
                :aria-label="tourGallery[6].alt"
                :style="coverStyle(tourGallery[6].src)"
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

<style scoped>
.cover-bg {
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
</style>
