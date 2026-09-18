# Vault Structure Contract

## Stable layers

```text
00-系统/        governance, templates, client protocol, system indexes
01-项目/        one directory per project, one 项目记忆.md authority note
02-复用知识/     cross-project verified techniques and reusable constraints
自动生成/        only inside an approved target; rebuildable machine output
```

Root notes should be navigation only. A project folder must use a meaningful stable name and contain `项目记忆.md`; session summaries belong under that project and link back to the authority note.

## Naming repair

`未命名`, `Untitled`, `New note`, and similar names are audit findings, not rename instructions. First inspect content, decide the owning layer and authority note, then rename one item at a time while checking wikilinks. Empty or duplicate Base views should be given a purpose-based name or removed only after the user confirms they are disposable.

## Retrieval design

Keep the central project index small and current. Put detail in the project memory or reusable notes and link to it. Use generated reports as views, not as a second source of truth. When the Vault grows, compile a question-directed brief from an explicit allowlist rather than asking an Agent to read every note.

## Audit limits

The bundled audit reports missing metadata, missing project authorities, unregistered project folders, and broken internal links. It does not decide whether a note is valuable, whether two notes are duplicates, or what a placeholder should be called.
