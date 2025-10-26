'use client'

import { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { apiClient } from '@/lib/api-client'
import { toast } from 'react-hot-toast'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { MetricCard } from '@/components/ui/metric-card'
import { 
  Calculator, 
  DollarSign, 
  Calendar,
  TrendingUp,
  Shield,
  Target,
  AlertCircle
} from 'lucide-react'
import { formatCurrency } from '@/lib/utils'

interface SafeSpendingCalculation {
  daily_safe_spending: number
  weekly_safe_spending: number
  monthly_safe_spending: number
  emergency_fund_months: number
  financial_health_score: number
  recommendations: string[]
}

export default function CalculatorPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [calculation, setCalculation] = useState<SafeSpendingCalculation | null>(null)
  const [formData, setFormData] = useState({
    monthly_income: '',
    monthly_expenses: '',
    emergency_fund_target: '',
    savings_goals: [
      { name: '', target_amount: '', target_date: '' }
    ]
  })

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/login')
      return
    }

    if (status === 'authenticated') {
      loadFinancialProfile()
    }
  }, [status, router])

  const loadFinancialProfile = async () => {
    try {
      const response = await apiClient.getFinancialProfile()
      if (response.data) {
        const profile = response.data
        setFormData({
          monthly_income: profile.monthly_income?.toString() || '',
          monthly_expenses: profile.monthly_expenses?.toString() || '',
          emergency_fund_target: profile.emergency_fund_target?.toString() || '',
          savings_goals: [
            { name: '', target_amount: '', target_date: '' }
          ]
        })
      }
    } catch (error) {
      console.error('Error loading financial profile:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.monthly_income || !formData.monthly_expenses) {
      toast.error('Please fill in your monthly income and expenses')
      return
    }

    try {
      setIsLoading(true)
      
      const calculationData = {
        monthly_income: parseFloat(formData.monthly_income),
        monthly_expenses: parseFloat(formData.monthly_expenses),
        emergency_fund_target: parseFloat(formData.emergency_fund_target) || 0,
        savings_goals: formData.savings_goals
          .filter(goal => goal.name && goal.target_amount && goal.target_date)
          .map(goal => ({
            name: goal.name,
            target_amount: parseFloat(goal.target_amount),
            target_date: goal.target_date
          }))
      }

      const result = apiClient.calculateSafeSpending(
        calculationData.monthly_income,
        calculationData.monthly_expenses,
        0, // variableExpenses
        calculationData.emergency_fund_target,
        12 // monthsToSave
      )
      
      // Convert the result to match the expected interface
      const calculation = {
        daily_safe_spending: result.daily,
        weekly_safe_spending: result.weekly,
        monthly_safe_spending: result.monthly,
        emergency_fund_months: result.emergencyMonths,
        financial_health_score: apiClient.calculateFinancialHealthScore({
          monthly_income: calculationData.monthly_income,
          fixed_expenses: calculationData.monthly_expenses,
          variable_expenses: 0,
          emergency_fund: calculationData.emergency_fund_target,
          total_debt: 0,
          credit_score: 0,
          age: 30
        }),
        recommendations: []
      }
      
      setCalculation(calculation)
      toast.success('Calculation completed!')
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to calculate safe spending')
    } finally {
      setIsLoading(false)
    }
  }

  const addSavingsGoal = () => {
    setFormData(prev => ({
      ...prev,
      savings_goals: [...prev.savings_goals, { name: '', target_amount: '', target_date: '' }]
    }))
  }

  const removeSavingsGoal = (index: number) => {
    setFormData(prev => ({
      ...prev,
      savings_goals: prev.savings_goals.filter((_, i) => i !== index)
    }))
  }

  const updateSavingsGoal = (index: number, field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      savings_goals: prev.savings_goals.map((goal, i) => 
        i === index ? { ...goal, [field]: value } : goal
      )
    }))
  }

  if (status === 'loading') {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (status === 'unauthenticated') {
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
      {/* Header */}
      <div className="glass-header">
        <div className="relative z-10">
          <h1 className="text-4xl font-bold mb-2">Safe Spending Calculator</h1>
          <p className="text-xl opacity-90">Calculate how much you can safely spend each day, week, and month</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Calculator Form */}
          <Card className="modern-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calculator className="h-5 w-5" />
                Financial Information
              </CardTitle>
              <CardDescription>
                Enter your financial details to calculate your safe spending amounts
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Basic Financial Info */}
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="monthly_income">Monthly Income</Label>
                    <Input
                      id="monthly_income"
                      type="number"
                      value={formData.monthly_income}
                      onChange={(e) => setFormData(prev => ({ ...prev, monthly_income: e.target.value }))}
                      placeholder="5000"
                      required
                    />
                  </div>

                  <div>
                    <Label htmlFor="monthly_expenses">Monthly Expenses</Label>
                    <Input
                      id="monthly_expenses"
                      type="number"
                      value={formData.monthly_expenses}
                      onChange={(e) => setFormData(prev => ({ ...prev, monthly_expenses: e.target.value }))}
                      placeholder="3000"
                      required
                    />
                  </div>

                  <div>
                    <Label htmlFor="emergency_fund_target">Emergency Fund Target</Label>
                    <Input
                      id="emergency_fund_target"
                      type="number"
                      value={formData.emergency_fund_target}
                      onChange={(e) => setFormData(prev => ({ ...prev, emergency_fund_target: e.target.value }))}
                      placeholder="15000"
                    />
                  </div>
                </div>

                {/* Savings Goals */}
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <Label>Savings Goals</Label>
                    <Button type="button" variant="outline" size="sm" onClick={addSavingsGoal}>
                      Add Goal
                    </Button>
                  </div>

                  {formData.savings_goals.map((goal, index) => (
                    <div key={index} className="grid grid-cols-1 md:grid-cols-4 gap-2 p-4 border rounded-lg">
                      <Input
                        placeholder="Goal name"
                        value={goal.name}
                        onChange={(e) => updateSavingsGoal(index, 'name', e.target.value)}
                      />
                      <Input
                        type="number"
                        placeholder="Amount"
                        value={goal.target_amount}
                        onChange={(e) => updateSavingsGoal(index, 'target_amount', e.target.value)}
                      />
                      <Input
                        type="date"
                        value={goal.target_date}
                        onChange={(e) => updateSavingsGoal(index, 'target_date', e.target.value)}
                      />
                      <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        onClick={() => removeSavingsGoal(index)}
                        className="text-red-600 hover:text-red-700"
                      >
                        Remove
                      </Button>
                    </div>
                  ))}
                </div>

                <Button type="submit" className="w-full" disabled={isLoading}>
                  {isLoading ? (
                    <>
                      <LoadingSpinner size="sm" className="mr-2" />
                      Calculating...
                    </>
                  ) : (
                    'Calculate Safe Spending'
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Results */}
          <div className="space-y-6">
            {calculation ? (
              <>
                {/* Safe Spending Amounts */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <MetricCard
                    title="Daily Safe Spending"
                    value={formatCurrency(calculation.daily_safe_spending)}
                    icon={DollarSign}
                    color="success"
                    subtitle="Amount you can spend daily"
                  />
                  <MetricCard
                    title="Weekly Safe Spending"
                    value={formatCurrency(calculation.weekly_safe_spending)}
                    icon={TrendingUp}
                    color="primary"
                    subtitle="Amount you can spend weekly"
                  />
                  <MetricCard
                    title="Monthly Safe Spending"
                    value={formatCurrency(calculation.monthly_safe_spending)}
                    icon={Calendar}
                    color="info"
                    subtitle="Amount you can spend monthly"
                  />
                </div>

                {/* Financial Health Score */}
                <Card className="modern-card">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Shield className="h-5 w-5" />
                      Financial Health Score
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center">
                      <div className="text-4xl font-bold text-primary-600 mb-2">
                        {calculation.financial_health_score}/100
                      </div>
                      <div className="w-full bg-muted rounded-full h-3 mb-4">
                        <div 
                          className="bg-gradient-to-r from-primary-500 to-secondary-500 h-3 rounded-full transition-all duration-500"
                          style={{ width: `${calculation.financial_health_score}%` }}
                        />
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {calculation.financial_health_score >= 80 ? 'Excellent' : 
                         calculation.financial_health_score >= 60 ? 'Good' : 
                         calculation.financial_health_score >= 40 ? 'Fair' : 'Needs Improvement'}
                      </p>
                    </div>
                  </CardContent>
                </Card>

                {/* Emergency Fund Info */}
                <Card className="modern-card">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Target className="h-5 w-5" />
                      Emergency Fund
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-primary-600 mb-2">
                        {calculation.emergency_fund_months} months
                      </div>
                      <p className="text-sm text-muted-foreground">
                        Your emergency fund will last {calculation.emergency_fund_months} months
                      </p>
                    </div>
                  </CardContent>
                </Card>

                {/* Recommendations */}
                {calculation.recommendations && calculation.recommendations.length > 0 && (
                  <Card className="modern-card">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <AlertCircle className="h-5 w-5" />
                        Recommendations
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ul className="space-y-2">
                        {calculation.recommendations.map((rec, index) => (
                          <li key={index} className="flex items-start gap-2 text-sm">
                            <span className="text-primary-600 mt-1">•</span>
                            <span>{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>
                )}
              </>
            ) : (
              <Card className="modern-card">
                <CardContent className="text-center py-12">
                  <Calculator className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
                  <h3 className="text-xl font-semibold mb-2">Calculate Your Safe Spending</h3>
                  <p className="text-muted-foreground">
                    Fill in your financial information and click "Calculate Safe Spending" to see your personalized results
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
