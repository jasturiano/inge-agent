#!/usr/bin/env python3
"""Validate this distribution; no OpenCode/provider calls or installed configuration writes.

Requires Python 3, Git, and Ruby's standard YAML library. Git commits/worktrees created
here exist only in disposable fixtures. No user repository is initialized or modified.
"""
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / 'repo/dilbert'
MODELS = {
    'dilbert': ('litellm/claude-sonnet-5', 'github-copilot/claude-sonnet-5'),
    'dilbert-worker': ('litellm/claude-sonnet-5', 'github-copilot/claude-sonnet-5'),
    'dilbert-worker-strong': ('litellm/claude-opus-4-8', 'github-copilot/gpt-5.6-sol'),
    'dilbert-expert': ('litellm/claude-opus-4-8', 'github-copilot/gpt-5.6-sol'),
    'dilbert-scout': ('litellm/claude-haiku', 'github-copilot/claude-haiku-4.5'),
}
COMMANDS = {'dilbert', 'dilbert-work', 'dilbert-review', 'dilbert-arch', 'dilbert-status'}
STAGES = {'rpi-research', 'rpi-questions', 'rpi-scenario-check', 'rpi-plan',
          'rpi-explain', 'rpi-plan-review', 'rpi-implement', 'rpi-review',
          'rpi-arch-claimed', 'rpi-arch-actual', 'rpi-arch-drift',
          'rpi-arch-scenario', 'rpi-arch-report', 'recon-map', 'recon-orient', 'recon-trace'}


def run(args, cwd=None, **kwargs):
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, **kwargs)


def frontmatter(path):
    text = path.read_text()
    match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    if not match:
        raise AssertionError(f'Missing frontmatter: {path}')
    result = run(['ruby', '-r', 'yaml', '-r', 'json', '-e',
                  'puts JSON.generate(YAML.safe_load(STDIN.read))'], input=match[1])
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout), match[1]


