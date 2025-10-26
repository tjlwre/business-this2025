// User and Authentication Types
export interface User {
  id: string
  email: string
  name: string
  created_at: string
  updated_at: string
  subscription?: Subscription
}

export interface AuthResponse {
  success: boolean
  user: User
  token: string
  message?: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterCredentials {
  email: string
  password: string
  name: string
}

// Financial Profile Types
export interface FinancialProfile {
  id: string
  user_id: string
  monthly_income: number
  monthly_expenses: number
  emergency_fund_target: number
  risk_tolerance: 'conservative' | 'moderate' | 'aggressive'
  financial_goals: string[]
  created_at: string
  updated_at: string
}

// Savings Goal Types
export interface SavingsGoal {
  id: string
  user_id: string
  name: string
  target_amount: number
  current_amount: number
  target_date: string
  priority: 'low' | 'medium' | 'high'
  category: string
  created_at: string
  updated_at: string
}

export interface CreateSavingsGoal {
  name: string
  target_amount: number
  current_amount?: number
  target_date: string
  priority: 'low' | 'medium' | 'high'
  category: string
}

// Calculator Types
export interface SafeSpendingCalculation {
  daily_safe_spending: number
  weekly_safe_spending: number
  monthly_safe_spending: number
  emergency_fund_months: number
  financial_health_score: number
  recommendations: string[]
}

export interface CalculatorInput {
  monthly_income: number
  monthly_expenses: number
  emergency_fund_target: number
  savings_goals: Array<{
    name: string
    target_amount: number
    target_date: string
  }>
}

// Investment Types
export interface InvestmentRecommendation {
  asset_class: string
  percentage: number
  risk_level: string
  description: string
}

export interface AssetAllocation {
  stocks: number
  bonds: number
  cash: number
  alternative: number
  recommendations: InvestmentRecommendation[]
}

// Subscription Types
export interface Subscription {
  id: string
  user_id: string
  subscription_tier: 'free' | 'premium' | 'pro'
  subscription_status: 'active' | 'inactive' | 'cancelled'
  current_period_start: string
  current_period_end: string
  created_at: string
  updated_at: string
}

export interface SubscriptionUpgrade {
  plan: 'premium' | 'pro'
  checkout_url: string
}

// AI Types
export interface AICoachingResponse {
  coaching: string
  recommendations: string[]
  confidence_score: number
}

export interface SpendingRecommendation {
  category: string
  current_spending: number
  recommended_spending: number
  potential_savings: number
  reasoning: string
}

// Report Types
export interface FinancialReport {
  id: string
  type: 'monthly' | 'quarterly' | 'annual' | 'custom'
  period_start: string
  period_end: string
  data: {
    income: number
    expenses: number
    savings: number
    goals_progress: Array<{
      goal_name: string
      progress_percentage: number
    }>
    financial_health_score: number
  }
  created_at: string
}

// Admin Types
export interface AdminMetrics {
  total_users: number
  active_users: number
  premium_users: number
  pro_users: number
  monthly_revenue: number
  churn_rate: number
  conversion_rate: number
  user_growth: Array<{
    month: string
    new_users: number
    total_users: number
  }>
}

// API Response Types
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  limit: number
  has_more: boolean
}

// Form Types
export interface FormErrors {
  [key: string]: string | undefined
}

export interface FormState<T> {
  data: T
  errors: FormErrors
  isSubmitting: boolean
  isValid: boolean
}

// UI Component Types
export interface MetricCardProps {
  title: string
  value: string | number
  icon: string
  subtitle?: string
  color?: 'primary' | 'success' | 'warning' | 'error' | 'info'
  trend?: number
}

export interface ChartData {
  name: string
  value: number
  color?: string
}

// Navigation Types
export interface NavItem {
  label: string
  href: string
  icon: string
  badge?: string | number
  children?: NavItem[]
}

// Theme Types
export type Theme = 'light' | 'dark' | 'system'

// Store Types
export interface AppState {
  user: User | null
  isAuthenticated: boolean
  subscription: Subscription | null
  financialProfile: FinancialProfile | null
  savingsGoals: SavingsGoal[]
  isLoading: boolean
  error: string | null
}

export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

export interface FinancialState {
  profile: FinancialProfile | null
  goals: SavingsGoal[]
  calculations: SafeSpendingCalculation | null
  isLoading: boolean
  error: string | null
}
