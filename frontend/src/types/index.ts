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
  subject: string | null
  body_text: string | null
  timestamp: string | null
  is_read: boolean
  labels: string[]
  priority?: 'critical' | 'high' | 'medium' | 'low'
  category?: string
}

export interface ActionItem {
  id: string
  description: string
  due_date: string | null
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled'
  priority: 'critical' | 'high' | 'medium' | 'low'
  source_email_id: string | null
}

export interface AIMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  sources?: Array<{ email_id: string; subject: string }>
  created_at: string
}
