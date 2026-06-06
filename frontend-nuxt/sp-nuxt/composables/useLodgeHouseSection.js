import { ref, computed, watch } from "vue";

const prefetchedUrls = new Set();

function prefetchUrl(url) {
  if (!url || prefetchedUrls.has(url)) return;
  prefetchedUrls.add(url);
  const img = new Image();
  img.src = url;
}

function collectHouseImageUrls(house) {
  if (!house) return [];
  const urls = [];
  if (house.img) urls.push(house.img);
  if (house.photo_gallery_set?.length) {
    for (const photo of house.photo_gallery_set) {
      if (photo?.img) urls.push(photo.img);
    }
  }
  return urls;
}

function schedulePrefetch(run) {
  if (typeof window === "undefined") return;
  if (typeof requestIdleCallback !== "undefined") {
    requestIdleCallback(() => run(), { timeout: 1800 });
  } else {
    setTimeout(run, 150);
  }
}

function preloadAdjacentHouseImages(houses, index) {
  if (!houses?.length || houses.length <= 1 || typeof window === "undefined") return;
  const len = houses.length;
  const nextIndex = index === len - 1 ? 0 : index + 1;
  const prevIndex = index === 0 ? len - 1 : index - 1;
  const targets =
    nextIndex === prevIndex ? [houses[nextIndex]] : [houses[nextIndex], houses[prevIndex]];
  const urls = new Set();
  for (const house of targets) {
    for (const u of collectHouseImageUrls(house)) urls.add(u);
  }
  schedulePrefetch(() => {
    urls.forEach(prefetchUrl);
  });
}

export function useLodgeHouseSection(props) {
  const selectHouseIndex = ref(0);
  const selectedHouse = computed(() => props.houses[selectHouseIndex.value]);

  const photoViewerOpen = ref(false);
  const photoViewerImages = ref([]);
  const photoViewerInitialIndex = ref(0);

  const getAllHouseImages = (house) => {
    const images = [];
    if (house.viewerImg || house.img) {
      images.push(house.viewerImg || house.img);
    }
    if (house.photo_gallery_set?.length) {
      house.photo_gallery_set.forEach((photo) => {
        if (photo.viewerImg || photo.img) {
          images.push(photo.viewerImg || photo.img);
        }
      });
    }
    return images;
  };

  const openPhotoViewer = (house, imageIndex = 0) => {
    const images = getAllHouseImages(house);
    if (images.length > 0) {
      photoViewerImages.value = images;
      photoViewerInitialIndex.value = imageIndex;
      photoViewerOpen.value = true;
    }
  };

  const closePhotoViewer = () => {
    photoViewerOpen.value = false;
  };

  const setHouseIndex = (houseId) => {
    if (houseId == null) return;
    const index = props.houses.findIndex(
      (house) => Number(house.id) === Number(houseId)
    );
    if (index !== -1) {
      selectHouseIndex.value = index;
    }
  };

  watch(
    [() => props.houses?.length, () => props.initialHouseId],
    () => {
      if (props.initialHouseId == null) return;
      if (!props.houses?.length) return;
      setHouseIndex(props.initialHouseId);
    },
    { immediate: true }
  );

  watch(
    [selectHouseIndex, () => props.houses],
    () => {
      preloadAdjacentHouseImages(props.houses, selectHouseIndex.value);
    },
    { flush: "post", immediate: true }
  );

  const swiperBreakpoints = {
    0: { slidesPerView: 2, spaceBetween: 12 },
    640: { slidesPerView: 2, spaceBetween: 14 },
    1024: { slidesPerView: 2, spaceBetween: 16 },
  };

  const decSelectHouseIndex = () => {
    if (selectHouseIndex.value > 0) {
      selectHouseIndex.value--;
    } else {
      selectHouseIndex.value = props.houses.length - 1;
    }
  };

  const addSelectHouseIndex = () => {
    if (selectHouseIndex.value === props.houses.length - 1) {
      selectHouseIndex.value = 0;
    } else {
      selectHouseIndex.value++;
    }
  };

  return {
    selectHouseIndex,
    selectedHouse,
    photoViewerOpen,
    photoViewerImages,
    photoViewerInitialIndex,
    getAllHouseImages,
    openPhotoViewer,
    closePhotoViewer,
    decSelectHouseIndex,
    addSelectHouseIndex,
    swiperBreakpoints,
  };
}
