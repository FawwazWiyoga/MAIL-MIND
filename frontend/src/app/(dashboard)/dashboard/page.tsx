'use client'

import { useQuery } from '@tanstack/react-query'
import Link from 'next/link'
import { Mail, AlertCircle, CheckSquare, Sparkles, ArrowRight } from 'lucide-react'
import { api } from '@/lib/api'
import { EmailMessage, ActionItem } from '@/types'

export default function DashboardPage() {
  const { data: emails = [] } = useQuery<EmailMessage[]>({
    queryKey: ['emails'],
    queryFn: async () => {
      const res = await api.get('/emails?per_page=50')
      return res.data
    },
  })

  const { data: actions = [] } = useQuery<ActionItem[]>({
    queryKey: ['actions'],
    queryFn: async () => {
      const res = await api.get('/actions')
      return res.data
    },
  })

  const highPriorityCount = emails.filter(
    (e) => e.priority === 'critical' || e.priority === 'high'
  ).length

  const pendingActions = actions.filter((a) => a.status === 'pending')

  return (
    <div className="space-y-6 max-w-6xl">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Workspace Overview</h1>
        <p className="text-muted-foreground mt-1">Your AI-driven email summary and daily priorities</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="bg-card border border-border rounded-xl p-5 space-y-3">
          <div className="flex items-center justify-between text-muted-foreground">
            <span className="text-xs font-semibold uppercase tracking-wider">Synced Emails</span>
            <Mail className="w-5 h-5 text-primary" />
          </div>
          <div className="text-3xl font-bold text-foreground">{emails.length}</div>
          <Link
            href="/inbox"
            className="text-xs text-primary font-medium hover:underline flex items-center gap-1"
          >
            Open Inbox <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="bg-card border border-border rounded-xl p-5 space-y-3">
          <div className="flex items-center justify-between text-muted-foreground">
            <span className="text-xs font-semibold uppercase tracking-wider">Urgent Emails</span>
            <AlertCircle className="w-5 h-5 text-orange-500" />
          </div>
          <div className="text-3xl font-bold text-foreground">{highPriorityCount}</div>
          <Link
            href="/important"
            className="text-xs text-orange-600 font-medium hover:underline flex items-center gap-1"
          >
            Review Priority <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="bg-card border border-border rounded-xl p-5 space-y-3">
          <div className="flex items-center justify-between text-muted-foreground">
            <span className="text-xs font-semibold uppercase tracking-wider">Pending Tasks</span>
            <CheckSquare className="w-5 h-5 text-blue-500" />
          </div>
          <div className="text-3xl font-bold text-foreground">{pendingActions.length}</div>
          <Link
            href="/actions"
            className="text-xs text-blue-600 font-medium hover:underline flex items-center gap-1"
          >
            View Action Items <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* Action Items Quick Peek */}
      <div className="bg-card border border-border rounded-xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-primary" />
            <h3 className="font-bold text-foreground text-lg">AI-Extracted Action Items</h3>
          </div>
          <Link href="/actions" className="text-xs text-primary hover:underline font-medium">
            View All ({actions.length})
          </Link>
        </div>

        {pendingActions.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            No pending action items. Analyze emails in your Inbox to automatically extract tasks and deadlines.
          </p>
        ) : (
          <div className="space-y-2">
            {pendingActions.slice(0, 5).map((item) => (
              <div
                key={item.id}
                className="flex items-center justify-between p-3 bg-muted/20 border border-border rounded-lg text-sm"
              >
                <div className="flex items-center gap-2 truncate">
                  <span className="w-2 h-2 rounded-full bg-primary" />
                  <span className="text-foreground font-medium truncate">{item.description}</span>
                </div>
                <span className="text-[10px] uppercase font-bold text-muted-foreground bg-muted px-2 py-0.5 rounded">
                  {item.priority}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
