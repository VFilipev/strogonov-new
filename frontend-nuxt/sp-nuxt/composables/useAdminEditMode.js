import { AdminStatusApi } from "~/utils/api";

export const useAdminEditMode = () => {
  const isEditMode = useState('is-edit-mode-enabled', () => false)

  const { data, error, pending, refresh } = useAsyncData("admin-status", () => {
    return AdminStatusApi.getList({}, { withCredentials: true })
  }, {
    server: false,
    default: () => ({
      is_authenticated: false,
      is_staff: false,
      is_superuser: false,
      can_edit: false,
      username: '',
    }),
  })

  const isAdmin = computed(() => Boolean(data.value?.can_edit))
  const adminName = computed(() => data.value?.username || '')

  const enableEditMode = () => {
    if (isAdmin.value) isEditMode.value = true
  }

  const disableEditMode = () => {
    isEditMode.value = false
  }

  const toggleEditMode = () => {
    if (!isAdmin.value) return
    isEditMode.value = !isEditMode.value
  }

  return {
    isAdmin,
    adminName,
    isEditMode,
    pending,
    error,
    refresh,
    enableEditMode,
    disableEditMode,
    toggleEditMode,
  }
}
