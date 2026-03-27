import { StatisticsApi } from "~/utils/api";
import { useNormalizedAsyncList } from "./useAsyncApiResource";

export const useStatistics = (options = {}) => {
  const { data, list: statistics, error, refresh, pending } = useNormalizedAsyncList(
    "statistics",
    () => StatisticsApi.getList(),
    { default: () => [], server: false, ...options },
  );

  return {
    data,
    statistics,
    error,
    refresh,
    pending,
  };
};
