# Session Summary Contract

Use this mode when the user explicitly requests session summaries, or when a Vault or compatible Agent global rule has enabled it.

## One note per substantive session

Create exactly one summary only after a substantive session has a verified, durable result. Do not create one for a simple answer, temporary exploration, or a session with no lasting conclusion. Update the same note if the session continues; do not split one session into chat-like fragments.

## Location and authority

Follow the Vault's existing layout. If no layout exists, use:

- project session: `<vault>/01-项目/<项目名>/会话摘要/YYYY-MM-DD-HHmm-<short-topic>.md`, linked to `<项目名>/项目记忆.md`;
- system or Vault session: `<vault>/00-系统/会话摘要/YYYY-MM-DD-HHmm-<short-topic>.md`, linked to the relevant system note or state note.

The project or system note remains authoritative for durable facts. The summary is a concise navigation and handoff record that creates a useful Obsidian backlink.

## Required content

Use the Vault's existing template, or create a small template with only:

1. task goal;
2. retrieved context;
3. verified outcome;
4. key decision or change;
5. risks and next step; and
6. links to the authority note and meaningful artifacts.

Do not copy code blocks, raw prompts, chain-of-thought, full command output, or a chat transcript. Never store passwords, API keys, tokens, credentials, private keys, cookies, or other sensitive data.

## Backlinks and external clients

An internal link from the summary to its authority note is enough for Obsidian Backlinks to show the reverse relationship. This does not make external chat history available to Obsidian. An external client may create or append a summary only when it has been explicitly configured with the Vault rules; do not claim automatic real-time chat capture.
