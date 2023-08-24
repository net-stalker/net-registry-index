#!/usr/bin/env python
import os
import sys
import re
import toml

def get_ignored_members(manifest_dir):
    registry_ignore = os.path.join(manifest_dir, ".registryignore")
    ignored_members = []
    with open(registry_ignore, 'r') as file:
        for line in file:
            ignored_members.append(line.strip())
    return ignored_members

def get_workspace_members(manifest_dir):
    cargo_toml_path = os.path.join(manifest_dir, "Cargo.toml") 
    with open(cargo_toml_path, 'r') as f:
        cargo_toml = toml.load(f)
        return cargo_toml['workspace']['members']

def filter_workspace_members_by_ignored(workspace_members, ignored_members):
    return [member for member in workspace_members if member not in ignored_members]   

def get_versions_from_toml(manifest_dir, workspace_members):
    versions = []
    for member in [os.path.join(manifest_dir, member) for member in workspace_members]:
        path_cargo_toml = os.path.join(member, "Cargo.toml")
        with open(path_cargo_toml, 'r') as f:
            cargo_toml = toml.load(f)
            versions.append(cargo_toml['package']['version'])
    return versions

def get_current_version_from_changelog(manifest_dir):
    changelog_path = os.path.join(manifest_dir, "CHANGELOG.md")
    ans = ''
    with open(changelog_path, 'r') as changelog:
        pattern = r"\[\d+.\d+.\d+\]"
        prog = re.compile(pattern)
        for line in changelog:
            res = prog.search(line)
            if res == None:
                continue
            res = res.group()
            ans = res[1:len(res) - 1]
            break
    
    return ans

def get_a_new_tag(members_versions, current_version):
    if not all(version == members_versions[0] for version in members_versions):
        raise RuntimeError("The versions of the workspace members aren't equal")
    
    if current_version == '':
        return members_versions[0]
            
    new_version_splitted = members_versions[0].split('.')
    current_version_splitted = current_version.split('.')
    for i in range(0, len(new_version_splitted)):
        if int(current_version_splitted[i]) > int(new_version_splitted[i]):
            raise RuntimeError("A new version is smaller than the current one")
        if int(current_version_splitted[i]) < int(new_version_splitted[i]):
            return members_versions[0]        
    raise RuntimeError("A new version is equal to the current one")
    
def main():
    args = sys.argv[1:]
    if len(args) != 1:
        raise RuntimeError("wrong number of args. 1 is required")
    manifest_dir = args[0]
    ignored_members = get_ignored_members(manifest_dir)
    workspace_members = get_workspace_members(manifest_dir)
    filtered_members = filter_workspace_members_by_ignored(workspace_members, ignored_members)
    current_version = get_current_version_from_changelog(manifest_dir)
    versions = get_versions_from_toml(manifest_dir, filtered_members)
    print(get_a_new_tag(versions, current_version))


if __name__ == "__main__":
    main()
