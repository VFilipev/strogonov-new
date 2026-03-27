<script setup>
import { onBeforeUnmount, ref, watch } from 'vue'
import { Menu, Phone, X } from 'lucide-vue-next'
import logo from '~/assets/resort/logo.webp'
import nac from '~/assets/resort/nac.webp'

const props = defineProps({
  activePage: {
    type: String,
    default: '',
  },
  compact: {
    type: Boolean,
    default: false,
  },
})

const mobileMenuOpen = ref(false)

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

const getLinkClass = (page) =>
  props.activePage === page
    ? 'font-semibold text-primary-foreground underline decoration-primary-foreground/50 underline-offset-4'
    : 'text-primary-foreground transition-all duration-300 hover:translate-y-[-2px] hover:text-primary-foreground/80'

const handleWindowKeydown = (event) => {
  if (event.key === 'Escape') {
    closeMobileMenu()
  }
}

watch(mobileMenuOpen, (isOpen) => {
  if (!import.meta.client) return
  document.body.style.overflow = isOpen ? 'hidden' : ''
})

if (import.meta.client) {
  window.addEventListener('keydown', handleWindowKeydown)
}

onBeforeUnmount(() => {
  closeMobileMenu()
  if (import.meta.client) {
    document.body.style.overflow = ''
    window.removeEventListener('keydown', handleWindowKeydown)
  }
})

const { showServicesNav, showToursNav } = useNavVisibility()
</script>

<template>
  <header class="fixed left-0 right-0 top-0 z-50 bg-primary/95 shadow backdrop-blur-md">
    <nav class="px-4 md:px-8" :class="compact ? 'py-1.5 md:py-1' : 'py-2'">
      <div class="container mx-auto flex items-center justify-between gap-4">
        <div class="flex items-center gap-4 md:gap-8">
          <div class="flex items-center">
            <NuxtLink to="/" class="inline-flex items-center">
              <NuxtImg
                :src="logo"
                alt="Строгановские Просторы"
                class="transition-transform duration-300 hover:scale-105"
                :class="compact ? 'h-9 md:h-10' : 'h-10 md:h-12'"
                fetchpriority="high"
                decoding="async"
                sizes="140px"
              />
            </NuxtLink>
            <div
              class="mx-[0.6rem] w-px bg-primary-foreground/40 md:mx-[0.8rem]"
              :class="compact ? 'h-10 md:h-12' : 'h-12 md:h-14'"
            />
            <NuxtImg
              :src="nac"
              alt="Национальные проекты"
              :class="compact ? 'h-10 md:h-12' : 'h-12 md:h-14'"
              decoding="async"
              sizes="120px"
            />
          </div>

          <div class="hidden items-center gap-6 lg:flex">
            <NuxtLink :class="getLinkClass('complain')" to="/complain">ваше мнение</NuxtLink>
            <NuxtLink :class="getLinkClass('lodge')" to="/lodge">дома</NuxtLink>
            <a v-if="showServicesNav" :class="getLinkClass('services')" href="/#active">услуги</a>
            <NuxtLink v-if="showToursNav" :class="getLinkClass('tours')" to="/tours">туры</NuxtLink>
            <NuxtLink :class="getLinkClass('events')" to="/event-calculator">афиша и мероприятия</NuxtLink>
          </div>
        </div>

        <div class="hidden items-center gap-4 md:flex">
          <a
            href="tel:+73422333332"
            class="inline-flex items-center gap-2 text-primary-foreground transition-transform duration-300 hover:scale-105 hover:text-primary-foreground/80"
          >
            <Phone class="h-5 w-5" />
            <span class="hidden lg:inline">+7 (342) 2-33-33-32</span>
          </a>
        </div>

        <div class="flex items-center md:hidden">
          <button
            class="flex h-10 w-10 items-center justify-center rounded-full border border-primary-foreground/70 bg-black/20 text-primary-foreground backdrop-blur-sm transition-colors hover:bg-primary-foreground/15"
            :aria-label="mobileMenuOpen ? 'Закрыть меню' : 'Открыть меню'"
            :aria-expanded="mobileMenuOpen"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <X v-if="mobileMenuOpen" class="h-5 w-5" />
            <Menu v-else class="h-5 w-5" />
          </button>
        </div>
      </div>

      <div
        v-if="mobileMenuOpen"
        class="mt-3 ml-auto w-full max-w-[360px] rounded-2xl border border-white/20 bg-primary/95 p-4 shadow-xl backdrop-blur-md md:hidden"
      >
        <div class="flex flex-col gap-3 text-primary-foreground">
          <NuxtLink :class="getLinkClass('complain')" to="/complain" @click="closeMobileMenu">ваше мнение</NuxtLink>
          <NuxtLink :class="getLinkClass('lodge')" to="/lodge" @click="closeMobileMenu">дома</NuxtLink>
          <!-- <a
            v-if="showServicesNav"
            :class="getLinkClass('services')"
            href="/#active"
            @click="closeMobileMenu"
            >услуги</a
          > -->
          <NuxtLink
            v-if="showToursNav"
            :class="getLinkClass('tours')"
            to="/tours"
            @click="closeMobileMenu"
            >туры</NuxtLink
          >
          <NuxtLink :class="getLinkClass('events')" to="/event-calculator" @click="closeMobileMenu">
            афиша и мероприятия
          </NuxtLink>
          <a
            href="tel:+73422333332"
            class="mt-2 inline-flex w-fit items-center gap-2 text-primary-foreground transition-transform duration-300 hover:scale-105 hover:text-primary-foreground/80"
            @click="closeMobileMenu"
          >
            <Phone class="h-5 w-5" />
            <span>+7 (342) 2-33-33-32</span>
          </a>
        </div>
      </div>
    </nav>
  </header>
</template>
