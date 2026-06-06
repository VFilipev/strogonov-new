<script setup>
import SaunaHero from "~/components/sections/SaunaHero.vue";
import SaunaComplexSection from "~/components/sections/SaunaComplexSection.vue";
import SaunaPriceSection from "~/components/sections/SaunaPriceSection.vue";
import saunaImage1 from "~/assets/resort/sauna-1.jpeg";
import saunaImage2 from "~/assets/resort/sauna-2.jpeg";
import saunaImage3 from "~/assets/resort/sauna-3.jpeg";
import saunaImage4 from "~/assets/resort/sauna-4.jpeg";
import spaImage1 from "~/assets/resort/spa-1.jpeg";
import spaImage2 from "~/assets/resort/spa-2.jpeg";
import spaImage3 from "~/assets/resort/spa-3.jpeg";
import spaImage4 from "~/assets/resort/spa-4.jpeg";
import spaImage5 from "~/assets/resort/spa-5.jpeg";
import spaImage6 from "~/assets/resort/spa-6.jpeg";

const config = useRuntimeConfig();
const siteUrl = config.public.siteUrl;

const heroIntro =
  "Два самостоятельных комплекса для глубокой перезагрузки: русская баня с сибирским чаном и SPA-баня с ванной Фурако.";

const russianComplexImages = [
  saunaImage1,
  saunaImage2,
  saunaImage3,
  saunaImage4,
];

const spaComplexImages = [spaImage3, spaImage2, spaImage1, spaImage4, spaImage5, spaImage6];

useHead({
  title: "Спа и баня — Строгановские Просторы",
  meta: [
    {
      name: "description",
      content:
        "Спа и банные комплексы в Строгановских Просторах: русская баня с сибирским чаном и отдельный SPA-комплекс с ванной Фурако.",
    },
  ],
  link: [{ rel: "canonical", href: `${siteUrl}/sauna` }],
});
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <SaunaHero
      title="Тепло, которое возвращает в ресурс"
      :intro="heroIntro"
      cta-href="#complexes"
    />

    <section
      id="complexes"
      class="scroll-mt-24 border-b border-border bg-background py-16 md:py-24"
    >
      <div class="container mx-auto px-6 md:px-8">
        <div class="mt-10 space-y-3">
          <SaunaComplexSection
            title="Русская баня и Сибирский чан"
            description="Классический банный ритуал с мягким паром, пармастером и глубоким прогревом в сибирском чане на свежем воздухе."
            :images="russianComplexImages"
            :highlights="[
              'Русская баня с пармастером',
              'Сибирский чан с горячей водой',
              'Формат для глубокого прогрева и восстановления',
            ]"
          />
          <SaunaComplexSection
            title="SPA-баня и ванна Фурако"
            description="Отдельный SPA-комплекс для размеренного отдыха: мягкий пар, расслабляющая атмосфера и японская ванна Фурако."
            :images="spaComplexImages"
            :highlights="[
              'SPA-баня как самостоятельный комплекс',
              'Ванна Фурако как отдельная часть программы',
              'Формат для приватного релакс-отдыха',
            ]"
            reverse
          />
        </div>
      </div>
    </section>

    <SaunaPriceSection />

    <LazyFooterSection />
  </div>
</template>
