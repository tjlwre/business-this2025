import React from 'react'
import { Card, CardContent } from './card'
import { cn } from '@/lib/utils'
import { LucideIcon } from 'lucide-react'

interface MetricCardProps {
  title: string
  value: string | number
  icon?: LucideIcon
  subtitle?: string
  color?: 'primary' | 'success' | 'warning' | 'error' | 'info'
  trend?: number
  className?: string
}

const colorMap = {
  primary: 'text-primary-600',
  success: 'text-green-600',
  warning: 'text-yellow-600',
  error: 'text-red-600',
  info: 'text-blue-600',
}

const bgColorMap = {
  primary: 'bg-primary-50',
  success: 'bg-green-50',
  warning: 'bg-yellow-50',
  error: 'bg-red-50',
  info: 'bg-blue-50',
}

export function MetricCard({
  title,
  value,
  icon: Icon,
  subtitle,
  color = 'primary',
  trend,
  className,
}: MetricCardProps) {
  const trendIcon = trend ? (trend > 0 ? '↗' : trend < 0 ? '↘' : '→') : null
  const trendColor = trend
    ? trend > 0
      ? 'text-green-600'
      : trend < 0
      ? 'text-red-600'
      : 'text-gray-500'
    : ''

  return (
    <Card className={cn('metric-card', className)}>
      <CardContent className="p-6">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            {Icon && (
              <div className={cn('p-2 rounded-lg', bgColorMap[color])}>
                <Icon className={cn('h-5 w-5', colorMap[color])} />
              </div>
            )}
            <span className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
              {title}
            </span>
          </div>
          {trend !== undefined && (
            <div className={cn('text-sm font-medium', trendColor)}>
              {trendIcon} {Math.abs(trend)}%
            </div>
          )}
        </div>
        <div className={cn('text-2xl font-bold mb-1', colorMap[color])}>
          {value}
        </div>
        {subtitle && (
          <div className="text-sm text-muted-foreground">{subtitle}</div>
        )}
      </CardContent>
    </Card>
  )
}
