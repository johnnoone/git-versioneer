from git_versioneer import run
from git_versioneer import cli
from git_versioneer import DEFAULT_BUILD_NUMBER


def test_fresh(fresh):
    version = run(fresh, tag_prefix='v', style='rpm')
    assert version == '0.0.0-%s' % DEFAULT_BUILD_NUMBER

    version = run(fresh, tag_prefix='v', style='rpm', build=42)
    assert version == '0.0.0-42'

    version = run(fresh, 'HEAD', tag_prefix='v', style='rpm')
    assert version == '0.0.0-%s' % DEFAULT_BUILD_NUMBER

    version = run(fresh, 'HEAD', tag_prefix='v', style='rpm', build=42)
    assert version == '0.0.0-42'


def test_clean(clean):
    version = run(clean, tag_prefix='v', style='rpm')
    assert version == '0.0.2-%s' % DEFAULT_BUILD_NUMBER

    version = run(clean, tag_prefix='v', style='rpm', build=42)
    assert version == '0.0.2-42'

    version = run(clean, 'HEAD', tag_prefix='v', style='rpm')
    assert version == '0.0.2-%s' % DEFAULT_BUILD_NUMBER

    version = run(clean, 'HEAD', tag_prefix='v', style='rpm', build=42)
    assert version == '0.0.2-42'


def test_dirty(dirty):
    version = run(dirty, tag_prefix='v', style='rpm')
    assert version == '0.0.1-%s' % DEFAULT_BUILD_NUMBER

    version = run(dirty, 'HEAD', tag_prefix='v', style='rpm')
    assert version == '0.0.1-%s' % DEFAULT_BUILD_NUMBER


def test_prerelease(clean):
    version = run(clean, 'v0.0.1a', tag_prefix='v', style='rpm')
    assert version == '0.0.1-0.%s.a' % DEFAULT_BUILD_NUMBER

    version = run(clean, 'v0.0.1a', tag_prefix='v', style='rpm', build=42)
    assert version == '0.0.1-0.42.a'

    version = run(clean, 'v0.0.1b', tag_prefix='v', style='rpm')
    assert version == '0.0.1-0.%s.b' % DEFAULT_BUILD_NUMBER

    version = run(clean, 'v0.0.1b', tag_prefix='v', style='rpm', build=42)
    assert version == '0.0.1-0.42.b'

    version = run(clean, 'v0.0.1pre', tag_prefix='v', style='rpm')
    assert version == '0.0.1-0.%s.pre' % DEFAULT_BUILD_NUMBER

    version = run(clean, 'v0.0.1pre', tag_prefix='v', style='rpm', build=42)
    assert version == '0.0.1-0.42.pre'

    version = run(clean, 'v0.0.1rc', tag_prefix='v', style='rpm')
    assert version == '0.0.1-0.%s.rc' % DEFAULT_BUILD_NUMBER

    version = run(clean, 'v0.0.1rc', tag_prefix='v', style='rpm', build=42)
    assert version == '0.0.1-0.42.rc'
