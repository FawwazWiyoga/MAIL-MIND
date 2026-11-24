import { useAuthStore } from '@/store/authStore'

export function useAuth() {
  const { user, token, setUser, setToken, logout } = useAuthStore()

  const isAuthenticated = !!token

  const login = (accessToken: string, userData: { id: string; email: string; full_name: string | null }) => {
    setToken(accessToken)
    setUser(userData)
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    logout,
  }
}
