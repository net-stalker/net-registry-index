import os
import toml

# TODO: write unit tests
def get_registry_ignore(manifest_dir):
    path_reg_ignore = os.path.join(manifest_dir, '.registryignore')
    res = []
    with open(path_reg_ignore, 'r') as file_reg_ignore:
        for line in file_reg_ignore:
            line = line.strip()
            res.append(line)
    return res

def get_workspace_members(manifest_dir):
    cargo_toml_path = os.path.join(manifest_dir, "Cargo.toml") 
    with open(cargo_toml_path, 'r') as f:
        cargo_toml = toml.load(f)
        return cargo_toml['workspace']['members']

def filter_workspace_members_by_ignored(workspace_members, ignored_members):
    return [member for member in workspace_members if member not in ignored_members]