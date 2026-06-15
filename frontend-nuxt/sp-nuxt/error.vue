<template>
  <div class="error-page">
    <div class="error-card">
      <p class="error-code">{{ error?.statusCode || 500 }}</p>
      <h1 class="error-title">Что-то пошло не так</h1>
      <p class="error-text">
        Страница временно недоступна или была обновлена.
        Попробуйте обновить страницу или вернуться на главную.
      </p>
      <div class="error-actions">
        <button class="error-btn error-btn--primary" @click="reload">
          Обновить
        </button>
        <button class="error-btn" @click="goHome">
          На главную
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  error: {
    type: Object,
    default: () => ({}),
  },
});

useHead({
  title: "Ошибка",
  titleTemplate: "%s - Строгановские Просторы",
  meta: [{ name: "robots", content: "noindex, nofollow" }],
});

const isChunkError = computed(() => {
  const msg = props.error?.message || "";
  return /dynamically imported module|Importing a module script failed|ChunkLoadError/i.test(
    msg
  );
});

function reload() {
  window.location.reload();
}

function goHome() {
  clearError({ redirect: "/" });
}

onMounted(() => {
  if (isChunkError.value && import.meta.client) {
    const key = "sp-chunk-reload";
    if (!sessionStorage.getItem(key)) {
      sessionStorage.setItem(key, "1");
      window.location.reload();
    }
  } else if (import.meta.client) {
    sessionStorage.removeItem("sp-chunk-reload");
  }
});
</script>

<style scoped>
.error-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: #f7f6f3;
}

.error-card {
  max-width: 480px;
  text-align: center;
}

.error-code {
  font-size: 64px;
  font-weight: 300;
  line-height: 1;
  margin: 0 0 8px;
  color: #1f2a24;
}

.error-title {
  font-size: 24px;
  font-weight: 500;
  margin: 0 0 12px;
  color: #1f2a24;
}

.error-text {
  font-size: 16px;
  line-height: 1.5;
  color: #5a625d;
  margin: 0 0 24px;
}

.error-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.error-btn {
  padding: 12px 24px;
  border-radius: 8px;
  border: 1px solid #1f2a24;
  background: transparent;
  color: #1f2a24;
  font-size: 15px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.error-btn:hover {
  opacity: 0.8;
}

.error-btn--primary {
  background: #1f2a24;
  color: #fff;
}
</style>
