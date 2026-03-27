<script setup>
import { computed, nextTick, ref } from 'vue'
import { useHead } from '#imports'
import { CheckCircle2, Loader2, Paperclip, Send, X } from 'lucide-vue-next'
import FooterSection from '~/components/sections/FooterSection.vue'
import SiteHeaderNavigation from '~/components/sections/SiteHeaderNavigation.vue'

const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl
const { postForm } = useAdminContentApi()

const TOPICS = [
  { value: '', label: 'Выберите тему' },
  { value: 'gratitude', label: 'Благодарность' },
  { value: 'complaint', label: 'Жалоба' },
  { value: 'question', label: 'Вопрос' },
  { value: 'suggestion', label: 'Предложение' },
  { value: 'other', label: 'Иное' },
]

const MAX_FILE_BYTES = 10 * 1024 * 1024
const ALLOWED_EXT = /\.(doc|pdf|ppt|docx|pptx|xls|xlsx|jpg|jpeg|png)$/i

const topic = ref('')
const name = ref('')
const email = ref('')
const phone = ref('')
const visitDate = ref('')
const visitTime = ref('')
const message = ref('')
const attachment = ref(null)
const attachmentName = ref('')
const attachmentError = ref('')
const fieldErrors = ref({})
const submitStatus = ref('idle')
const submitError = ref('')
const isSubmitting = ref(false)
const fileInputRef = ref(null)

function firstError(val) {
  if (!val) return ''
  if (Array.isArray(val)) return val[0] || ''
  return String(val)
}

function applyServerErrors(data) {
  if (!data || typeof data !== 'object') return
  const err = {}
  const map = {
    topic: 'topic',
    name: 'name',
    email: 'email',
    phone: 'phone',
    visit_date: 'visitDate',
    visit_time: 'visitTime',
    message: 'message',
    attachment: 'attachment',
  }
  for (const [apiKey, localKey] of Object.entries(map)) {
    if (data[apiKey]) err[localKey] = firstError(data[apiKey])
  }
  if (data.non_field_errors) {
    err.contact = firstError(data.non_field_errors)
  }
  if (Object.keys(err).length) {
    fieldErrors.value = { ...fieldErrors.value, ...err }
  }
}

const hasContact = computed(() => {
  const e = email.value.trim()
  const digits = phone.value.replace(/\D/g, '')
  return Boolean(e.length) || digits.length >= 10
})

function validateEmail(value) {
  if (!value.trim()) return true
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim())
}

function validate() {
  const err = {}
  if (!topic.value) err.topic = 'Выберите тему обращения'
  if (!name.value.trim()) err.name = 'Укажите имя'
  if (!validateEmail(email.value)) err.email = 'Некорректный e-mail'
  if (!hasContact.value) err.contact = 'Укажите e-mail или телефон для обратной связи'
  if (!message.value.trim()) err.message = 'Введите текст сообщения'
  else if (message.value.trim().length < 5) err.message = 'Сообщение слишком короткое'

  fieldErrors.value = err
  return Object.keys(err).length === 0
}

function onFileChange(event) {
  attachmentError.value = ''
  const file = event.target.files?.[0]
  if (!file) {
    attachment.value = null
    attachmentName.value = ''
    return
  }
  if (file.size > MAX_FILE_BYTES) {
    attachmentError.value = 'Файл больше 10 МБ'
    attachment.value = null
    attachmentName.value = ''
    event.target.value = ''
    return
  }
  if (!ALLOWED_EXT.test(file.name)) {
    attachmentError.value =
      'Допустимые форматы: .doc, .pdf, .ppt, .docx, .pptx, .xls, .xlsx, .jpg, .png'
    attachment.value = null
    attachmentName.value = ''
    event.target.value = ''
    return
  }
  attachment.value = file
  attachmentName.value = file.name
}

function clearFile() {
  attachment.value = null
  attachmentName.value = ''
  attachmentError.value = ''
  if (fileInputRef.value) fileInputRef.value.value = ''
}

