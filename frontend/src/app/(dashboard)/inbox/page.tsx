import { EmailList } from '@/components/email/EmailList'

export default function InboxPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Inbox</h1>
        <p className="text-muted-foreground mt-1">Your synchronized emails</p>
      </div>
      <EmailList />
    </div>
  )
}
