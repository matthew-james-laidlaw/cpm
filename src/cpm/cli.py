import argparse
from cpm.commands import new, build, run

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
    subcommand_new.set_defaults(func=new.handle)

    subcommand_build = subparsers.add_parser(
        name='build',
        help='Build this project',
        description='Build this project'
    )

    subcommand_build.add_argument('--release', help='Build with release flags', action='store_true')
    subcommand_build.set_defaults(func=build.handle)

    subcommand_run = subparsers.add_parser(
        name='run',
        help='Run this project',
        description='Run this project'
    )

    subcommand_run.add_argument('--release', help='Build with release flags', action='store_true')
    subcommand_run.set_defaults(func=run.handle)

    args = parser.parse_args()
    args.func(args)
