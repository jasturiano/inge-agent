#!/usr/bin/env python3
"""Read-only, bounded inventory of Inge installations and legacy leftovers.

Compare with this trusted source checkout, never a fetched release. Use --root
(repeatable) and optionally --opencode-dir. No scanned code is imported or run.
Unexpected symlinks/special files are reported, not followed. Explicit CLI roots
are resolved once as operator-selected locations. Output escapes control characters.
Exit 0 means inspection completed, not secure/current; 2 means incomplete/error.
Limits: 1 MiB per file, 10,000 inspected directory entries, 30 seconds cooperative
work time. A blocked kernel I/O call on a hostile mount cannot be interrupted here.
Requires the source checkout's safeio helper and POSIX directory descriptors.
"""
import argparse
import os
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE / 'repo/inge/scripts'))
from safeio import Budget, display, entries, files, kind, read_bytes

SKIP = {'.git', '.hg', '.svn', 'node_modules', '.venv', 'venv', '__pycache__',
        '.next', '.cache', 'vendor', 'dist', 'build', 'backup'}
LEGACY_PATHS = {'dilbert', '.dilbert', 'dilbert_scripts', 'dilbert_templates',
                'dilbert_arch-templates', 'dilbert_prompts', 'dilbert.md'}


def emit(message):
    """Print a report line with all untrusted control/formatting characters escaped."""
    print(display(message))


def agent_body(data):
    """Strip recognizable frontmatter for drift classification, not permission approval."""
    parts = data.split(b'---', 2)
    return parts[2] if data.startswith(b'---\n') and len(parts) == 3 else data


