<script setup>
const config = useRuntimeConfig();
const siteUrl = config.public.siteUrl;

useHead({
  title: "Политика обработки персональных данных - Строгановские Просторы",
  meta: [
    {
      name: "description",
      content:
        "Политика обработки персональных данных базы отдыха Строгановские Просторы",
    },
  ],
  link: [{ rel: "canonical", href: `${siteUrl}/privacy` }],
});
</script>

<template>
  <div class="flex min-h-screen flex-col bg-background text-foreground">
    <iframe
      src="/policy.pdf"
      class="min-h-0 w-full flex-1 border-0 bg-muted/30"
      title="Политика обработки персональных данных"
    />
  </div>
</template>
