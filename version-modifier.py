import os
import toml
import re

commit_hash = str(os.environ.get("SHORT_COMMIT_HASH"))
manifest_dir = str(os.environ.get("CARGO_MANIFEST_DIR"))

def modify_cargo_toml_version(file_path, commit_hash):
    with open(file_path, 'r') as f:
        cargo_toml = toml.load(f)

    pattern = r'(-\w+)'
    prefix = re.split(pattern, cargo_toml['package']['version'], maxsplit=1)[0]
    cargo_toml['package']['version'] = prefix + '-' + commit_hash
    
    with open(file_path, 'w') as f:
        toml.dump(cargo_toml, f)
    
    print(f"Modified version in {file_path} to {commit_hash}")

def modify_members_versions(workspace_members, new_version):
    for member in workspace_members:
        modify_cargo_toml_version(os.path.join(member, "Cargo.toml"), new_version)

def get_workspace_members(file_path):
    try:
        with open(file_path, 'r') as f:
            cargo_toml = toml.load(f)

        return cargo_toml['workspace']['members']
    except Exception as e:
        print(f"Error modifying {file_path}: {e}")

def get_workspace_members_directories(root_directory):
    files = os.listdir(root_directory)
    if 'Cargo.toml' not in files:
        raise Exception("No Cargo.toml in root directory")
    return list(map(
        lambda crate: os.path.join(root_directory, crate),
        get_workspace_members(os.path.join(root_directory, 'Cargo.toml'))
    ))
    
    

workspace_members = get_workspace_members_directories(manifest_dir)
modify_members_versions(workspace_members, commit_hash)
