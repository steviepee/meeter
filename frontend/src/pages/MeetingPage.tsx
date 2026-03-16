import { useState, useRef, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { fetchStaff } from '../api'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

interface Task {
  id?: number
  description: string
  assignee_id: number | null
  due_date: string | null
  confidence?: number
}

export default function MeetingPage() {
  const [meetingId, setMeetingId] = useState<number | null>(null)
  const [_recording, setRecording] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [status, setStatus] = useState<'idle' | 'recording' | 'reviewing'>('idle')
  const [tasks, setTasks] = useState<Task[]>([])
  const [error, setError] = useState<string | null>(null)
  const [sending, setSending] = useState(false)
  const [sent, setSent] = useState(false)

  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const esRef = useRef<EventSource | null>(null)

  const { data: staff = [] } = useQuery({ queryKey: ['staff'], queryFn: fetchStaff })

  async function startRecording() {
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/meetings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: `Meeting ${new Date().toLocaleString()}` }),
      })
      if (!res.ok) throw new Error('Failed to create meeting')
      const meeting = await res.json()
      setMeetingId(meeting.id)

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mr = new MediaRecorder(stream)
      mediaRecorderRef.current = mr

      mr.addEventListener('dataavailable', async (e) => {
        if (e.data.size === 0) return
        const buf = await e.data.arrayBuffer()
        await fetch(`${API_BASE}/meetings/${meeting.id}/transcript/chunk`, {
          method: 'POST',
          body: buf,
        })
      })

      mr.start(3000)
      setRecording(true)
      setStatus('recording')

      const es = new EventSource(`${API_BASE}/meetings/${meeting.id}/transcript/stream`)
      esRef.current = es
      es.onmessage = (e) => setTranscript(e.data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    }
  }

  async function stopRecording() {
    mediaRecorderRef.current?.stop()
    mediaRecorderRef.current?.stream.getTracks().forEach((t) => t.stop())
    esRef.current?.close()
    setRecording(false)

    if (meetingId) {
      await fetch(`${API_BASE}/meetings/${meetingId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: 'reviewing' }),
      })
      const res = await fetch(`${API_BASE}/meetings/${meetingId}/extract`, { method: 'POST' })
      if (res.ok) {
        const extracted = await res.json()
        setTasks(extracted)
      }
    }
    setStatus('reviewing')
  }

  async function sendTasks() {
    if (!meetingId) return
    setSending(true)
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/meetings/${meetingId}/send`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tasks }),
      })
      if (!res.ok) throw new Error('Failed to send tasks')
      setSent(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Send failed')
    } finally {
      setSending(false)
    }
  }

  function updateTask(index: number, patch: Partial<Task>) {
    setTasks((prev) => prev.map((t, i) => (i === index ? { ...t, ...patch } : t)))
  }

  function deleteTask(index: number) {
    setTasks((prev) => prev.filter((_, i) => i !== index))
  }

  function addTask() {
    setTasks((prev) => [...prev, { description: '', assignee_id: null, due_date: null, confidence: 1 }])
  }

  useEffect(() => {
    return () => { esRef.current?.close() }
  }, [])

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Meeting</h1>

      {error && <p className="text-red-600 mb-4">{error}</p>}

      {status === 'idle' && (
        <button
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          onClick={startRecording}
        >
          Start Recording
        </button>
      )}

      {status === 'recording' && (
        <div className="flex gap-3 items-center mb-4">
          <button
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
            onClick={stopRecording}
          >
            Stop Recording
          </button>
          <span className="text-red-500 animate-pulse">● Recording</span>
        </div>
      )}

      {transcript && status === 'recording' && (
        <div className="border rounded p-4 bg-gray-50 whitespace-pre-wrap text-sm mb-4">
          <h2 className="font-semibold mb-2">Transcript</h2>
          {transcript}
        </div>
      )}

      {status === 'reviewing' && !sent && (
        <div className="mt-4">
          <h2 className="text-xl font-semibold mb-3">Review Tasks</h2>

          {tasks.length === 0 && <p className="text-gray-500 mb-3">No tasks extracted.</p>}

          <ul className="space-y-3 mb-4">
            {tasks.map((task, i) => (
              <li
                key={i}
                className={`border rounded p-3 ${
                  task.confidence !== undefined && task.confidence < 0.6
                    ? 'border-yellow-400 bg-yellow-50'
                    : ''
                }`}
              >
                {task.confidence !== undefined && task.confidence < 0.6 && (
                  <span className="text-xs text-yellow-600 font-medium">Low confidence</span>
                )}
                <div className="flex gap-2 mt-1 flex-wrap">
                  <input
                    className="border rounded px-2 py-1 flex-1 min-w-48 text-sm"
                    value={task.description}
                    onChange={(e) => updateTask(i, { description: e.target.value })}
                    placeholder="Task description"
                  />
                  <select
                    className="border rounded px-2 py-1 text-sm"
                    value={task.assignee_id ?? ''}
                    onChange={(e) => updateTask(i, { assignee_id: e.target.value ? Number(e.target.value) : null })}
                  >
                    <option value="">Unassigned</option>
                    {staff.map((s) => (
                      <option key={s.id} value={s.id}>{s.name}</option>
                    ))}
                  </select>
                  <input
                    type="date"
                    className="border rounded px-2 py-1 text-sm"
                    value={task.due_date ?? ''}
                    onChange={(e) => updateTask(i, { due_date: e.target.value || null })}
                  />
                  <button
                    className="text-red-500 hover:text-red-700 text-sm px-2"
                    onClick={() => deleteTask(i)}
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>

          <div className="flex gap-3">
            <button
              className="border rounded px-3 py-2 text-sm hover:bg-gray-100"
              onClick={addTask}
            >
              + Add Task
            </button>
            <button
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              onClick={sendTasks}
              disabled={sending}
            >
              {sending ? 'Sending...' : 'Confirm & Send'}
            </button>
          </div>
        </div>
      )}

      {sent && (
        <p className="mt-4 text-green-600 font-medium">Tasks sent successfully.</p>
      )}
    </div>
  )
}
