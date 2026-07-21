// @nuxtjs/robots выставляет X-Robots-Tag по пути запроса ещё до рендера,
// поэтому 404/500-ответы (в т.ч. страница ошибки при устаревшем чанке)
// уходили с "index, follow" в заголовке, хотя error.vue ставит noindex
// в meta. Заголовок обычно приоритетнее meta-тега — из-за этого битые
// страницы попадали в индекс Яндекса. Переопределяем заголовок по факту
// финального статус-кода ответа.
export default defineNitroPlugin((nitroApp) => {
  nitroApp.hooks.hook("beforeResponse", (event) => {
    if (event.node.res.statusCode >= 400) {
      event.node.res.setHeader("X-Robots-Tag", "noindex, nofollow");
    }
  });
});
