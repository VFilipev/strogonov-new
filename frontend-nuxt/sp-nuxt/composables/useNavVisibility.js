export function useNavVisibility() {
  const { data: siteSettings } = useSiteSettings()

  const showServicesNav = computed(
    () => siteSettings.value?.nav_show_services !== false,
  )
  const showToursNav = computed(() => siteSettings.value?.nav_show_tours !== false)

  return { showServicesNav, showToursNav, siteSettings }
}
