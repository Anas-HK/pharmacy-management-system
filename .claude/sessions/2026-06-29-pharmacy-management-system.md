# 2026-06-29  -  Pharmacy Management System

## Session segment 1 at 21:24

### Done
- Built the whole project from scratch: schema.sql, seed.sql, queries.sql, init_db.py, db.py, app.py (Tkinter GUI), generate_erd.py, generate_report.py, README.md, requirements.txt.
- Generated the ERD (report/ERD.png) and the Word report (report/Pharmacy_Management_System_Report.docx) with 7 embedded images.
- Wrote and ran an automated end-to-end GUI test: 13/13 checks pass (View/Add/Update/Delete/Search/Reports, FK integrity, derived totals).
- Generated 6 full-window GUI screenshots and embedded them in the report.
- Committed everything: bb07be3.

### Decisions (with WHY)
- Stack = Python + Tkinter + SQLite; report as .docx. Why: user asked and confirmed; zero-setup, viva-friendly, matches "not overengineered".
- 7 tables including the Sale_Item junction. Why: resolves the Sale <-> Medicine many-to-many and keeps the schema in 3NF (descriptive fields live once in their parent table, no transitive dependencies).
- db.py opens/closes a connection per call (try/finally). Why: `with sqlite3_conn:` only commits the transaction, it does NOT close the connection; leaked connections locked pharmacy.db on Windows so init_db's os.remove failed.
- Screenshots captured via an on-screen but zero-opacity (-alpha 0.0) window read with the Win32 PrintWindow API. Why: invisible to the user yet fully painted, and PrintWindow reads the window's own buffer so it is immune to focus loss / occlusion.
- Rounded subtotal and total_amount to 2dp in seed.sql and the report queries. Why: 6 * 2.2 displayed as 13.200000000000001 in the reports screen.
- The delete-confirmation screenshot is a PIL composite (app window + the captured dialog). Why: PrintWindow grabs a single window, so the raw dialog shot lacked the app behind it and looked inconsistent with the other five full-window shots.

### Tried but abandoned (with WHY)
- Playwright MCP for the E2E "visual test". Abandoned because: Playwright drives web browsers (DOM/URL); this is a native Tkinter app with nothing for it to attach to. Built a Tkinter-native driver + screenshots instead.
- Off-screen (negative coordinates) PrintWindow capture. Abandoned because: Tkinter never paints an unexposed window, so only the title bar + header rendered; switched to an on-screen zero-opacity window.
- ImageGrab(bbox) screen capture. Abandoned because: it captured black frames whenever the window lost foreground while the user was using the PC.

### Surprises / things learned
- A Tk window at -alpha 0.0 is invisible to the user but is still painted by Windows, so PrintWindow yields a complete, clean capture with no flash.
- sqlite3's `with connection:` is a transaction context manager, not a close().

### Commits
- bb07be3 Initial commit: Pharmacy Management System (DBMS lab project)

## Session segment 2 at 21:35

### Done
- Added a strict rule to C:/Users/Anas/.claude/CLAUDE.md: never list Claude/AI as a commit or PR author/co-author (all projects, existing and new).
- Removed the Co-Authored-By trailer by rebuilding history as a single clean commit (b14437d), authored by Anas-HK, no trailer.
- Added .claude/ to .gitignore so session notes stay local (not pushed).
- Added remote origin and pushed main. Verified origin/main = b14437d, 20 files.

### Decisions (with WHY)
- Rebuilt git history (rm -rf .git + one fresh commit) instead of filter-branch. Why: repo was brand-new and local (nothing pushed), so a clean re-init is simpler than rewriting messages, and it let me drop .claude from the tree in the same step.
- Excluded .claude/ from the GitHub repo. Why: user asked to push "code and doc report"; internal session journals are not deliverables and should not sit in a public university repo.
- Pushed via the active gh account using an ephemeral credential helper (git -c credential.helper='!gh auth git-credential'). Why: gh's active account is Anas-HK (owns the repo, has repo scope); avoids credential-manager account ambiguity and changes no persistent config.

### Surprises / things learned
- gh had two accounts (Anas-HK active, DezySolutions inactive); the repo owner (Anas-HK) was active, so the push used the right token.

### Notes
- Segment 1's hashes (bb07be3, 647542b) no longer exist after the history rebuild; the current single commit is b14437d.

## Session segment 3 at 21:40

### Done
- Per user request, removed .claude/ from .gitignore and pushed the session notes (STATE.md + this journal) to GitHub as a second commit on top of b14437d.

### Decisions (with WHY)
- Added the notes as a new commit rather than rewriting b14437d. Why: b14437d was already pushed; appending avoids a force-push.
