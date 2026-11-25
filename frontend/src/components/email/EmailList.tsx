'use client'

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import Link from 'next/link'
import { RefreshCw, Inbox, AlertCircle } from 'lucide-react'
import { api } from '@/lib/api'
import { EmailCard } from './EmailCard'
import { EmailMessage } from '@/types'

export function EmailList() {
  const queryClient = useQueryClient()

  const { data: emails = [], isLoading, error } = useQuery<EmailMessage[]>({
    queryKey: ['emails'],
    queryFn: async () => {
      const res = await api.get('/emails?per_page=50')
      return res.data
    },
  })

  const syncMutation = useMutation({
    mutationFn: async () => {
      await api.post('/emails/sync')
    },
    onSuccess: () => {
      setTimeout(() => {
        queryClient.invalidateQueries({ queryKey: ['emails'] })
      }, 2000)
    },
  })

  if (isLoading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3, 4, 5].map((i) => (
          <div key={i} className="bg-card border border-border rounded-lg p-4 animate-pulse">
            <div className="h-4 bg-muted rounded w-1/4 mb-2" />
            <div className="h-4 bg-muted rounded w-3/4 mb-2" />
            <div className="h-3 bg-muted rounded w-1/2" />
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <span className="text-sm text-muted-foreground">
          Showing {emails.length} email{emails.length === 1 ? '' : 's'}
        </span>
        <button
          onClick={() => syncMutation.mutate()}
          disabled={syncMutation.isPending}
          className="flex items-center gap-2 px-3 py-1.5 bg-secondary text-secondary-foreground hover:bg-muted text-xs font-medium rounded-md transition-colors"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${syncMutation.isPending ? 'animate-spin' : ''}`} />
          {syncMutation.isPending ? 'Syncing...' : 'Sync Now'}
        </button>
      </div>

      {emails.length === 0 ? (
        <div className="bg-card border border-border rounded-lg p-12 text-center space-y-3">
          <Inbox className="w-10 h-10 text-muted-foreground mx-auto" />
          <h3 className="font-semibold text-foreground">No emails found</h3>
          <p className="text-sm text-muted-foreground max-w-sm mx-auto">
            Connect your Gmail account in Settings or trigger a sync to load your messages.
          </p>
          <Link
            href="/settings"
            className="inline-block mt-2 px-4 py-2 bg-primary text-primary-foreground text-sm font-medium rounded-md hover:opacity-90"
          >
            Go to Settings
          </Link>
        </div>
      ) : (
        <div className="space-y-2">
          {emails.map((email) => (
            <EmailCard
              key={email.id}
              sender={email.sender_name || email.sender_email || 'Unknown'}
              subject={email.subject || '(No Subject)'}
              snippet={email.body_text || ''}
              timestamp={email.timestamp ? new Date(email.timestamp) : new Date()}
              isRead={email.is_read}
              priority={email.priority}
              category={email.category}
            />
          ))}
        </div>
      )}
    </div>
  )
}
