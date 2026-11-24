export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Settings</h1>
        <p className="text-muted-foreground mt-1">Manage your account and preferences</p>
      </div>
      <div className="grid gap-4">
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="font-semibold text-card-foreground mb-1">Email Accounts</h3>
          <p className="text-muted-foreground text-sm mb-4">Connect and manage your email providers.</p>
          <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:opacity-90">
            Connect Gmail
          </button>
        </div>
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="font-semibold text-card-foreground mb-1">AI Preferences</h3>
          <p className="text-muted-foreground text-sm">Configure AI provider and privacy settings.</p>
        </div>
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="font-semibold text-card-foreground mb-1">Daily Digest</h3>
          <p className="text-muted-foreground text-sm">Schedule and configure your morning digest.</p>
        </div>
      </div>
    </div>
  )
}
