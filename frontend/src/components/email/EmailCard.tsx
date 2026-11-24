import { formatDistanceToNow } from 'date-fns'

interface EmailCardProps {
  sender: string
  subject: string
  snippet: string
  timestamp: Date
  isRead: boolean
  priority?: 'critical' | 'high' | 'medium' | 'low'
  category?: string
}

const priorityColors = {
  critical: 'bg-red-100 text-red-700',
  high: 'bg-orange-100 text-orange-700',
  medium: 'bg-yellow-100 text-yellow-700',
  low: 'bg-gray-100 text-gray-600',
}

export function EmailCard({ sender, subject, snippet, timestamp, isRead, priority, category }: EmailCardProps) {
  return (
    <div className={`bg-card border border-border rounded-lg p-4 hover:bg-muted/50 cursor-pointer transition-colors ${!isRead ? 'border-l-4 border-l-primary' : ''}`}>
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className={`text-sm font-medium truncate ${!isRead ? 'text-foreground' : 'text-muted-foreground'}`}>
              {sender}
            </span>
            {priority && (
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${priorityColors[priority]}`}>
                {priority}
              </span>
            )}
            {category && (
              <span className="text-xs px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground">
                {category}
              </span>
            )}
          </div>
          <p className={`text-sm truncate ${!isRead ? 'font-semibold text-foreground' : 'text-foreground'}`}>
            {subject}
          </p>
          <p className="text-xs text-muted-foreground truncate mt-1">{snippet}</p>
        </div>
        <span className="text-xs text-muted-foreground flex-shrink-0">
          {formatDistanceToNow(timestamp, { addSuffix: true })}
        </span>
      </div>
    </div>
  )
}
