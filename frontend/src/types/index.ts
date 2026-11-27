export interface User {
  id: string
  email: string
  full_name: string | null
  is_active: boolean
  created_at: string
}

export interface EmailAccount {
  id: string
  provider: string
  email_address: string
  is_active: boolean
}

export interface EmailMessage {
  id: string
  thread_id: string
  sender_email: string | null
  sender_name: string | null
  recipient_emails?: string[]
  subject: string | null
  body_text: string | null
  body_html?: string | null
  timestamp: string | null
  is_read: boolean
  labels: string[]
  priority?: 'critical' | 'high' | 'medium' | 'low'
  category?: string
}

export interface ActionItem {
  id: string
  user_id: string
  message_id: string | null
  description: string
  due_date: string | null
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled'
  priority: 'critical' | 'high' | 'medium' | 'low'
  created_at: string
  updated_at: string
}

export interface AIAnalysis {
  id: string
  message_id: string
  summary: string
  category: string
  priority: 'critical' | 'high' | 'medium' | 'low'
  action_items: Array<{ description: string; due_date: string | null; priority: string }>
  confidence_score: number
  ai_provider: string
  model_used: string
  created_at: string
}

export interface AIMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  sources?: Array<{ email_id: string; subject: string }>
  created_at: string
}