async function onSubmit() {
  submitStatus.value = 'idle'
  submitError.value = ''
  if (!validate()) return

  const formData = new FormData()
  formData.append('topic', topic.value)
  formData.append('name', name.value.trim())
  formData.append('email', email.value.trim())
  formData.append('phone', phone.value.trim())
  formData.append('visit_date', visitDate.value || '')
  formData.append('visit_time', visitTime.value.trim())
  formData.append('message', message.value.trim())
  if (attachment.value) {
    formData.append('attachment', attachment.value)
  }

  isSubmitting.value = true
  try {
    await postForm('/guest-feedback/', formData)
    submitStatus.value = 'success'
    topic.value = ''
    name.value = ''
    email.value = ''
    phone.value = ''
    visitDate.value = ''
    visitTime.value = ''
    message.value = ''
    clearFile()
    fieldErrors.value = {}
    await nextTick()
    if (import.meta.client) {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  } catch (e) {
    const data = e?.data ?? e?.response?._data
    if (data && typeof data === 'object') {
      applyServerErrors(data)
      submitError.value =
        firstError(data.detail) ||
        firstError(data.non_field_errors) ||
        'Проверьте поля формы или попробуйте позже.'
    } else {
      submitError.value = 'Не удалось отправить форму. Проверьте соединение и попробуйте снова.'
    }
  } finally {
    isSubmitting.value = false
  }
}

useHead({
  title: 'Ваше мнение — Строгановские Просторы',
  meta: [
    {
      name: 'description',
      content:
        'Обратная связь, жалобы, вопросы и предложения. Форма обращения на базе отдыха Строгановские Просторы.',
    },
  ],
  link: [{ rel: 'canonical', href: `${siteUrl}/complain` }],
})
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <SiteHeaderNavigation active-page="complain" />

    <main
      class="px-6 pb-20 pt-[calc(6.5rem+env(safe-area-inset-top,0px))] md:pt-[calc(7.5rem+env(safe-area-inset-top,0px))]"
    >
      <div class="container mx-auto max-w-2xl">
        <!-- Успех: вместо формы -->
        <div
          v-if="submitStatus === 'success'"
          class="rounded-2xl border border-primary/20 bg-card px-6 py-12 text-center shadow-sm md:px-12 md:py-16"
          role="status"
        >
          <div class="mx-auto mb-6 flex justify-center text-primary">
            <CheckCircle2 class="h-16 w-16 md:h-20 md:w-20" aria-hidden="true" />
          </div>
          <h1 class="mb-4 font-serif text-3xl font-semibold tracking-tight text-primary md:text-4xl">
            Спасибо за обращение
          </h1>
          <p class="mx-auto max-w-lg text-pretty text-base leading-relaxed text-muted-foreground md:text-lg">
            Ваше мнение важно для нас: мы его проверим и обязательно с вами свяжемся.
          </p>
          <NuxtLink
            to="/"
            class="mt-10 inline-flex items-center justify-center rounded-full border border-primary bg-transparent px-8 py-3 text-sm font-semibold uppercase tracking-wide text-primary transition-colors hover:bg-primary hover:text-primary-foreground"
          >
            На главную
          </NuxtLink>
        </div>

        <template v-else>
          <header class="mb-10 scroll-mt-28 text-center md:mb-12 md:scroll-mt-32">
            <h1 class="mb-4 font-serif text-3xl font-semibold tracking-tight text-primary md:text-4xl">
              Ваше мнение
            </h1>
            <p class="text-pretty text-base leading-relaxed text-muted-foreground md:text-lg">
              Нам очень важна обратная связь от вас: все жалобы, вопросы и предложения разбираются
              сотрудниками компании, включая руководство. Пожалуйста, заполните форму ниже.
            </p>
          </header>

          <div
            v-if="submitError"
            class="mb-8 rounded-xl border border-destructive/30 bg-destructive/5 p-4 text-center text-sm text-destructive"
            role="alert"
          >
            {{ submitError }}
          </div>

          <form
            class="rounded-2xl border border-border bg-card p-6 shadow-sm md:p-10"
            @submit.prevent="onSubmit"
          >
          <div class="space-y-8">
            <!-- Тема -->
            <div>
              <label for="complain-topic" class="mb-2 block text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                Тема обращения <span class="text-destructive">*</span>
              </label>
              <select
                id="complain-topic"
                v-model="topic"
                class="w-full rounded-md border border-input bg-background px-3 py-2.5 text-foreground shadow-sm transition-colors focus:border-ring focus:outline-none focus:ring-2 focus:ring-ring/30"
                :class="{ 'border-destructive': fieldErrors.topic }"
              >
                <option v-for="opt in TOPICS" :key="String(opt.value)" :value="opt.value">
                  {{ opt.label }}
                </option>
              </select>
              <p v-if="fieldErrors.topic" class="mt-1.5 text-sm text-destructive">{{ fieldErrors.topic }}</p>
            </div>

            <!-- Имя -->
            <div>
              <label for="complain-name" class="mb-2 block text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                Ваше имя <span class="text-destructive">*</span>
              </label>
              <input
                id="complain-name"
                v-model="name"
                type="text"
                autocomplete="name"
                class="w-full rounded-md border border-input bg-background px-3 py-2.5 text-foreground shadow-sm transition-colors focus:border-ring focus:outline-none focus:ring-2 focus:ring-ring/30"
                :class="{ 'border-destructive': fieldErrors.name }"
              />
              <p v-if="fieldErrors.name" class="mt-1.5 text-sm text-destructive">{{ fieldErrors.name }}</p>
            </div>

            <!-- Email + телефон -->
            <div>
              <div class="grid gap-6 md:grid-cols-2">
                <div>
                  <label for="complain-email" class="mb-2 block text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                    Ваш e-mail <span class="text-destructive">*</span>
                  </label>
                  <input
                    id="complain-email"
                    v-model="email"
                    type="email"
                    autocomplete="email"
                    placeholder="Введите ваш email"
                    class="w-full rounded-md border border-input bg-background px-3 py-2.5 text-foreground shadow-sm transition-colors placeholder:text-muted-foreground/60 focus:border-ring focus:outline-none focus:ring-2 focus:ring-ring/30"
                    :class="{ 'border-destructive': fieldErrors.email || fieldErrors.contact }"
                  />
                </div>
                <div>
                  <label for="complain-phone" class="mb-2 block text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                    Ваш телефон <span class="text-destructive">*</span>
                  </label>
                  <input
                    id="complain-phone"
                    v-model="phone"
                    type="tel"
                    autocomplete="tel"
                    placeholder="+7-999-999-99-99"
                    class="w-full rounded-md border border-input bg-background px-3 py-2.5 text-foreground shadow-sm transition-colors placeholder:text-muted-foreground/60 focus:border-ring focus:outline-none focus:ring-2 focus:ring-ring/30"
                    :class="{ 'border-destructive': fieldErrors.contact || fieldErrors.phone }"
                  />
                  <p v-if="fieldErrors.phone" class="mt-1.5 text-sm text-destructive">{{ fieldErrors.phone }}</p>
                </div>
              </div>
              <p class="mt-2 text-xs leading-relaxed text-muted-foreground">
                <span class="text-destructive">*</span>
                Обязательно для заполнения — укажите ваш e-mail или телефон для обратной связи (достаточно
                одного способа).
              </p>
              <p v-if="fieldErrors.contact" class="mt-1.5 text-sm text-destructive">{{ fieldErrors.contact }}</p>
              <p v-if="fieldErrors.email" class="mt-1.5 text-sm text-destructive">{{ fieldErrors.email }}</p>
            </div>



            <!-- Дата и время -->
            <div class="grid gap-6 md:grid-cols-2">
              <div>
                <label for="complain-date" class="mb-2 block text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                  Дата посещения
                </label>
                <input
                  id="complain-date"
                  v-model="visitDate"
                  type="date"
                  class="w-full rounded-md border border-input bg-background px-3 py-2.5 text-foreground shadow-sm transition-colors focus:border-ring focus:outline-none focus:ring-2 focus:ring-ring/30"
                  :class="{ 'border-destructive': fieldErrors.visitDate }"
                />
                <p v-if="fieldErrors.visitDate" class="mt-1.5 text-sm text-destructive">{{ fieldErrors.visitDate }}</p>
              </div>
              <div>
                <label for="complain-time" class="mb-2 block text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                  Время посещения
                </label>
                <input
                  id="complain-time"
                  v-model="visitTime"
                  type="text"
                  placeholder="Введите время посещения"
                  class="w-full rounded-md border border-input bg-background px-3 py-2.5 text-foreground shadow-sm transition-colors placeholder:text-muted-foreground/60 focus:border-ring focus:outline-none focus:ring-2 focus:ring-ring/30"
                  :class="{ 'border-destructive': fieldErrors.visitTime }"
                />
                <p v-if="fieldErrors.visitTime" class="mt-1.5 text-sm text-destructive">{{ fieldErrors.visitTime }}</p>
              </div>
            </div>

            <!-- Сообщение -->
            <div>
              <label for="complain-message" class="mb-2 block text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                Сообщение <span class="text-destructive">*</span>
              </label>
              <textarea
                id="complain-message"
                v-model="message"
                rows="6"
                placeholder="Введите текст сообщения"
                class="w-full resize-y rounded-md border border-input bg-background px-3 py-2.5 text-foreground shadow-sm transition-colors placeholder:text-muted-foreground/60 focus:border-ring focus:outline-none focus:ring-2 focus:ring-ring/30"
                :class="{ 'border-destructive': fieldErrors.message }"
              />
              <p v-if="fieldErrors.message" class="mt-1.5 text-sm text-destructive">{{ fieldErrors.message }}</p>
            </div>

            <!-- Файл -->
            <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div class="flex flex-wrap items-center gap-3">
                <input
                  ref="fileInputRef"
                  type="file"
                  class="sr-only"
                  accept=".doc,.pdf,.ppt,.docx,.pptx,.xls,.xlsx,.jpg,.jpeg,.png"
                  @change="onFileChange"
                />
                <button
                  type="button"
                  class="inline-flex items-center gap-2 rounded-full border border-border bg-muted/80 px-5 py-2.5 text-sm font-medium text-foreground transition-colors hover:bg-muted"
                  @click="fileInputRef?.click()"
                >
                  <Paperclip class="h-4 w-4 shrink-0" />
                  Прикрепить файл
                </button>
                <span v-if="attachmentName" class="flex max-w-full items-center gap-2 text-sm text-muted-foreground">
                  <span class="truncate">{{ attachmentName }}</span>
                  <button
                    type="button"
                    class="rounded-full p-1 text-muted-foreground hover:bg-muted hover:text-foreground"
                    aria-label="Удалить файл"
                    @click="clearFile"
                  >
                    <X class="h-4 w-4" />
                  </button>
                </span>
              </div>
            </div>
            <p class="text-xs text-muted-foreground">
              Допустимые форматы: .doc, .pdf, .ppt, .docx, .pptx, .xls, .xlsx, .jpg, .png — до 10 Мб.
            </p>
            <p v-if="attachmentError || fieldErrors.attachment" class="text-sm text-destructive">
              {{ attachmentError || fieldErrors.attachment }}
            </p>

            <!-- Отправить -->
            <div class="flex flex-col items-stretch gap-4 pt-2 sm:flex-row sm:items-center sm:justify-between">
              <button
                type="submit"
                :disabled="isSubmitting"
                class="inline-flex items-center justify-center gap-2 rounded-full bg-primary px-8 py-3 text-sm font-semibold uppercase tracking-wide text-primary-foreground shadow-sm transition-all hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none disabled:opacity-60"
              >
                <Loader2 v-if="isSubmitting" class="h-4 w-4 animate-spin" />
                <Send v-else class="h-4 w-4" />
                {{ isSubmitting ? 'Отправка…' : 'Отправить' }}
              </button>
            </div>

            <p class="text-center text-xs leading-relaxed text-muted-foreground md:text-left">
              Отправляя сообщение, вы принимаете условия соглашения об использовании сайта, в том числе в
              части обработки и использования персональных данных.
            </p>
          </div>
        </form>
        </template>
      </div>
    </main>

    <FooterSection />
  </div>
</template>
