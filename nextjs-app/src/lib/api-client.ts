import { supabase, signIn, signUp, signOut, getCurrentUser, getFinancialProfile, upsertFinancialProfile, getSavingsGoals, createSavingsGoal, updateSavingsGoal, deleteSavingsGoal, getUserProfile, updateUserProfile } from './supabase'

class ApiClient {
  constructor() {
    // Supabase client is already configured in supabase.ts
  }

  // Auth methods
  async login(email: string, password: string) {
    const { data, error } = await signIn(email, password)
    if (error) {
      throw new Error(error.message)
    }
    return { success: true, user: data.user }
  }

  async register(userData: {
    email: string
    password: string
    name: string
  }) {
    const { data, error } = await signUp(userData.email, userData.password, userData.name)
    if (error) {
      throw new Error(error.message)
    }
    return { success: true, user: data.user }
  }

  async logout() {
    const { error } = await signOut()
    if (error) {
      throw new Error(error.message)
    }
    return { success: true }
  }

  async getCurrentUser() {
    const { user, error } = await getCurrentUser()
    if (error) {
      throw new Error(error.message)
    }
    return { user }
  }

  // Financial Profile methods
  async getFinancialProfile() {
    const { user } = await this.getCurrentUser()
    if (!user) throw new Error('User not authenticated')
    
    const { data, error } = await getFinancialProfile(user.id)
    if (error) {
      throw new Error(error.message)
    }
    return { data }
  }

  async updateFinancialProfile(profileData: any) {
    const { user } = await this.getCurrentUser()
    if (!user) throw new Error('User not authenticated')
    
    const { data, error } = await upsertFinancialProfile(user.id, profileData)
    if (error) {
      throw new Error(error.message)
    }
    return { data }
  }

  // Savings Goals methods
  async getSavingsGoals() {
    const { user } = await this.getCurrentUser()
    if (!user) throw new Error('User not authenticated')
    
    const { data, error } = await getSavingsGoals(user.id)
    if (error) {
      throw new Error(error.message)
    }
    return { data }
  }

  async createSavingsGoal(goalData: any) {
    const { user } = await this.getCurrentUser()
    if (!user) throw new Error('User not authenticated')
    
    const { data, error } = await createSavingsGoal(user.id, goalData)
    if (error) {
      throw new Error(error.message)
    }
    return { data }
  }

  async updateSavingsGoal(goalId: string, goalData: any) {
    const { data, error } = await updateSavingsGoal(goalId, goalData)
    if (error) {
      throw new Error(error.message)
    }
    return { data }
  }

  async deleteSavingsGoal(goalId: string) {
    const { error } = await deleteSavingsGoal(goalId)
    if (error) {
      throw new Error(error.message)
    }
    return { success: true }
  }

  // Calculator methods - these will be client-side calculations
  calculateSafeSpending(monthlyIncome: number, fixedExpenses: number, variableExpenses: number, emergencyFund: number, monthsToSave: number) {
    const totalExpenses = fixedExpenses + variableExpenses
    const monthlySavings = monthlyIncome - totalExpenses
    const emergencyTarget = emergencyFund
    const monthsToEmergency = monthlySavings > 0 ? emergencyTarget / monthlySavings : 0
    
    const dailySafeSpend = monthlySavings / 30
    const weeklySafeSpend = monthlySavings / 4.33
    const monthlySafeSpend = monthlySavings
    
    return {
      daily: Math.max(0, dailySafeSpend),
      weekly: Math.max(0, weeklySafeSpend),
      monthly: Math.max(0, monthlySafeSpend),
      emergencyMonths: monthsToEmergency,
      savingsRate: monthlyIncome > 0 ? (monthlySavings / monthlyIncome) * 100 : 0
    }
  }

  calculateFinancialHealthScore(profile: any) {
    let score = 0
    
    // Emergency fund (30 points)
    const emergencyRatio = profile.emergency_fund / (profile.monthly_income * 3)
    score += Math.min(30, emergencyRatio * 30)
    
    // Savings rate (25 points)
    const savingsRate = ((profile.monthly_income - profile.fixed_expenses - profile.variable_expenses) / profile.monthly_income) * 100
    score += Math.min(25, savingsRate * 0.25)
    
    // Debt-to-income ratio (20 points)
    const debtRatio = profile.total_debt / profile.monthly_income
    score += Math.max(0, 20 - (debtRatio * 20))
    
    // Credit score (15 points)
    const creditScore = profile.credit_score || 0
    score += (creditScore / 850) * 15
    
    // Age factor (10 points)
    const age = profile.age || 30
    score += Math.max(0, 10 - (age - 25) * 0.2)
    
    return Math.min(100, Math.max(0, score))
  }

  // User profile methods
  async getUserProfile() {
    const { user } = await this.getCurrentUser()
    if (!user) throw new Error('User not authenticated')
    
    const { data, error } = await getUserProfile(user.id)
    if (error) {
      throw new Error(error.message)
    }
    return { data }
  }

  async updateUserProfile(updates: any) {
    const { user } = await this.getCurrentUser()
    if (!user) throw new Error('User not authenticated')
    
    const { data, error } = await updateUserProfile(user.id, updates)
    if (error) {
      throw new Error(error.message)
    }
    return { data }
  }

  // Subscription methods
  async getSubscriptionStatus() {
    const { data } = await this.getUserProfile()
    return {
      tier: data.subscription_tier || 'free',
      status: data.subscription_status || 'active',
      expiresAt: data.subscription_expires_at
    }
  }

  async upgradeSubscription(plan: string) {
    // This would integrate with Stripe for payment processing
    // For now, just update the user's subscription tier
    return this.updateUserProfile({ subscription_tier: plan })
  }
}

export const apiClient = new ApiClient()