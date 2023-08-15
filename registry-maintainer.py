import os
import subprocess
import json

packages = os.environ.get("PACKAGES_DIR")
registry = os.environ.get("REGISTRY")

def cargo_index(name):
    path = str(os.path.join(packages, name))
    cmd = 'cargo index metadata --crate ' + path + ' --index-url url | grep "{*}"'
    return cmd

def get_metainfo(directory):
    ans = {}
    files = os.listdir(directory)
    for file in files:
        if not file.endswith(".crate"):
            continue
        cargo = cargo_index(file)
        metainfo = subprocess.run(cargo, shell=True, capture_output=True, text=True).stdout
        json_metainfo = json.loads(metainfo)
        name = json_metainfo['name']
        ans[name] = [file, metainfo]
    return ans

def update_or_create_index(metainfo):
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
        with open(file_path, "w") as json_file:
            json.dump(json.loads(meta[1]), json_file, separators=(",", ":"))

def move_crate_binaries(metainfo):
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
    

metainfo = get_metainfo(packages)
update_or_create_index(metainfo)
move_crate_binaries(metainfo)

