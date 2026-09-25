#!/usr/bin/env python3
"""Validate this distribution; no OpenCode/provider calls or installed configuration writes.

Requires Python 3, Git, and Ruby's standard YAML library. Git commits/worktrees created
here exist only in disposable fixtures. No user repository is initialized or modified.

The suite checks source contracts, path discovery, task creation and Git evidence
semantics. It does not execute a model, enforce prompt-injection resistance, or
validate effective OpenCode permissions. A passing test means the named invariant
held in its fixture, not that an agent will honor the corresponding prose.
Run with python3 validation/validate.py; unittest exits nonzero on failure.
The full suite mutates Git in disposable fixtures and is human-maintainer-only.
Agents use --policy-only, which runs static checks without invoking Git or creating
repositories, commits, worktrees or metadata.
"""
import json
import fnmatch
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / 'repo/inge'
MODELS = ('inge', 'inge-worker', 'inge-worker-strong', 'inge-expert', 'inge-scout')
COMMANDS = {'inge', 'inge-work', 'inge-review', 'inge-arch', 'inge-status'}
STAGES = {'rpi-research', 'rpi-questions', 'rpi-scenario-check', 'rpi-plan',
          'rpi-explain', 'rpi-plan-review', 'rpi-implement', 'rpi-review',
          'rpi-arch-claimed', 'rpi-arch-actual', 'rpi-arch-drift',
          'rpi-arch-scenario', 'rpi-arch-report', 'recon-map', 'recon-orient', 'recon-trace'}


def run(args, cwd=None, **kwargs):
    """Run an argument-vector fixture command and capture decoded stdout/stderr.

    Optional subprocess keyword arguments supply input or an environment. No
    shell is enabled by default, and exit-code assertions belong to each caller.
    """
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, **kwargs)


