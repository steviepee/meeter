import { BrowserRouter, Routes, Route } from 'react-router-dom'
import MeetingPage from './pages/MeetingPage'
import TaskListPage from './pages/TaskListPage'
import SettingsPage from './pages/SettingsPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MeetingPage />} />
        <Route path="/tasks" element={<TaskListPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </BrowserRouter>
  )
}
