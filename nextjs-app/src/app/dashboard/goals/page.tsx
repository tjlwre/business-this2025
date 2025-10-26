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
import { Progress } from '@/components/ui/progress'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { 
  Target, 
  Plus, 
  Edit, 
  Trash2, 
  Calendar,
  DollarSign,
  TrendingUp
} from 'lucide-react'
import { formatCurrency, calculateProgress, calculateDaysUntil } from '@/lib/utils'

interface SavingsGoal {
  id: string
  name: string
  target_amount: number
  current_amount: number
  target_date: string
  priority: 'low' | 'medium' | 'high'
  category: string
}

export default function GoalsPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [goals, setGoals] = useState<SavingsGoal[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingGoal, setEditingGoal] = useState<SavingsGoal | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    target_amount: '',
    current_amount: '',
    target_date: '',
    priority: 'medium' as 'low' | 'medium' | 'high',
    category: '',
  })

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/login')
      return
    }

    if (status === 'authenticated') {
      loadGoals()
    }
  }, [status, router])

  const loadGoals = async () => {
    try {
      setIsLoading(true)
      const response = await apiClient.getSavingsGoals()
      setGoals(response.data.goals || [])
    } catch (error) {
      console.error('Error loading goals:', error)
      toast.error('Failed to load savings goals')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const goalData = {
        name: formData.name,
        target_amount: parseFloat(formData.target_amount),
        current_amount: parseFloat(formData.current_amount) || 0,
        target_date: formData.target_date,
        priority: formData.priority,
        category: formData.category,
      }

      if (editingGoal) {
        await apiClient.updateSavingsGoal(editingGoal.id, goalData)
        toast.success('Goal updated successfully!')
      } else {
        await apiClient.createSavingsGoal(goalData)
        toast.success('Goal created successfully!')
      }

      setShowForm(false)
      setEditingGoal(null)
      setFormData({
        name: '',
        target_amount: '',
        current_amount: '',
        target_date: '',
        priority: 'medium',
        category: '',
      })
      loadGoals()
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to save goal')
    }
  }

  const handleEdit = (goal: SavingsGoal) => {
    setEditingGoal(goal)
    setFormData({
      name: goal.name,
      target_amount: goal.target_amount.toString(),
      current_amount: goal.current_amount.toString(),
      target_date: goal.target_date,
      priority: goal.priority,
      category: goal.category,
    })
    setShowForm(true)
  }

  const handleDelete = async (goalId: string) => {
    if (!confirm('Are you sure you want to delete this goal?')) return

    try {
      await apiClient.deleteSavingsGoal(goalId)
      toast.success('Goal deleted successfully!')
      loadGoals()
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to delete goal')
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-50'
      case 'medium': return 'text-yellow-600 bg-yellow-50'
      case 'low': return 'text-green-600 bg-green-50'
      default: return 'text-gray-600 bg-gray-50'
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
      {/* Header */}
      <div className="glass-header">
        <div className="relative z-10">
          <h1 className="text-4xl font-bold mb-2">Savings Goals</h1>
          <p className="text-xl opacity-90">Track your progress towards financial milestones</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Add Goal Button */}
        <div className="mb-8">
          <Button
            onClick={() => setShowForm(true)}
            className="flex items-center gap-2"
          >
            <Plus className="h-4 w-4" />
            Add New Goal
          </Button>
        </div>

        {/* Goals List */}
        {goals.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {goals.map((goal) => {
              const progress = calculateProgress(goal.current_amount, goal.target_amount)
              const daysLeft = calculateDaysUntil(goal.target_date)
              
              return (
                <Card key={goal.id} className="modern-card">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle className="text-lg">{goal.name}</CardTitle>
                        <CardDescription className="capitalize">
                          {goal.category} • {goal.priority} priority
                        </CardDescription>
                      </div>
                      <div className="flex gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleEdit(goal)}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDelete(goal.id)}
                          className="text-red-600 hover:text-red-700"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {/* Progress */}
                      <div>
                        <div className="flex justify-between text-sm mb-2">
                          <span>Progress</span>
                          <span className="font-semibold">{progress.toFixed(1)}%</span>
                        </div>
                        <Progress value={progress} className="h-2" />
                      </div>

                      {/* Amounts */}
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <div className="text-sm text-muted-foreground">Current</div>
                          <div className="font-semibold">{formatCurrency(goal.current_amount)}</div>
                        </div>
                        <div>
                          <div className="text-sm text-muted-foreground">Target</div>
                          <div className="font-semibold">{formatCurrency(goal.target_amount)}</div>
                        </div>
                      </div>

                      {/* Remaining */}
                      <div className="pt-2 border-t">
                        <div className="flex justify-between items-center">
                          <div>
                            <div className="text-sm text-muted-foreground">Remaining</div>
                            <div className="font-semibold">
                              {formatCurrency(goal.target_amount - goal.current_amount)}
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="text-sm text-muted-foreground">Days left</div>
                            <div className="font-semibold">{daysLeft}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        ) : (
          <Card className="modern-card">
            <CardContent className="text-center py-12">
              <Target className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">No savings goals yet</h3>
              <p className="text-muted-foreground mb-6">
                Create your first savings goal to start tracking your financial progress
              </p>
              <Button onClick={() => setShowForm(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Create Your First Goal
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Add/Edit Goal Form */}
        {showForm && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <Card className="w-full max-w-md modern-card">
              <CardHeader>
                <CardTitle>
                  {editingGoal ? 'Edit Goal' : 'Add New Goal'}
                </CardTitle>
                <CardDescription>
                  {editingGoal ? 'Update your savings goal' : 'Create a new savings goal to track your progress'}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <Label htmlFor="name">Goal Name</Label>
                    <Input
                      id="name"
                      value={formData.name}
                      onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                      placeholder="e.g., Emergency Fund"
                      required
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="target_amount">Target Amount</Label>
                      <Input
                        id="target_amount"
                        type="number"
                        value={formData.target_amount}
                        onChange={(e) => setFormData(prev => ({ ...prev, target_amount: e.target.value }))}
                        placeholder="10000"
                        required
                      />
                    </div>
                    <div>
                      <Label htmlFor="current_amount">Current Amount</Label>
                      <Input
                        id="current_amount"
                        type="number"
                        value={formData.current_amount}
                        onChange={(e) => setFormData(prev => ({ ...prev, current_amount: e.target.value }))}
                        placeholder="0"
                      />
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="target_date">Target Date</Label>
                    <Input
                      id="target_date"
                      type="date"
                      value={formData.target_date}
                      onChange={(e) => setFormData(prev => ({ ...prev, target_date: e.target.value }))}
                      required
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="priority">Priority</Label>
                      <select
                        id="priority"
                        value={formData.priority}
                        onChange={(e) => setFormData(prev => ({ ...prev, priority: e.target.value as 'low' | 'medium' | 'high' }))}
                        className="w-full h-10 px-3 py-2 border border-input bg-background rounded-md"
                      >
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                      </select>
                    </div>
                    <div>
                      <Label htmlFor="category">Category</Label>
                      <Input
                        id="category"
                        value={formData.category}
                        onChange={(e) => setFormData(prev => ({ ...prev, category: e.target.value }))}
                        placeholder="e.g., Emergency"
                      />
                    </div>
                  </div>

                  <div className="flex gap-2 pt-4">
                    <Button type="submit" className="flex-1">
                      {editingGoal ? 'Update Goal' : 'Create Goal'}
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => {
                        setShowForm(false)
                        setEditingGoal(null)
                        setFormData({
                          name: '',
                          target_amount: '',
                          current_amount: '',
                          target_date: '',
                          priority: 'medium',
                          category: '',
                        })
                      }}
                    >
                      Cancel
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}
