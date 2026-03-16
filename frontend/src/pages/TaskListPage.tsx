import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

interface Meeting {
  id: number
  title: string
  created_at: string
  status: string
}

interface Task {
  id: number
  description: string
  assignee_id: number | null
  due_date: string | null
  sent_at: string | null
}

interface StaffMember {
  id: number
  name: string
  email: string
}

async function fetchMeetings(): Promise<Meeting[]> {
  const res = await fetch(`${API_BASE}/meetings`)
  if (!res.ok) throw new Error('Failed to fetch meetings')
  return res.json()
}

async function fetchMeetingTasks(id: number): Promise<Task[]> {
  const res = await fetch(`${API_BASE}/meetings/${id}/tasks`)
  if (!res.ok) throw new Error('Failed to fetch tasks')
  return res.json()
}

async function fetchStaff(): Promise<StaffMember[]> {
  const res = await fetch(`${API_BASE}/staff`)
  if (!res.ok) throw new Error('Failed to fetch staff')
  return res.json()
}

function MeetingRow({ meeting, staff }: { meeting: Meeting; staff: StaffMember[] }) {
  const [expanded, setExpanded] = useState(false)
  const { data: tasks = [], isLoading } = useQuery({
    queryKey: ['meeting-tasks', meeting.id],
    queryFn: () => fetchMeetingTasks(meeting.id),
    enabled: expanded,
  })

  const byAssignee = tasks.reduce<Record<string, Task[]>>((acc, t) => {
    const key = t.assignee_id ? String(t.assignee_id) : 'unassigned'
    acc[key] = [...(acc[key] ?? []), t]
    return acc
  }, {})

  const staffById = Object.fromEntries(staff.map((s) => [String(s.id), s.name]))

  return (
    <li className="border rounded mb-2">
      <button
        className="w-full text-left px-4 py-3 flex justify-between items-center hover:bg-gray-50"
        onClick={() => setExpanded((v) => !v)}
      >
        <span>
          <span className="font-medium">{meeting.title}</span>
          <span className="text-gray-400 text-sm ml-3">{new Date(meeting.created_at).toLocaleString()}</span>
        </span>
        <span className="text-xs text-gray-500 uppercase">{meeting.status}</span>
      </button>

      {expanded && (
        <div className="px-4 pb-3">
          {isLoading && <p className="text-sm text-gray-400">Loading tasks...</p>}
          {!isLoading && tasks.length === 0 && <p className="text-sm text-gray-400">No tasks.</p>}
          {Object.entries(byAssignee).map(([key, groupTasks]) => (
            <div key={key} className="mb-3">
              <h3 className="font-semibold text-sm mb-1">
                {key === 'unassigned' ? 'Unassigned' : staffById[key] ?? `Staff #${key}`}
              </h3>
              <ul className="space-y-1">
                {groupTasks.map((t) => (
                  <li key={t.id} className="text-sm pl-3 border-l-2 border-gray-200">
                    {t.description}
                    {t.due_date && <span className="text-gray-400 ml-2">due {t.due_date}</span>}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </li>
  )
}

export default function TaskListPage() {
  const { data: meetings = [], isLoading, isError } = useQuery({ queryKey: ['meetings'], queryFn: fetchMeetings })
  const { data: staff = [] } = useQuery({ queryKey: ['staff'], queryFn: fetchStaff })

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">All Meetings</h1>

      {isLoading && <p>Loading...</p>}
      {isError && <p className="text-red-600">Failed to load meetings.</p>}

      {!isLoading && meetings.length === 0 && (
        <p className="text-gray-500">No meetings yet.</p>
      )}

      <ul>
        {meetings.map((m) => (
          <MeetingRow key={m.id} meeting={m} staff={staff} />
        ))}
      </ul>
    </div>
  )
}
