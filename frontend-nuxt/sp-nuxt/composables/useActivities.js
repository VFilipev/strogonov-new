import { ActivitiesApi } from "~/utils/api";
import { useAsyncResourceById, useNormalizedAsyncList } from "./useAsyncApiResource";

export const useActivities = (category, options = {}) => {
  const { data, list: activities, error, refresh, pending } = useNormalizedAsyncList(
    `activities-${category}`,
    () => ActivitiesApi.getList({ category }),
    { default: () => null, ...options },
  );

  return {
    activities,
    error,
    refresh,
    data,
    pending,
  };
};

export const useActivity = (id, options = {}) => {
  const { data: activity, error, refresh, pending } = useAsyncResourceById(
    "activity",
    id,
    (i) => ActivitiesApi.getById(i),
    options,
  );

  return {
    activity,
    error,
    refresh,
    pending,
  };
};
