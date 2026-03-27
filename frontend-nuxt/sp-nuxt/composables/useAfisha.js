import afishaPlaceholder from '~/assets/resort/afisha-placeholder.svg'
import { AfishaApi } from "~/utils/api";

function normalizeAfishaItem(item) {
  if (!item) return item
  return {
    ...item,
    image: item.image || afishaPlaceholder,
  }
}

export const useAfisha = (options = {}) => {
  const { data, error, refresh, pending } = useAsyncData("afisha", () => {
    return AfishaApi.getList()
  }, {
    default: () => ({ main_events: [], masterclasses: [] }),
    ...options,
  })

  const mainEvents = computed(() => {
    const v = data.value
    if (!v || !Array.isArray(v.main_events)) return []
    return v.main_events.map(normalizeAfishaItem)
  })

  const masterclasses = computed(() => {
    const v = data.value
    if (!v || !Array.isArray(v.masterclasses)) return []
    return v.masterclasses.map(normalizeAfishaItem)
  })

  return {
    data,
    mainEvents,
    masterclasses,
    error,
    pending,
    refresh,
  }
}
