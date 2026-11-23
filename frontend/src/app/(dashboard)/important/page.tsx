export default function ImportantPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Important</h1>
        <p className="text-muted-foreground mt-1">High-priority and critical emails</p>
      </div>
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <p className="text-muted-foreground">Important emails will appear here after AI analysis.</p>
      </div>
    </div>
  )
}
