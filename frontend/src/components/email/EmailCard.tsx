interface EmailCardProps {
  sender: string
  subject: string
  snippet: string
  timestamp: Date
  isRead: boolean
  priority?: 'critical' | 'high' | 'medium' | 'low'
  category?: string
  onClick?: () => void
}

const priorityColors: Record<string, string> = {
  critical: 'bg-red-500/10 text-red-600 border-red-500/20',
  high: 'bg-orange-500/10 text-orange-600 border-orange-500/20',
  medium: 'bg-amber-500/10 text-amber-600 border-amber-500/20',
  low: 'bg-slate-500/10 text-slate-600 border-slate-500/20',
}

export function EmailCard({
  sender,
  subject,
  snippet,
  timestamp,
  isRead,
  priority,
  category,
  onClick,
}: EmailCardProps) {
  return (
    <div
      onClick={onClick}
      className={`bg-card border border-border rounded-lg p-4 hover:border-primary/40 hover:bg-muted/30 cursor-pointer transition-all ${
        !isRead ? 'border-l-4 border-l-primary font-medium' : ''
      }`}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0 space-y-1">
          <div className="flex items-center gap-2">
            <span
              className={`text-sm truncate ${
                !isRead ? 'font-semibold text-foreground' : 'text-muted-foreground'
              }`}
            >
              {sender}
            </span>
            {priority && (
              <span
                className={`text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-full font-bold border ${
                  priorityColors[priority] || priorityColors.medium
                }`}
              >
                {priority}
              </span>
            )}
            {category && (
              <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground border border-border">
                {category}
              </span>
            )}
          </div>
          <p
            className={`text-sm truncate ${
              !isRead ? 'font-semibold text-foreground' : 'text-foreground/90'
            }`}
          >
            {subject}
          </p>
          <p className="text-xs text-muted-foreground truncate line-clamp-1">{snippet}</p>
        </div>
        <span className="text-xs text-muted-foreground flex-shrink-0">
          {timestamp.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
        </span>
      </div>
    </div>
  )
}
