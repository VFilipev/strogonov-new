<script setup>
import { ref, onMounted } from 'vue'
import snowmobileImage from '~/assets/resort/active-snowmobile.webp'
import skatingImage from '~/assets/resort/active-skating.webp'
import skiingImage from '~/assets/resort/active-skiing.webp'
import skatingVideo from '~/assets/resort/active-skating-video.mp4'
import snowmobileVideo from '~/assets/resort/active-snowmobile-video.mp4'

const FALLBACK = [
  { image: snowmobileImage, video: snowmobileVideo, title: 'Снегоходы', description: 'Зимние приключения на скоростных снегоходах' },
  { image: skatingImage, video: skatingVideo, title: 'Коньки', description: 'Катание на коньках на открытом катке' },
  { image: skiingImage, title: 'Лыжи', description: 'Лыжные прогулки по живописным трассам' },
]

const { activities: apiList } = useActivities('active')

const activities = computed(() => {
  const list = apiList.value
  if (!list.length) return FALLBACK
  return list.map((a) => ({
    id: a.id,
    image: a.image_webp_url || a.image_url,
    video: a.video_url || null,
    title: a.title,
    description: a.description,
  }))
})

const hoveredIndex = ref(null)
const videoRefs = ref([])
const videoUnlocked = ref(false)

const setVideoRef = (index) => (el) => {
  if (el && process.client) {
    videoRefs.value[index] = el
  }
}

const unlockVideo = () => {
  if (!process.client) return
  videoUnlocked.value = true
}

const handleMouseEnter = (index) => {
  if (!process.client) return

  if (!videoUnlocked.value) {
    unlockVideo()
  }

  hoveredIndex.value = index
  const video = videoRefs.value[index]
  const item = activities.value[index]

  if (item?.video && video && videoUnlocked.value) {
    if (!video.paused) {
      return
    }

    if (video.readyState >= 2) {
      video.currentTime = 0
      const playPromise = video.play()
      if (playPromise !== undefined) {
        playPromise
          .then(() => {})
          .catch(() => {})
      }
    } else {
      const onLoadedData = () => {
        if (hoveredIndex.value === index && video) {
          video.currentTime = 0
          const playPromise = video.play()
          if (playPromise !== undefined) {
            playPromise.catch(() => {})
          }
        }
        video.removeEventListener('loadeddata', onLoadedData)
      }

      if (!video.hasAttribute('data-listener-added')) {
        video.addEventListener('loadeddata', onLoadedData)
        video.setAttribute('data-listener-added', 'true')
      }
    }
  }
}

const handleMouseLeave = (index) => {
  if (!process.client) return

  const video = videoRefs.value[index]
  if (video) {
    video.pause()
    video.currentTime = 0
  }
  hoveredIndex.value = null
}

onMounted(() => {
  if (process.client) {
    const testVideo = document.createElement('video')
    testVideo.muted = true
    testVideo.playsInline = true
    const testPromise = testVideo.play()
    if (testPromise !== undefined) {
      testPromise
        .then(() => {
          videoUnlocked.value = true
        })
        .catch(() => {})
    }
  }
})
</script>

<template>
  <ClientOnly>
    <section id="active" class="bg-background py-20">
      <div class="container mx-auto px-6 md:px-8">
        <div class="animate-fade-in mb-12 text-center">
          <h2 class="mb-4 text-4xl font-serif text-primary md:text-5xl">Активный отдых</h2>
          <p class="mx-auto max-w-2xl text-lg text-muted-foreground">
            Почувствуйте прилив адреналина и испытайте незабываемые эмоции среди уральской природы
          </p>
        </div>

        <div class="grid gap-6 md:grid-cols-3">
          <div
            v-for="(activity, index) in activities"
            :key="activity.id ?? activity.title"
            class="group relative overflow-hidden rounded-2xl border border-border/50 bg-white/70 transition-all duration-500 hover:scale-105 hover:shadow-2xl animate-fade-in"
            :style="{ animationDelay: `${index * 150}ms` }"
            @click="unlockVideo"
            @mouseenter="handleMouseEnter(index)"
            @mouseleave="handleMouseLeave(index)"
          >
            <div class="relative h-[400px] overflow-hidden">
              <NuxtImg
                :src="activity.image"
                :alt="activity.title"
                :width="406"
                :height="541"
                :quality="75"
                loading="lazy"
                sizes="406px"
                class="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
              />
              <video
                v-if="activity.video"
                :ref="setVideoRef(index)"
                :src="activity.video"
                muted
                loop
                playsinline
                preload="metadata"
                class="absolute inset-0 h-full w-full object-cover transition-all duration-1000 ease-out"
                :class="hoveredIndex === index ? 'opacity-100 scale-100' : 'opacity-0 scale-105'"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
              <div class="absolute inset-0 flex flex-col justify-end p-6 text-white">
                <h3 class="mb-2 text-2xl font-semibold transition-transform duration-300 group-hover:-translate-y-1">{{ activity.title }}</h3>
                <p class="line-clamp-4 text-white/90 transition-all duration-300 group-hover:-translate-y-1">{{ activity.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </ClientOnly>
</template>
