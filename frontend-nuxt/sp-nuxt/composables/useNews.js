import { NewsApi } from "~/utils/api";
import { useAsyncResourceById, useNormalizedAsyncList } from "./useAsyncApiResource";

export const useNews = (options = {}) => {
  const { data: news, list: newsList, error, refresh, pending } = useNormalizedAsyncList(
    "news",
    () => NewsApi.getList(),
    { default: () => [], ...options },
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
