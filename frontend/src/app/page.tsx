import { redirect } from 'next/navigation'

export default function Home() {
  // TODO: Check auth status server-side and redirect accordingly
  redirect('/login')
}
