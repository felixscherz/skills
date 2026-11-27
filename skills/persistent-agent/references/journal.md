# Journal

What happened,
for audit and for rebuilding a stale STATUS.
Boot reads the last ~20 lines;
hardly anyone reads the rest.

- One file per month:
  `journal/YYYY-MM.md`.
  Create it when the month's first line is written.
- **Append-only.** Never edit or delete a line.
  Correct a wrong line with a new one.
- One line per entry, dated, from `date '+%Y-%m-%d %H:%M'`:

  ```
  - 2026-11-16 14:05 Split auth rework into 3 briefs, dropped in engineer-1/inbox. Waiting on the user to dispatch.
  ```

- One or two lines per checkpoint.
  Say what changed and what was decided,
  with a pointer (PR, branch, message file)
  instead of detail.
- Append with `>>`,
  so nothing above is touched:

  ```sh
  echo "- $(date '+%Y-%m-%d %H:%M') <what happened>" >> "journal/$(date '+%Y-%m').md"
  ```
