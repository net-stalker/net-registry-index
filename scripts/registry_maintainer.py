#!/usr/bin/env python
"""Module providing methods for cargo registry maintenance"""
# pylint: disable=unspecified-encoding

import sys
import os
import subprocess
import json

def cargo_index(packages, name):
    """Function for getting crates metadata using cargo index"""
    path = str(os.path.join(packages, name))
    cmd = 'cargo index metadata --crate ' + path + ' --index-url url | grep "{*}"'
    return cmd

def get_metainfo(packages):
    """Function for getting metainfo for all the packages in manifest/target/package"""
    ans = {}
    for package in os.listdir(packages):
        if not package.endswith(".crate"):
            continue
        cargo = cargo_index(packages, package)
        metainfo = subprocess.run(
            cargo,
            shell=True,
            capture_output=True,
            text=True,
            check=False).stdout
        json_metainfo = json.loads(metainfo)
        name = json_metainfo['name']
        ans[name] = [package, metainfo]
    return ans

def update_or_create_index(metainfo, registry):
    """Function for creating coresponding direcotries in rust registries"""
    for name, meta in metainfo.items():
        dir_name = ""
        if len(name) <= 3:
            directory = os.path.join(registry, str(len(name)))
            try:
                os.mkdir(directory)
            except FileExistsError as error:
                print(f"{error}")
            dir_name = str(directory)
        else:
            child_dir  = os.path.join(registry, name[:2], name[2:4])
            try:
                os.makedirs(child_dir)
            except FileExistsError as error:
                print(f"{error}")
            dir_name = str(child_dir)
        file_path = os.path.join(dir_name, name)
        with open(file_path, "a") as json_file:
            json.dump(json.loads(meta[1]), json_file, separators=(",", ":"))
            json_file.write("\n")

def move_crate_binaries(packages, metainfo, registry):
    """Function for moving crates to registry"""
    crates = os.path.join(registry, 'crates')
    for name, meta in metainfo.items():
        crate = os.path.join(crates, name)
        try:
            os.makedirs(crate)
        except FileExistsError as error:
            print(f"{error}")
        crate = os.path.join(crate, json.loads(meta[1])['vers'])
        crate = os.path.join(crate, 'download')
        try:
            os.makedirs(crate)
        except FileExistsError as error:
            print(f"{error}")
        target = str(os.path.join(packages, meta[0]))
        print(target)
        print(str(crate))
        cmd = f'mv {target} {str(crate)}'
        subprocess.run(cmd, shell=True, check=False)

def main():
    """Main function"""
    args = sys.argv[1:]
    if len(args) != 2:
        raise RuntimeError("wrong number of args. 2 is required")
    packages = args[0]
    registry = args[1]

    metainfo = get_metainfo(packages)
    update_or_create_index(metainfo, registry)
    move_crate_binaries(packages, metainfo, registry)

if __name__ == "__main__":
    main()
