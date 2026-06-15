// Генерирует микроразметку BreadcrumbList (Schema.org, JSON-LD) для навигационной
// цепочки в выдаче Яндекса/Google.
//
// Использование на странице:
//   useBreadcrumbs([
//     { name: "Коттеджи и дома", path: "/doma" },
//   ]);
//
// "Главная" добавляется автоматически первым элементом. URL формируются
// абсолютными на основе siteUrl, домен совпадает с адресом сайта.
//
// Требования Яндекса, которые здесь учтены:
//   - формат JSON-LD, тип BreadcrumbList;
//   - поля name (Text), item (URL), position (Integer);
//   - name >= 4 символов (иначе элемент может выпасть из цепочки);
//   - рекомендуется до 3 элементов в цепочке.
export const useBreadcrumbs = (items) => {
  const config = useRuntimeConfig();
  const siteUrl = config.public.siteUrl;

  const absolute = (path) => {
    if (!path) return siteUrl;
    if (/^https?:\/\//.test(path)) return path;
    return `${siteUrl}${path.startsWith("/") ? path : `/${path}`}`;
  };

  const chain = [{ name: "Главная", path: "/" }, ...items];

  const itemListElement = chain.map((crumb, index) => ({
    "@type": "ListItem",
    position: index + 1,
    name: crumb.name,
    item: absolute(crumb.path),
  }));

  useStructuredData({
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement,
  });
};
