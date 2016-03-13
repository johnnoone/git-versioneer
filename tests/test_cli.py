from git_versioneer import run
from git_versioneer import cli
import pytest


@pytest.mark.parametrize("args, validate", [
    (['--', 'foobar'], lambda x: x.description == 'foobar'),
    (['--directory', '/foo/bar'], lambda x: x.directory == '/foo/bar'),
    (['--style', 'rpm'], lambda x: x.style == 'rpm'),
])
def test_args(args, validate):
    args, _ = cli.parse_args(args)
    assert validate(args), args
