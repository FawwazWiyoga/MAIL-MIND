'use client'

export function EmailList() {
  return (
    <div className="space-y-2">
      {[1, 2, 3].map((i) => (
        <div key={i} className="bg-card border border-border rounded-lg p-4 animate-pulse">
          <div className="h-4 bg-muted rounded w-1/4 mb-2" />
          <div className="h-4 bg-muted rounded w-3/4 mb-2" />
          <div className="h-3 bg-muted rounded w-1/2" />
        </div>
      ))}
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <p className="text-muted-foreground">Connect your Gmail account to see emails here.</p>
      </div>
    </div>
  )
}
