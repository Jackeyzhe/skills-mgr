---
name: skills-mgr
description: >-
  Manage installed AI skills across Claude Code and Codex. Use when the user
  wants to list skills, estimate skill usage frequency and prompt size, find
  duplicate or overlapping skills, safely remove or restore skills, check skill
  runtime health, apply skill updates, or sync one-way symlinks from
  ~/.agents/skills to ~/.claude/skills and ~/.codex/skills. Also use for
  Chinese requests such as skill管理, 清理skill, 检查skill, 更新skill, 重复skill,
  and skill列表.
---

# skills-mgr

Use `skills-mgr` for unified skill management. The source of truth is
`~/.agents/skills/`; Claude Code and Codex consume symlinks from
`~/.claude/skills/` and `~/.codex/skills/`.

## Commands

| Command | Purpose |
|---------|---------|
| `skills-mgr list` | List skills with version, size, file count, symlink status, and category |
| `skills-mgr analyze` | Estimate usage frequency, prompt tokens, and size from conversation transcripts |
| `skills-mgr duplicates` | Find overlapping skills using known subset rules and keyword overlap |
| `skills-mgr remove <name>` | Back up a skill and remove its Claude Code/Codex symlinks |
| `skills-mgr restore <name>` | Restore a removed skill from backup |
| `skills-mgr doctor` | Check runtime dependency health for installed skills |
| `skills-mgr update` | Show local versions and safe update guidance |
| `skills-mgr update --apply` | Apply global skill updates with `npx skills add --global` |
| `skills-mgr sync` | One-way sync symlinks from `~/.agents/skills` to Claude Code and Codex |

## Workflows

When cleaning up skills:
1. Run `skills-mgr analyze` to estimate recent usage.
2. Run `skills-mgr duplicates` to find likely overlap.
3. Run `skills-mgr doctor` to find missing dependencies.
4. Recommend removals, then use `skills-mgr remove <name>` only after the user agrees.

When checking updates:
1. Run `skills-mgr update` for a read-only local version report.
2. Run `skills-mgr update --apply --dry-run` to preview update commands.
3. Run `skills-mgr update --apply` only when the user explicitly wants global updates.

## Notes

- Usage analysis is approximate. It scans user messages for trigger keywords; it does not track exact skill invocation events.
- Removal is reversible by default because skills are moved to `~/.local/share/skill-backups/`.
- `skills-mgr sync` is intentionally one-way and does not import skills from Claude Code or Codex directories.
