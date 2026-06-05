---
name: skills-manager
description: >-
  Manage installed AI skills across Claude Code and Codex. Use when the user
  wants to list skills, estimate skill usage frequency and prompt size, find
  duplicate or overlapping skills, safely remove or restore skills, check skill
  runtime health, apply skill updates, or sync one-way symlinks from
  ~/.agents/skills to ~/.claude/skills and ~/.codex/skills. Also use for
  Chinese requests such as skill管理, 清理skill, 检查skill, 更新skill, 重复skill,
  and skill列表.
---

# Skills Manager

Use `skill-mgr` for unified skill management. The source of truth is
`~/.agents/skills/`; Claude Code and Codex consume symlinks from
`~/.claude/skills/` and `~/.codex/skills/`.

## Commands

| Command | Purpose |
|---------|---------|
| `skill-mgr list` | List skills with version, size, file count, symlink status, and category |
| `skill-mgr analyze` | Estimate usage frequency, prompt tokens, and size from conversation transcripts |
| `skill-mgr duplicates` | Find overlapping skills using known subset rules and keyword overlap |
| `skill-mgr remove <name>` | Back up a skill and remove its Claude Code/Codex symlinks |
| `skill-mgr restore <name>` | Restore a removed skill from backup |
| `skill-mgr doctor` | Check runtime dependency health for installed skills |
| `skill-mgr update` | Show local versions and safe update guidance |
| `skill-mgr update --apply` | Apply global skill updates with `npx skills add --global` |
| `skill-mgr sync` | One-way sync symlinks from `~/.agents/skills` to Claude Code and Codex |

## Workflows

When cleaning up skills:
1. Run `skill-mgr analyze` to estimate recent usage.
2. Run `skill-mgr duplicates` to find likely overlap.
3. Run `skill-mgr doctor` to find missing dependencies.
4. Recommend removals, then use `skill-mgr remove <name>` only after the user agrees.

When checking updates:
1. Run `skill-mgr update` for a read-only local version report.
2. Run `skill-mgr update --apply --dry-run` to preview update commands.
3. Run `skill-mgr update --apply` only when the user explicitly wants global updates.

## Notes

- Usage analysis is approximate. It scans user messages for trigger keywords; it does not track exact skill invocation events.
- Removal is reversible by default because skills are moved to `~/.local/share/skill-backups/`.
- `skill-mgr sync` is intentionally one-way and does not import skills from Claude Code or Codex directories.
