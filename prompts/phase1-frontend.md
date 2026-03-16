# Phase 1 — Frontend Scaffold

You are working on a project called Meeter. Start every iteration by reading
these files in order:

1. /root/meeter/CLAUDE.md — conventions and stack decisions
2. /root/meeter/PRD.md — product requirements
3. /root/meeter/CHECKLIST.md — your progress tracker

Then check what files currently exist under /root/meeter/frontend/.

Your job is to complete every unchecked item under "Phase 1 — Frontend Scaffold"
in CHECKLIST.md. Work through them one at a time. After completing each item,
mark it [x] in CHECKLIST.md before moving to the next.

---

## What to build

### Step 1 — Scaffold the Vite project
If /root/meeter/frontend/ does not exist or has no package.json, run:

```
cd /root/meeter && npm create vite@latest frontend -- --template react-ts
```

### Step 2 — Install dependencies
```
cd /root/meeter/frontend && npm install
npm install react-router-dom @tanstack/react-query
npm install tailwindcss @tailwindcss/vite
```

### Step 3 — Configure Tailwind
In vite.config.ts, add the Tailwind plugin:
```ts
import tailwindcss from '@tailwindcss/vite'
// add to plugins array: tailwindcss()
```

In src/index.css, replace all contents with:
```css
@import "tailwindcss";
```

### Step 4 — Create src/api/index.ts
Empty file with a placeholder comment:
```ts
// API hooks (TanStack Query) — added per phase
```

### Step 5 — Create page shells in src/pages/
Create these three files:

**MeetingPage.tsx**
```tsx
export default function MeetingPage() {
  return <div>Meeting</div>
}
```

**TaskListPage.tsx**
```tsx
export default function TaskListPage() {
  return <div>Tasks</div>
}
```

**SettingsPage.tsx**
```tsx
export default function SettingsPage() {
  return <div>Settings</div>
}
```

### Step 6 — Wire up React Router in src/App.tsx
Replace the contents of App.tsx with:
```tsx
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
```

### Step 7 — Wrap app in QueryClientProvider in src/main.tsx
Add `QueryClient` and `QueryClientProvider` from `@tanstack/react-query`
wrapping the `<App />` component.

### Step 8 — Create .env.example
At /root/meeter/frontend/.env.example:
```
VITE_API_BASE_URL=http://localhost:8000
```

---

## Verification

After all files are in place, run:

```
cd /root/meeter/frontend && npm run build
```

If the build fails, read the TypeScript or module errors carefully, fix the
root cause, and run again. Do not move on until the build exits 0 with no errors.

---

## Completion

When `npm run build` exits 0 with no errors and all Phase 1 frontend items in
CHECKLIST.md are marked [x], output exactly:

<promise>PHASE1_FRONTEND_COMPLETE</promise>

Do not output the promise until the build actually passes.
