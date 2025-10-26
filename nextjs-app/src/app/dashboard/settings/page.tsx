'use client'

import { useEffect, useState } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { apiClient } from '@/lib/api-client'
import { toast } from 'react-hot-toast'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { Shield, Crown } from 'lucide-react'

export default function SettingsPage() {
  const { status } = useSession()
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(true)
  const [subscription, setSubscription] = useState<any>(null)

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/login')
      return
    }

    if (status === 'authenticated') {
      loadSubscription()
    }
  }, [status, router])

  const loadSubscription = async () => {
    try {
      setIsLoading(true)
      const response = await apiClient.getSubscriptionStatus()
      setSubscription(response)
    } catch (error) {
      console.error('Failed to load subscription', error)
      toast.error('Failed to load subscription status')
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpgrade = async (plan: 'premium' | 'pro') => {
    try {
      const response = await apiClient.upgradeSubscription(plan)
      if ((response as any)?.checkout_url) {
        window.location.href = (response as any).checkout_url
      } else {
        toast.success('Subscription upgraded successfully!')
      }
    } catch (error) {
      toast.error('Failed to start upgrade process')
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

  const tier = subscription?.subscription_tier || 'free'
  const statusLabel = subscription?.subscription_status || 'active'

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
      <div className="glass-header">
        <div className="relative z-10">
          <h1 className="text-4xl font-bold mb-2">Settings</h1>
          <p className="text-xl opacity-90">Manage your account and subscription</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8 space-y-8">
        <Card className="modern-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Subscription
            </CardTitle>
            <CardDescription>Your current plan and upgrade options</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-1 p-4 border rounded-xl">
                <div className="text-sm text-muted-foreground">Current Plan</div>
                <div className="text-2xl font-bold capitalize mt-1">{tier}</div>
                <div className="text-sm text-muted-foreground mt-1">Status: {statusLabel}</div>
              </div>

              <div className="lg:col-span-2 space-y-4">
                {tier === 'free' && (
                  <>
                    <div className="p-4 border rounded-xl">
                      <div className="flex items-center gap-2 font-semibold mb-1">
                        <Crown className="h-4 w-4 text-yellow-500" />
                        Premium ($9.99/month)
                      </div>
                      <div className="text-sm text-muted-foreground mb-3">
                        5 goals, advanced analytics, PDF exports, email notifications
                      </div>
                      <Button onClick={() => handleUpgrade('premium')} className="btn-primary">
                        Upgrade to Premium
                      </Button>
                    </div>

                    <div className="p-4 border rounded-xl">
                      <div className="flex items-center gap-2 font-semibold mb-1">
                        <Crown className="h-4 w-4 text-yellow-600" />
                        Pro ($19.99/month)
                      </div>
                      <div className="text-sm text-muted-foreground mb-3">
                        Unlimited goals, AI coaching, API access, white-label options
                      </div>
                      <Button onClick={() => handleUpgrade('pro')} variant="outline">
                        Upgrade to Pro
                      </Button>
                    </div>
                  </>
                )}

                {tier === 'premium' && (
                  <div className="p-4 border rounded-xl">
                    <div className="font-semibold mb-1">You're on Premium</div>
                    <div className="text-sm text-muted-foreground mb-3">Enjoy advanced analytics and more</div>
                    <Button onClick={() => handleUpgrade('pro')} variant="outline">
                      Upgrade to Pro
                    </Button>
                  </div>
                )}

                {tier === 'pro' && (
                  <div className="p-4 border rounded-xl">
                    <div className="font-semibold mb-1">You're on Pro</div>
                    <div className="text-sm text-muted-foreground">All features unlocked</div>
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
