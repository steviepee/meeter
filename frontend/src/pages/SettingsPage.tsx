import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { fetchStaff, createStaff, deleteStaff } from '../api'

export default function SettingsPage() {
  const qc = useQueryClient()
  const { data: staff = [], isLoading, isError } = useQuery({ queryKey: ['staff'], queryFn: fetchStaff })

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [slackHandle, setSlackHandle] = useState('')

  const addMutation = useMutation({
    mutationFn: () => createStaff({ name, email, slack_handle: slackHandle || null }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['staff'] })
      setName('')
      setEmail('')
      setSlackHandle('')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => deleteStaff(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['staff'] }),
  })

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Settings — Staff Roster</h1>

      <form
        className="mb-6 flex gap-2 flex-wrap"
        onSubmit={(e) => { e.preventDefault(); addMutation.mutate() }}
      >
        <input
          className="border px-2 py-1 rounded flex-1 min-w-32"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          className="border px-2 py-1 rounded flex-1 min-w-40"
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          className="border px-2 py-1 rounded flex-1 min-w-28"
          placeholder="Slack handle"
          value={slackHandle}
          onChange={(e) => setSlackHandle(e.target.value)}
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700"
          disabled={addMutation.isPending}
        >
          Add
        </button>
      </form>

      {isLoading && <p>Loading...</p>}
      {isError && <p className="text-red-600">Failed to load staff.</p>}

      <ul className="space-y-2">
        {staff.map((m) => (
          <li key={m.id} className="flex items-center justify-between border rounded px-3 py-2">
            <span>
              <span className="font-medium">{m.name}</span>
              <span className="text-gray-500 ml-2">{m.email}</span>
              {m.slack_handle && <span className="text-gray-400 ml-2">{m.slack_handle}</span>}
            </span>
            <button
              className="text-red-500 hover:text-red-700 text-sm"
              onClick={() => deleteMutation.mutate(m.id)}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
