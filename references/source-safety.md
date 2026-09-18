# Source Safety Rules

## Default scope

Scan only paths the user names or explicitly confirms after a read-only discovery. Prefer focused media/project folders over a home directory or disk root.

## Default exclusions

The script skips common generated and dependency directories: `.git`, `.obsidian`, `node_modules`, `__pycache__`, `.venv`, `venv`, `dist`, `build`, `out`, `coverage`, `.idea`, and `.vscode`. It does not claim these exclusions prove that every remaining file is an authored work.

## Privacy boundary

Do not scan chat-app attachments, browser profiles/download caches, email stores, cloud-drive roots, system folders, or unknown removable/network drives by default. A user may approve a precise subfolder after seeing the privacy implication; still avoid copying private material into notes.

## Classification boundary

File extension and directory grouping are inventory facts, not authorship, ownership, copyright, or artistic-quality judgments. Screenshots, reference images, and exported previews should be marked for human review when their role is unclear.

## Memory and context boundary

Vault structure audits are read-only by default. Context briefs read only explicitly approved Markdown notes and must preserve `needs_review` and `blocked` states. A project name never authorizes recursive code, session, chat, browser, cloud, or dependency scanning.

## Duplicate boundary

`--hash-content` identifies byte-for-byte duplicate content only. Similar-looking images, resized versions, and derivative works are not considered duplicates unless a human decides so.
