const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export interface StaffMember {
  id: number
  name: string
  email: string
  slack_handle: string | null
}

export async function fetchStaff(): Promise<StaffMember[]> {
  const res = await fetch(`${API_BASE}/staff`)
  if (!res.ok) throw new Error('Failed to fetch staff')
  return res.json()
}

export async function createStaff(data: Omit<StaffMember, 'id'>): Promise<StaffMember> {
  const res = await fetch(`${API_BASE}/staff`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error('Failed to create staff member')
  return res.json()
}

export async function deleteStaff(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/staff/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Failed to delete staff member')
}
