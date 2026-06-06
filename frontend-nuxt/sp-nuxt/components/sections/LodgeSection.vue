<script setup>
import { computed, defineAsyncComponent, onBeforeUnmount, ref, watch } from 'vue'
import { LodgeCategoriesApi, LodgesApi, LodgeTypesApi } from '~/utils/api'
import { normalizeListResponse } from '~/utils/apiHelpers'

const LodgeModal = defineAsyncComponent(() =>
  import('~/components/lodge/LodgeModal.vue')
)

const { data: lodgeTypesData } = await useAsyncData(
  'lodge-types-modal-compact',
  () => LodgeTypesApi.getList({ compact: 1 }),
  {
    default: () => [],
    server: true,
  }
)

const lodgeTypes = computed(() => normalizeListResponse(lodgeTypesData.value))

const selectedType = ref(null)
const showContent = ref(false)
const isClosing = ref(false)
const modalCategories = ref([])
const modalItems = ref([])
const loadingCategories = ref(false)
const loadingItems = ref(false)

const cardRefs = ref({})
const setCardRef = (slug) => (el) => {
  if (el) {
    cardRefs.value[slug] = el
  }
}

const modalMeta = computed(() => {
  if (!selectedType.value || !lodgeTypes.value) return null

  const type = lodgeTypes.value.find((t) => t.slug === selectedType.value || t.id === selectedType.value)
  if (!type) return null

  return {
    title: type.name,
    subtitle: type.subtitle || type.description || '',
    heroImage: type.hero_image_webp_url || type.hero_image_url || type.hero_image_variants?.main,
    heroImageVariants: type.hero_image_variants,
  }
})

const isModularType = (type) => {
  if (!type) return false
  return type.slug === 'modulnye-doma' || String(type.name || '').toLowerCase().includes('модульн')
}

const mapLodgeToModalItem = (lodge, houseType, selectedCategoryId = null) => {
  const categories = lodge.categories || []
  const selectedCategory = selectedCategoryId
    ? categories.find((item) => Number(item.id) === Number(selectedCategoryId))
    : null
  const primaryCategory = selectedCategory || categories[0] || null

  return {
    id: lodge.id,
    name: lodge.name,
    slug: lodge.slug,
    description: lodge.short_description || '',
    capacityNum: lodge.capacity,
    area: parseFloat(lodge.area) || 0,
    priceFrom: parseFloat(lodge.price_from) || 0,
    quantity: Number(lodge.quantity || 0),
    houseType,
    categories,
    category: primaryCategory?.name || null,
    images: lodge.images?.map((img) =>
      img.image_webp_url || img.image_url || img.image_variants?.card
    ) || [],
    imageVariants: lodge.images?.map(img => img.image_variants) || [],
  }
}

const loadCategories = async (typeId) => {
  loadingCategories.value = true
  try {
    const data = await LodgeCategoriesApi.getList({ lodge_type: typeId })
    modalCategories.value = normalizeListResponse(data)
  } finally {
    loadingCategories.value = false
  }
}

const loadLodges = async (typeId, categoryId = null) => {
  loadingItems.value = true
  try {
    const filter = { lodge_type: typeId }
    if (categoryId) {
      filter.category = categoryId
    }
    const data = await LodgesApi.getList(filter)
    const selectedTypeData = lodgeTypes.value.find((t) => t.id === typeId || t.slug === selectedType.value)
    const houseType = isModularType(selectedTypeData) ? 'modular' : 'wooden'
    modalItems.value = normalizeListResponse(data).map((lodge) =>
      mapLodgeToModalItem(lodge, houseType, categoryId)
    )
  } finally {
    loadingItems.value = false
  }
}

const isOpen = computed(() => !!selectedType.value)

const setCardVars = (slug) => {
  if (!process.client) return
  const cardEl = cardRefs.value[slug]
  if (!cardEl) return
  const rect = cardEl.getBoundingClientRect()
  if (!rect) return
  document.documentElement.style.setProperty('--card-top', `${rect.top}px`)
  document.documentElement.style.setProperty('--card-left', `${rect.left}px`)
  document.documentElement.style.setProperty('--card-width', `${rect.width}px`)
  document.documentElement.style.setProperty('--card-height', `${rect.height}px`)
}

