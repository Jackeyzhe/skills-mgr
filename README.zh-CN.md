# skills-mgr

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/Jackeyzhe/skills-mgr/actions/workflows/ci.yml/badge.svg)](https://github.com/Jackeyzhe/skills-mgr/actions/workflows/ci.yml)

统一管理 Claude Code、Codex 和 Hermes 使用的 AI skills：列表查看、使用估算、重复检测、
安全删除与恢复、依赖健康检查、显式更新，以及从统一目录同步软链接。

## 功能

- **列表查看**：显示版本、大小、文件数、软链接状态和分类
- **使用分析**：估算触发频率、skill 文件 prompt token 和体积
- **重复检测**：通过已知子集关系和关键词重叠发现功能重叠
- **安全删除**：删除前备份到 `~/.local/share/skill-backups/`
- **恢复备份**：从备份恢复已删除的 skill
- **健康检查**：检查 `bun`、`node`、`python3`、`npx` 等运行时依赖
- **显式更新**：通过 `skills-mgr update --apply` 应用更新
- **同步软链接**：从 `~/.agents/skills` 单向同步到 Claude Code、Codex 和 Hermes

## 快速开始

### 环境要求

- Python 3.8+
- Node.js / `npx`，用于安装 skills
- `bun` 只在运行带 TypeScript 脚本的 skill 时需要

### 作为 Skill 安装

```bash
npx skills add Jackeyzhe/skills-mgr
bash ~/.agents/skills/skills-mgr/install.sh
```

如果 `~/.local/bin` 已在 `PATH` 中，就可以直接使用：

```bash
skills-mgr list
skills-mgr doctor --summary
skills-mgr analyze --top 10
```

### 从源码运行

```bash
git clone https://github.com/Jackeyzhe/skills-mgr.git
cd skills-mgr
python3 scripts/skills-mgr list
python3 scripts/skills-doctor --summary
```

### 卸载

```bash
bash ~/.agents/skills/skills-mgr/install.sh --uninstall
npx skills remove skills-mgr
```

## CLI 参考

| 命令 | 说明 |
|------|------|
| `skills-mgr list` | 列出 skill 的版本、大小、文件数、软链接状态和分类 |
| `skills-mgr analyze [--json] [--top N] [--zero] [--no-trend]` | 基于关键词估算使用频率、prompt token 和体积 |
| `skills-mgr duplicates` | 检查重复或功能重叠的 skill |
| `skills-mgr remove <名称> [-y]` | 备份 skill 并移除 Claude Code/Codex/Hermes 软链接 |
| `skills-mgr restore [名称]` | 从备份恢复已删除的 skill |
| `skills-mgr doctor [名称] [--summary] [--json]` | 检查运行时依赖健康状态 |
| `skills-mgr update` | 只读显示本地版本和安全更新说明 |
| `skills-mgr update --apply [名称] [--dry-run]` | 预览或应用全局 skill 更新 |
| `skills-mgr sync [--include-unknown]` | 从 `~/.agents/skills` 单向同步软链接到 Claude Code、Codex 和 Hermes |

安装后也可以直接运行独立脚本：

```bash
skills-analyzer --json --top 10
skills-remove --list
skills-doctor --summary
skills-update --apply --dry-run
skills-sync
```

## 工作原理

### Skill 存储结构

```text
~/.agents/skills/          # 统一源目录
~/.claude/skills/          # Claude Code 软链接
~/.codex/skills/           # Codex 软链接
~/.hermes/skills/<分类>/   # Hermes 软链接（按分类）
```

`skills-mgr sync` 是单向同步：它会把 `~/.agents/skills` 中缺失的 skill
软链接到 Claude Code、Codex 和 Hermes 目录，不会从这些工具目录反向导入 skill。

#### Hermes 同步说明

Hermes 使用两级目录布局（`~/.hermes/skills/<分类>/<skill>/`）以便加载器按
分类聚合 skill。`skills-mgr sync` 会用与 `skills-mgr list` 相同的关键词逻辑
自动把每个 skill 路由到合适的分类：

| 显示分类 | 同步到 `~/.hermes/skills/<目录>/` |
|----------|----------------------------------|
| Image Gen（图像生成）| `creative/` |
| Publishing（发布）| `social-media/` |
| Conversion（转换）| `creative/` |
| Tool（工具）| `creative/` |
| Meta（元）| `software-development/` |
| Other（未识别）| **默认跳过** |

如果想把未识别的 skill 也同步到 `other/` 兜底目录，加 `--include-unknown`（或
`-u`）。前提是你的 Hermes 实例确实会从 `~/.hermes/skills/other/` 加载 skill。

### 使用分析

`skills-analyzer` 会从每个 skill 的 `SKILL.md` 中提取触发关键词，再扫描
Claude Code 和 Codex 的 JSONL 对话记录，输出近似匹配次数、估算 prompt
token、体积和影响分数。

这不是精确调用追踪。Skill 通常被注入到 prompt 中，而不是作为工具事件调用，
所以关键词匹配只是一个实用近似。

### 更新安全性

`skills-mgr update` 默认只读，只显示本地版本和安全更新说明。只有
`skills-mgr update --apply` 会通过 git fetch + rsync 从上游 repo 修改全局
skill 安装。

## 开发

```bash
python3 -m py_compile scripts/skills-mgr scripts/skills-analyzer scripts/skills-remove scripts/skills-doctor scripts/skills-update
python3 -m unittest discover -s tests
```

如果环境不能写默认 Python 缓存目录，可以指定临时缓存：

```bash
PYTHONPYCACHEPREFIX=/tmp/skills-mgr-pycache python3 -m py_compile scripts/skills-mgr scripts/skills-analyzer scripts/skills-remove scripts/skills-doctor scripts/skills-update
```

## 许可证

MIT，详见 [LICENSE](LICENSE)。
