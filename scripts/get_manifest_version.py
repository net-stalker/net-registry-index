#!/usr/bin/env python
# pylint: disable=unspecified-encoding,duplicate-code
"""Module providing a method for getting manifest version
in Cargo.toml of one of the manifest members using workspace members and cargo manifest direcotry"""
import sys
import os
import toml
from core import get_registry_ignore, get_workspace_members, filter_workspace_members_by_ignored


def get_current_version(manifest_dir, workspace_members):
    """
    Get cargo manifest version from workscpace members.
    Workspace members are supposed to have the same versions.
    """
    if len(workspace_members) == 0:
        raise RuntimeError("0 members to be published")
    member = os.path.join(manifest_dir, workspace_members[0])
    with open(os.path.join(member, "Cargo.toml"), 'r') as file:
        cargo_toml = toml.load(file)
        return cargo_toml['package']['version']


def main():
    """Main function"""
    args = sys.argv[1:]
    if len(args) != 1:
        raise RuntimeError("wrong number of args. 1 is required")
    manifest_dir = args[0]
    ignored_members = get_registry_ignore(manifest_dir)
    workspace_members = get_workspace_members(manifest_dir)
    filtered_members = filter_workspace_members_by_ignored(
        workspace_members, ignored_members)
    print(get_current_version(manifest_dir, filtered_members))


if __name__ == "__main__":
    main()