def frontmatter(path):
    """Parse a Markdown YAML header through Ruby's safe loader for assertions.

    Return (parsed mapping, original header text). Missing delimiters or YAML
    parser failure raises AssertionError. Only distribution files are supplied;
    this test helper is not a validator for untrusted installations.
    """
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
    """Check shipped naming, permissions, references and compatibility contracts."""
    def test_no_old_brand_in_runtime_distribution(self):
        """Keep the old brand out of active prompts, helpers and runtime paths."""
        for directory in [LOCAL, ROOT / 'opencode_global', ROOT / 'repo/.opencode']:
            for path in directory.rglob('*'):
                self.assertNotIn('dilbert', str(path.relative_to(ROOT)).lower())
                if path.suffix in {'.md', '.py'}:
                    self.assertNotIn('dilbert', path.read_text().lower(), str(path))
        self.assertFalse((ROOT / 'repo/dilbert').exists())

    def test_exact_roles_and_permissions(self):
        """Verify the five roles and their explicit edit/Bash/delegation rules."""
        agents = {p.stem: p for p in (ROOT / 'opencode_global/agents').glob('*.md')}
        self.assertEqual(set(agents), set(MODELS))
        for name, path in agents.items():
            with self.subTest(role=name):
                data, header = frontmatter(path)
                writer = name in {'inge-worker', 'inge-worker-strong'}
                if writer:
                    self.assertEqual(data['permission']['edit']['*'], 'ask')
                    self.assertEqual(data['permission']['edit']['**/.git/**'], 'deny')
                    self.assertEqual(data['permission']['bash']['*'], 'ask')
                    self.assertEqual(data['permission']['bash']['*git*'], 'deny')
                else:
                    self.assertEqual(data['permission']['edit'], 'deny')
                    self.assertEqual(data['permission']['bash'], 'deny')
                self.assertEqual(data['permission']['*'], 'deny')
                self.assertEqual(next(iter(data['permission'])), '*')
                for tool in ['webfetch', 'websearch', 'skill', 'external_directory', 'grep']:
                    self.assertEqual(data['permission'][tool], 'ask')
                self.assertEqual(data['permission']['read']['*.env'], 'deny')
                if name == 'inge':
                    self.assertEqual(data['mode'], 'primary')
                    self.assertEqual(data['permission']['task'],
                                     {'*': 'deny', **{n: 'allow' for n in MODELS if n != 'inge'}})
                    self.assertEqual(next(iter(data['permission']['task'])), '*')
                else:
                    self.assertEqual(data['mode'], 'subagent')
                    self.assertEqual(data['permission']['task'], 'deny')

    def test_git_is_suggestion_only(self):
        """Check no-write policy and representative deny patterns without running Git.

        fnmatch models simple last-match rule selection for these patterns only;
        it does not certify OpenCode's command parser or effective merged policy.
        """
        for name in MODELS:
            path = ROOT / 'opencode_global/agents' / (name + '.md')
            data, _ = frontmatter(path)
            self.assertIn('Git is human-operated', path.read_text())
            rules = data['permission']['bash']
            if isinstance(rules, dict):
                for command in ['git commit -m example', 'git -C repo pull', '/usr/bin/git push',
                                'git merge main', 'git add .', 'git fetch', 'git status',
                                'git worktree add example', 'git stash clear', 'git stash drop',
                                'git stash apply', 'git stash branch other', 'git stash store abc',
                                'git stash export --to-ref refs/test', 'git -C repo stash pop',
                                'gh repo sync', 'glab mr merge']:
                    matched = [value for pattern, value in rules.items()
                               if fnmatch.fnmatchcase(command, pattern)]
                    self.assertEqual(matched[-1], 'deny', command)
                for command in ['git stash', 'git stash push', 'git stash push -m task',
                                'git stash pop', 'git stash pop stash@{1}', 'git stash list']:
                    matched = [value for pattern, value in rules.items()
                               if fnmatch.fnmatchcase(command, pattern)]
                    self.assertEqual(matched[-1], 'ask', command)
                edits = data['permission']['edit']
                for target in ['.git', '.git/config', '/repo/.git/index', '/repo/.git']:
                    matched = [value for pattern, value in edits.items()
                               if fnmatch.fnmatchcase(target, pattern)]
                    self.assertEqual(matched[-1], 'deny', target)
        self.assertIn('Git belongs to the user', (LOCAL / 'SOUL.md').read_text())
        self.assertIn('### Approved stash exception', (LOCAL / 'WORKFLOW.md').read_text())

    def test_model_pins_and_commented_alternatives(self):
        """Check model-ID syntax without probing providers or asserting availability."""
        # Configuration is authoritative; tests validate shape, not provider availability.
        for name in MODELS:
            with self.subTest(role=name):
                data, header = frontmatter(ROOT / 'opencode_global/agents' / (name + '.md'))
                self.assertEqual(len(re.findall(r'^model:\s*(\S+)', header, re.M)), 1)
                self.assertRegex(data['model'], r'^\S+/\S+$')
                self.assertLessEqual(len(re.findall(r'^#\s*model:\s*(\S+)', header, re.M)), 1)

    def test_commands_router_arguments_no_model_overrides(self):
        """Ensure command aliases route to inge and preserve user arguments."""
        commands = list((ROOT / 'repo/.opencode/commands').glob('*.md'))
        self.assertEqual({p.stem for p in commands}, COMMANDS)
        for path in commands:
            data, header = frontmatter(path)
            self.assertEqual(data['agent'], 'inge')
            self.assertNotIn('model', data)
            self.assertNotRegex(header, r'(?m)^#?\s*model:')
            self.assertIn('$ARGUMENTS', path.read_text())
        self.assertFalse((ROOT / 'repo/.opencode/command').exists())
        self.assertFalse((ROOT / 'opencode_global/agent').exists())

    def test_shared_references_and_local_document_links(self):
        """Resolve local Markdown links, heading anchors and bundled references."""
        documents = (list(LOCAL.rglob('*.md')) + list((ROOT / 'opencode_global').rglob('*.md'))
                     + list((ROOT / 'repo/.opencode').rglob('*.md'))
                     + [ROOT / 'README.md'] + list((ROOT / 'docs').glob('*.md'))
                     + list((ROOT / 'validation').glob('*.md')))
        references = {p.name for p in (LOCAL / 'references').glob('*.md')}
        checked = set()
        for path in documents:
            text = path.read_text()
            for ref in re.findall(r'`((?:inge/|references/)[\w./-]+\.md)`', text):
                target = ROOT / 'repo' / ref if ref.startswith('inge/') else LOCAL / ref
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
        self.assertNotIn('inge-build', active)
        self.assertNotIn('source unavailable', active.lower())
        self.assertNotIn('original contracts cannot', active.lower())

    def test_original_stage_contract_coverage_static(self):
        """Check legacy stage contracts remain documented, without running an LLM."""
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
        """Test ignore rules in a temporary Git repo without touching real excludes."""
        self.assertFalse((ROOT / 'repo/.agents').exists())
        with tempfile.TemporaryDirectory(prefix='inge source rules ') as tmp:
            target = Path(tmp)
            shutil.copy2(ROOT / '.gitignore', target / '.gitignore')
            self.assertEqual(run(['git', 'init', '-q'], cwd=target).returncode, 0)
            for path in ['backup/original-kit.zip', 'backup/notes.md', '.DS_Store',
                         'archive.zip', 'old.textClipping', 'validation/results.txt',
                         'validation/__pycache__/validate.pyc']:
                self.assertEqual(run(['git', 'check-ignore', '-q', '--', path], cwd=target).returncode, 0, path)
            for path in ['README.md', 'docs/DRILLS.md', 'validation/validate.py',
                         'repo/.opencode/commands/inge.md', 'opencode_global/agents/inge.md']:
                self.assertEqual(run(['git', 'check-ignore', '-q', '--', path], cwd=target).returncode, 1, path)


