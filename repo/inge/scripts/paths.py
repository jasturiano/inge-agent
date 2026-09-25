"""Resolve target worktrees independently from an operator-trusted framework.

No implicit local or ancestor framework is accepted. Select --framework or INGE_HOME
from a trusted launcher. These are trust assertions, not signatures: protect the
selected installation from untrusted writers. Discovery removes inherited Git
overrides and checks containment before callers perform writes.
"""
import os
from pathlib import Path
import subprocess
from safeio import kind


def repository(path):
    """Return a verified worktree root or the existing non-Git target.

    Explicit symlinked targets resolve once. Git receives a five-second timeout,
    no inherited GIT_* overrides, disabled optional locks and no global/system configuration. Successful
    output must be an existing ancestor of the requested target. Missing Git or
    nonzero discovery falls back only when no ancestor has a .git marker.
    Invalid targets, timeouts and unrelated roots raise ValueError/OSError.
    PATH and the Python installation remain operator-trusted executable inputs.
    """
    start = Path(path).expanduser().resolve(strict=True)
    if not start.is_dir():
        raise ValueError(f'Repository target is not a directory: {start}')
    marker_root = None
    for parent in (start, *start.parents):
        marker_kind = kind(parent / '.git')
        if marker_kind == 'missing':
            continue
        if marker_kind not in {'file', 'directory'}:
            raise ValueError('Unsafe Git worktree marker; target not selected')
        marker_root = parent
        break
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull, GIT_OPTIONAL_LOCKS='0')
    try:
        result = subprocess.run(['git', '-C', str(start), 'rev-parse', '--show-toplevel'],
                                capture_output=True, text=True, check=False, env=env, timeout=5)
    except FileNotFoundError as error:
        if marker_root is not None:
            raise ValueError('Git is unavailable for an existing checkout; target not selected') from error
        return start
    except subprocess.TimeoutExpired as error:
        raise ValueError('Git discovery timed out; target not selected') from error
    if result.returncode != 0:
        if marker_root is not None:
            raise ValueError('Git discovery failed for an existing checkout; target not selected')
        return start
    candidate = Path(result.stdout.removesuffix('\n'))
    if not candidate.is_absolute():
        raise ValueError('Git returned a non-absolute worktree root')
    candidate = candidate.resolve(strict=True)
    if not candidate.is_dir() or not start.is_relative_to(candidate):
        raise ValueError('Git worktree root does not contain the requested target')
    if marker_root != candidate:
        raise ValueError('Git root disagrees with the nearest worktree marker; refusing redirected target')
    return candidate


def framework(root, explicit=None):
    """Validate one operator-selected framework without local/ancestor fallback.

    root preserves the API's distinction from the target. explicit wins over
    INGE_HOME; neither may be inferred from repository content. An explicitly
    selected root symlink resolves once; linked core files/subdirectories are
    rejected. Missing selection/incomplete kits raise ValueError, unsafe paths
    OSError. Presence checks do not authenticate a revision or its author.
    """
    selected = explicit or os.environ.get('INGE_HOME')
    if not selected:
        raise ValueError('Framework trust required: select --framework or set INGE_HOME in a trusted launcher')
    candidate = Path(selected).expanduser().resolve()
    for name in ['BOOTSTRAP.md', 'SOUL.md', 'WORKFLOW.md', 'references/routing.md',
                 'adapters/generic.md', 'adapters/opencode.md', 'templates/task.md']:
        if kind(candidate / name) != 'file':
            raise ValueError(f'Incomplete framework or unsafe linked file: {candidate / name}')
    return candidate
