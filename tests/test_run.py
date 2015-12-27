from git_versioneer import run
from git_versioneer import cli


def test_fresh(fresh):
    version = run(fresh, tag_prefix='v')
    assert version.startswith('0+untagged.2.g')
    assert not version.endswith('.dirty')

    version = run(fresh, 'HEAD', tag_prefix='v')
    assert version.startswith('0+untagged.2.g')
    assert not version.endswith('.dirty')


def test_clean(clean):
    version = run(clean, tag_prefix='v')
    assert version == '0.0.2'
    assert not version.endswith('.dirty')

    version = run(clean, 'HEAD', tag_prefix='v')
    assert version == '0.0.2'
    assert not version.endswith('.dirty')


def test_dirty(dirty):
    version = run(dirty, tag_prefix='v')
    assert version.startswith('0.0.1+1.g')
    assert version.endswith('.dirty')

    version = run(dirty, 'HEAD', tag_prefix='v')
    assert version.startswith('0.0.1+1.g')
    assert not version.endswith('.dirty')


def test_cli():
    args, _ = cli.parse_args(['--directory', '/foo/bar'])
    assert args.directory == '/foo/bar'
