import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { FinancialProfile, SavingsGoal, SafeSpendingCalculation } from '@/types'

interface FinancialState {
  profile: FinancialProfile | null
  goals: SavingsGoal[]
  calculations: SafeSpendingCalculation | null
  isLoading: boolean
  error: string | null
}

interface FinancialActions {
  setProfile: (profile: FinancialProfile | null) => void
  setGoals: (goals: SavingsGoal[]) => void
  addGoal: (goal: SavingsGoal) => void
  updateGoal: (id: string, goal: Partial<SavingsGoal>) => void
  removeGoal: (id: string) => void
  setCalculations: (calculations: SafeSpendingCalculation | null) => void
  setLoading: (isLoading: boolean) => void
  setError: (error: string | null) => void
  clearError: () => void
  reset: () => void
}

export const useFinancialStore = create<FinancialState & FinancialActions>()(
  persist(
    (set, get) => ({
      // State
      profile: null,
      goals: [],
      calculations: null,
      isLoading: false,
      error: null,

      // Actions
      setProfile: (profile) => set({ profile }),
      setGoals: (goals) => set({ goals }),
      
      addGoal: (goal) => set((state) => ({
        goals: [...state.goals, goal]
      })),
      
      updateGoal: (id, updates) => set((state) => ({
        goals: state.goals.map(goal => 
          goal.id === id ? { ...goal, ...updates } : goal
        )
      })),
      
      removeGoal: (id) => set((state) => ({
        goals: state.goals.filter(goal => goal.id !== id)
      })),
      
      setCalculations: (calculations) => set({ calculations }),
      setLoading: (isLoading) => set({ isLoading }),
      setError: (error) => set({ error }),
      clearError: () => set({ error: null }),
      
      reset: () => set({
        profile: null,
        goals: [],
        calculations: null,
        error: null,
      }),
    }),
    {
      name: 'financial-storage',
      partialize: (state) => ({
        profile: state.profile,
        goals: state.goals,
        calculations: state.calculations,
      }),
    }
  )
)
