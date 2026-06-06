<script setup>
import SiteHeaderNavigation from '~/components/sections/SiteHeaderNavigation.vue'

const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl

const documents = [
  {
    title: 'Публичная оферта средства размещения',
    href: '/documents/public-offer.pdf',
  },
  {
    title: 'Политика конфиденциальности',
    href: '/policy.pdf',
  },
  {
    title: 'Согласие на обработку персональных данных',
    href: '/documents/consent-new.pdf',
  },
  {
    title: 'Правила предоставления услуг средства размещения',
    href: '/documents/placement-rules.pdf',
  },
  {
    title: 'Правила пожарной безопасности',
    href: '/documents/fire-safety-rules.pdf',
  },
  {
    title: 'Согласие на отправку рекламный и маркетинговых материалов посредством средств связи',
    href: '/documents/consent-marketing.pdf',
  },
]

useHead({
  title: 'Документы — Строгановские Просторы',
  meta: [
    {
      name: 'description',
      content: 'Правовые документы базы отдыха Строгановские Просторы',
    },
  ],
  link: [{ rel: 'canonical', href: `${siteUrl}/documents` }],
})
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <SiteHeaderNavigation />

    <main class="px-6 pb-16 pt-20 md:pb-20 md:pt-24">
      <div class="container mx-auto">
        <h1 class="text-3xl font-serif font-light text-primary md:text-4xl">Документы</h1>

        <ul class="mt-6 space-y-3">
          <li v-for="document in documents" :key="document.href">
            <a
              :href="document.href"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-block text-lg text-foreground underline decoration-primary/40 underline-offset-4 transition-colors hover:text-primary hover:decoration-primary"
            >
              {{ document.title }}
            </a>
          </li>
        </ul>
      </div>
    </main>
  </div>
</template>
