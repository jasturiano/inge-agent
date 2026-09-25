#!/usr/bin/env python3
"""Inspect Inge discovery and selected dependency relationships without writes.

Usage: doctor.py --repo TARGET [--framework KIT] [--skills-dir CATALOG ...].
The JSON report separates the target repository, reusable framework, optional
profile, task-note destination, missing bundled references, and known skill gaps.
Exit codes are 0 for no detected gaps, 1 for missing references/dependencies or
duplicate skill directories, and 2 for invalid input or inspection errors.

Git is invoked only for repository discovery; no provider, model, skill script,
or OpenCode process is invoked. Bytecode writes are disabled before importing the
local path helper. File presence is not proof of safe prompts or native discovery.
Framework Markdown is limited to 1 MiB per file and rejects nested symlinks. A
shared 10,000-entry/30-second cooperative budget bounds traversal. Run only a
trusted helper installation; filesystem presence does not authenticate prompts.
"""
import argparse
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from paths import framework, repository
from safeio import Budget, display, entries, files, kind, read_bytes


def main():
    """Parse CLI arguments, inspect the selected kit, and print one JSON report.

    Only literal references/<name>.md links and the curated skill-directory edges
    below are checked. Skill prose, transitive resources, invocation permissions,
    and runtime model identity are not validated. Catalogs inspect immediate
    children; duplicate directory names are reported without choosing a winner.

    Returns:
        0 for a clean filesystem/dependency report, or 1 for reported gaps.
        argparse exits with status 2 for bad arguments, OSError or ValueError.

    Output includes local paths, not Markdown contents. This is diagnostic
    evidence rather than an authorization decision or a security certificate.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='.', help='Target checkout or non-Git directory')
    parser.add_argument('--framework', help='Explicit framework; overrides INGE_HOME')
    parser.add_argument('--skills-dir', action='append', default=[],
                        help='Inspect immediate skill children; repeat for additional catalogs')
    args = parser.parse_args()
    try:
        root = repository(args.repo)
        home = framework(root, args.framework)
        budget = Budget()
        missing = set()
        for doc in files(home, budget):
            if doc.suffix != '.md':
                continue
            budget.check()
            content = read_bytes(doc).decode('utf-8')
            for ref in re.findall(r'(?<![\w/])references/([\w-]+\.md)', content):
                if kind(home / 'references' / ref) != 'file':
                    missing.add(f'references/{ref}')
        skills = {}
        for directory in args.skills_dir:
            directory = Path(directory).expanduser().resolve(strict=True)
            if not directory.is_dir():
                raise ValueError(f'Skill catalog is not a directory: {directory}')
            for name, category in entries(directory, budget):
                if category == 'link':
                    raise ValueError(f'Linked skill directory requires separate explicit selection: {directory / name}')
                if category != 'directory':
                    continue
                path = directory / name / 'SKILL.md'
                category = kind(path)
                if category == 'file':
                    skills.setdefault(name, []).append(str(path))
                elif category != 'missing':
                    raise ValueError(f'Unsafe skill file: {path}')
        # Curated integration edges, not a claim to parse arbitrary skill prose.
        dependencies = {'grill-with-docs': ['grilling', 'domain-modeling'],
                        'tdd': ['codebase-design']}
        skill_gaps = {name: [dep for dep in deps if dep not in skills]
                      for name, deps in dependencies.items() if name in skills}
        skill_gaps = {name: deps for name, deps in skill_gaps.items() if deps}
        duplicates = {name: paths for name, paths in skills.items() if len(paths) > 1}
        profile = root / 'inge/PROJECT.md'
        profile_kind = kind(profile)
        if profile_kind not in {'file', 'missing'}:
            raise ValueError(f'Unsafe linked or special project profile: {profile}')
        result = {
            'repository': str(root), 'framework': str(home),
            'profile': str(profile) if profile_kind == 'file' else None,
            'notes': str(root / 'thoughts'), 'missing_references': sorted(missing),
            'skill_files': skills, 'known_skill_dependency_gaps': skill_gaps,
            'duplicate_skill_directories': duplicates,
            'runtime': 'UNVERIFIED: commands, skills, permissions, models and dispatch require harness checks',
        }
        print(json.dumps(result, indent=2))
        return 1 if missing or skill_gaps or duplicates else 0
    except (OSError, ValueError) as error:
        parser.exit(2, f'Inge doctor: {display(error)}\n')


if __name__ == '__main__':
    sys.exit(main())
