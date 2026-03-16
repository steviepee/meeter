# Ralph Loop — Meeter

You are building Meeter, a meeting-to-tasks application.

## Before every iteration

Read these files first — every time, no exceptions:
- /root/meeter/CLAUDE.md — stack, conventions, project structure
- /root/meeter/PRD.md — full product requirements
- /root/meeter/prd.md — your task list (Status: PENDING / DONE / BLOCKED)
- /root/meeter/progress.md — log of what has already been completed

Check what files already exist under /root/meeter/ before doing any work.

## Your job each iteration

1. Find the FIRST task in prd.md with `Status: PENDING`
2. Read its Description and Verify fields carefully
3. Implement it — create or edit only what that task requires
4. Run the verification command (if one is specified)
5. If verification passes: change `Status: PENDING` to `Status: DONE` in prd.md
6. If verification fails after two fix attempts: change status to `Status: BLOCKED`
   and add a `BlockedReason:` line explaining why
7. Append a entry to progress.md (see format below)
8. Then stop — do not attempt the next task

## progress.md entry format

```
## Iteration [N] — [YYYY-MM-DD]
Task: [task title from prd.md]
Result: DONE | BLOCKED
Notes: [brief note on what was built or why it's blocked]
```

## Important rules

- Work on exactly ONE task per session
- Never skip a PENDING task to do a later one
- If a task is already DONE, move past it — do not redo it
- Do not modify PROMPT.md or ralph.sh
- Always check if a file already exists before creating it
- Follow all conventions in CLAUDE.md exactly
