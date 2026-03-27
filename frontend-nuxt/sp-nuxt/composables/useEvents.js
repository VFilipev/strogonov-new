import { EventTypesApi } from "~/utils/api";
import { useAsyncResourceById, useNormalizedAsyncList } from "./useAsyncApiResource";

export const useEvents = (options = {}) => {
  const { list: eventTypes, error: eventTypesError, refresh, pending } = useNormalizedAsyncList(
    "event-types",
    () => EventTypesApi.getList(),
    { default: () => [], ...options },
  );

  return {
    eventTypes,
    eventTypesError,
    refresh,
    pending,
  };
};

export const useEventType = (id, options = {}) => {
  const { data: eventType, error: eventTypeError, refresh, pending } = useAsyncResourceById(
    "event-type",
    id,
    (i) => EventTypesApi.getById(i),
    options,
  );

  return {
    eventType,
    eventTypeError,
    refresh,
    pending,
  };
};