class Report:
    """Collect read-only findings; unsafe/skipped inspection sets a nonzero status."""

    def __init__(self):
        """Create independent traversal, deduplication and shared resource-budget state."""
        self.errors = False
        self.visited = set()
        self.leftovers = set()
        self.budget = Budget()

    def error(self, path, error):
        """Flag incomplete inspection and emit a safely escaped diagnostic."""
        self.errors = True
        emit(f'  Cannot inspect {path}: {error.strerror or str(error)}')

    def leftover(self, path, reason):
        """Report one legacy candidate per path/reason without deleting anything."""
        key = (path, reason)
        if key not in self.leftovers:
            self.leftovers.add(key)
            emit(f'  Legacy Dilbert leftover: {path} ({reason}; review manually).')

    def listing(self, path):
        """Return bounded no-follow children, treating absent paths as empty."""
        try:
            return entries(path, self.budget)
        except FileNotFoundError:
            return []
        except OSError as error:
            self.error(path, error)
            return []

    def references(self, path):
        """Read one bounded known file safely; print old-name line numbers, not contents."""
        try:
            self.budget.check()
            data = read_bytes(path).decode('utf-8', errors='replace')
            lines = [str(i) for i, line in enumerate(data.splitlines(), 1)
                     if re.search('dilbert', line, re.IGNORECASE)]
            if lines:
                self.leftover(path, 'old-name reference on lines ' + ', '.join(lines))
        except FileNotFoundError:
            pass
        except OSError as error:
            self.error(path, error)

    def legacy_entries(self, directory, children=None):
        """Report old names and backups from an immediate no-follow directory listing."""
        for name, category in self.listing(directory) if children is None else children:
            path = directory / name
            lower = name.lower()
            if path != SOURCE and (lower in LEGACY_PATHS or lower.startswith(
                    ('dilbert-', 'dilbert_', 'dilbert.', '.dilbert.'))):
                self.leftover(path, 'old-name file, directory or symlink')

    def compare(self, label, target, reference, agent=False, profile=False):
        """Compare bounded regular files only, rejecting links in every path component.

        agent distinguishes header-only customization without approving permissions.
        profile excludes user-owned PROJECT.md. Unknown extra framework files are
        not compared. Missing/different files are drift, unsafe reads are errors.
        """
        missing, different, customized = [], [], []
        incomplete = False
        try:
            for source in files(reference, self.budget):
                if profile and source.name == 'PROJECT.md':
                    continue
                relative = source.relative_to(reference)
                try:
                    self.budget.check()
                    actual = read_bytes(target / relative)
                    current = read_bytes(source)
                    if actual != current:
                        group = customized if agent and agent_body(actual) == agent_body(current) else different
                        group.append(str(relative))
                except FileNotFoundError:
                    missing.append(str(relative))
                except OSError as error:
                    incomplete = True
                    self.error(target / relative, error)
        except OSError as error:
            incomplete = True
            self.error(reference, error)
        if incomplete:
            emit(f'  {label} comparison is incomplete because some files could not be read.')
        elif missing or different:
            emit(f'  {label} is incomplete or differs from this checkout (out of date or customized).')
        elif customized:
            emit(f'  {label} instructions are current; model/permission metadata is customized.')
            emit('  Customized metadata is NOT a security approval; inspect effective permissions.')
        else:
            emit(f'  {label} is up to date with this checkout.')
        for title, paths in [('Missing', missing), ('Different', different), ('Customized metadata', customized)]:
            if paths:
                emit(f'    {title}: {", ".join(paths)}')

    def definitions(self, root, global_scope=False):
        """Inspect singular/plural definition folders without resolving discovered links."""
        found = False
        self.legacy_entries(root)
        for category, reference in [('agents', SOURCE / 'opencode_global/agents'),
                                    ('commands', SOURCE / 'repo/.opencode/commands')]:
            locations = []
            for name in [category, category[:-1]]:
                directory = root / name
                children = self.listing(directory)
                self.legacy_entries(directory, children)
                names = [n for n, _ in children if n.startswith('inge') and n.endswith('.md')]
                if names:
                    found = True
                    locations.append(directory)
                    emit(f'  Inge {category} found: {directory}')
                    self.compare(f'{"Global OpenCode" if global_scope else "Local OpenCode"} {category}',
                                 directory, reference, agent=category == 'agents')
                    known = {p.name for p in files(reference, self.budget)}
                    extra = [n for n in names if n not in known]
                    if extra:
                        emit(f'    Additional/legacy definitions: {", ".join(extra)}')
                for name in names:
                    self.references(directory / name)
            if len(locations) > 1:
                emit(f'  Multiple {category} directories contain Inge; check duplicate discovery.')
            if global_scope and not locations:
                emit(f'  No Inge Markdown {category} found in {root}.')
        for name in ['opencode.json', 'opencode.jsonc', 'AGENTS.md']:
            self.references(root / name)
        return found

    def scan(self, root):
        """Walk bounded no-follow directories, never import discovered code or policy.

        Shared/local installations are inventory candidates, not trusted selections.
        Dependency/build directories and source distribution are excluded. Links
        and special files are reported as skipped; contents are never traversed.
        """
        emit(f'Scanning repositories beneath: {root}')
        pending, count = [root], 0
        while pending:
            self.budget.check()
            here = pending.pop()
            if here in self.visited:
                continue
            self.visited.add(here)
            if here == SOURCE:
                emit(f'Inge source checkout: {here} (distribution files are not installations).')
                continue
            children = self.listing(here)
            names = dict(children)
            self.legacy_entries(here, children)
            for name in ['AGENTS.md', 'CLAUDE.md', 'opencode.json', 'opencode.jsonc', '.gitignore']:
                if name in names:
                    self.references(here / name)
            if names.get('.git') == 'directory':
                self.references(here / '.git/info/exclude')
            local = here / 'inge'
            local_names = dict(self.listing(local)) if 'inge' in names else {}
            has_framework = 'WORKFLOW.md' in local_names
            has_profile = 'PROJECT.md' in local_names
            if '.git' in names or 'inge' in names or '.opencode' in names:
                count += 1
                emit(f'Repository/directory: {here}')
                if has_framework:
                    emit(f'Inge is installed locally in this repo: {local}')
                    self.compare('Local framework', local, SOURCE / 'repo/inge', profile=True)
                elif has_profile:
                    emit(f'Inge has a local project profile in this repo: {local / "PROJECT.md"}')
                    emit('  A profile alone is not a local framework installation.')
                elif 'inge' in names:
                    emit(f'Possible incomplete Inge installation: {local} (no WORKFLOW.md).')
                else:
                    emit('No local Inge framework or profile found.')
                self.definitions(here / '.opencode')
                if has_profile:
                    self.references(local / 'PROJECT.md')
                selected = os.environ.get('INGE_HOME')
                if selected:
                    emit(f'  INGE_HOME explicitly selects: {Path(selected).expanduser()} (trust asserted by launcher).')
                else:
                    emit('  No trusted framework selected; set INGE_HOME or supply an approved session path.')
            if '.inge' in names:
                shared = here / '.inge'
                emit(f'Shared Inge directory: {shared} (candidate only; explicit trust required).')
                self.compare('Shared framework', shared, SOURCE / 'repo/inge', profile=True)
            for name, category in reversed(children):
                if category == 'link' and name not in SKIP:
                    self.errors = True
                    emit(f'  Skipping directory symlink or file symlink during traversal: {here / name}')
                if category == 'other' and name not in SKIP:
                    self.errors = True
                    emit(f'  Skipping special file during traversal: {here / name}')
                if category == 'directory' and name not in SKIP | {'.inge', '.opencode'}:
                    if name.lower() not in LEGACY_PATHS and not (name == 'inge' and (has_framework or has_profile)):
                        pending.append(here / name)
        if not count:
            emit('No repositories or local Inge installations found in this scan.')


