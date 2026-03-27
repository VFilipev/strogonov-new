export default defineNuxtConfig({
  ssr: true,

  experimental: {
    payloadExtraction: false,
    viewTransition: true,
    watcher: "chokidar-granular",
  },

  modules: [
    "@nuxtjs/tailwindcss",
    "@nuxt/image",
    "@pinia/nuxt",
    "@nuxtjs/seo",
    "@nuxtjs/critters",
  ],

  critters: {
    preload: "swap",
    pruneSource: true,
    compress: true,
  },

  css: ["~/assets/css/main.css"],

  alias: {
    "@": ".",
  },

  components: [
    {
      path: "~/components",
      pathPrefix: false,
    },
  ],

  runtimeConfig: {
    apiSecret: process.env.API_SECRET || "",

    public: {
      apiBase:
        process.env.API_BASE_URL ||
        (process.env.NODE_ENV === "production"
          ? "http://45.153.69.10:8009/api"
          : "http://localhost:8000/api"),
      siteUrl:
        process.env.SITE_URL ||
        (process.env.NODE_ENV === "production"
          ? "http://45.153.69.10:8009"
          : "http://localhost:3000"),
    },
  },

  image: {
    provider: "raw",
    providers: {
      raw: {
        provider: "~/providers/raw",
      },
    },
    domains: ["localhost", "45.153.69.10"],
    quality: 100,
    format: [],
  },

  site: {
    url: (process.env.SITE_URL || "http://localhost:3000").replace(/[§]/g, ""),
    name: "Строгановские Просторы",
    description: "Уютные коттеджи и глэмпинг на берегу камского моря",
    defaultLocale: "ru",
  },

  sitemap: {
    hostname: (process.env.SITE_URL || "http://localhost:3000").replace(/[§]/g, "").replace(/\/$/, ""),
  },

  robots: {
    allow: ["/"],
    disallow: ["/admin/", "/api/"],
    sitemap: (() => {
      const siteUrl = (process.env.SITE_URL || "http://localhost:3000").replace(/[§]/g, "");
      return `${siteUrl.replace(/\/$/, "")}/api/sitemap.xml`;
    })(),
  },

  nitro: {
    compressPublicAssets: {
      gzip: true,
      brotli: true,
    },
    prerender: {
      crawlLinks: false,
      failOnError: false,
    },
  },

  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "@/assets/scss/variables.scss" as *;',
        },
      },
    },
  },

  app: {
    head: {
      charset: "utf-8",
      viewport: "width=device-width, initial-scale=1",
      title: "Строгановские Просторы",
      titleTemplate: "%s - Строгановские Просторы",
      meta: [
        {
          name: "description",
          content:
            "Уютные коттеджи и глэмпинг на берегу камского моря. Уединённый отдых в хвойном лесу с европейским уровнем комфорта.",
        },
        {
          name: "keywords",
          content:
            "коттеджи, глэмпинг, отдых, Пермский край, база отдыха, Камское море, активный отдых, спокойный отдых",
        },
        { name: "author", content: "Строгановские Просторы" },
        { name: "language", content: "ru" },
        { property: "og:type", content: "website" },
        { property: "og:locale", content: "ru_RU" },
        { property: "og:site_name", content: "Строгановские Просторы" },
        { name: "twitter:card", content: "summary_large_image" },
      ],
      link: [
        { rel: "icon", type: "image/x-icon", href: "/favicon.ico" },
        { rel: "canonical", href: process.env.SITE_URL || "http://localhost:3000" },
        { rel: "preload", as: "font", type: "font/ttf", href: "/fonts/Lato-Light.ttf", crossorigin: "anonymous" },
        { rel: "preload", as: "font", type: "font/ttf", href: "/fonts/Lato-Regular.ttf", crossorigin: "anonymous" },
        { rel: "preload", as: "font", type: "font/ttf", href: "/fonts/Lato-Medium.ttf", crossorigin: "anonymous" },
        { rel: "preload", as: "font", type: "font/ttf", href: "/fonts/Lato-SemiBold.ttf", crossorigin: "anonymous" },
        { rel: "preload", as: "font", type: "font/ttf", href: "/fonts/Lato-Bold.ttf", crossorigin: "anonymous" },
      ],
    },
  },

  compatibilityDate: "2025-07-15",

  devtools: { enabled: true },
});
