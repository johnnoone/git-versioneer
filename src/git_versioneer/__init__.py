#!/usr/bin/env python

import re
import subprocess
from .cli import parse_args
from .const import DEFAULT_BUILD_NUMBER

__all__ = ['run', 'DEFAULT_BUILD_NUMBER']


def shell(*args, **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    if args and isinstance(args[0], str):
        kwargs.setdefault('shell', True)
    proc = subprocess.Popen(*args, **kwargs)
    stdout, stderr = proc.communicate()
    return proc, stdout, stderr


def parse(directory, ref, tag_prefix, defaults=None):
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
        'short': None
    }
    pieces.update(defaults or {})

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


def render_rpm(pieces):
    version = None
    release = None
    build = pieces.get('build', DEFAULT_BUILD_NUMBER)
    distribution = pieces.get('distribution')

    full = pieces.get('closest-tag', '0.0.0')
    matches = re.match('(?P<version>\d+\.\d+\.\d+)[.-]?(?P<rel>.+)$', full)
    if matches:
        version, rel = matches.group('version'), matches.group('rel')
        if any(rel.startswith(tag) for tag in ['a', 'b', 'pre', 'rc']):
            release = '0.%s.%s' % (build, rel)
        else:
            release = '%s.%s' % (build, rel)
    else:
        version = full
        release = '%s' % build

    rendered = '%s-%s' % (version, release)

    if distribution:
        rendered += '.%s' % distribution
    return rendered


def run(directory, ref=None, tag_prefix=None, style=None, **defaults):
    pieces = parse(directory, ref, tag_prefix or '', defaults=defaults)
    if style == 'rpm':
        return render_rpm(pieces)
    return render_pep440(pieces)


def main():
    try:
        args, parser = parse_args()
        defaults = {
            'build': args.build
        }
        version = run(args.directory, args.ref, args.tag_prefix, **defaults)
    except Exception as error:
        parser.error(error)
    print(version)


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