def main():
    """Resolve operator-selected roots once, run bounded reports and return 0 or 2.

    Explicit roots may intentionally be symlinks. Discovered links are never
    resolved. Unsupported platforms and incomplete coverage return 2; drift alone
    returns 0. Environment paths are launch configuration, not repository authority.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', action='append', required=True)
    parser.add_argument('--opencode-dir', action='append')
    args = parser.parse_args()
    roots = []
    for value in args.root:
        path = Path(value).expanduser().resolve()
        if not path.is_dir():
            parser.error(display(f'Scan root is not an existing directory: {path}'))
        roots.append(path)
    if args.opencode_dir:
        configs = [Path(p).expanduser().resolve() for p in args.opencode_dir]
    else:
        configs = [Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config'))) / 'opencode']
        if os.environ.get('OPENCODE_CONFIG_DIR'):
            configs.append(Path(os.environ['OPENCODE_CONFIG_DIR']).expanduser())
    report = Report()
    emit(f'Read-only installation report. Reference: {SOURCE}')
    emit('Comparison is against local source files, not the latest upstream release.')
    if os.environ.get('DILBERT_HOME'):
        emit('Legacy Dilbert leftover: DILBERT_HOME is set; migrate to INGE_HOME (not used by inge).')
    try:
        for root in roots:
            for parent in root.parents:
                old_shared = parent / '.dilbert'
                if kind(old_shared) != 'missing':
                    report.leftover(old_shared, 'ancestor shared framework')
        for config in dict.fromkeys(p.resolve() for p in configs):
            emit(f'Global/custom OpenCode configuration: {config}')
            report.definitions(config, global_scope=True)
        if os.environ.get('OPENCODE_CONFIG'):
            emit('OPENCODE_CONFIG is set; overrides are not evaluated.')
            report.references(Path(os.path.abspath(Path(os.environ['OPENCODE_CONFIG']).expanduser())))
        for root in roots:
            report.scan(root)
    except (OSError, ValueError) as error:
        report.errors = True
        emit(f'Incomplete inspection: {error}')
    emit('No files changed. Runtime discovery, JSON/managed overrides and model access are unverified.')
    return 2 if report.errors else 0


if __name__ == '__main__':
    sys.exit(main())
