<template>
  <noscript>
    <div>
      <img
        :src="`https://mc.yandex.ru/watch/${yandexMetrikaId}`"
        style="position: absolute; left: -9999px"
        alt=""
      >
    </div>
  </noscript>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
  <ClientOnly>
    <PrivacyConsentBanner />
  </ClientOnly>
</template>

<script setup>
const {
  public: { yandexMetrikaId },
} = useRuntimeConfig();
</script>
