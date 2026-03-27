<script setup>
import { BOOKING_URL } from '~/utils/booking'
</script>

<template>
  <section class="border-t border-border/60 bg-background py-16 md:py-24">
    <div class="container mx-auto max-w-3xl px-6 text-center md:px-8">
      <h1 class="font-serif text-3xl font-light text-foreground md:text-4xl">
        Сайт на техническом обслуживании
      </h1>
      <p class="mt-6 text-base leading-relaxed text-muted-foreground md:text-lg">
        Мы обновляем разделы сайта. Онлайн-бронирование проживания работает в обычном режиме — вы
        можете выбрать даты и оформить бронь.
      </p>
      <div class="mt-10">
        <a
          :href="BOOKING_URL"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-flex rounded-full bg-primary px-10 py-3.5 text-sm font-semibold uppercase tracking-wide text-primary-foreground transition-transform duration-300 hover:scale-[1.02] hover:bg-primary/90"
        >
          Перейти к бронированию
        </a>
      </div>
    </div>
  </section>
</template>
