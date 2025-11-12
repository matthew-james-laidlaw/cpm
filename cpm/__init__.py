import argparse
from cookiecutter.main import cookiecutter
import subprocess

from pathlib import Path

def get_project_name_from_cache():
    cache_file = Path('build') / 'CMakeCache.txt'
    for line in cache_file.read_text().splitlines():
        if line.startswith('CMAKE_PROJECT_NAME:STATIC='):
            return line.split('=', 1)[1]
    raise RuntimeError('could not find \'CMAKE_PROJECT_NAME\' in CMakeCache.txt')

def handle_new(args):
    template_dir = Path(__file__).parent / 'templates' / 'main'
    cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context={
            'project_name': args.name
        }
    )

def handle_build(args):
    config = 'Release' if args.release else 'Debug'
    subprocess.run(['cmake', '-B', 'build', '-G', 'Ninja Multi-Config'], check=True)
    subprocess.run(['cmake', '--build', 'build', '--config', f'{config}'], check=True)

def handle_run(args):
    config = 'Release' if args.release else 'Debug'
    subprocess.run(['cmake', '--build', 'build', '--config', f'{config}', '--target', 'run'], check=True)

def main():

    parser = argparse.ArgumentParser(
        prog='cpm',
        description='C++ Project Manager'
    )

    subparsers = parser.add_subparsers(
        title='sub-commands',
        metavar='',
    )

    subcommand_new = subparsers.add_parser(
        name='new',
        help='Create a new CPM project',
        description='Create a new CPM project'
    )

    subcommand_new.add_argument('name', help='The project\'s name')
    subcommand_new.set_defaults(func=handle_new)

    subcommand_build = subparsers.add_parser(
        name='build',
        help='Build this project',
        description='Build this project'
    )

    subcommand_build.add_argument('--release', help='Build with release flags', action='store_true')
    subcommand_build.set_defaults(func=handle_build)

    subcommand_run = subparsers.add_parser(
        name='run',
        help='Run this project',
        description='Run this project'
    )

    subcommand_run.add_argument('--release', help='Build with release flags', action='store_true')
    subcommand_run.set_defaults(func=handle_run)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