class Configuration(unittest.TestCase):
    def test_exact_roles_and_permissions(self):
        agents = {p.stem: p for p in (ROOT / 'opencode_global/agents').glob('*.md')}
        self.assertEqual(set(agents), set(MODELS))
        for name, path in agents.items():
            with self.subTest(role=name):
                data, header = frontmatter(path)
                writer = name in {'dilbert-worker', 'dilbert-worker-strong'}
                self.assertEqual(data['permission']['edit'], 'ask' if writer else 'deny')
                self.assertEqual(data['permission']['bash'], 'ask')
                if name == 'dilbert':
                    self.assertEqual(data['mode'], 'primary')
                    self.assertEqual(data['permission']['task'],
                                     {'*': 'deny', **{n: 'allow' for n in MODELS if n != 'dilbert'}})
                    self.assertEqual(next(iter(data['permission']['task'])), '*')
                else:
                    self.assertEqual(data['mode'], 'subagent')
                    self.assertEqual(data['permission']['task'], 'deny')

    def test_model_pins_and_commented_alternatives(self):
        for name, (active, alternate) in MODELS.items():
            with self.subTest(role=name):
                data, header = frontmatter(ROOT / 'opencode_global/agents' / (name + '.md'))
                self.assertEqual(re.findall(r'^model:\s*(\S+)', header, re.M), [active])
                self.assertEqual(data['model'], active)
                self.assertEqual(re.findall(r'^#\s*model:\s*(\S+)', header, re.M), [alternate])
                self.assertNotRegex(header, r'(?im)^#?\s*model:.*terra')

    def test_commands_router_arguments_no_model_overrides(self):
        commands = list((ROOT / 'repo/.opencode/commands').glob('*.md'))
        self.assertEqual({p.stem for p in commands}, COMMANDS)
        for path in commands:
            data, header = frontmatter(path)
            self.assertEqual(data['agent'], 'dilbert')
            self.assertNotIn('model', data)
            self.assertNotRegex(header, r'(?m)^#?\s*model:')
            self.assertIn('$ARGUMENTS', path.read_text())
        self.assertFalse((ROOT / 'repo/.opencode/command').exists())
        self.assertFalse((ROOT / 'opencode_global/agent').exists())

    def test_shared_references_and_local_document_links(self):
        documents = (list(LOCAL.rglob('*.md')) + list((ROOT / 'opencode_global').rglob('*.md'))
                     + list((ROOT / 'repo/.opencode').rglob('*.md'))
                     + [ROOT / 'README.md'] + list((ROOT / 'docs').glob('*.md'))
                     + list((ROOT / 'validation').glob('*.md')))
        references = {p.name for p in (LOCAL / 'references').glob('*.md')}
        checked = set()
        for path in documents:
            text = path.read_text()
            for ref in re.findall(r'`((?:dilbert/|references/)[\w./-]+\.md)`', text):
                target = ROOT / 'repo' / ref if ref.startswith('dilbert/') else LOCAL / ref
                self.assertTrue(target.is_file(), f'{path}: {ref}')
                checked.add(ref)
            for name in re.findall(r'(?<![\w/-])([a-z][a-z-]+\.md)', text):
                if name in references:
                    self.assertTrue((LOCAL / 'references' / name).is_file())
            for link in re.findall(r'\]\(([^)]+)\)', text):
                if link.startswith(('https://', 'http://')):
                    continue
                file_part, _, anchor = link.partition('#')
                target = path.parent / file_part if file_part else path
                self.assertTrue(target.exists(), f'{path.name}: broken link {link}')
                if anchor and target.suffix == '.md':
                    headings = re.findall(r'^#{1,6} (.+)$', target.read_text(), re.M)
                    slugs = {re.sub(r'[^\w -]', '', h.lower()).replace(' ', '-') for h in headings}
                    self.assertIn(anchor, slugs, f'{path.name}: missing heading {link}')
        self.assertGreaterEqual(len(checked), 10)
        active = '\n'.join(p.read_text() for p in documents if p.is_relative_to(LOCAL)
                           or p.is_relative_to(ROOT / 'opencode_global')
                           or p.is_relative_to(ROOT / 'repo/.opencode'))
        self.assertNotIn('dilbert-build', active)
        self.assertNotIn('source unavailable', active.lower())
        self.assertNotIn('original contracts cannot', active.lower())

    def test_original_stage_contract_coverage_static(self):
        text = (LOCAL / 'references/legacy-stages.md').read_text()
        for name in STAGES:
            self.assertRegex(text, rf'\| `{name} ')
        for contract in ['rpi-explain <ID> <file>', 'rpi-plan-review <ID> <round>',
                         'rpi-implement <ID> <phase>', 'rpi-review <ID> <fixed-point>',
                         'rpi-review <ID> --working-tree', 'recon-map <repo-path>',
                         'rpi-arch-scenario <SYSTEM> <quality-number>']:
            self.assertIn(contract, text)
        for artifact in ['00-intake.md', '01-research.md', '02-questionnaire.md',
                         '03-scenarios.md', '04-plan.md', '05-implement.md', '06-closure.md',
                         'A0-intent.md', 'A1-claimed.md', 'A2-actual.md', 'A3-drift.md',
                         'A4-quality-scenarios.md', 'A5-risks-and-report.md',
                         '00-graph.md', '01-inventory.md', '02-flows.md',
                         '03-architecture.md', '04-drift.md']:
            self.assertIn(artifact, text)
        # These are prompt-contract checks, never claims that an LLM honored them.
        continuity = (LOCAL / 'references/continuity.md').read_text()
        self.assertIn('newer\ntimestamp alone is not authority', continuity)
        self.assertIn('status request alone does not authorize', continuity)
        self.assertIn('no code/file names in stakeholder explanation', text)
        self.assertIn('current oracle decisions', text)

    def test_source_distribution_ignore_rules(self):
        self.assertFalse((ROOT / 'repo/.agents').exists())
        with tempfile.TemporaryDirectory(prefix='dilbert source rules ') as tmp:
            target = Path(tmp)
            shutil.copy2(ROOT / '.gitignore', target / '.gitignore')
            self.assertEqual(run(['git', 'init', '-q'], cwd=target).returncode, 0)
            for path in ['backup/original-kit.zip', 'backup/notes.md', '.DS_Store',
                         'archive.zip', 'old.textClipping', 'validation/results.txt',
                         'validation/__pycache__/validate.pyc']:
                self.assertEqual(run(['git', 'check-ignore', '-q', '--', path], cwd=target).returncode, 0, path)
            for path in ['README.md', 'docs/DRILLS.md', 'validation/validate.py',
                         'repo/.opencode/commands/dilbert.md', 'opencode_global/agents/dilbert.md']:
                self.assertEqual(run(['git', 'check-ignore', '-q', '--', path], cwd=target).returncode, 1, path)


