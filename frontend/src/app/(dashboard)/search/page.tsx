export default function SearchPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Search</h1>
        <p className="text-muted-foreground mt-1">Keyword and semantic email search</p>
      </div>
      <input
        type="search"
        placeholder="Search emails by meaning or keywords..."
        className="w-full px-4 py-3 border border-input rounded-lg bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring text-lg"
      />
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <p className="text-muted-foreground">Search results will appear here.</p>
      </div>
    </div>
  )
}
