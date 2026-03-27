import { computed } from "vue";
import { normalizeListResponse } from "~/utils/api";

export function useNormalizedAsyncList(key, fetcher, options = {}) {
  const { normalize = normalizeListResponse, ...asyncOptions } = options;
  const { data, error, refresh, pending } = useAsyncData(key, fetcher, {
    default: () => [],
    server: true,
    ...asyncOptions,
  });
  const list = computed(() => normalize(data.value));
  return { data, list, error, refresh, pending };
}

export function useAsyncResourceById(keyPrefix, id, fetcher, options = {}) {
  const { data, error, refresh, pending } = useAsyncData(
    `${keyPrefix}-${id}`,
    () => fetcher(id),
    {
      default: () => null,
      server: true,
      ...options,
    },
  );
  return { data, error, refresh, pending };
}
