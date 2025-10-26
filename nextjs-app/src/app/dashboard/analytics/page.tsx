"use client"

import { useEffect, useState } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { apiClient } from '@/lib/api-client'
import { toast } from 'react-hot-toast'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { MetricCard } from '@/components/ui/metric-card'
import { BarChart3, PieChart as PieChartIcon, TrendingUp } from 'lucide-react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts'

export default function AnalyticsPage() {
  const { status } = useSession()
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(true)
  const [analytics, setAnalytics] = useState<any>(null)

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/login')
      return
    }

    if (status === 'authenticated') {
      loadAnalytics()
    }
  }, [status, router])

  const loadAnalytics = async () => {
    try {
      setIsLoading(true)
      // Example calls; adapt to your existing endpoints as needed
      const profile = await apiClient.getFinancialProfile()
      const goals = await apiClient.getSavingsGoals()
      const health = await apiClient.getFinancialHealthScore()

      // Build simple mock series from available data
      const monthlySeries = [
        { name: 'Jan', income: profile.data?.profile?.monthly_income || 0, expenses: profile.data?.profile?.monthly_expenses || 0 },
        { name: 'Feb', income: (profile.data?.profile?.monthly_income || 0) * 1.02, expenses: (profile.data?.profile?.monthly_expenses || 0) * 1.01 },
        { name: 'Mar', income: (profile.data?.profile?.monthly_income || 0) * 1.05, expenses: (profile.data?.profile?.monthly_expenses || 0) * 0.98 },
        { name: 'Apr', income: (profile.data?.profile?.monthly_income || 0) * 1.03, expenses: (profile.data?.profile?.monthly_expenses || 0) * 1.00 },
      ]

      const spendingBreakdown = [
        { name: 'Housing', value: Math.max(0, (profile.data?.profile?.monthly_expenses || 0) * 0.35) },
        { name: 'Food', value: Math.max(0, (profile.data?.profile?.monthly_expenses || 0) * 0.15) },
        { name: 'Transport', value: Math.max(0, (profile.data?.profile?.monthly_expenses || 0) * 0.1) },
        { name: 'Utilities', value: Math.max(0, (profile.data?.profile?.monthly_expenses || 0) * 0.1) },
        { name: 'Other', value: Math.max(0, (profile.data?.profile?.monthly_expenses || 0) * 0.3) },
      ]

      setAnalytics({ profile: profile.data, goals: goals.data, health: health.data, monthlySeries, spendingBreakdown })
    } catch (error) {
      console.error('Failed to load analytics', error)
      toast.error('Failed to load analytics')
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

  if (status === 'unauthenticated') return null

  const COLORS = ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6']

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
      <div className="glass-header">
        <div className="relative z-10">
          <h1 className="text-4xl font-bold mb-2">Analytics</h1>
          <p className="text-xl opacity-90">Spending trends, income vs. expenses, and goal progress</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8 space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <MetricCard
            title="Health Score"
            value={analytics?.health?.score ? `${analytics.health.score}/100` : 'N/A'}
            icon={BarChart3}
            color={analytics?.health?.score >= 70 ? 'success' : 'warning'}
            subtitle="Overall financial health"
          />
          <MetricCard
            title="Goals"
            value={analytics?.goals?.goals?.length || 0}
            icon={TrendingUp}
            color="primary"
            subtitle="Active savings goals"
          />
          <MetricCard
            title="Monthly Net"
            value={(() => {
              const inc = analytics?.profile?.profile?.monthly_income || 0
              const exp = analytics?.profile?.profile?.monthly_expenses || 0
              const net = inc - exp
              return net >= 0 ? `$${net.toLocaleString()}` : `-$${Math.abs(net).toLocaleString()}`
            })()}
            icon={TrendingUp}
            color="info"
            subtitle="Income - Expenses"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="modern-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Income vs Expenses
              </CardTitle>
              <CardDescription>Last few months</CardDescription>
            </CardHeader>
            <CardContent>
              <div style={{ width: '100%', height: 300 }}>
                <ResponsiveContainer>
                  <LineChart data={analytics?.monthlySeries || []}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="income" stroke="#22c55e" strokeWidth={2} />
                    <Line type="monotone" dataKey="expenses" stroke="#ef4444" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card className="modern-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <PieChartIcon className="h-5 w-5" />
                Spending Breakdown
              </CardTitle>
              <CardDescription>By category</CardDescription>
            </CardHeader>
            <CardContent>
              <div style={{ width: '100%', height: 300 }}>
                <ResponsiveContainer>
                  <PieChart>
                    <Pie
                      data={analytics?.spendingBreakdown || []}
                      dataKey="value"
                      nameKey="name"
                      outerRadius={110}
                      label
                    >
                      {(analytics?.spendingBreakdown || []).map((entry: any, index: number) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
