#!/usr/bin/env python
import sys
import toml
import os

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

def get_current_version(manifest_dir, workspace_members):
    if len(workspace_members) == 0:
        raise RuntimeError("0 members to be published")
    member = os.path.join(manifest_dir, workspace_members[0])
    with open(os.path.join(member, "Cargo.toml"), 'r') as f:
        cargo_toml = toml.load(f)
        return cargo_toml['package']['version']

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        raise RuntimeError("wrong number of args. 1 is required")
    manifest_dir = args[0]
    ignored_members = get_ignored_members(manifest_dir)
    workspace_members = get_workspace_members(manifest_dir)
    filtered_members = filter_workspace_members_by_ignored(workspace_members, ignored_members)
    print(get_current_version(manifest_dir, filtered_members))

if __name__ == "__main__":
    main()