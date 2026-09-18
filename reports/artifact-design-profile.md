# Artifact Design Profile

## Artifact family

This Skill emits compact operational reports and context briefs, not dashboards or marketing pages.

## Design rules

- Put scope, status, source count, and unresolved items near the top.
- Use one table for repeated findings and short headings for navigation.
- Keep the context brief single-file friendly; do not add decorative cards or duplicate source bodies.
- Put machine details in JSON and human decisions in the authority note.
- Use an explicit warning block for managed output, truncation, blocked sensitivity, or missing evidence.

## Quality gate

Review the rendered Markdown for UTF-8, readable tables, valid internal links, visible evidence states, and no raw credentials. File paths must remain relative in machine manifests unless the output contract specifically requires an external `file:///` link.
