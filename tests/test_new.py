from tempfile import TemporaryDirectory
import pytest
from cpm.cli import main
from pathlib import Path

@pytest.fixture
def tmpdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path

def describe_new():

    def it_creates_a_template_project(tmpdir, monkeypatch):
        main(['new', 'test'])
        assert (tmpdir / 'test' / 'CMakeLists.txt').exists()
        assert (tmpdir / 'test' / 'main.cpp').exists()

    def it_fails_if_directory_already_exists(tmpdir, monkeypatch):
        main(['new', 'test'])
        with pytest.raises(Exception):
            main(['new', 'test'])
