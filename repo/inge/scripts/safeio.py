"""Bounded no-follow filesystem primitives for trusted Inge helper code.

Requires POSIX directory descriptors, O_NOFOLLOW and O_DIRECTORY; unsupported
platforms fail closed. Explicit operator-selected roots may be resolved first.
Every subsequent component is opened without following links. This is not an OS
sandbox: protect directories against privileged moves and untrusted mounts.
"""
from contextlib import contextmanager
import os
from pathlib import Path
import stat
import time

MAX_BYTES = 1024 * 1024
MAX_ENTRIES = 10000


def display(value):
    """Escape controls, surrogates and Unicode formatting characters for one line."""
    return ''.join(c if c.isprintable() else
                   c.encode('unicode_escape').decode('ascii') for c in str(value))


def supported():
    """Fail closed without required no-follow, descriptor-relative operations."""
    if not all(hasattr(os, n) for n in ('O_NOFOLLOW', 'O_DIRECTORY', 'O_NONBLOCK')) or not all(
            f in os.supports_dir_fd for f in (os.open, os.mkdir, os.stat)):
        raise OSError('Safe filesystem operations require POSIX directory descriptors')


@contextmanager
def directory(path):
    """Yield a directory descriptor, opening every absolute path component no-follow.

    Parent traversal is rejected. Handles close on all exits. Missing paths,
    links, non-directories and permission failures raise OSError.
    """
    supported()
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts:
        raise ValueError('Expected absolute path without parent traversal')
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open(path.anchor, flags)
    try:
        for part in path.parts[1:]:
            child = os.open(part, flags, dir_fd=fd)
            os.close(fd)
            fd = child
        yield fd
    finally:
        os.close(fd)


def kind(path):
    """Return file/directory/link/other/missing without following any path link."""
    path = Path(path)
    try:
        with directory(path.parent) as fd:
            mode = os.stat(path.name, dir_fd=fd, follow_symlinks=False).st_mode
    except FileNotFoundError:
        return 'missing'
    return ('link' if stat.S_ISLNK(mode) else 'file' if stat.S_ISREG(mode) else
            'directory' if stat.S_ISDIR(mode) else 'other')


def read_bytes(path, limit=MAX_BYTES):
    """Read a bounded regular file through verified parents and a no-follow open.

    Nonblocking open plus fstat rejects FIFOs/devices before reading. Both initial
    size and chunked-read length are bounded, including concurrent file growth.
    """
    path = Path(path)
    with directory(path.parent) as parent:
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode):
            raise OSError('Refusing non-regular file')
        if info.st_size > limit:
            raise OSError(f'File exceeds {limit} byte inspection limit')
        chunks, count = [], 0
        while True:
            chunk = stream.read(min(65536, limit + 1 - count))
            if not chunk:
                return b''.join(chunks)
            chunks.append(chunk)
            count += len(chunk)
            if count > limit:
                raise OSError(f'File exceeds {limit} byte inspection limit')


class Budget:
    """Cooperative work limit; cannot interrupt a stalled kernel I/O call."""
    def __init__(self, entries=MAX_ENTRIES, seconds=30):
        """Set the shared entry allowance and monotonic inspection deadline."""
        self.remaining = entries
        self.deadline = time.monotonic() + seconds

    def check(self, count=0):
        """Consume entries and raise OSError when coverage must stop."""
        self.remaining -= count
        if self.remaining < 0 or time.monotonic() > self.deadline:
            raise OSError('Inspection budget exceeded; coverage is incomplete')


def entries(path, budget):
    """List bounded immediate (name, kind) pairs using a no-follow directory handle."""
    result = []
    budget.check()
    with directory(path) as fd, os.scandir(fd) as iterator:
        for item in iterator:
            budget.check(1)
            mode = item.stat(follow_symlinks=False).st_mode
            category = ('link' if stat.S_ISLNK(mode) else 'directory' if stat.S_ISDIR(mode)
                        else 'file' if stat.S_ISREG(mode) else 'other')
            result.append((item.name, category))
    return sorted(result)


def files(root, budget):
    """Yield regular files below root; fail visibly on links or special files."""
    pending = [Path(root)]
    while pending:
        here = pending.pop()
        for name, category in entries(here, budget):
            path = here / name
            if category == 'directory':
                if name != '__pycache__':
                    pending.append(path)
            elif category == 'file':
                yield path
            else:
                raise OSError(f'Refusing linked or special path: {display(path)}')
