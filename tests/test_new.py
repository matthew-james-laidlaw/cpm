import os
import tempfile
from pathlib import Path
import argparse
import cpm

def test_integration():
    # Create an isolated temp workspace
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        # Change into the sandbox
        old_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            # 1️⃣ Create a new CPM project
            args = argparse.Namespace(name="demo")
            cpm.handle_new(args)

            project_dir = tmp_path / "demo"
            assert project_dir.exists()
            assert (project_dir / "CMakeLists.txt").exists()

            # 2️⃣ Build the project
            os.chdir(project_dir)  # CMake/Ninja expect this
            cpm.handle_build()
            assert (project_dir / "build").exists()

            # 3️⃣ Run the resulting binary
            cpm.handle_run()

        finally:
            os.chdir(old_cwd)
