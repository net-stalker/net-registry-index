# pylint: disable=unspecified-encoding
"""Module proving core functions for scripts for registry maintenance"""
import os
import toml

def get_registry_ignore(manifest_dir):
    """Get ignored members in cargo manifest"""
    path_reg_ignore = os.path.join(manifest_dir, '.registryignore')
    res = []
    with open(path_reg_ignore, 'r') as file_reg_ignore:
        for line in file_reg_ignore:
            line = line.strip()
            res.append(line)
    return res

def get_workspace_members(manifest_dir):
    """Get all the workspace members in cargo manifest including ignored ones"""
    cargo_toml_path = os.path.join(manifest_dir, "Cargo.toml")
    with open(cargo_toml_path, 'r') as file:
        cargo_toml = toml.load(file)
        return cargo_toml['workspace']['members']

def filter_workspace_members_by_ignored(workspace_members, ignored_members):
    """Filter actual workspace members from ignored workspace ones"""
    return [member for member in workspace_members if member not in ignored_members]
