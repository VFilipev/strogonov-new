import { BenefitsApi, MealTypesApi, RestaurantApi, RestaurantImagesApi } from "~/utils/api";

export const useRestaurant = () => ({
  getRestaurant: () => RestaurantApi.getList(),
  getRestaurantImages: () => RestaurantImagesApi.getList(),
  getMealTypes: () => MealTypesApi.getList(),
  getBenefits: () => BenefitsApi.getList(),
});
