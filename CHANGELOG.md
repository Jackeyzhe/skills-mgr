# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Hermes sync target: `skills-mgr sync` now also creates categorized symlinks
  under `~/.hermes/skills/<category>/<name>/` for Claude-Code/Codex skills.
- `--include-unknown` / `-u` flag for `skills-mgr sync` to route skills that
  do not match a known Hermes category into a catch-all `other/` bucket.
- New `H` column in `skills-mgr list` showing Hermes link status and category.
- `skills-remove` now also cleans up symlinks under `~/.hermes/skills/<cat>/`.
  Restore prints a hint to re-run `skills-mgr sync` to recreate Hermes links.

### Changed
- `categorize_skill()` now returns `(display_category, hermes_dir)` instead of a
  bare display string. The display string is unchanged, so list output is
  backward-compatible.

## [1.0.0] - 2026-06-05

### Added
- Initial open-source release as `skills-mgr`.
- Unified CLI (`skills-mgr`) with list, analyze, duplicates, remove, restore, doctor, update, and one-way sync subcommands.
- Usage frequency, size, and estimated prompt token analysis (`skills-analyzer`).
- Safe skill removal with automatic backup and restore (`skills-remove`).
- Runtime dependency health check (`skills-doctor`).
- Read-only local version reporting and explicit global update application (`skills-update`).
- Symlink synchronization across Claude Code and Codex (`skills-sync`).
- Full English localization of all output strings and documentation.
- Chinese documentation (`README.zh-CN.md`).
- OpenAI skill metadata (`agents/openai.yaml`).
- Smoke tests and GitHub Actions CI.
- MIT License.
