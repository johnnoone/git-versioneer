import argparse
import sys


class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def parse_args(args=None):
    parser = Parser(prog='git versioneer',
                    usage='%(prog)s <commit-ish>',
                    description='define version number')
    parser.add_argument('ref',
                        help=('Commit-ish object names to describe.\n'
                              'Defaults to HEAD if omitted.'),
                        metavar='commit-ish', nargs='?')
    parser.add_argument('--directory')
    parser.add_argument('--tag-prefix', default='v')
    parser.add_argument('--style', choices=['pep440', 'rpm'], default='pep440')
    parser.add_argument('--rpm', dest='style', action='store_const', const='rpm')
    parser.add_argument('--build', default='${BUILD_NUMBER}', help='in case of rpm')

    args = parser.parse_args(args)
    return args, parser
