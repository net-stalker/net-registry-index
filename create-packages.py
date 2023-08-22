#!/usr/bin/env python
import os
import subprocess
import toml
import sys

def get_registry_ignore(manifest_dir):
    path_reg_ignore = os.path.join(manifest_dir, '.registryignore')
    res = []
    try:
        with open(path_reg_ignore, 'r') as file_reg_ignore:
            for line in file_reg_ignore:
                line = line.strip()
                res.append(line)
    except:
        print(f'')
    return res

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
