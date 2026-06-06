import { NewsApi } from "~/utils/api";
import { normalizeListResponse } from "~/utils/apiHelpers";
import { useAsyncResourceById, useNormalizedAsyncList } from "./useAsyncApiResource";

export const useNews = (options = {}) => {
  const { limit, ...asyncOptions } = options;
  const cacheKey = limit ? `news-${limit}` : "news";

  const { data: news, list: newsList, error, refresh, pending } = useNormalizedAsyncList(
    cacheKey,
    async () => {
      const data = await NewsApi.getList();
      const items = normalizeListResponse(data);
      return limit ? items.slice(0, limit) : items;
    },
    { default: () => [], ...asyncOptions },
  );

  return {
    news,
    newsList,
    newsError: error,
    refresh,
    pending,
  };
};

export const useNewsItem = (id, options = {}) => {
  const { data: newsItem, error: newsItemError, refresh, pending } = useAsyncResourceById(
    "news",
    id,
    (i) => NewsApi.getById(i),
    options,
  );

  return {
    newsItem,
    newsItemError,
    refresh,
    pending,
  };
};
