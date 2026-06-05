# skills-mgr

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/Jackeyzhe/skills-mgr/actions/workflows/ci.yml/badge.svg)](https://github.com/Jackeyzhe/skills-mgr/actions/workflows/ci.yml)
[中文文档](README.zh-CN.md)

Manage installed AI skills across Claude Code and Codex: list skills, estimate
usage, find overlap, safely remove and restore skills, check runtime health,
apply updates, and sync symlinks from one shared source directory.

## Features

- **List** skills with version, size, file count, symlink status, and category
- **Analyze** approximate usage frequency, prompt token estimates, and size
- **Find duplicates** using known subset rules and keyword overlap
- **Safely remove** skills with backups in `~/.local/share/skill-backups/`
- **Restore** removed skills from backup
- **Health check** runtime dependencies such as `bun`, `node`, `python3`, and `npx`
- **Update** skills explicitly with `npx skills add --global`
- **Sync** one-way symlinks from `~/.agents/skills` to Claude Code and Codex

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js / `npx` for installing or applying updates
- `bun` only for skills that include TypeScript scripts

### Install as a Skill

```bash
npx skills add Jackeyzhe/skills-mgr
bash ~/.agents/skills/skills-mgr/install.sh
```

If `~/.local/bin` is on your `PATH`, the CLI is then available:

```bash
skills-mgr list
skills-mgr doctor --summary
skills-mgr analyze --top 10
```

### Run from Source

```bash
git clone https://github.com/Jackeyzhe/skills-mgr.git
cd skills-mgr
python3 scripts/skills-mgr list
python3 scripts/skills-doctor --summary
```

### Uninstall

```bash
bash ~/.agents/skills/skills-mgr/install.sh --uninstall
npx skills remove skills-mgr
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `skills-mgr list` | List skills with version, size, file count, symlink status, and category |
| `skills-mgr analyze [--json] [--top N] [--zero] [--no-trend]` | Estimate keyword-based usage frequency, prompt tokens, and size |
| `skills-mgr duplicates` | Find overlapping or duplicate skills |
| `skills-mgr remove <name> [-y]` | Back up a skill and remove its Claude Code/Codex symlinks |
| `skills-mgr restore [name]` | Restore a previously removed skill from backup |
| `skills-mgr doctor [name] [--summary] [--json]` | Check runtime dependency health |
| `skills-mgr update` | Show local versions and safe update guidance without modifying installs |
| `skills-mgr update --apply [name] [--dry-run]` | Preview or apply global skill updates |
| `skills-mgr sync` | One-way sync symlinks from `~/.agents/skills` to Claude Code and Codex |

Standalone scripts are also available after installation:

```bash
skills-analyzer --json --top 10
skills-remove --list
skills-doctor --summary
skills-update --apply --dry-run
skills-sync
```

## How It Works

### Skill Storage

```text
~/.agents/skills/          # Source of truth
~/.claude/skills/          # Claude Code symlinks
~/.codex/skills/           # Codex symlinks
```

`skills-mgr sync` is intentionally one-way. It creates missing symlinks from
`~/.agents/skills` into Claude Code and Codex directories; it does not import
skills back from those tool-specific directories.

### Usage Analysis

`skills-analyzer` scans Claude Code and Codex JSONL transcripts for trigger
keywords extracted from each skill's `SKILL.md`. It reports approximate match
counts, estimated prompt tokens from skill files, size, and an impact score.

This is not exact invocation tracking. Skills are injected into prompts rather
than called as tool events, so keyword matching is a practical approximation.

### Update Safety

`skills-mgr update` is read-only by default. It prints local versions and explains
how to preview or apply updates. Only `skills-mgr update --apply` modifies global
skill installs by running `npx skills add <name> --global`.

## Development

```bash
python3 -m py_compile scripts/skills-mgr scripts/skills-analyzer scripts/skills-remove scripts/skills-doctor scripts/skills-update
python3 -m unittest discover -s tests
```

Use a temporary pycache directory when your environment cannot write to the
default Python cache:

```bash
PYTHONPYCACHEPREFIX=/tmp/skills-mgr-pycache python3 -m py_compile scripts/skills-mgr scripts/skills-analyzer scripts/skills-remove scripts/skills-doctor scripts/skills-update
```

## License

MIT. See [LICENSE](LICENSE).
