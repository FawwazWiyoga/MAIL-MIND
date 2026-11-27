'use client'

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  X,
  Sparkles,
  Send,
  Copy,
  Check,
  Calendar,
  AlertCircle,
  Tag,
  Clock,
} from 'lucide-react'
import { api } from '@/lib/api'
import { EmailMessage, AIAnalysis } from '@/types'

interface EmailDetailModalProps {
  email: EmailMessage | null
  onClose: () => void
}

const priorityColors: Record<string, string> = {
  critical: 'bg-red-500/10 text-red-600 border-red-500/20',
  high: 'bg-orange-500/10 text-orange-600 border-orange-500/20',
  medium: 'bg-amber-500/10 text-amber-600 border-amber-500/20',
  low: 'bg-slate-500/10 text-slate-600 border-slate-500/20',
}

export function EmailDetailModal({ email, onClose }: EmailDetailModalProps) {
  const queryClient = useQueryClient()
  const [tone, setTone] = useState<'professional' | 'formal' | 'friendly' | 'concise'>('professional')
  const [instructions, setInstructions] = useState('')
  const [draft, setDraft] = useState('')
  const [copied, setCopied] = useState(false)

  // Fetch cached AI analysis
  const { data: analysis, isLoading: analysisLoading, refetch: refetchAnalysis } = useQuery<AIAnalysis | null>({
    queryKey: ['email-analysis', email?.id],
    queryFn: async () => {
      if (!email?.id) return null
      try {
        const res = await api.get(`/ai/analysis/${email.id}`)
        return res.data
      } catch {
        return null
      }
    },
    enabled: !!email?.id,
  })

  // Trigger AI analysis mutation
  const analyzeMutation = useMutation({
    mutationFn: async () => {
      if (!email?.id) return
      const res = await api.post(`/ai/analyze/${email.id}`)
      return res.data
    },
    onSuccess: () => {
      refetchAnalysis()
      queryClient.invalidateQueries({ queryKey: ['emails'] })
      queryClient.invalidateQueries({ queryKey: ['actions'] })
    },
  })

  // Reply draft generator mutation
  const replyMutation = useMutation({
    mutationFn: async () => {
      if (!email?.id) return
      const res = await api.post('/ai/reply-draft', {
        email_id: email.id,
        tone,
        instructions: instructions.trim() || null,
      })
      return res.data
    },
    onSuccess: (data) => {
      if (data?.draft) {
        setDraft(data.draft)
      }
    },
  })

  if (!email) return null

  const copyDraft = () => {
    navigator.clipboard.writeText(draft)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm">
      <div className="bg-card border border-border w-full max-w-4xl max-h-[90vh] rounded-xl flex flex-col shadow-2xl overflow-hidden">
        {/* Modal Header */}
        <div className="p-5 border-b border-border flex items-start justify-between bg-muted/30">
          <div className="space-y-1 pr-6">
            <h2 className="text-xl font-bold text-foreground leading-tight">
              {email.subject || '(No Subject)'}
            </h2>
            <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-muted-foreground">
              <span>
                <strong>From:</strong> {email.sender_name} &lt;{email.sender_email}&gt;
              </span>
              <span>
                <strong>Date:</strong> {email.timestamp ? new Date(email.timestamp).toLocaleString() : 'N/A'}
              </span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* AI Intelligence Card */}
          <div className="bg-primary/5 border border-primary/20 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-primary font-semibold text-sm">
                <Sparkles className="w-4 h-4" />
                <span>AI Email Intelligence</span>
              </div>
              <button
                onClick={() => analyzeMutation.mutate()}
                disabled={analyzeMutation.isPending}
                className="px-3 py-1 bg-primary text-primary-foreground text-xs font-medium rounded-md hover:opacity-90 disabled:opacity-50 transition-all flex items-center gap-1.5"
              >
                <Sparkles className="w-3.5 h-3.5" />
                {analyzeMutation.isPending ? 'Analyzing...' : analysis ? 'Re-Analyze' : 'Analyze Email'}
              </button>
            </div>

            {analysis ? (
              <div className="space-y-3">
                <div className="flex flex-wrap gap-2">
                  <span
                    className={`text-xs px-2.5 py-0.5 rounded-full font-medium border ${
                      priorityColors[analysis.priority] || priorityColors.medium
                    }`}
                  >
                    Priority: {analysis.priority.toUpperCase()}
                  </span>
                  <span className="text-xs px-2.5 py-0.5 rounded-full font-medium bg-secondary text-secondary-foreground border border-border">
                    Category: {analysis.category}
                  </span>
                  <span className="text-xs text-muted-foreground self-center ml-auto">
                    Confidence: {(analysis.confidence_score * 100).toFixed(0)}%
                  </span>
                </div>

                <div>
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-1">
                    Summary
                  </h4>
                  <p className="text-sm text-foreground leading-relaxed">{analysis.summary}</p>
                </div>

                {analysis.action_items && analysis.action_items.length > 0 && (
                  <div>
                    <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-1.5">
                      Extracted Action Items
                    </h4>
                    <ul className="space-y-1.5">
                      {analysis.action_items.map((item, idx) => (
                        <li
                          key={idx}
                          className="flex items-start gap-2 text-xs bg-background/80 border border-border p-2 rounded-md"
                        >
                          <span className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5 flex-shrink-0" />
                          <span className="flex-1 font-medium text-foreground">{item.description}</span>
                          {item.due_date && (
                            <span className="flex items-center gap-1 text-muted-foreground text-[10px] bg-muted px-2 py-0.5 rounded">
                              <Clock className="w-3 h-3" />
                              {item.due_date}
                            </span>
                          )}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-xs text-muted-foreground">
                Click &quot;Analyze Email&quot; to generate an AI summary, priority level, category, and action tasks.
              </p>
            )}
          </div>

          {/* Email Body */}
          <div className="space-y-2">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Original Message
            </h3>
            <div className="p-4 rounded-lg bg-muted/20 border border-border text-sm text-foreground whitespace-pre-wrap font-sans leading-relaxed">
              {email.body_text || email.snippet || '(No message body available)'}
            </div>
          </div>

          {/* AI Reply Generator */}
          <div className="bg-card border border-border rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-foreground flex items-center gap-2">
                <Send className="w-4 h-4 text-primary" />
                Draft AI Reply
              </h3>
              <div className="flex items-center gap-2">
                <span className="text-xs text-muted-foreground">Tone:</span>
                <select
                  value={tone}
                  onChange={(e) => setTone(e.target.value as any)}
                  className="text-xs bg-background border border-input rounded-md px-2.5 py-1 text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
                >
                  <option value="professional">Professional</option>
                  <option value="formal">Formal</option>
                  <option value="friendly">Friendly</option>
                  <option value="concise">Concise</option>
                </select>
              </div>
            </div>

            <div className="flex gap-2">
              <input
                type="text"
                value={instructions}
                onChange={(e) => setInstructions(e.target.value)}
                placeholder="Optional instructions (e.g., 'Say I agree and propose meeting on Friday at 2 PM')"
                className="flex-1 px-3 py-1.5 text-xs bg-background border border-input rounded-md text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring"
              />
              <button
                onClick={() => replyMutation.mutate()}
                disabled={replyMutation.isPending}
                className="px-4 py-1.5 bg-primary text-primary-foreground text-xs font-medium rounded-md hover:opacity-90 disabled:opacity-50 transition-all flex items-center gap-1.5"
              >
                <Sparkles className="w-3.5 h-3.5" />
                {replyMutation.isPending ? 'Drafting...' : 'Generate Draft'}
              </button>
            </div>

            {draft && (
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <span>Generated Reply Draft:</span>
                  <button
                    onClick={copyDraft}
                    className="flex items-center gap-1 hover:text-foreground transition-colors font-medium text-primary"
                  >
                    {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                    {copied ? 'Copied!' : 'Copy to Clipboard'}
                  </button>
                </div>
                <textarea
                  value={draft}
                  onChange={(e) => setDraft(e.target.value)}
                  rows={6}
                  className="w-full p-3 text-xs bg-muted/30 border border-input rounded-md text-foreground font-mono leading-relaxed focus:outline-none focus:ring-1 focus:ring-ring"
                />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
