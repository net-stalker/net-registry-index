#!/usr/bin/env python
"""Module providing method for packaging workspace members"""
import subprocess
import sys
import os
from core import get_registry_ignore

def create_packages(manifest_dir, ignored_members):
    """Function for packaging workspace members except ignored ones"""
    manifest_dir = os.path.join(manifest_dir, "Cargo.toml")
    cmd = "cargo package --manifest-path " + manifest_dir + " --allow-dirty --workspace"
    old_len = len(cmd)
    for package in ignored_members:
        cmd += ' --exclude ' + package
    if old_len == len(cmd):
        cmd = "cargo package --manifest-path " + manifest_dir + " --allow-dirty"
    subprocess.run(cmd, shell=True, check=False)


def main():
    """Main function"""
    args = sys.argv[1:]
    if len(args) != 1:
        raise RuntimeError("wrong number of args. 1 is required")
    manifest_dir = args[0]
    ignored_packages = get_registry_ignore(manifest_dir)
    create_packages(manifest_dir, ignored_packages)

if __name__ == "__main__":
    main()
