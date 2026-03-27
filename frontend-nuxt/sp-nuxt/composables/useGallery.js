import { computed } from "vue";
import { GalleryApi } from "~/utils/api";
import { useNormalizedAsyncList } from "./useAsyncApiResource";

export const useGallery = (options = {}) => {
  const { position = null, ordering = "order", ...asyncOptions } = options;

  const { data, list: galleryImages, error, refresh, pending } = useNormalizedAsyncList(
    `gallery-${position || "all"}-${ordering}`,
    () => GalleryApi.getList({ position, ordering }),
    { default: () => [], server: false, ...asyncOptions },
  );

  const getImagesByPosition = (pos) =>
    computed(() => galleryImages.value.filter((img) => img.position === pos));

  const getImagesByColumn = (column) =>
    computed(() =>
      galleryImages.value.filter((img) => img.column === column && img.position === "main"),
    );

  return {
    data,
    galleryImages,
    error,
    refresh,
    pending,
    getImagesByPosition,
    getImagesByColumn,
  };
};