class Helper(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='dilbert helper ')
        self.addCleanup(self.temp.cleanup)
        self.other = Path(self.temp.name)
        self.repo = self.other / 'repository with spaces'
        shutil.copytree(LOCAL, self.repo / 'dilbert')
        self.helper = self.repo / 'dilbert/scripts/new-task.py'

    def create(self, name):
        return run(['python3', str(self.helper), name], cwd=self.other)

    def test_creation_from_other_cwd_no_git_and_valid_boundary(self):
        for name in ['OPS-123', 'A' * 80]:
            result = self.create(name)
            self.assertEqual(result.returncode, 0, result.stderr)
            text = (self.repo / 'thoughts' / name / 'task.md').read_text()
            self.assertIn('# Task ' + name, text)
            self.assertNotIn('__ID__', text)
        self.assertFalse((self.repo / '.git').exists())
        self.assertFalse((self.other / 'thoughts').exists())

    def test_artifact_continuity_and_duplicate_preservation(self):
        dest = self.repo / 'thoughts/LEGACY-1'
        dest.mkdir(parents=True)
        artifacts = {'02-questionnaire.md': 'Q1: owner approved keep retries; source: ticket 12\n',
                     '03-scenarios.md': 'SC1 confirmed: retries preserve request ID\n',
                     '05-implement.md': 'Phase 1 verified at revision ABC; phase 2 pending\n',
                     'recon/02-flows.md': '## other subsystem\nExisting observed flow\n'}
        for name, value in artifacts.items():
            path = dest / name
            path.parent.mkdir(exist_ok=True)
            path.write_text(value)
        self.assertEqual(self.create('LEGACY-1').returncode, 0)
        note = dest / 'task.md'
        note.write_text('User decision: retain existing numbered evidence\n')
        self.assertNotEqual(self.create('LEGACY-1').returncode, 0)
        self.assertEqual(note.read_text(), 'User decision: retain existing numbered evidence\n')
        for name, value in artifacts.items():
            self.assertEqual((dest / name).read_text(), value)

    def test_unsafe_ids_and_symlink_collisions(self):
        for name in ['', '../escape', 'a/b', 'a\\b', 'has space', 'x\ny', 'a;echo',
                     '-bad', '_bad', 'a.b', 'A' * 81]:
            with self.subTest(id=name):
                self.assertNotEqual(self.create(name).returncode, 0)
        outside = self.other / 'outside'
        outside.mkdir()
        notes = self.repo / 'thoughts'
        notes.symlink_to(outside, target_is_directory=True)
        self.assertNotEqual(self.create('ESCAPE').returncode, 0)
        notes.unlink()
        notes.mkdir()
        (notes / 'ESCAPE').symlink_to(outside, target_is_directory=True)
        self.assertNotEqual(self.create('ESCAPE').returncode, 0)
        dest = notes / 'FILELINK'
        dest.mkdir()
        target = outside / 'keep.md'
        target.write_text('preserve')
        (dest / 'task.md').symlink_to(target)
        self.assertNotEqual(self.create('FILELINK').returncode, 0)
        self.assertEqual(target.read_text(), 'preserve')
        self.assertEqual({p.name for p in outside.iterdir()}, {'keep.md'})


