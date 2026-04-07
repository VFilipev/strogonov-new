import { ref, computed, watch, onMounted } from "vue";

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
    if (houseId) {
      const index = props.houses.findIndex((house) => house.id === houseId);
      if (index !== -1) {
        selectHouseIndex.value = index;
      }
    }
  };

  onMounted(() => {
    if (props.initialHouseId) {
      setHouseIndex(props.initialHouseId);
    }
  });

  watch(
    () => props.initialHouseId,
    (newId) => {
      if (newId) {
        setHouseIndex(newId);
      }
    },
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
