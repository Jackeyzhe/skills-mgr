import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cmd(args, home, check=True, extra_env=None):
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["PYTHONPYCACHEPREFIX"] = str(home / ".pycache")
    env.update(extra_env or {})
    result = subprocess.run(
        args,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"command failed: {args}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def install_fixture(home):
    skills_dir = home / ".agents" / "skills"
    target = skills_dir / "skill-manager"
    skills_dir.mkdir(parents=True)
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"),
    )
    return target


class SkillManagerCliTests(unittest.TestCase):
    def test_help_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_fixture(home)
            result = run_cmd([sys.executable, "scripts/skill-mgr", "help"], home)
            self.assertIn("skill-mgr list", result.stdout)

    def test_list_sync_remove_restore_with_temp_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_fixture(home)

            result = run_cmd([sys.executable, "scripts/skill-mgr", "list"], home)
            self.assertIn("skill-manager", result.stdout)
            self.assertIn("1.0.0", result.stdout)

            result = run_cmd([sys.executable, "scripts/skill-mgr", "sync"], home)
            self.assertIn("Sync complete", result.stdout)
            self.assertTrue((home / ".claude" / "skills" / "skill-manager").is_symlink())
            self.assertTrue((home / ".codex" / "skills" / "skill-manager").is_symlink())

            result = run_cmd([sys.executable, "scripts/skill-remove", "--yes", "skill-manager"], home)
            self.assertIn("Backed up skill-manager", result.stdout)
            self.assertFalse((home / ".agents" / "skills" / "skill-manager").exists())
            self.assertFalse((home / ".claude" / "skills" / "skill-manager").exists())

            result = run_cmd(
                [sys.executable, "scripts/skill-mgr", "restore", "skill-manager", "--yes"],
                home,
            )
            self.assertIn("Restored skill-manager", result.stdout)
            self.assertTrue((home / ".agents" / "skills" / "skill-manager").exists())
            self.assertTrue((home / ".codex" / "skills" / "skill-manager").is_symlink())

    def test_sync_wrapper_runs_from_source_without_path_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_fixture(home)
            result = run_cmd(["scripts/sync-skills"], home)
            self.assertIn("Sync complete", result.stdout)

    def test_update_default_is_read_only_and_apply_dry_run_is_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_fixture(home)

            result = run_cmd([sys.executable, "scripts/skill-update"], home)
            self.assertIn("Local skill versions", result.stdout)
            self.assertIn("skill-update --apply", result.stdout)

            result = run_cmd(
                [sys.executable, "scripts/skill-update", "--apply", "skill-manager", "--dry-run"],
                home,
            )
            self.assertIn("[dry-run]", result.stdout)
            self.assertIn("npx --yes skills add skill-manager --global", result.stdout)


if __name__ == "__main__":
    unittest.main()
