export default function ActionsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Action Items</h1>
        <p className="text-muted-foreground mt-1">Tasks and follow-ups extracted from your emails</p>
      </div>
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <p className="text-muted-foreground">Action items extracted by AI will appear here.</p>
      </div>
    </div>
  )
}
