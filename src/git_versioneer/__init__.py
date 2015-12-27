#!/usr/bin/env python

import subprocess
from .cli import parse_args

__all__ = ['run']


def shell(*args, **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    if args and isinstance(args[0], str):
        kwargs.setdefault('shell', True)
    proc = subprocess.Popen(*args, **kwargs)
    stdout, stderr = proc.communicate()
    return proc, stdout, stderr


def parse(directory, ref, tag_prefix):
    cmd = ['git', 'describe', '--tags', '--always', '--long']
    if not ref:
        _, stdout, _ = shell('git config core.bare', cwd=directory)
        if 'false' in stdout.decode('utf-8'):
            cmd.append('--dirty')
    else:
        cmd.append(ref)
    proc, stdout, stderr = shell(cmd, cwd=directory)
    if proc.returncode:
        raise Exception(stderr)
    pieces = {
        'dirty': False,
        'distance': None,
        'short': None,
    }

    description = stdout.strip().decode('utf-8')
    if description.endswith('-dirty'):
        description = description[:-6]
        pieces['dirty'] = True
    if '-g' in description:
        # in the format: TAG-DISTANCE-gSHORT
        a, b, c = description.rsplit('-', 2)
        if a.startswith(tag_prefix):
            pieces['closest-tag'] = a[len(tag_prefix):]
        pieces['distance'] = int(b)
        pieces['short'] = c[1:]
    else:
        # in the format: SHORT
        cmd = ['git', 'rev-list', 'HEAD', '--count']
        proc, stdout, stderr = shell(cmd, cwd=directory)
        pieces['short'] = description
        pieces['distance'] = int(stdout.strip().decode('utf-8'))
    return pieces


def render_pep440(pieces):
    rendered = pieces.get('closest-tag', '0+untagged')
    if pieces["distance"] or pieces["dirty"]:
        rendered += '.' if '+' in rendered else '+'
        rendered += '%d.g%s' % (pieces['distance'], pieces['short'])
        if pieces['dirty']:
            rendered += '.dirty'
    return rendered


def run(directory, ref=None, tag_prefix=None):
    pieces = parse(directory, ref, tag_prefix or '')
    return render_pep440(pieces)


def main():
    try:
        args, parser = parse_args()
        version = run(args.directory, args.ref, args)
    except Exception as error:
        parser.error(error)
    print(version)


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
