<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";

const reviewsSectionRef = ref(null);
const shouldLoadReviews = ref(false);
let reviewsObserver = null;

onMounted(() => {
  const section = reviewsSectionRef.value;
  if (!section || typeof IntersectionObserver === "undefined") {
    shouldLoadReviews.value = true;
    return;
  }

  reviewsObserver = new IntersectionObserver(
    ([entry]) => {
      if (!entry?.isIntersecting) return;
      shouldLoadReviews.value = true;
      reviewsObserver?.disconnect();
      reviewsObserver = null;
    },
    { rootMargin: "600px 0px" },
  );

  reviewsObserver.observe(section);
});

onBeforeUnmount(() => {
  reviewsObserver?.disconnect();
  reviewsObserver = null;
});
</script>

<template>
  <section
    id="guest-reviews"
    ref="reviewsSectionRef"
    class="relative overflow-hidden bg-background py-20"
  >
    <div class="container relative mx-auto px-6 md:px-8">
      <div class="relative grid gap-10 lg:grid-cols-[minmax(0,1fr)_minmax(520px,560px)] lg:items-start lg:gap-12 xl:gap-16">
        <div class="relative z-[1] max-w-2xl">
          <h2 class="font-serif text-4xl text-primary md:text-5xl">
            Отзывы наших гостей
          </h2>

          <p class="mt-5 max-w-xl text-lg leading-8 text-muted-foreground">
            Спокойный отдых ощущается не только в кадре, но и в впечатлениях гостей. Чаще всего отмечают тишину, уединение, заботу и атмосферу настоящей перезагрузки.
          </p>
        </div>

        <div class="relative w-full">
            <div class="relative h-[310px] overflow-hidden rounded-[24px] bg-white md:h-[450px] lg:h-[450px]">
              <iframe
                v-if="shouldLoadReviews"
                title="Отзывы гостей на Яндекс Картах"
                class="h-full w-full rounded-[24px] border border-[#e6e6e6]"
                src="https://yandex.ru/maps-reviews-widget/1277179994?comments"
                loading="lazy"
              />
              <div
                v-else
                class="h-full w-full rounded-[24px] border border-[#e6e6e6] bg-muted/40"
                aria-hidden="true"
              />
              <a
                href="https://yandex.com/maps/org/stroganovskye_prostory/1277179994/"
                target="_blank"
                rel="noopener noreferrer"
                class="absolute bottom-2 left-0 block w-full overflow-hidden px-4 text-center text-[10px] text-[#b3b3b3] whitespace-nowrap text-ellipsis"
              >
                Строгановские просторы на карте Пермского края — Яндекс Карты
              </a>
            </div>
          </div>
        </div>
    </div>
  </section>
</template>