class Helper(unittest.TestCase):
    """Exercise task creation and existing-artifact protection in copied kits."""
    def setUp(self):
        """Copy the framework into a disposable repository-shaped directory."""
        self.temp = tempfile.TemporaryDirectory(prefix='inge helper ')
        self.addCleanup(self.temp.cleanup)
        self.other = Path(self.temp.name)
        self.repo = self.other / 'repository with spaces'
        shutil.copytree(LOCAL, self.repo / 'inge')
        self.helper = self.repo / 'inge/scripts/new-task.py'

    def create(self, name):
        """Run the copied helper with a task ID and an explicit fixture target."""
        return run(['python3', str(self.helper), name, '--repo', str(self.repo)], cwd=self.other)

    def test_explicit_target_required_and_shared_helper_does_not_write_at_installation(self):
        """Require --repo and ensure a shared helper writes only to its target."""
        result = run(['python3', str(self.helper), 'NO-TARGET'], cwd=self.other)
        self.assertNotEqual(result.returncode, 0)
        target = self.other / 'another repository'
        target.mkdir()
        result = run(['python3', str(self.helper), 'SHARED', '--repo', str(target)], cwd=self.repo)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((target / 'thoughts/SHARED/task.md').is_file())
        self.assertFalse((self.repo / 'thoughts').exists())
        result = run(['python3', str(self.helper), 'BAD', '--repo', str(target / 'missing')])
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((target / 'missing').exists())

    def test_creation_from_other_cwd_no_git_and_valid_boundary(self):
        """Accept a boundary-length ID without initializing Git or using shell cwd."""
        for name in ['OPS-123', 'A' * 80]:
            result = self.create(name)
            self.assertEqual(result.returncode, 0, result.stderr)
            text = (self.repo / 'thoughts' / name / 'task.md').read_text()
            self.assertIn('# Task ' + name, text)
            self.assertNotIn('__ID__', text)
        self.assertFalse((self.repo / '.git').exists())
        self.assertFalse((self.other / 'thoughts').exists())

    def test_artifact_continuity_and_duplicate_preservation(self):
        """Preserve numbered evidence and reject replacement of an existing note."""
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
        """Reject traversal-like IDs and pre-existing directory/final-file symlinks.

        These static fixtures do not simulate concurrent path replacement; passing
        them does not establish race-free filesystem containment.
        """
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


