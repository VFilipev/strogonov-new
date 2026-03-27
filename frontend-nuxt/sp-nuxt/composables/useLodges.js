import { LodgesApi, LodgeTypesApi } from "~/utils/api";
import { useAsyncResourceById, useNormalizedAsyncList } from "./useAsyncApiResource";

export const useLodge = (id, options = {}) => {
  const { data: lodge, error: lodgeError, refresh, pending } = useAsyncResourceById(
    "lodge",
    id,
    (i) => LodgesApi.getById(i),
    options,
  );

  return {
    lodge,
    lodgeError,
    refresh,
    pending,
  };
};

export const useLodgeTypes = (options = {}) => {
  const { list: types, error: typesError, refresh, pending } = useNormalizedAsyncList(
    "lodge-types",
    () => LodgeTypesApi.getList(),
    options,
  );

  return {
    types,
    typesError,
    refresh,
    pending,
  };
};
