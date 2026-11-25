'use client'

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { Mail, Trash2, CheckCircle2 } from 'lucide-react'
import { api } from '@/lib/api'
import { EmailAccount } from '@/types'

export default function SettingsPage() {
  const queryClient = useQueryClient()
  const [connecting, setConnecting] = useState(false)

  const { data: accounts = [], isLoading } = useQuery<EmailAccount[]>({
    queryKey: ['accounts'],
    queryFn: async () => {
      const res = await api.get('/accounts')
      return res.data
    },
  })

  const connectGmail = async () => {
    setConnecting(true)
    try {
      const res = await api.post('/accounts/gmail/connect')
      if (res.data?.auth_url) {
        window.location.href = res.data.auth_url
      }
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to start Gmail connection')
    } finally {
      setConnecting(false)
    }
  }

  const deleteAccount = useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/accounts/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accounts'] })
      queryClient.invalidateQueries({ queryKey: ['emails'] })
    },
  })

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Settings</h1>
        <p className="text-muted-foreground mt-1">Manage email connections and workspace preferences</p>
      </div>

      <div className="grid gap-6">
        <div className="bg-card border border-border rounded-lg p-6 space-y-4">
          <div>
            <h3 className="font-semibold text-card-foreground text-lg">Connected Accounts</h3>
            <p className="text-muted-foreground text-sm">
              Connect your Gmail account via Google OAuth to synchronize emails.
            </p>
          </div>

          {isLoading ? (
            <p className="text-sm text-muted-foreground">Loading accounts...</p>
          ) : accounts.length === 0 ? (
            <div className="bg-muted/50 rounded-lg p-4 text-center">
              <p className="text-sm text-muted-foreground mb-3">No email accounts connected yet.</p>
              <button
                onClick={connectGmail}
                disabled={connecting}
                className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:opacity-90 disabled:opacity-50"
              >
                {connecting ? 'Connecting...' : 'Connect Gmail Account'}
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              {accounts.map((acc) => (
                <div
                  key={acc.id}
                  className="flex items-center justify-between p-3 border border-border rounded-md bg-background"
                >
                  <div className="flex items-center gap-3">
                    <Mail className="w-5 h-5 text-primary" />
                    <div>
                      <p className="text-sm font-medium text-foreground">{acc.email_address}</p>
                      <p className="text-xs text-muted-foreground capitalize">{acc.provider}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => deleteAccount.mutate(acc.id)}
                    disabled={deleteAccount.isPending}
                    className="p-2 text-destructive hover:bg-destructive/10 rounded-md transition-colors"
                    title="Disconnect account"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))}
              <button
                onClick={connectGmail}
                disabled={connecting}
                className="mt-2 px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-muted"
              >
                Add Another Gmail Account
              </button>
            </div>
          )}
        </div>

        <div className="bg-card border border-border rounded-lg p-6 space-y-2">
          <h3 className="font-semibold text-card-foreground text-lg">AI Preferences</h3>
          <p className="text-muted-foreground text-sm">
            Primary provider: <strong>Google Gemini</strong>. Cloud AI processing is opt-in for maximum privacy.
          </p>
        </div>
      </div>
    </div>
  )
}