class GitEvidence(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='dilbert git evidence ')
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / 'repository with spaces'
        self.repo.mkdir()
        self.git('init', '-q')
        self.git('config', 'user.name', 'Disposable fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.hooksPath', str(Path(self.temp.name) / 'no-hooks'))

    def git(self, *args):
        result = run(['git', *args], cwd=self.repo)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def base(self):
        (self.repo / 'tracked.txt').write_text('baseline\n')
        self.git('add', '--', 'tracked.txt')
        self.git('commit', '-qm', 'Disposable baseline')
        return self.git('rev-parse', 'HEAD').strip()

    def test_local_staged_unstaged_new_and_commit_scope_differ(self):
        base = self.base()
        (self.repo / 'committed.txt').write_text('committed change\n')
        self.git('add', '--', 'committed.txt')
        self.git('commit', '-qm', 'Disposable branch change')
        (self.repo / 'tracked.txt').write_text('staged change\n')
        self.git('add', '--', 'tracked.txt')
        (self.repo / 'tracked.txt').write_text('working change\n')
        new = 'new file with spaces.txt'
        (self.repo / new).write_text('new behavior\n')
        self.assertIn('+staged change', self.git('diff', '--cached', '--'))
        self.assertIn('+working change', self.git('diff', '--'))
        self.assertIn('+working change', self.git('diff', 'HEAD', '--'))
        self.assertIn(new, self.git('ls-files', '--others', '--exclude-standard', '-z').split('\0'))
        merge_base = self.git('merge-base', base, 'HEAD').strip()
        committed = self.git('diff', '--name-only', merge_base, 'HEAD', '--').splitlines()
        self.assertEqual(committed, ['committed.txt'])
        self.assertEqual((self.repo / 'tracked.txt').read_text(), 'working change\n')
        # Reverting the disk to HEAD must not hide a still-staged edit.
        (self.repo / 'tracked.txt').write_text('baseline\n')
        self.assertEqual(self.git('diff', 'HEAD', '--'), '')
        self.assertIn('+staged change', self.git('diff', '--cached', '--'))
        self.assertIn('+baseline', self.git('diff', '--'))

    def test_unborn_repository_review(self):
        (self.repo / 'staged.txt').write_text('first staged file\n')
        self.git('add', '--', 'staged.txt')
        (self.repo / 'staged.txt').write_text('first disk edit\n')
        (self.repo / 'new.txt').write_text('untracked\n')
        self.assertNotEqual(run(['git', 'rev-parse', '--verify', 'HEAD'], cwd=self.repo).returncode, 0)
        self.assertIn('first staged file', self.git('diff', '--cached', '--'))
        self.assertIn('first disk edit', self.git('diff', '--'))
        self.assertIn('new.txt', self.git('ls-files', '--others', '--exclude-standard'))

    def test_resolved_worktree_excludes_preserve_unrelated_config(self):
        self.base()
        worktree = Path(self.temp.name) / 'linked worktree'
        self.git('worktree', 'add', '--detach', str(worktree), 'HEAD')
        result = run(['git', 'rev-parse', '--git-path', 'info/exclude'], cwd=worktree)
        self.assertEqual(result.returncode, 0, result.stderr)
        exclude = Path(result.stdout.strip())
        if not exclude.is_absolute():
            exclude = worktree / exclude
        original = exclude.read_text()
        # Use the exact rules printed in README, not a duplicate test-only list.
        rules = re.search(r'```gitignore\n(.*?)```', (ROOT / 'README.md').read_text(), re.S).group(1)
        exclude.write_text(original + '\n' + rules)
        shutil.copytree(ROOT / 'repo/.opencode', worktree / '.opencode')
        shutil.copytree(LOCAL, worktree / 'dilbert')
        note = worktree / 'thoughts/EXAMPLE/task.md'
        note.parent.mkdir(parents=True)
        note.write_text('local note')
        for path in ['dilbert/WORKFLOW.md', 'thoughts/EXAMPLE/task.md'] + [
                f'.opencode/commands/{n}.md' for n in COMMANDS]:
            self.assertEqual(run(['git', 'check-ignore', '-q', '--', path], cwd=worktree).returncode, 0, path)
        custom = worktree / '.opencode/commands/custom.md'
        custom.write_text('unrelated config')
        self.assertEqual(run(['git', 'check-ignore', '-q', '--', str(custom)], cwd=worktree).returncode, 1)
        self.assertTrue(exclude.read_text().startswith(original))
        self.assertTrue((worktree / '.git').is_file())
        self.assertFalse((self.repo / 'thoughts').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
