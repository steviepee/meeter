## Making it betta##

- We can spit out a version of the transcript with all the places where a task was extracted highlighted for review and calibration (anyway, how would we remember what the tasks are actually supposed to be if we don't take a look at the words in the moment?).

- Eventually a space/color/workflow for disagreements and calls for clarification or mediation

- System keeps tasteful profiles on all meeting employees, judging the task deployment on things like proclivity, availability, etc

- Can do self-prompt creation through the Prompt-maker, then send a planned fix to the person who has the task for them to review (if the task is under a certain rank)

- Human checkpoint can include the ranking of the task. Certain rankings prompt an attempt from the agent to come up with a plan itself. Maybe we can make this feature toggle-able, since it does come with costs and computing power and some people may not like being nudged at the onset...

- Can follow up periodically on tasks depending on the importance of the task and/or the amount of time/complication regarding the task's completion.

---

## Android / Mobile Access (PWA)

Use your phone as a meeting recorder when your laptop isn't present. No native app or Play Store required — runs in Chrome on Android.

### Phase A — Backend deployment
- Deploy FastAPI backend to a cloud VPS (Render / Railway / Fly.io)
- Update CORS in `main.py` to allow the deployed frontend origin
- Move `meeter.db` to a persistent volume (SQLite on a VPS is fine for small teams)
- Update `backend/.env` with production SMTP credentials and Anthropic key

### Phase B — Frontend deployment
- Set `VITE_API_BASE_URL` to the deployed backend URL
- Build and deploy React app to Vercel or Netlify
- Verify `MediaRecorder` mic capture works in Chrome on Android

### Phase C — PWA shell
- Install `vite-plugin-pwa` and configure in `vite.config.ts`
- Add `public/manifest.json` (app name, theme color, display: standalone)
- Generate icon assets at 192x192 and 512x512
- Test "Add to Home Screen" prompt in Chrome on Android

### Phase D — Mobile UX
- Make `MeetingPage` layout responsive for small screens
- Ensure Start/Stop recording buttons are thumb-friendly (large tap targets)
- Test full flow on Android: record → extract → review → send
