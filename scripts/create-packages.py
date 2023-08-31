#!/usr/bin/env python
import subprocess
import sys
from core import get_registry_ignore

# TODO: import core module
def create_packages(ignored_packages):
    cmd = "cargo package --allow-dirty --workspace"
    old_len = len(cmd)
    for package in ignored_packages:
        cmd += ' --exclude ' + package
    if old_len == len(cmd):
        cmd = "cargo package --allow-dirty"
    subprocess.run(cmd, shell=True)
    

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        raise RuntimeError("wrong number of args. 1 is required")
    manifest_dir = args[0]
    ignored_packages = get_registry_ignore(manifest_dir)
    create_packages(ignored_packages)

if __name__ == "__main__":
    main()
