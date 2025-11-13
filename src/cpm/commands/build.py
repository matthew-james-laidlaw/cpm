import subprocess

def handle(args):
    config = "Release" if args.release else "Debug"
    subprocess.run(['cmake', '--build', 'build', '--config', config])
