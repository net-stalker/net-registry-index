#!/usr/bin/env python
import sys
import os
import subprocess
import json

def cargo_index(packages, name):
    path = str(os.path.join(packages, name))
    cmd = 'cargo index metadata --crate ' + path + ' --index-url url | grep "{*}"'
    return cmd

def get_metainfo(packages):
    ans = {}
    files = os.listdir(packages)
    for package in os.listdir(packages):
        if not package.endswith(".crate"):
            continue
        cargo = cargo_index(packages, package)
        metainfo = subprocess.run(cargo, shell=True, capture_output=True, text=True).stdout
        json_metainfo = json.loads(metainfo)
        name = json_metainfo['name']
        ans[name] = [package, metainfo]
    return ans

def update_or_create_index(metainfo, registry):
    for name, meta in metainfo.items():
        dir_name = ""
        if len(name) <= 3:
            directory = os.path.join(registry, str(len(name)))
            try:
                os.mkdir(directory)
            except FileExistsError as e:
                print(f"{e}")
            dir_name = str(directory)
        else:
            parent_dir = os.path.join(registry, name[:2])
            child_dir = os.path.join(parent_dir, name[2:4])
            try:
                os.makedirs(child_dir)
            except FileExistsError as e:
                print(f"{e}")
            dir_name = str(child_dir)
        file_path = os.path.join(dir_name, name)
        with open(file_path, "a") as json_file:
            json.dump(json.loads(meta[1]), json_file, separators=(",", ":"))
            json_file.write("\n")

def move_crate_binaries(packages, metainfo, registry):
    crates = os.path.join(registry, 'crates')
    for name, meta in metainfo.items():
        crate = os.path.join(crates, name)
        try:
            os.makedirs(crate)
        except FileExistsError as e:
            print(f"{e}")
        crate = os.path.join(crate, json.loads(meta[1])['vers'])
        crate = os.path.join(crate, 'download')
        try:
            os.makedirs(crate)
        except FileExistsError as e:
            print(f"{e}")
        target = str(os.path.join(packages, meta[0]))
        print(target)
        print(str(crate))
        cmd = f'mv {target} {str(crate)}'
        subprocess.run(cmd, shell=True)
    
def main():
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
