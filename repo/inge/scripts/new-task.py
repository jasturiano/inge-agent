#!/usr/bin/env python3
"""Create a private, exclusive task note through no-follow directory descriptors.

Usage: new-task.py ID --repo TARGET. Execute only a reviewed helper installation.
The template belongs to that installation; notes belong to the independently
resolved target. New directories use 0700 and files 0600, subject to umask.
Existing notes are never replaced. Unsupported platforms fail closed, without
race-prone pathname fallbacks. No model/network/commit operations run.
"""
from contextlib import ExitStack
import argparse
import os
import re
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from paths import repository
from safeio import directory, display, read_bytes


def create_note(root, task_id, text):
    """Create thoughts/task_id/task.md relative to verified directory handles.

    Validate IDs for non-CLI callers too. mkdir/open pairs use no-follow opens:
    replacing a parent name with a symlink cannot redirect creation. Open handles
    remain anchored if names change. Exclusive final creation rejects existing
    files/links; I/O failure may leave a partial new file. OSError propagates,
    with FileExistsError identifying a collision at final creation.
    """
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', task_id):
        raise ValueError('Invalid task ID')
    with ExitStack() as stack:
        parent = stack.enter_context(directory(root))
        for component in ['thoughts', task_id]:
            try:
                os.mkdir(component, mode=0o700, dir_fd=parent)
            except FileExistsError:
                pass
            child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
            stack.callback(os.close, child)
            parent = child
        fd = os.open('task.md', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     0o600, dir_fd=parent)
        with os.fdopen(fd, 'w', encoding='utf-8') as out:
            out.write(text.replace('__ID__', task_id))


def main():
    """Parse explicit target and ID; emit escaped paths and controlled exit codes.

    CLI status is 0 on success, 1 for an existing note, 2 for invalid input,
    unsafe paths or failed discovery/reads. Bounded template reads and all write
    operations reject nested links. Native harness write authorization still applies.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('id', help='Alphanumeric first; letters/digits/_/-; max 80')
    parser.add_argument('--repo', required=True, help='Explicit target worktree or non-Git directory')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', args.id):
        parser.error('Invalid ID; example: OPS-123')
    try:
        root = repository(args.repo)
        local = Path(__file__).resolve().parents[1]
        text = read_bytes(local / 'templates/task.md').decode('utf-8')
        create_note(root, args.id, text)
    except FileExistsError:
        parser.exit(1, 'Not overwritten: task note already exists\n')
    except (OSError, ValueError) as error:
        parser.exit(2, f'Cannot create note: {display(error)}\n')
    print(f'Created in selected repository: {display(root / "thoughts" / args.id / "task.md")}')
    print('Next: describe the request and confirm the oracle with Inge.')


if __name__ == '__main__':
    main()
