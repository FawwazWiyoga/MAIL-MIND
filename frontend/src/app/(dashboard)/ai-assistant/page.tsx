import { ChatInterface } from '@/components/ai/ChatInterface'

export default function AIAssistantPage() {
  return (
    <div className="flex flex-col h-full space-y-4">
      <div>
        <h1 className="text-2xl font-bold text-foreground">AI Assistant</h1>
        <p className="text-muted-foreground mt-1">Ask questions about your emails</p>
      </div>
      <div className="flex-1">
        <ChatInterface />
      </div>
    </div>
  )
}
