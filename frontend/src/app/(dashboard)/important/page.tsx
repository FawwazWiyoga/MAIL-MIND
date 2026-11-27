'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Star, Inbox } from 'lucide-react'
import { api } from '@/lib/api'
import { EmailCard } from '@/components/email/EmailCard'
import { EmailDetailModal } from '@/components/email/EmailDetailModal'
import { EmailMessage } from '@/types'

export function ImportantPage() {
  const [selectedEmail, setSelectedEmail] = useState<EmailMessage | null>(null)

  const { data: emails = [], isLoading } = useQuery<EmailMessage[]>({
    queryKey: ['emails'],
    queryFn: async () => {
      const res = await api.get('/emails?per_page=100')
      return res.data
    },
  })

  // Filter critical or high priority emails, or category == 'Important'
  const importantEmails = emails.filter(
    (e) =>
      e.priority === 'critical' ||
      e.priority === 'high' ||
      (e.category && e.category.toLowerCase() === 'important') ||
      (e.labels && e.labels.includes('IMPORTANT'))
  )

  if (isLoading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-20 bg-muted/40 rounded-lg animate-pulse" />
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Star className="w-6 h-6 text-amber-500 fill-amber-500" />
        <div>
          <h1 className="text-2xl font-bold text-foreground">Important Emails</h1>
          <p className="text-muted-foreground mt-0.5">
            Emails categorized with High or Critical priority by AI analysis
          </p>
        </div>
      </div>

      {importantEmails.length === 0 ? (
        <div className="bg-card border border-border rounded-lg p-12 text-center space-y-3">
          <Inbox className="w-10 h-10 text-muted-foreground mx-auto" />
          <h3 className="font-semibold text-foreground">No urgent emails</h3>
          <p className="text-sm text-muted-foreground max-w-sm mx-auto">
            Emails marked as high or critical priority will be automatically surfaced here.
          </p>
        </div>
      ) : (
        <div className="space-y-2">
          {importantEmails.map((email) => (
            <EmailCard
              key={email.id}
              sender={email.sender_name || email.sender_email || 'Unknown'}
              subject={email.subject || '(No Subject)'}
              snippet={email.body_text || ''}
              timestamp={email.timestamp ? new Date(email.timestamp) : new Date()}
              isRead={email.is_read}
              priority={email.priority}
              category={email.category}
              onClick={() => setSelectedEmail(email)}
            />
          ))}
        </div>
      )}

      {selectedEmail && (
        <EmailDetailModal email={selectedEmail} onClose={() => setSelectedEmail(null)} />
      )}
    </div>
  )
}

export default ImportantPage
