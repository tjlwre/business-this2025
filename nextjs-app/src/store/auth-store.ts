import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { User, Subscription } from '@/types'

interface AuthState {
  user: User | null
  subscription: Subscription | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

interface AuthActions {
  setUser: (user: User | null) => void
  setSubscription: (subscription: Subscription | null) => void
  setAuthenticated: (isAuthenticated: boolean) => void
  setLoading: (isLoading: boolean) => void
  setError: (error: string | null) => void
  login: (user: User, subscription?: Subscription) => void
  logout: () => void
  clearError: () => void
}

export const useAuthStore = create<AuthState & AuthActions>()(
  persist(
    (set, get) => ({
      // State
      user: null,
      subscription: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // Actions
      setUser: (user) => set({ user }),
      setSubscription: (subscription) => set({ subscription }),
      setAuthenticated: (isAuthenticated) => set({ isAuthenticated }),
      setLoading: (isLoading) => set({ isLoading }),
      setError: (error) => set({ error }),
      
      login: (user, subscription) => set({
        user,
        subscription,
        isAuthenticated: true,
        error: null,
      }),
      
      logout: () => set({
        user: null,
        subscription: null,
        isAuthenticated: false,
        error: null,
      }),
      
      clearError: () => set({ error: null }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        subscription: state.subscription,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
