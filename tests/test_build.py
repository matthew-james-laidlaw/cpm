from tempfile import TemporaryDirectory
import pytest
from cpm.cli import main
from pathlib import Path
import subprocess

@pytest.fixture
def tmpdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path

def describe_build():

    def it_builds_debug_executable_by_default(tmpdir, monkeypatch):
        main(['new', 'test'])
        monkeypatch.chdir('test')
        main(['build'])

        exe = tmpdir / 'test' / 'build' / 'bin' / 'Debug' / 'test.exe'
        assert exe.exists()

        result = subprocess.run(
            [str(exe)],
            capture_output=True,
            text=True,
            check=True
        )

        stdout = result.stdout.strip()
        assert stdout == 'Hello, test! [Debug]'

    def it_builds_release_executable_if_requested(tmpdir, monkeypatch):
        main(['new', 'test'])
        monkeypatch.chdir('test')
        main(['build', '--release'])

        exe = tmpdir / 'test' / 'build' / 'bin' / 'Release' / 'test.exe'
        assert exe.exists()

        result = subprocess.run(
            [str(exe)],
            capture_output=True,
            text=True,
            check=True
        )

        stdout = result.stdout.strip()
        assert stdout == 'Hello, test! [Release]'
