'use client'

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { CheckSquare, Square, Trash2, Plus, Clock, Tag } from 'lucide-react'
import { api } from '@/lib/api'
import { ActionItem } from '@/types'

const priorityColors: Record<string, string> = {
  critical: 'bg-red-500/10 text-red-600 border-red-500/20',
  high: 'bg-orange-500/10 text-orange-600 border-orange-500/20',
  medium: 'bg-amber-500/10 text-amber-600 border-amber-500/20',
  low: 'bg-slate-500/10 text-slate-600 border-slate-500/20',
}

export default function ActionsPage() {
  const queryClient = useQueryClient()
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all')
  const [newDesc, setNewDesc] = useState('')
  const [newPriority, setNewPriority] = useState<'critical' | 'high' | 'medium' | 'low'>('medium')

  const { data: actions = [], isLoading } = useQuery<ActionItem[]>({
    queryKey: ['actions'],
    queryFn: async () => {
      const res = await api.get('/actions')
      return res.data
    },
  })

  const toggleStatus = useMutation({
    mutationFn: async ({ id, currentStatus }: { id: string; currentStatus: string }) => {
      const newStatus = currentStatus === 'completed' ? 'pending' : 'completed'
      await api.patch(`/actions/${id}`, { status: newStatus })
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['actions'] })
    },
  })

  const createAction = useMutation({
    mutationFn: async () => {
      if (!newDesc.trim()) return
      await api.post('/actions', {
        description: newDesc.trim(),
        priority: newPriority,
      })
    },
    onSuccess: () => {
      setNewDesc('')
      queryClient.invalidateQueries({ queryKey: ['actions'] })
    },
  })

  const deleteAction = useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/actions/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['actions'] })
    },
  })

  const filteredActions = actions.filter((item) => {
    if (filter === 'all') return true
    return item.status === filter
  })

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Action Items</h1>
          <p className="text-muted-foreground mt-1">
            Tasks, requests, and deadlines extracted from your emails
          </p>
        </div>
        <div className="flex gap-1 bg-muted p-1 rounded-lg">
          {(['all', 'pending', 'completed'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setFilter(tab)}
              className={`px-3 py-1 text-xs font-medium rounded-md capitalize transition-all ${
                filter === tab
                  ? 'bg-background text-foreground shadow-sm'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Quick Add Form */}
      <div className="flex gap-2 bg-card border border-border p-3 rounded-lg">
        <input
          type="text"
          value={newDesc}
          onChange={(e) => setNewDesc(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && createAction.mutate()}
          placeholder="Add an action task manually..."
          className="flex-1 bg-background border border-input rounded-md px-3 py-1.5 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
        />
        <select
          value={newPriority}
          onChange={(e) => setNewPriority(e.target.value as any)}
          className="bg-background border border-input rounded-md px-2.5 py-1.5 text-xs text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>
        <button
          onClick={() => createAction.mutate()}
          disabled={!newDesc.trim() || createAction.isPending}
          className="px-4 py-1.5 bg-primary text-primary-foreground text-xs font-medium rounded-md hover:opacity-90 disabled:opacity-50 flex items-center gap-1.5"
        >
          <Plus className="w-4 h-4" />
          Add
        </button>
      </div>

      {/* Task List */}
      {isLoading ? (
        <div className="space-y-2">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-12 bg-muted/40 rounded-lg animate-pulse" />
          ))}
        </div>
      ) : filteredActions.length === 0 ? (
        <div className="bg-card border border-border rounded-lg p-12 text-center">
          <p className="text-muted-foreground text-sm">No action items found in this category.</p>
        </div>
      ) : (
        <div className="space-y-2">
          {filteredActions.map((item) => (
            <div
              key={item.id}
              className={`flex items-center justify-between p-3.5 bg-card border border-border rounded-lg transition-all ${
                item.status === 'completed' ? 'opacity-60 bg-muted/20' : 'hover:border-primary/40'
              }`}
            >
              <div className="flex items-center gap-3 flex-1 min-w-0 mr-4">
                <button
                  onClick={() =>
                    toggleStatus.mutate({ id: item.id, currentStatus: item.status })
                  }
                  className="text-primary hover:opacity-80 transition-opacity"
                >
                  {item.status === 'completed' ? (
                    <CheckSquare className="w-5 h-5 text-green-600" />
                  ) : (
                    <Square className="w-5 h-5 text-muted-foreground" />
                  )}
                </button>
                <span
                  className={`text-sm text-foreground truncate ${
                    item.status === 'completed' ? 'line-through text-muted-foreground' : 'font-medium'
                  }`}
                >
                  {item.description}
                </span>
                <span
                  className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border ${
                    priorityColors[item.priority] || priorityColors.medium
                  }`}
                >
                  {item.priority}
                </span>
                {item.due_date && (
                  <span className="flex items-center gap-1 text-[11px] text-muted-foreground bg-muted px-2 py-0.5 rounded">
                    <Clock className="w-3 h-3" />
                    {new Date(item.due_date).toLocaleDateString()}
                  </span>
                )}
              </div>
              <button
                onClick={() => deleteAction.mutate(item.id)}
                disabled={deleteAction.isPending}
                className="p-1.5 text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded-md transition-colors"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
