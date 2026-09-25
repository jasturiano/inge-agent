"""Test installation reporting using disposable source copies and fake configs.

Every subprocess receives explicit scan/config roots and a cleaned set of relevant
environment variables. No real OpenCode configuration is inspected. Snapshots check
file contents before/after selected scans; they do not establish preservation of
access times, atomic symlink safety, effective permissions or runtime discovery.
Run with python3 validation/test_installation_check.py; failures exit nonzero.
"""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]
SCRIPT = SOURCE / 'scripts/check-installation.py'


class InstallationCheck(unittest.TestCase):
    """Verify inventory categories, migration hints and non-mutating behavior."""
    def setUp(self):
        """Create temporary scan/config roots and remove live discovery overrides."""
        self.temp = tempfile.TemporaryDirectory(prefix='inge inventory ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / 'code'
        self.root.mkdir()
        self.config = self.base / 'opencode'
        self.config.mkdir()
        self.env = {k: v for k, v in os.environ.items()
                    if k not in {'INGE_HOME', 'DILBERT_HOME', 'OPENCODE_CONFIG', 'OPENCODE_CONFIG_DIR'}}

    def run_check(self, *extra):
        """Capture the checker for fixture roots plus optional repeated CLI flags."""
        return subprocess.run(['python3', str(SCRIPT), '--root', str(self.root),
                               '--opencode-dir', str(self.config), *extra],
                              text=True, capture_output=True, env=self.env)

    def snapshot(self):
        """Return relative filenames mapped to bytes, excluding symlinks."""
        return {str(p.relative_to(self.base)): p.read_bytes()
                for p in self.base.rglob('*') if p.is_file() and not p.is_symlink()}

    def test_global_current_customized_and_changed(self):
        """Distinguish byte-identical, header-customized and changed agent bodies."""
        shutil.copytree(SOURCE / 'opencode_global/agents', self.config / 'agents')
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Global OpenCode agents is up to date', result.stdout)
        agent = self.config / 'agents/inge.md'
        agent.write_text(agent.read_text().replace('model: litellm/claude-sonnet-5', 'model: custom/model'))
        self.assertIn('metadata is customized', self.run_check().stdout)
        agent.write_text(agent.read_text() + '\nOld or custom instruction\n')
        self.assertIn('out of date or customized', self.run_check().stdout)

    def test_nested_local_profile_shared_and_worktree_without_mutation(self):
        """Discover local/shared kits and profile-only worktrees without content edits."""
        shutil.copytree(SOURCE / 'repo/inge', self.root / '.inge')
        repo = self.root / 'project/backend'
        repo.mkdir(parents=True)
        (repo / '.git').mkdir()
        shutil.copytree(SOURCE / 'repo/inge', repo / 'inge')
        (repo / 'inge/PROJECT.md').write_text('Private local profile')
        worktree = self.root / 'project/worktree'
        (worktree / 'inge').mkdir(parents=True)
        (worktree / '.git').write_text('gitdir: /fixture/not-used')
        (worktree / 'inge/PROJECT.md').write_text('Profile only')
        before = self.snapshot()
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f'installed locally in this repo: {repo / "inge"}', result.stdout)
        self.assertIn('local project profile', result.stdout)
        self.assertIn('Shared framework is up to date', result.stdout)
        self.assertNotIn('Private local profile', result.stdout)
        self.assertEqual(self.snapshot(), before)

    def test_legacy_definitions_missing_files_and_skipped_symlink(self):
        """Report partial singular-directory installs and prune traversal loops."""
        repo = self.root / 'repo'
        (repo / '.opencode/command').mkdir(parents=True)
        (repo / '.opencode/command/inge.md').write_text('old command')
        (self.root / 'loop').symlink_to(self.root, target_is_directory=True)
        result = self.run_check()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn('Local OpenCode commands is incomplete', result.stdout)
        self.assertIn('Skipping directory symlink', result.stdout)
        self.assertIn('No Inge Markdown agents found', result.stdout)

    def test_source_checkout_is_not_reported_as_installation(self):
        """Exclude source distribution files from installed-kit classification."""
        result = self.run_check('--root', str(SOURCE))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('distribution files are not installations', result.stdout)
        self.assertNotIn(f'installed locally in this repo: {SOURCE / "repo/inge"}', result.stdout)

    def test_legacy_leftovers_and_references_are_read_only_and_redacted(self):
        """Locate old names and backups without printing config contents or editing."""
        shutil.copytree(SOURCE / 'opencode_global/agents', self.config / 'agents')
        (self.config / 'agents/dilbert.md').write_text('old agent')
        (self.config / 'agents/dilbert.md.bak').write_text('old primary backup')
        (self.config / 'agents/dilbert-worker.md.bak').write_text('old backup')
        (self.config / 'opencode.jsonc').write_text('{"agent": "dilbert", "token": "SECRET"}')
        repo = self.root / 'project/repo'
        (repo / '.opencode/command').mkdir(parents=True)
        (repo / '.opencode/command/dilbert-review.md').write_text('old command')
        (repo / 'dilbert_scripts').mkdir()
        (repo / 'dilbert').mkdir()
        (repo / 'dilbert/PROJECT.md').write_text('preserve local customizations')
        (repo / 'DILBERT.md').write_text('old policy')
        (repo / 'AGENTS.md').write_text('Read .dilbert/WORKFLOW.md; SECRET')
        (repo / '.gitignore').write_text('/dilbert/\n')
        (self.root / '.dilbert').mkdir()
        self.env['DILBERT_HOME'] = str(self.root / '.dilbert')
        before = self.snapshot()
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ['dilbert.md', 'dilbert.md.bak', 'dilbert-worker.md.bak', 'opencode.jsonc',
                     'dilbert-review.md', 'dilbert_scripts', 'DILBERT.md',
                     'AGENTS.md', '.gitignore', '.dilbert']:
            self.assertIn(name, result.stdout)
        self.assertIn('DILBERT_HOME is set', result.stdout)
        self.assertIn('old-name reference on lines 1', result.stdout)
        self.assertIn('Global OpenCode agents is up to date', result.stdout)
        self.assertNotIn('SECRET', result.stdout)
        self.assertEqual(self.snapshot(), before)

    def test_partial_install_non_git_and_external_config(self):
        """Detect partial kits, explicit config references and old shared ancestors."""
        (self.root / 'partial/inge').mkdir(parents=True)
        external = self.base / 'custom.json'
        external.write_text('{"default_agent": "dilbert"}')
        self.env['OPENCODE_CONFIG'] = str(external)
        (self.root / '.dilbert').mkdir()
        nested = self.root / 'nested'
        nested.mkdir()
        result = self.run_check('--root', str(nested))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Possible incomplete Inge installation', result.stdout)
        self.assertIn(str(external), result.stdout)
        self.assertIn('ancestor shared framework', result.stdout)

    def test_unrelated_files_are_not_cleanup_candidates(self):
        """Keep unrelated agents and historical task/README mentions out of findings."""
        (self.config / 'agents').mkdir()
        (self.config / 'agents/reviewer.md').write_text('custom agent')
        (self.root / 'README.md').write_text('historical Dilbert mention')
        (self.root / 'thoughts').mkdir()
        (self.root / 'thoughts/task.md').write_text('historical Dilbert evidence')
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('Legacy Dilbert leftover:', result.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
