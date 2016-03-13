#!/usr/bin/env python

import re
import subprocess
from .cli import parse_args
from .const import DEFAULT_BUILD_NUMBER, DEFAULT_STYLE
from ._version import get_versions

__all__ = ['run', 'DEFAULT_BUILD_NUMBER', 'DEFAULT_STYLE']
__version__ = get_versions()['version']
del get_versions


def shell(*args, **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    if args and isinstance(args[0], str):
        kwargs.setdefault('shell', True)
    proc = subprocess.Popen(*args, **kwargs)
    stdout, stderr = proc.communicate()
    return proc, stdout, stderr


class Parser(object):

    def __init__(self, tag_prefix):
        self.tag_prefix = tag_prefix

    def from_git(self, directory, ref):
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

        description = stdout.strip().decode('utf-8')
        # in the format: TAG-DISTANCE-gSHORT
        pieces = self.parse_description(description)

        # in the format: SHORT
        if not pieces['short']:
            # in the format: SHORT
            cmd = ['git', 'rev-list', 'HEAD', '--count']
            proc, stdout, stderr = shell(cmd, cwd=directory)
            pieces['short'] = description
            pieces['distance'] = int(stdout.strip().decode('utf-8'))
        return pieces

    def from_description(self, description):
        pieces = self.parse_description(description)
        if not pieces['short']:
            pieces['short'] = description
        return pieces

    def parse_description(self, description):
        """Parse git-describe output.

        Parameters:
            description (str): in the format: TAG-DISTANCE-gSHORT
        Returns:
            dict: parsed pieces

        """
        pieces = {
            'dirty': False,
            'distance': None,
            'short': None
        }
        if description.endswith('-dirty'):
            description = description[:-6]
            pieces['dirty'] = True
        if '-g' in description:
            # in the format: TAG-DISTANCE-gSHORT
            a, b, c = description.rsplit('-', 2)
            if a.startswith(self.tag_prefix):
                pieces['closest-tag'] = a[len(self.tag_prefix):]
            pieces['distance'] = int(b)
            pieces['short'] = c[1:]
        return pieces


def parse(directory, ref, tag_prefix, description=None):
    parser = Parser(tag_prefix)
    if description:
        return parser.from_description(description)
    return parser.from_git(directory, ref)


def render_pep440(pieces, opts):
    rendered = pieces.get('closest-tag', '0+untagged')
    if pieces["distance"] or pieces["dirty"]:
        rendered += '.' if '+' in rendered else '+'
        rendered += '%d.g%s' % (pieces['distance'], pieces['short'])
        if pieces['dirty']:
            rendered += '.dirty'
    return rendered


def render_rpm(pieces, opts):
    version = None
    release = None
    build = opts.get('build', DEFAULT_BUILD_NUMBER)
    distribution = opts.get('distribution')

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


def run(directory, ref=None, tag_prefix=None, style=None,
        description=None, **opts):
    pieces = parse(directory, ref, tag_prefix or '', description=description)
    if style == 'rpm':
        return render_rpm(pieces, opts)
    return render_pep440(pieces, opts)


def main():
    try:
        args, parser = parse_args()
        kwargs = {
            'directory': args.directory,
            'ref': args.ref,
            'tag_prefix': args.tag_prefix,
            'build': args.build,
            'style': args.style,
            'description': args.description
        }
        version = run(**kwargs)
    except Exception as error:
        parser.error(error)
    print(version)
