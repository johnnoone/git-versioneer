#!/usr/bin/env python

import subprocess
import sys


def run(*args, **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    if args and isinstance(args[0], str):
        kwargs.setdefault('shell', True)
    proc = subprocess.Popen(*args, **kwargs)
    stdout, stderr = proc.communicate()
    return proc, stdout, stderr


def parse(ref, directory, config):
    cmd = ['git', 'describe', '--tags', '--always', '--long']
    _, stdout, _ = run('git config core.bare', cwd=directory)
    if 'false' in stdout.decode('utf-8'):
        cmd.append('--dirty')
    if ref:
        cmd.append(ref)
    proc, stdout, stderr = run(cmd, cwd=directory)
    if proc.returncode:
        sys.exit(stderr)
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
        if a.startswith(config.tag_prefix):
            pieces['closest-tag'] = a[len(config.tag_prefix):]
        pieces['distance'] = int(b)
        pieces['short'] = c[1:]
    else:
        # in the format: SHORT
        cmd = ['git', 'rev-list', 'HEAD', '--count']
        proc, stdout, stderr = run(cmd, cwd=directory)
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


def main(ref, directory, config):
    pieces = parse(ref, directory, config)
    return render_pep440(pieces)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='git versioneer',
                                     usage='%(prog)s <commit-ish>',
                                     description='define version number')
    parser.add_argument('ref',
                        help=('Commit-ish object names to describe.\n'
                              'Defaults to HEAD if omitted.'),
                        metavar='commit-ish', nargs='?')
    parser.add_argument('--directory')
    parser.add_argument('--tag-prefix', default='v')
    args = parser.parse_args()
    version = main(args.ref, args.directory, args)
    print(version)