class SharedDiscovery(unittest.TestCase):
    """Check framework/target separation and limited dependency diagnostics."""
    def setUp(self):
        """Create a shared kit and explicitly select it using fixture INGE_HOME."""
        self.temp = tempfile.TemporaryDirectory(prefix='inge shared ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.shared = self.base / '.inge'
        shutil.copytree(LOCAL, self.shared)
        self.repo = self.base / 'group/project/repository'
        self.repo.mkdir(parents=True)
        result = run(['git', 'init', '-q'], cwd=self.repo)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.env = dict(os.environ)
        self.env['INGE_HOME'] = str(self.shared)

    def doctor(self, target=None, *args):
        """Capture JSON diagnostics from the fixture kit with optional CLI flags."""
        return run(['python3', str(self.shared / 'scripts/doctor.py'), '--repo',
                    str(target or self.repo), *args], env=self.env, cwd=self.base)

    def test_nested_checkout_profile_and_nearest_framework(self):
        """Resolve nested targets; neither a local profile nor nearer kit overrides trust."""
        subdir = self.repo / 'src/deep'
        subdir.mkdir(parents=True)
        (self.repo / 'inge').mkdir()
        (self.repo / 'inge/PROJECT.md').write_text('local only')
        result = self.doctor(subdir)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data['repository'], str(self.repo.resolve()))
        self.assertEqual(data['framework'], str(self.shared.resolve()))
        self.assertEqual(data['profile'], str(self.repo.resolve() / 'inge/PROJECT.md'))
        self.assertEqual(data['notes'], str(self.repo.resolve() / 'thoughts'))
        nearer = self.repo.parent / '.inge'
        shutil.copytree(LOCAL, nearer)
        self.assertEqual(json.loads(self.doctor().stdout)['framework'], str(self.shared.resolve()))
        self.assertFalse((self.shared / 'scripts/__pycache__').exists())
        self.assertFalse((self.repo / 'thoughts').exists())

    def test_precedence_and_incomplete_explicit_selection(self):
        """Verify explicit/environment selection and reject absent trust or incomplete kits."""
        shutil.copytree(LOCAL, self.repo / 'inge')
        self.assertEqual(json.loads(self.doctor().stdout)['framework'], str(self.shared.resolve()))
        self.env['INGE_HOME'] = str(self.shared)
        self.assertEqual(json.loads(self.doctor().stdout)['framework'], str(self.shared.resolve()))
        result = self.doctor(None, '--framework', str(self.repo / 'inge'))
        self.assertEqual(json.loads(result.stdout)['framework'], str(self.repo.resolve() / 'inge'))
        result = self.doctor(None, '--framework', str(self.base / 'missing'))
        self.assertEqual(result.returncode, 2)
        self.assertIn('Incomplete framework', result.stderr)
        self.env.pop('INGE_HOME')
        (self.repo / 'inge/SOUL.md').unlink()
        self.assertEqual(self.doctor().returncode, 2)

    def test_skill_dependency_gaps_and_duplicates(self):
        """Report curated missing skill names and duplicate catalog directories."""
        catalog = self.base / 'skills'
        for name in ['grill-with-docs', 'tdd']:
            (catalog / name).mkdir(parents=True)
            (catalog / name / 'SKILL.md').write_text('fixture')
        result = self.doctor(None, '--skills-dir', str(catalog))
        self.assertEqual(result.returncode, 1)
        data = json.loads(result.stdout)
        self.assertEqual(data['known_skill_dependency_gaps']['grill-with-docs'], ['grilling', 'domain-modeling'])
        for name in ['grilling', 'domain-modeling', 'codebase-design']:
            (catalog / name).mkdir()
            (catalog / name / 'SKILL.md').write_text('fixture')
        self.assertEqual(self.doctor(None, '--skills-dir', str(catalog)).returncode, 0)
        other = self.base / 'other-skills'
        shutil.copytree(catalog, other)
        result = self.doctor(None, '--skills-dir', str(catalog), '--skills-dir', str(other))
        self.assertEqual(result.returncode, 1)
        self.assertIn('tdd', json.loads(result.stdout)['duplicate_skill_directories'])

    def test_non_git_symlinked_framework_and_missing_reference(self):
        """Allow explicit symlinked kits and report missing referenced documents."""
        target = self.base / 'plain directory'
        target.mkdir()
        link = self.base / 'framework link'
        link.symlink_to(self.shared, target_is_directory=True)
        result = self.doctor(target, '--framework', str(link))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['repository'], str(target.resolve()))
        (self.shared / 'references/security.md').unlink()
        result = self.doctor(target, '--framework', str(link))
        self.assertEqual(result.returncode, 1)
        self.assertIn('references/security.md', json.loads(result.stdout)['missing_references'])
        self.assertFalse((target / '.git').exists())

    def test_linked_worktree_target_and_explicit_framework_outside_ancestor(self):
        """Keep linked-worktree notes separate from the main repo and external kit."""
        for key, value in [('user.name', 'Fixture'), ('user.email', 'fixture@example.invalid'),
                           ('commit.gpgsign', 'false'), ('core.hooksPath', str(self.base / 'no-hooks'))]:
            self.assertEqual(run(['git', 'config', key, value], cwd=self.repo).returncode, 0)
        result = run(['git', 'commit', '--allow-empty', '-qm', 'fixture'], cwd=self.repo)
        self.assertEqual(result.returncode, 0, result.stderr)
        with tempfile.TemporaryDirectory(prefix='inge outside ') as outside:
            worktree = Path(outside) / 'worktree'
            result = run(['git', 'worktree', 'add', '--detach', str(worktree), 'HEAD'], cwd=self.repo)
            self.assertEqual(result.returncode, 0, result.stderr)
            subdir = worktree / 'src'
            subdir.mkdir()
            result = self.doctor(subdir, '--framework', str(self.shared))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['repository'], str(worktree.resolve()))
            helper = self.shared / 'scripts/new-task.py'
            result = run(['python3', str(helper), 'WT', '--repo', str(subdir)], cwd=self.base)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((worktree / 'thoughts/WT/task.md').is_file())
            self.assertFalse((self.repo / 'thoughts').exists())
            self.assertFalse((self.base / 'thoughts').exists())


