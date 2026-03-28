<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import { useRoute } from "vue-router";
import WoodenHousesSection from "~/components/lodge/WoodenHousesSection.vue";
import ModularHousesSection from "~/components/lodge/ModularHousesSection.vue";
import SiteHeaderNavigation from "~/components/sections/SiteHeaderNavigation.vue";
import { useLodgeTypes } from "~/composables/useLodges";
import { findLodgeTypeByKind, transformLodgeForSection } from "~/utils/lodge";

const { types: lodgeTypes } = useLodgeTypes();

const houseList = computed(() => {
  const cottagesType = findLodgeTypeByKind(lodgeTypes.value, "cottages");
  if (!cottagesType?.lodges?.length) return [];
  return cottagesType.lodges.map((l) => transformLodgeForSection(l));
});

const modularHouseList = computed(() => {
  const modularType = findLodgeTypeByKind(lodgeTypes.value, "modular");
  if (!modularType?.lodges?.length) return [];
  return modularType.lodges.map((l) => transformLodgeForSection(l));
});

const woodenSectionRef = ref(null);
const modularSectionRef = ref(null);

const route = useRoute();

const initialWoodenHouseId = computed(() => {
  if (route.query.houseType === "wooden" && route.query.houseId) {
    const id = parseInt(route.query.houseId, 10);
    return Number.isNaN(id) ? undefined : id;
  }
  return undefined;
});

const initialModularHouseId = computed(() => {
  if (route.query.houseType === "modular" && route.query.houseId) {
    const id = parseInt(route.query.houseId, 10);
    return Number.isNaN(id) ? undefined : id;
  }
  return undefined;
});

onMounted(async () => {
  if (!import.meta.client) return;

  const houseId = route.query.houseId;
  const houseType = route.query.houseType;

  if (houseId && houseType) {
    await nextTick();

    if (houseType === "modular") {
      setTimeout(() => {
        const modularSection = document.querySelector('[data-section="modular"]');
        if (modularSection) {
          const yOffset = -80;
          const y = modularSection.getBoundingClientRect().top + window.pageYOffset + yOffset;
          window.scrollTo({ top: y, behavior: "smooth" });
        }
      }, 500);
    } else {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  } else {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
});
</script>

<template>
  <div>
    <SiteHeaderNavigation active-page="lodge" />
    <main class="pt-20 lg:pt-32 main-bg">
      <WoodenHousesSection
        ref="woodenSectionRef"
        :houses="houseList"
        title="Деревянные дома"
        :initial-house-id="initialWoodenHouseId"
      />
      <ModularHousesSection
        ref="modularSectionRef"
        :houses="modularHouseList"
        title="Модульные дома"
        :initial-house-id="initialModularHouseId"
      />
    </main>
  </div>
</template>

<style scoped>
.main-bg {
  background-color: #f5f3f1;
}
</style>
