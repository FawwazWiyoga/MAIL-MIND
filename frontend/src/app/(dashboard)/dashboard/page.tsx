export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
        <p className="text-muted-foreground mt-1">Your email intelligence overview</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-card border border-border rounded-lg p-4">
          <h3 className="font-semibold text-card-foreground mb-2">Email Overview</h3>
          <p className="text-muted-foreground text-sm">Connect your Gmail account to get started.</p>
        </div>
        <div className="bg-card border border-border rounded-lg p-4">
          <h3 className="font-semibold text-card-foreground mb-2">Pending Actions</h3>
          <p className="text-muted-foreground text-sm">No action items yet.</p>
        </div>
        <div className="bg-card border border-border rounded-lg p-4">
          <h3 className="font-semibold text-card-foreground mb-2">AI Daily Digest</h3>
          <p className="text-muted-foreground text-sm">Your daily digest will appear here.</p>
        </div>
      </div>
    </div>
  )
}
