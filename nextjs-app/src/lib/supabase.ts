import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Auth helpers
export const signUp = async (email: string, password: string, fullName?: string) => {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        full_name: fullName || ''
      }
    }
  })
  return { data, error }
}

export const signIn = async (email: string, password: string) => {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password
  })
  return { data, error }
}

export const signOut = async () => {
  const { error } = await supabase.auth.signOut()
  return { error }
}

export const getCurrentUser = async () => {
  const { data: { user }, error } = await supabase.auth.getUser()
  return { user, error }
}

// Financial Profile helpers
export const getFinancialProfile = async (userId: string) => {
  const { data, error } = await supabase
    .from('financial_profiles')
    .select('*')
    .eq('user_id', userId)
    .single()
  return { data, error }
}

export const upsertFinancialProfile = async (userId: string, profile: any) => {
  const { data, error } = await supabase
    .from('financial_profiles')
    .upsert({ user_id: userId, ...profile })
    .select()
    .single()
  return { data, error }
}

// Savings Goals helpers
export const getSavingsGoals = async (userId: string) => {
  const { data, error } = await supabase
    .from('savings_goals')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false })
  return { data, error }
}

export const createSavingsGoal = async (userId: string, goal: any) => {
  const { data, error } = await supabase
    .from('savings_goals')
    .insert({ user_id: userId, ...goal })
    .select()
    .single()
  return { data, error }
}

export const updateSavingsGoal = async (goalId: string, updates: any) => {
  const { data, error } = await supabase
    .from('savings_goals')
    .update(updates)
    .eq('id', goalId)
    .select()
    .single()
  return { data, error }
}

export const deleteSavingsGoal = async (goalId: string) => {
  const { error } = await supabase
    .from('savings_goals')
    .delete()
    .eq('id', goalId)
  return { error }
}

// User helpers
export const getUserProfile = async (userId: string) => {
  const { data, error } = await supabase
    .from('users')
    .select('*')
    .eq('id', userId)
    .single()
  return { data, error }
}

export const updateUserProfile = async (userId: string, updates: any) => {
  const { data, error } = await supabase
    .from('users')
    .update(updates)
    .eq('id', userId)
    .select()
    .single()
  return { data, error }
}
