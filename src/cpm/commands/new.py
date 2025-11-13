from pathlib import Path
from cookiecutter.main import cookiecutter
from importlib.resources import files
import subprocess

def configure(source_dir):
    project_dir = Path(source_dir)
    build_dir = project_dir / 'build'
    subprocess.run(['cmake', '-S', str(project_dir), '-B', str(build_dir), '-G', 'Ninja Multi-Config'])

def handle(args):
    template_dir = files("cpm").joinpath("templates/main")
    cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context={
            'project_name': args.name
        }
    )
    configure(args.name)
