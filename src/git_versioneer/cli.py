import argparse
import sys
import textwrap
from .const import DEFAULT_BUILD_NUMBER, DEFAULT_STYLE


class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def parse_args(args=None):
    usage = '%(prog)s [options] [<commit-ish> | -- <description>]'
    description = textwrap.dedent("""\
    define version number

    If <description> is specified, git versioneer will just parse it.
    Otherwise it will  on the current branch it will find version from
    git-tree <commit-ish>.
    """)

    class Marker(str):
        pass

    try:
        if args and args[-2] == '--':
            args[-1] = Marker(args[-1])
    except IndexError:
        pass

    parser = Parser(prog='git-versioneer',
                    formatter_class=argparse.RawTextHelpFormatter,
                    usage=usage, description=description)
    parser.add_argument('ref',
                        help=('commit-ish object names to describe.\n'
                              'defaults to HEAD if omitted.'),
                        metavar='commit-ish', nargs='?')
    parser.add_argument('description',
                        help=('use this description instead of guessing it\n'
                              'from git-tree <commit-ish>.'),
                        metavar='description', nargs='?')
    parser.add_argument('--directory')
    parser.add_argument('--tag-prefix', default='v',
                        help='set tag prefix. defaults to %(default)s')

    parser.add_argument('--style', choices=['pep440', 'rpm'],
                        default=DEFAULT_STYLE,
                        help='switch between styles. defaults to %(default)s')
    group = parser.add_argument_group('rpm options')
    group.add_argument('--build', default=DEFAULT_BUILD_NUMBER,
                       help='build placeholder. defaults to %(default)s')

    args = parser.parse_args(args)
    if isinstance(args.ref, Marker):
        args.description, args.ref = str(args.ref), None
    elif args.ref and args.description:
        parser.error('Git reference and description are mutually exclusive')
    return args, parser
