'use client'

import { useRouter } from 'next/navigation'
import { Search, Bell, LogOut, User as UserIcon } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'

export function TopNav() {
  const router = useRouter()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    logout()
    router.push('/login')
  }

  return (
    <header className="h-16 border-b border-border bg-card flex items-center justify-between px-6">
      <div className="flex-1 max-w-xl">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            type="search"
            placeholder="Search emails..."
            className="w-full pl-10 pr-4 py-2 bg-background border border-input rounded-md text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>
      </div>
      <div className="flex items-center gap-3">
        {user && (
          <span className="text-xs text-muted-foreground font-medium hidden md:inline-block">
            {user.full_name || user.email}
          </span>
        )}
        <button className="p-2 hover:bg-muted rounded-md text-muted-foreground hover:text-foreground transition-colors">
          <Bell className="w-5 h-5" />
        </button>
        <button className="p-2 hover:bg-muted rounded-md text-muted-foreground hover:text-foreground transition-colors">
          <UserIcon className="w-5 h-5" />
        </button>
        <button
          onClick={handleLogout}
          className="p-2 hover:bg-muted rounded-md text-muted-foreground hover:text-foreground transition-colors"
          title="Logout"
        >
          <LogOut className="w-5 h-5" />
        </button>
      </div>
    </header>
  )
}
