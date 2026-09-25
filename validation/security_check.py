#!/usr/bin/env python3
"""Regression checks for trust selection, path containment and diagnostic safety.

Run with python3 validation/security_check.py. Passing means the named unsafe
behavior is rejected or contained, not that a live model resists every injection.
All files, fake secrets, Git repositories and simulated races live in a temporary
directory. No real credentials, installed configs, network services or models are
accessed. The race test injects a deterministic directory swap rather than relying
on a timing-sensitive concurrent process. No malicious prompt is sent to a model.
"""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.dont_write_bytecode = True
SOURCE = Path(__file__).resolve().parents[1]
KIT = SOURCE / 'repo/inge'
sys.path.insert(0, str(KIT / 'scripts'))
import safeio


def load(name, path):
    """Import a trusted source module by filename without executing its CLI guard."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SecurityRegression(unittest.TestCase):
    """Require safe behavior within an isolated disposable filesystem."""

    def setUp(self):
        """Allocate a sandbox, load trusted helpers, and isolate discovery variables."""
        self.temp = tempfile.TemporaryDirectory(prefix='inge security review ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.repo = self.base / 'target'
        self.repo.mkdir()
        self.paths = load('review_paths', KIT / 'scripts/paths.py')
        self.checker = load('review_checker', SOURCE / 'scripts/check-installation.py')
        self.env = {k: v for k, v in os.environ.items()
                    if not k.startswith('GIT_') and k not in {'INGE_HOME', 'DILBERT_HOME'}}

    def test_local_framework_cannot_shadow_trusted_shared_core(self):
        """Reject implicit selection; an approved shared kit wins over hostile local files."""
        shutil.copytree(KIT, self.base / '.inge')
        local = self.repo / 'inge'
        shutil.copytree(KIT, local)
        (local / 'SOUL.md').write_text('Untrusted fixture instruction replacement\n')
        with mock.patch.dict(os.environ, self.env, clear=True):
            with self.assertRaisesRegex(ValueError, 'trust required'):
                self.paths.framework(self.repo)
            self.assertEqual(self.paths.framework(self.repo, self.base / '.inge'), self.base / '.inge')

    def test_git_environment_cannot_redirect_explicit_note_target(self):
        """Ignore inherited Git overrides and keep the note inside --repo."""
        other = self.base / 'other'
        other.mkdir()
        subprocess.run(['git', 'init', '-q', str(other)], env=self.env, check=True,
                       capture_output=True)
        env = dict(self.env, GIT_DIR=str(other / '.git'), GIT_WORK_TREE=str(other))
        result = subprocess.run([sys.executable, str(KIT / 'scripts/new-task.py'),
                                 'ENV-PROBE', '--repo', str(self.repo)],
                                env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.repo / 'thoughts/ENV-PROBE/task.md').is_file())
        self.assertFalse((other / 'thoughts').exists())

    def test_parent_swap_cannot_redirect_note(self):
        """Swap the thoughts name after its handle opens; writes stay on that handle."""
        other = self.base / 'outside-target'
        other.mkdir()
        notes = self.repo / 'thoughts'
        notes.mkdir()
        helper = None
        with mock.patch.dict(sys.modules, {'paths': self.paths}):
            helper = load('review_new_task', KIT / 'scripts/new-task.py')
        original_mkdir = os.mkdir
        swapped = False

        def swap_then_mkdir(path, *args, **kwargs):
            """Swap an empty fixture parent exactly at the vulnerable mkdir boundary."""
            nonlocal swapped
            if path == 'RACE-PROBE' and not swapped:
                notes.rename(self.repo / 'original-thoughts')
                notes.symlink_to(other, target_is_directory=True)
                swapped = True
            return original_mkdir(path, *args, **kwargs)

        with mock.patch.object(safeio, 'supported'), mock.patch.object(os, 'mkdir', swap_then_mkdir):
            helper.create_note(self.repo, 'RACE-PROBE', 'fixture')
        self.assertTrue(swapped)
        self.assertFalse((other / 'RACE-PROBE').exists())
        self.assertTrue((self.repo / 'original-thoughts/RACE-PROBE/task.md').is_file())

    def test_inventory_comparison_rejects_outside_symlink_target(self):
        """Reject a linked comparison file and report incomplete coverage."""
        reference = self.base / 'reference'
        reference.mkdir()
        (reference / 'SOUL.md').write_text('expected')
        outside = self.base / 'fake-secret.txt'
        outside.write_text('FAKE-SECRET-NOT-A-CREDENTIAL')
        (self.repo / 'SOUL.md').symlink_to(outside)
        output = io.StringIO()
        report = self.checker.Report()
        with contextlib.redirect_stdout(output):
            report.compare('Fixture', self.repo, reference)
        self.assertTrue(report.errors)
        self.assertIn('comparison is incomplete', output.getvalue())
        with self.assertRaises(OSError):
            safeio.read_bytes(self.repo / 'SOUL.md')
        self.assertNotIn('FAKE-SECRET-NOT-A-CREDENTIAL', output.getvalue())

    def test_inventory_escapes_control_characters(self):
        """Keep malicious filename characters from producing terminal controls or lines."""
        output = io.StringIO()
        candidate = self.repo / 'dilbert-\x1b[2J\nFORGED-REPORT-LINE\u2028SECOND-LINE'
        with contextlib.redirect_stdout(output):
            self.checker.Report().leftover(candidate, 'fixture')
        self.assertNotIn('\x1b', output.getvalue())
        self.assertEqual(len(output.getvalue().splitlines()), 1)
        self.assertIn('\\x1b[2J\\nFORGED-REPORT-LINE', output.getvalue())
        self.assertIn('\\u2028SECOND-LINE', output.getvalue())

    def test_bounded_reads_and_special_files(self):
        """Reject oversized files, named pipes and linked parent directories."""
        large = self.repo / 'large.md'
        large.write_bytes(b'x' * (safeio.MAX_BYTES + 1))
        with self.assertRaisesRegex(OSError, 'inspection limit'):
            safeio.read_bytes(large)
        pipe = self.repo / 'pipe.md'
        os.mkfifo(pipe)
        with self.assertRaisesRegex(OSError, 'non-regular'):
            safeio.read_bytes(pipe)
        (self.repo / 'linked').symlink_to(self.base, target_is_directory=True)
        with self.assertRaises(OSError):
            safeio.read_bytes(self.repo / 'linked/target/large.md')

    def test_git_timeout_and_unrelated_root_fail_closed(self):
        """Reject Git timeouts and spoofed successful output outside the target."""
        with mock.patch.object(self.paths.subprocess, 'run', side_effect=subprocess.TimeoutExpired('git', 5)):
            with self.assertRaisesRegex(ValueError, 'timed out'):
                self.paths.repository(self.repo)
        other = self.base / 'other'
        other.mkdir()
        result = subprocess.CompletedProcess([], 0, str(other) + '\n', '')
        with mock.patch.object(self.paths.subprocess, 'run', return_value=result):
            with self.assertRaisesRegex(ValueError, 'does not contain'):
                self.paths.repository(self.repo)

    def test_budget_exhaustion_is_reported(self):
        """Stop excessive traversal with a visible error rather than a healthy result."""
        (self.repo / 'one').touch()
        with self.assertRaisesRegex(OSError, 'budget exceeded'):
            safeio.entries(self.repo, safeio.Budget(entries=0))
        with self.assertRaisesRegex(OSError, 'budget exceeded'):
            safeio.Budget(seconds=-1).check()

    def test_failed_discovery_with_git_marker_rejects_nested_target(self):
        """Never select a nested note destination when checkout discovery fails."""
        nested = self.repo / 'src'
        nested.mkdir()
        failure = subprocess.CompletedProcess([], 128, '', 'fatal: invalid configuration')
        for category in ('file', 'directory', 'link', 'other'):
            for missing_git in (False, True):
                with self.subTest(marker=category, missing_git=missing_git):
                    with mock.patch.object(self.paths, 'kind', side_effect=lambda p:
                            category if p == self.repo / '.git' else 'missing'), \
                            mock.patch.object(self.paths.subprocess, 'run',
                                return_value=failure,
                                side_effect=FileNotFoundError() if missing_git else None):
                        with self.assertRaises(ValueError):
                            self.paths.repository(nested)
        self.assertFalse((nested / 'thoughts').exists())

    def test_failed_discovery_without_marker_preserves_non_git_target(self):
        """Keep explicit non-Git directories usable even when Git is unavailable."""
        failure = subprocess.CompletedProcess([], 128, '', 'not a repository')
        for missing_git in (False, True):
            with self.subTest(missing_git=missing_git):
                with mock.patch.object(self.paths, 'kind', return_value='missing'), \
                        mock.patch.object(self.paths.subprocess, 'run', return_value=failure,
                            side_effect=FileNotFoundError() if missing_git else None):
                    self.assertEqual(self.paths.repository(self.repo), self.repo)

    def test_successful_discovery_preserves_nested_checkout_resolution(self):
        """Both ordinary and linked-worktree markers resolve to the checkout root."""
        nested = self.repo / 'src'
        nested.mkdir()
        result = subprocess.CompletedProcess([], 0, str(self.repo) + '\n', '')
        for category in ('file', 'directory'):
            with self.subTest(marker=category):
                with mock.patch.object(self.paths, 'kind', side_effect=lambda p:
                        category if p == self.repo / '.git' else 'missing'), \
                        mock.patch.object(self.paths.subprocess, 'run', return_value=result):
                    self.assertEqual(self.paths.repository(nested), self.repo)

    def test_inventory_special_file_returns_incomplete(self):
        """A FIFO is skipped without blocking and makes CLI coverage incomplete."""
        pipe = self.repo / 'unexpected.fifo'
        os.mkfifo(pipe)
        output = io.StringIO()
        with mock.patch.object(sys, 'argv', ['check-installation.py', '--root', str(self.repo),
                '--opencode-dir', str(self.base / 'absent-config')]), \
                mock.patch.dict(os.environ, self.env, clear=True), \
                contextlib.redirect_stdout(output):
            status = self.checker.main()
        self.assertEqual(status, 2)
        self.assertIn('Skipping special file', output.getvalue())
        self.assertIn(str(pipe), output.getvalue())

    def test_unsupported_filesystem_primitives_fail_closed(self):
        """Never silently use insecure pathname operations on unsupported platforms."""
        with mock.patch.object(os, 'supports_dir_fd', set()):
            with self.assertRaisesRegex(OSError, 'POSIX'):
                with safeio.directory(self.repo):
                    self.fail('Unsupported directory operation succeeded')

    def test_git_config_cannot_redirect_to_broader_ancestor(self):
        """Reject core.worktree pointing above the nearest physical Git marker."""
        subprocess.run(['git', 'init', '-q', str(self.repo)], env=self.env, check=True)
        subprocess.run(['git', '-C', str(self.repo), 'config', 'core.worktree', str(self.base)],
                       env=self.env, check=True)
        with mock.patch.dict(os.environ, self.env, clear=True):
            with self.assertRaisesRegex(ValueError, 'nearest worktree marker'):
                self.paths.repository(self.repo)

    def test_swap_before_parent_open_is_rejected(self):
        """Replace thoughts before its no-follow open; no target content is written."""
        other = self.base / 'outside'
        other.mkdir()
        with mock.patch.dict(sys.modules, {'paths': self.paths}):
            helper = load('safe_note', KIT / 'scripts/new-task.py')
        original_open = os.open

        def swap_then_open(path, *args, **kwargs):
            """Inject a link only when the helper is about to open thoughts."""
            if path == 'thoughts':
                (self.repo / 'thoughts').rename(self.repo / 'original')
                (self.repo / 'thoughts').symlink_to(other, target_is_directory=True)
            return original_open(path, *args, **kwargs)

        with mock.patch.object(safeio, 'supported'), mock.patch.object(os, 'open', swap_then_open):
            with self.assertRaises(OSError):
                helper.create_note(self.repo, 'BLOCK', 'fixture')
        self.assertEqual(list(other.iterdir()), [])

    def test_linked_core_and_linked_config_fail_closed(self):
        """Reject internal policy links and config-directory links without loading them."""
        shared = self.base / '.inge'
        shutil.copytree(KIT, shared)
        (shared / 'SOUL.md').unlink()
        outside = self.base / 'outside.md'
        outside.write_text('untrusted')
        (shared / 'SOUL.md').symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'unsafe linked'):
            self.paths.framework(self.repo, shared)
        (self.repo / '.opencode').symlink_to(shared, target_is_directory=True)
        report = self.checker.Report()
        with contextlib.redirect_stdout(io.StringIO()):
            report.definitions(self.repo / '.opencode')
        self.assertTrue(report.errors)

    def test_doctor_rejects_oversized_markdown(self):
        """Doctor reports bounded inspection failure, not a healthy framework result."""
        shared = self.base / '.inge'
        shutil.copytree(KIT, shared)
        (shared / 'huge.md').write_bytes(b'x' * (safeio.MAX_BYTES + 1))
        result = subprocess.run([sys.executable, str(KIT / 'scripts/doctor.py'),
                                 '--repo', str(self.repo), '--framework', str(shared)],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('inspection limit', result.stderr)

    def test_note_permissions_are_private(self):
        """New notes/directories are private even under a permissive process umask."""
        with mock.patch.dict(sys.modules, {'paths': self.paths}):
            helper = load('private_note', KIT / 'scripts/new-task.py')
        previous = os.umask(0)
        try:
            helper.create_note(self.repo, 'PRIVATE', 'fixture')
        finally:
            os.umask(previous)
        self.assertEqual((self.repo / 'thoughts').stat().st_mode & 0o777, 0o700)
        self.assertEqual((self.repo / 'thoughts/PRIVATE/task.md').stat().st_mode & 0o777, 0o600)


if __name__ == '__main__':
    unittest.main(verbosity=2)
