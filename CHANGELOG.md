# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-05

### Added
- Initial open-source release.
- Unified CLI (`skill-mgr`) with list, analyze, duplicates, remove, restore, doctor, update, and one-way sync subcommands.
- Usage frequency, size, and estimated prompt token analysis (`skill-analyzer`).
- Safe skill removal with automatic backup and restore (`skill-remove`).
- Runtime dependency health check (`skill-doctor`).
- Read-only local version reporting and explicit global update application (`skill-update`).
- Symlink synchronization across Claude Code and Codex (`sync-skills`).
- Full English localization of all output strings and documentation.
- Chinese documentation (`README.zh-CN.md`).
- OpenAI skill metadata (`agents/openai.yaml`).
- Smoke tests and GitHub Actions CI.
- MIT License.