const handleTypeClick = (slug) => {
  if (selectedType.value) return
  setCardVars(slug)
  selectedType.value = slug
}

const onTypeSelected = async (typeSlug) => {
  const type = lodgeTypes.value.find((item) => item.slug === typeSlug || item.id === typeSlug)
  if (!type) return
  modalCategories.value = []
  modalItems.value = []
  if (isModularType(type)) {
    await loadCategories(type.id)
    const firstCategory = modalCategories.value[0]
    if (firstCategory?.id) {
      await loadLodges(type.id, firstCategory.id)
      return
    }
  }
  await loadLodges(type.id)
}

const handleModalCategoryChange = async (categoryValue) => {
  if (!selectedType.value) return
  const type = lodgeTypes.value.find((item) => item.slug === selectedType.value || item.id === selectedType.value)
  if (!type || !isModularType(type)) return

  const category = modalCategories.value.find((item) =>
    String(item.slug || item.id) === String(categoryValue)
  )
  if (!category?.id) return
  await loadLodges(type.id, category.id)
}

const handleClose = () => {
  showContent.value = false
  isClosing.value = true
  setTimeout(() => {
    selectedType.value = null
    modalCategories.value = []
    modalItems.value = []
    isClosing.value = false
  }, 800)
}

watch(selectedType, (value) => {
  if (!process.client) return
  if (value) {
    document.body.style.overflow = 'hidden'
    setTimeout(() => (showContent.value = true), 500)
  } else {
    document.body.style.overflow = ''
    showContent.value = false
  }
})

watch(selectedType, async (value) => {
  if (!value) return
  await onTypeSelected(value)
})

onBeforeUnmount(() => {
  if (process.client) {
    document.body.style.overflow = ''
  }
})
</script>

<template>
  <section id="lodge" class="bg-background py-20">
    <div class="container mx-auto px-6 md:px-8">
      <div class="animate-fade-in mb-12 text-center">
        <h2 class="mb-4 text-4xl font-serif text-primary md:text-5xl">Проживание</h2>
        <p class="mx-auto max-w-2xl text-lg text-muted-foreground">Выберите подходящий для вас вариант размещения</p>
      </div>

      <div v-if="lodgeTypes && lodgeTypes.length > 0" class="relative mb-8 grid gap-4 md:grid-cols-2">
        <div
          v-for="type in lodgeTypes"
          :key="type.id"
          :ref="setCardRef(type.slug)"
          class="group relative cursor-pointer overflow-hidden rounded-2xl border border-border/60 bg-white/80"
          :class="[
            selectedType === type.slug ? '!invisible !transition-none' : '',
            selectedType && selectedType !== type.slug ? 'pointer-events-none opacity-30 transition-opacity duration-300' : 'hover:scale-[1.02] hover:shadow-2xl transition-all duration-300',
          ]"
          @click="handleTypeClick(type.slug)"
        >
          <div class="relative h-[400px]">
            <NuxtImg
              :src="type.hero_image_webp_url || type.hero_image_url || type.hero_image_variants?.card"
              :alt="type.name"
              :width="626"
              :height="456"
              :quality="75"
              loading="lazy"
              sizes="626px"
              class="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
            <div class="absolute inset-0 flex flex-col justify-end p-8">
              <h3 class="mb-3 text-3xl font-serif text-white md:text-4xl">{{ type.name }}</h3>
              <p class="mb-4 text-lg text-white/90">{{ type.subtitle || type.description }}</p>
              <div class="text-sm text-white/80">Нажмите, чтобы узнать больше</div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="relative mb-8 grid gap-4 md:grid-cols-2">
        <div class="h-[400px] animate-pulse rounded-2xl bg-gray-200" />
        <div class="h-[400px] animate-pulse rounded-2xl bg-gray-200" />
      </div>

      <ClientOnly>
        <LodgeModal
          :open="isOpen"
          :is-closing="isClosing"
          :show-content="showContent"
          :meta="modalMeta || {}"
          :items="modalItems"
          :categories="modalCategories"
          :loading-items="loadingItems || loadingCategories"
          @category-change="handleModalCategoryChange"
          @close="handleClose"
        />
        <template #fallback>
          <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
            <div class="text-white">Загрузка...</div>
          </div>
        </template>
      </ClientOnly>
    </div>
  </section>
</template>

