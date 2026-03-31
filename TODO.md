# Test Pipeline Implementation TODO

## 1. `backend/services/transcription.py` — Add `transcribe_file`
- [ ] Add `transcribe_file(file_path: str) -> str` wrapper that reads a file from disk and passes bytes to existing `transcribe_chunk`

## 2. `backend/services/extraction.py` — Add `extract_tasks_with_reasoning`
- [ ] Add enhanced prompt (`EXTRACTION_PROMPT_WITH_REASONING`) that asks Claude to explain why each task was identified, why the assignee was chosen, and what affects confidence
- [ ] Add tool schema with three extra fields per task: `task_reasoning`, `assignee_reasoning`, `confidence_reasoning`
- [ ] Add `extract_tasks_with_reasoning(transcript, staff)` function using the new prompt and schema (`max_tokens=4096`)

## 3. `backend/test_fixtures/sample_staff.json` — Default test roster
- [ ] Create file with 4 sample staff members (id, name, email)

## 4. `backend/test_pipeline.py` — CLI entry point
- [ ] Add `extract_audio(input_path)` helper: detect video by extension, extract 16kHz mono WAV via ffmpeg to a temp file, return path as-is for audio
- [ ] Implement pipeline steps:
  - [ ] Parse CLI args: positional file path, `--staff` (default: `test_fixtures/sample_staff.json`), `--output` (default: `report.md`)
  - [ ] Load staff roster from JSON
  - [ ] Call `extract_audio()` then `transcribe_file()`
  - [ ] Call `extract_tasks_with_reasoning()`
  - [ ] Build email previews using body logic from `email.py` (no sending)
  - [ ] Write markdown report
- [ ] Clean up temp WAV file after transcription

## 5. Verification
- [ ] Run `python test_pipeline.py <file>` with a real audio/video file and valid `ANTHROPIC_API_KEY`
- [ ] Confirm report contains all sections: transcription, tasks with reasoning, email previews, summary
- [ ] Confirm no emails are sent
- [ ] Run `pytest` to confirm existing 13 tests still pass
