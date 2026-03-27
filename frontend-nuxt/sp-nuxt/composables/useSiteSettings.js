import { SiteSettingsApi } from "~/utils/api";

export const useSiteSettings = (options = {}) => {
  const { data, error, refresh } = useAsyncData("site-settings", () => {
    return SiteSettingsApi.getList()
  }, {
    default: () => ({
      site_active: true,
      nav_show_services: true,
      nav_show_tours: true,
    }),
    server: true,
    ...options,
  })

  return {
    data,
    error,
    refresh,
  }
}
