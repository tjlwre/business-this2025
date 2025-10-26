'use client'

import { useEffect, useState } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { apiClient } from '@/lib/api-client'
import { toast } from 'react-hot-toast'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { MetricCard } from '@/components/ui/metric-card'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { Button } from '@/components/ui/button'
import { 
  DollarSign, 
  Target, 
  TrendingUp, 
  Shield,
  Plus,
  Settings,
  BarChart3,
  Calculator
} from 'lucide-react'
import Link from 'next/link'

export default function DashboardPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(true)
  const [financialData, setFinancialData] = useState<any>(null)

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/login')
      return
    }

    if (status === 'authenticated') {
      loadDashboardData()
    }
  }, [status, router])

  const loadDashboardData = async () => {
    try {
      setIsLoading(true)
      
      // Load financial profile
      const profileResponse = await apiClient.getFinancialProfile()
      
      // Load savings goals
      const goalsResponse = await apiClient.getSavingsGoals()
      
      // Load financial health score
      const healthResponse = await apiClient.getFinancialHealthScore()
      
      setFinancialData({
        profile: profileResponse.data,
        goals: goalsResponse.data,
        healthScore: healthResponse.data,
      })
    } catch (error) {
      console.error('Error loading dashboard data:', error)
      toast.error('Failed to load dashboard data')
    } finally {
      setIsLoading(false)
    }
  }

  if (status === 'loading' || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (status === 'unauthenticated') {
    return null
  }

  const profile = financialData?.profile
  const goals = financialData?.goals || []
  const healthScore = financialData?.healthScore

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
      {/* Header */}
      <div className="glass-header">
        <div className="relative z-10">
          <h1 className="text-4xl font-bold mb-2">Welcome back, {session?.user?.name}!</h1>
          <p className="text-xl opacity-90">Here's your financial overview</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Quick Actions */}
        <div className="mb-8">
          <div className="flex flex-wrap gap-4">
            <Link href="/dashboard/goals">
              <Button variant="gradient" className="flex items-center gap-2">
                <Target className="h-4 w-4" />
                Manage Goals
              </Button>
            </Link>
            <Link href="/dashboard/calculator">
              <Button variant="outline" className="flex items-center gap-2">
                <Calculator className="h-4 w-4" />
                Safe Spending Calculator
              </Button>
            </Link>
            <Link href="/dashboard/analytics">
              <Button variant="outline" className="flex items-center gap-2">
                <BarChart3 className="h-4 w-4" />
                Analytics
              </Button>
            </Link>
            <Link href="/dashboard/settings">
              <Button variant="outline" className="flex items-center gap-2">
                <Settings className="h-4 w-4" />
                Settings
              </Button>
            </Link>
          </div>
        </div>

        {/* Financial Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            title="Monthly Income"
            value={profile?.monthly_income ? `$${profile.monthly_income.toLocaleString()}` : 'Not set'}
            icon={DollarSign}
            color="success"
            subtitle="Your monthly income"
          />
          <MetricCard
            title="Monthly Expenses"
            value={profile?.monthly_expenses ? `$${profile.monthly_expenses.toLocaleString()}` : 'Not set'}
            icon={TrendingUp}
            color="warning"
            subtitle="Your monthly expenses"
          />
          <MetricCard
            title="Emergency Fund"
            value={profile?.emergency_fund_target ? `$${profile.emergency_fund_target.toLocaleString()}` : 'Not set'}
            icon={Shield}
            color="info"
            subtitle="Target emergency fund"
          />
          <MetricCard
            title="Financial Health"
            value={healthScore?.score ? `${healthScore.score}/100` : 'Not calculated'}
            icon={BarChart3}
            color={healthScore?.score && healthScore.score >= 70 ? 'success' : 'warning'}
            subtitle="Your financial health score"
          />
        </div>

        {/* Savings Goals */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="modern-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5" />
                Savings Goals
              </CardTitle>
              <CardDescription>
                Track your progress towards your financial goals
              </CardDescription>
            </CardHeader>
            <CardContent>
              {goals.length > 0 ? (
                <div className="space-y-4">
                  {goals.slice(0, 3).map((goal: any) => (
                    <div key={goal.id} className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
                      <div>
                        <h4 className="font-semibold">{goal.name}</h4>
                        <p className="text-sm text-muted-foreground">
                          ${goal.current_amount.toLocaleString()} / ${goal.target_amount.toLocaleString()}
                        </p>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium">
                          {Math.round((goal.current_amount / goal.target_amount) * 100)}%
                        </div>
                        <div className="w-20 bg-muted rounded-full h-2 mt-1">
                          <div 
                            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${Math.min((goal.current_amount / goal.target_amount) * 100, 100)}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                  {goals.length > 3 && (
                    <p className="text-sm text-muted-foreground text-center">
                      +{goals.length - 3} more goals
                    </p>
                  )}
                </div>
              ) : (
                <div className="text-center py-8">
                  <Target className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <h3 className="font-semibold mb-2">No savings goals yet</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Create your first savings goal to start tracking your progress
                  </p>
                  <Link href="/dashboard/goals">
                    <Button className="flex items-center gap-2">
                      <Plus className="h-4 w-4" />
                      Create Goal
                    </Button>
                  </Link>
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="modern-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Quick Insights
              </CardTitle>
              <CardDescription>
                Your financial health at a glance
              </CardDescription>
            </CardHeader>
            <CardContent>
              {healthScore ? (
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-primary-600 mb-2">
                      {healthScore.score}/100
                    </div>
                    <div className="text-sm text-muted-foreground mb-4">
                      Financial Health Score
                    </div>
                    <div className="w-full bg-muted rounded-full h-3">
                      <div 
                        className="bg-gradient-to-r from-primary-500 to-secondary-500 h-3 rounded-full transition-all duration-500"
                        style={{ width: `${healthScore.score}%` }}
                      />
                    </div>
                  </div>
                  
                  {healthScore.recommendations && healthScore.recommendations.length > 0 && (
                    <div>
                      <h4 className="font-semibold mb-2">Recommendations</h4>
                      <ul className="space-y-1">
                        {healthScore.recommendations.slice(0, 3).map((rec: string, index: number) => (
                          <li key={index} className="text-sm text-muted-foreground flex items-start gap-2">
                            <span className="text-primary-600 mt-1">•</span>
                            {rec}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-8">
                  <BarChart3 className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <h3 className="font-semibold mb-2">Complete your profile</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Add your financial information to get personalized insights
                  </p>
                  <Link href="/dashboard/profile">
                    <Button>Complete Profile</Button>
                  </Link>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
