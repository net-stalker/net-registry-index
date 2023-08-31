#!/usr/bin/env python
"""Modifier of the versions of cargo worspace members"""
# pylint: disable=unspecified-encoding
import sys
import os
import re
import toml
from core import get_registry_ignore, get_workspace_members, filter_workspace_members_by_ignored

def append_prerelease_to_cargo_version(file_path, commit_hash):
    """A function for appending prereleases to cargo version"""
    with open(file_path, 'r') as f:
        cargo_toml = toml.load(f)

    pattern = r'(-\w+)'
    prefix = re.split(pattern, cargo_toml['package']['version'], maxsplit=1)[0]
    cargo_toml['package']['version'] = prefix + '-' + commit_hash

    with open(file_path, 'w') as f:
        toml.dump(cargo_toml, f)

    print(f"Modified version in {file_path} to {commit_hash}")

def modify_cargo_tomls(members_workspace_dirs, new_version, version_modifier):
    """A function which modifies cargo tomls usiong a given callback"""
    for member in members_workspace_dirs:
        version_modifier(os.path.join(member, "Cargo.toml"), new_version)

def main():
    """Main function"""
    args = sys.argv[1:]
    if len(args) != 2:
        raise RuntimeError("wrong number of args. 2 is required")
    manifest_dir = args[0]
    commit_hash = args[1]

    ignored_members = get_registry_ignore(manifest_dir)
    workspace_members = get_workspace_members(manifest_dir)
    filtered_members = filter_workspace_members_by_ignored(workspace_members, ignored_members)
    members_workspace_dirs = list(map(
        lambda crate: os.path.join(manifest_dir, crate),
        filtered_members
    ))
    modify_cargo_tomls(members_workspace_dirs, commit_hash, append_prerelease_to_cargo_version)

if __name__ == "__main__":
    main()
