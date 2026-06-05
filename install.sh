#!/usr/bin/env bash
# ============================================================
# install.sh — Install (or uninstall) skills-mgr CLI tools.
#
# Symlinks scripts from the skill directory into ~/.local/bin/
# so they are available on PATH.
#
# Usage:
#   bash install.sh             Install CLI tools
#   bash install.sh --uninstall  Remove symlinks
# ============================================================
set -euo pipefail

BIN_DIR="${HOME}/.local/bin"

# Detect the skill directory (works whether run from root or scripts/)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ "$(basename "$SCRIPT_DIR")" = "scripts" ]; then
    SKILL_DIR="$(dirname "$SCRIPT_DIR")"
else
    SKILL_DIR="$SCRIPT_DIR"
fi

SCRIPTS_SRC="${SKILL_DIR}/scripts"

# ---- Uninstall ----
if [ "${1:-}" = "--uninstall" ] || [ "${1:-}" = "-u" ]; then
    echo "Removing skills-mgr symlinks from ${BIN_DIR}..."
    removed=0
    for script in skills-mgr skills-analyzer skills-remove skills-doctor skills-update skills-sync; do
        dst="${BIN_DIR}/${script}"
        if [ -L "$dst" ]; then
            rm "$dst"
            echo "  removed: ${script}"
            removed=$((removed + 1))
        fi
    done
    if [ "$removed" -eq 0 ]; then
        echo "  No symlinks found."
    else
        echo "Done. ${removed} symlink(s) removed."
    fi
    exit 0
fi

# ---- Install ----
echo "Installing skills-mgr CLI tools..."
echo "  Source: ${SCRIPTS_SRC}"
echo "  Target: ${BIN_DIR}"
echo ""

mkdir -p "$BIN_DIR"

for script in skills-mgr skills-analyzer skills-remove skills-doctor skills-update skills-sync; do
    src="${SCRIPTS_SRC}/${script}"
    dst="${BIN_DIR}/${script}"

    if [ ! -f "$src" ]; then
        echo "  SKIP: ${script} (not found in ${SCRIPTS_SRC})"
        continue
    fi

    chmod +x "$src"
    ln -sf "$src" "$dst"
    echo "  linked: ${script}"
done

echo ""
case ":$PATH:" in
    *":${BIN_DIR}:"*)
        echo "Done. Verify with: skills-mgr list"
        ;;
    *)
        echo "Done. ${BIN_DIR} is not currently on PATH."
        echo "Add it to your shell profile, then run: skills-mgr list"
        echo "Example: export PATH=\"${BIN_DIR}:\$PATH\""
        ;;
esac
