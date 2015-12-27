import os.path
import pytest
import subprocess
import tempfile

here = os.path.dirname(os.path.abspath(__file__))


def shell(cmd, **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    stdout, stderr = proc.communicate()
    return stdout, stderr


def _repo(request, script):
    data_dir = tempfile.mkdtemp()
    shell(['sh', os.path.join(here, script)], cwd=data_dir)

    def fin():
        shell(['rm', '-rf', data_dir])
    request.addfinalizer(fin)
    return data_dir


@pytest.fixture(scope='function')
def fresh(request):
    return _repo(request, 'fresh.sh')


@pytest.fixture(scope='function')
def clean(request):
    return _repo(request, 'clean.sh')


@pytest.fixture(scope='function')
def dirty(request):
    return _repo(request, 'dirty.sh')
