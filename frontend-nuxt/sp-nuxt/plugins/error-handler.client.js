export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.hook("app:error", (error) => {
    console.error("App error:", error);
  });

  nuxtApp.hook("vue:error", (error, instance, info) => {
    console.error("Vue error:", error, info);
  });
});