class GitEvidence(unittest.TestCase):
    """Demonstrate diff/exclude semantics using only disposable Git repositories."""
    def setUp(self):
        """Initialize a temporary repo with fixture identity, no signing or hooks."""
        self.temp = tempfile.TemporaryDirectory(prefix='inge git evidence ')
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / 'repository with spaces'
        self.repo.mkdir()
        self.git('init', '-q')
        self.git('config', 'user.name', 'Disposable fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.hooksPath', str(Path(self.temp.name) / 'no-hooks'))

    def git(self, *args):
        """Run fixture-local Git, assert success, and return captured standard output."""
        result = run(['git', *args], cwd=self.repo)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def base(self):
        """Commit a single baseline fixture file and return its revision identifier."""
        (self.repo / 'tracked.txt').write_text('baseline\n')
        self.git('add', '--', 'tracked.txt')
        self.git('commit', '-qm', 'Disposable baseline')
        return self.git('rev-parse', 'HEAD').strip()

    def test_local_staged_unstaged_new_and_commit_scope_differ(self):
        """Show why committed-only or HEAD-only review can miss working-tree changes."""
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
        """Inspect staged, unstaged and new files before the first repository commit."""
        (self.repo / 'staged.txt').write_text('first staged file\n')
        self.git('add', '--', 'staged.txt')
        (self.repo / 'staged.txt').write_text('first disk edit\n')
        (self.repo / 'new.txt').write_text('untracked\n')
        self.assertNotEqual(run(['git', 'rev-parse', '--verify', 'HEAD'], cwd=self.repo).returncode, 0)
        self.assertIn('first staged file', self.git('diff', '--cached', '--'))
        self.assertIn('first disk edit', self.git('diff', '--'))
        self.assertIn('new.txt', self.git('ls-files', '--others', '--exclude-standard'))

    def test_resolved_worktree_excludes_preserve_unrelated_config(self):
        """Apply README exclude examples only in a fixture and retain custom commands."""
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
        shutil.copytree(LOCAL, worktree / 'inge')
        note = worktree / 'thoughts/EXAMPLE/task.md'
        note.parent.mkdir(parents=True)
        note.write_text('local note')
        for path in ['inge/WORKFLOW.md', 'thoughts/EXAMPLE/task.md'] + [
                f'.opencode/commands/{n}.md' for n in COMMANDS]:
            self.assertEqual(run(['git', 'check-ignore', '-q', '--', path], cwd=worktree).returncode, 0, path)
        custom = worktree / '.opencode/commands/custom.md'
        custom.write_text('unrelated config')
        self.assertEqual(run(['git', 'check-ignore', '-q', '--', str(custom)], cwd=worktree).returncode, 1)
        self.assertTrue(exclude.read_text().startswith(original))
        self.assertTrue((worktree / '.git').is_file())
        self.assertFalse((self.repo / 'thoughts').exists())


if __name__ == '__main__':
    if '--policy-only' in sys.argv:
        # This subset never initializes repositories, writes metadata or invokes Git.
        names = [name for name in unittest.defaultTestLoader.getTestCaseNames(Configuration)
                 if name != 'test_source_distribution_ignore_rules']
        suite = unittest.TestSuite(Configuration(name) for name in names)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        sys.exit(0 if result.wasSuccessful() else 1)
    unittest.main(verbosity=2)
