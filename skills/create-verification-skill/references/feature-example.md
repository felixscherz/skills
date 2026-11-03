# Feature file example

A feature file in `.agents/skills/verify-<app>/features/` for a notes app with a web UI and a CLI. The app's
`CONTEXT.md` lists the feature as "Create a note", so the file is `features/create-a-note.md`. The skill's helper is
`scripts/notes-verify`, documented in its `SKILL.md`.

The file has a title, one line on what proving it means, and four sections in this order: Reach it, Drive it, Proof,
and Gotchas. What the feature does and where its code is stay in `CONTEXT.md`.

```markdown
# Create a note

Proven when a note created in the browser or the CLI can be reopened from the note list, and a cancelled draft cannot.

## Reach it

- The `New note` button in the toolbar.
- The `n` key, while focus is outside a text field.
- `notes create --title <title> --body <body>` in a terminal.

## Drive it

Preconditions: `scripts/notes-verify doctor` passes, and no note is titled `Release checklist`.

1. **Open the editor.** `scripts/notes-verify browser click --role button --name "New note"`. A form named
   `Note editor` appears, with focus in `Title`.
2. **Fill it in.** `scripts/notes-verify browser fill --role textbox --name "Title" --value "Release checklist"`, then
   the same for `Body` with `Tag and publish`. `Save note` becomes enabled.
3. **Save.** `scripts/notes-verify browser click --role button --name "Save note"`. A status reads `Note saved`.
4. **Reopen it.** Click the `All notes` link, then the `Release checklist` link. The editor shows both values.
5. **Cancel a draft.** Open a new note, enter the title `Discard me`, click `Cancel`. The list has no `Discard me`.
6. **From the CLI.** `scripts/notes-verify cli -- notes create --title "CLI note" --body "From the terminal" --format json`.
   Exit code 0, and stdout holds the new note's ID and title.

## Proof

- `scripts/notes-verify browser snapshot --aria --path proof/create-a-note/list.aria.txt` and
  `scripts/notes-verify browser screenshot --path proof/create-a-note/list.png` after step 6, both showing
  `Release checklist` and `CLI note` in the list.
- The CLI transcript of step 6: command, stdout, stderr, exit code.

## Gotchas

- `n` typed into a focused text field adds the letter instead of opening the editor.
- Titles are trimmed on save. Compare the rendered title, not the input value.
- `Note saved` alone proves nothing. Reopen the note from the list.
- Cleanup deletes both notes but keeps `proof/create-a-note/`.
```
