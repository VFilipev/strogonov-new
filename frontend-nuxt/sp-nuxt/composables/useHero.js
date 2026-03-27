import { HeroApi } from "~/utils/api";

export const useHero = (options = {}) => {
  const { data, error, refresh } = useAsyncData("hero", () => {
    return HeroApi.getList()
  }, {
    default: () => ({ images: [] }),
    server: true,
    ...options,
  })

  return {
    data,
    error,
    refresh,
  }
}

