# Contributing to skills-mgr

Thanks for your interest in contributing! This document outlines the process
for reporting issues, suggesting features, and submitting code changes.

## Code of Conduct

Be respectful and constructive. Assume good intent. We want this to be a
welcoming community for everyone.

## Reporting Issues

Found a bug? Please include:

- **What happened** — the unexpected behavior
- **What you expected** — the correct behavior
- **Steps to reproduce** — exact commands you ran
- **Environment** — OS, Python version (`python3 --version`), shell

Use [GitHub Issues](https://github.com/Jackeyzhe/skills-mgr/issues) to report.

## Suggesting Features

Open a GitHub Issue with the `enhancement` label. Describe:

- What problem the feature solves
- How you'd expect it to work
- Any alternatives you've considered

## Pull Requests

1. **Fork** the repository
2. **Create a branch** — `feature/your-feature` or `fix/your-bugfix`
3. **Make your changes** — keep them focused; one PR = one logical change
4. **Follow code style**:
   - Python: [PEP 8](https://peps.python.org/pep-0008/), 4-space indentation
   - Bash: POSIX `sh` compatible (no bashisms — macOS ships bash 3.2)
5. **Test your changes** — at minimum, verify the script runs without errors:
   ```bash
   PYTHONPYCACHEPREFIX=/tmp/skills-mgr-pycache python3 -m py_compile scripts/skills-mgr scripts/skills-analyzer scripts/skills-remove scripts/skills-doctor scripts/skills-update
   python3 -m unittest discover -s tests
   python3 scripts/skills-mgr list
   ```
6. **Update documentation** if your change affects CLI behavior:
   - `SKILL.md` command table
   - `README.md` CLI reference
   - `README.zh-CN.md` (Chinese translation)
7. **Write a clear commit message** — what and why, not how
8. **Open a Pull Request** against the `main` branch

## Development Setup

```bash
git clone https://github.com/Jackeyzhe/skills-mgr.git
cd skills-mgr

# No build step needed — run scripts directly
python3 scripts/skills-mgr list
python3 scripts/skills-doctor --json
```

## Adding a New Subcommand

The architecture is intentionally simple: each subcommand is a standalone
Python script in `scripts/`. To add one:

1. Create `scripts/skill-<name>` with:
   - `#!/usr/bin/env python3` shebang
   - `argparse`-based CLI
   - English output strings
2. Add a dispatch in `scripts/skills-mgr`:
   ```python
   elif subcommand == "<name>":
       script = find_script("skill-<name>")
       if script:
           os.execv(script, [script] + extra_args)
   ```
3. Document in `SKILL.md`, `README.md`, and `README.zh-CN.md`

## Translation

`README.zh-CN.md` is the Chinese translation of the English README. When
updating documentation, please update both files. Code comments and output
strings are English-only.

## Questions?

Open a [GitHub Discussion](https://github.com/Jackeyzhe/skills-mgr/discussions)
or file an issue.
