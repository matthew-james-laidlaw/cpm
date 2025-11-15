from tempfile import TemporaryDirectory
import pytest
from cpm.cli import main
from pathlib import Path
import subprocess

@pytest.fixture
def workdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path

@pytest.fixture
def new_project(workdir, monkeypatch):
    def create(name):
        main(['new', name])
        project_dir = workdir / name
        monkeypatch.chdir(project_dir)
        return project_dir
    return create

def build_project(release=False):
    args = ['build']
    if release:
        args.append('--release')
    main(args)

def exe_path(project_dir, config):
    return project_dir / 'build' / 'bin' / config / f'{project_dir.name}.exe'

def run_exe(exe):
    result = subprocess.run(
        [str(exe)],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

def describe_build():

    def it_builds_debug_executable_by_default(new_project):
        project = new_project('test')
        build_project()
        exe = exe_path(project, "Debug")
        assert exe.exists()
        assert run_exe(exe) == "Hello, test! [Debug]"

    def it_builds_release_executable_if_requested(new_project):
        project = new_project('test')
        build_project(release=True)
        exe = exe_path(project, "Release")
        assert exe.exists()
        assert run_exe(exe) == "Hello, test! [Release]"

    def it_rebuilds_executable_if_sources_changed(new_project):
        project = new_project('test')
        build_project()
        exe = exe_path(project, "Debug")
        orig_time = exe.stat().st_mtime

        # touch main.cpp
        src = project / 'main.cpp'
        src.write_text(src.read_text() + "\n")

        build_project()
        new_time = exe.stat().st_mtime
        assert new_time > orig_time

    def it_skips_rebuild_if_sources_unchanged(new_project):
        project = new_project('test')
        build_project()
        exe = exe_path(project, "Debug")
        orig_time = exe.stat().st_mtime

        build_project()
        new_time = exe.stat().st_mtime
        assert new_time == orig_time

    def it_reconfigures_project_if_cmake_changed(new_project):
        project = new_project('test')
        build_project()
        exe = exe_path(project, "Debug")
        orig_time = exe.stat().st_mtime

        # touch the CMakeLists file
        cmake = project / 'CMakeLists.txt'
        cmake.write_text(cmake.read_text() + "\n# change\n")

        build_project()
        new_time = exe.stat().st_mtime
        assert new_time > orig_time

    def it_skips_reconfigure_if_cmake_unchanged(new_project):
        project = new_project('test')
        build_project()
        exe = exe_path(project, "Debug")

        orig_time = exe.stat().st_mtime
        build_project()
        new_time = exe.stat().st_mtime

        assert new_time == orig_time
