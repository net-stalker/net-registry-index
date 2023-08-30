"""Module providing unit tests for core.py"""
# pylint: disable=unspecified-encoding, import-error, wrong-import-position
import sys
import unittest
import os
import toml

cur_dir = os.path.dirname(__file__)
core_module_dir = os.path.join(cur_dir, '..')
sys.path.append(core_module_dir)

from core import get_workspace_members
from version_modifier import modify_cargo_tomls, append_prerelease_to_cargo_version
from get_manifest_version import get_current_version

CARGO_MANIFEST_DIR = os.path.join(cur_dir, "rust-test-workspace")

class TestVersionModifier(unittest.TestCase):
    """Class providintg unit tests for get_manifest_version.py"""
    def assert_members_version(self, members_dirs, new_version):
        """Method to assert cargo toml versions"""
        for member in members_dirs:
            with open(str(os.path.join(member, 'Cargo.toml')), 'r') as file:
                cargo_toml = toml.load(file)
                self.assertEqual(
                    cargo_toml['package']['version'],
                    new_version,
                    f"{new_version} as expected as a new version"
                )

    def version_reverter(self, members_dirs, version):
        """Method to revert cargo toml versions"""
        for member in members_dirs:
            with open(str(os.path.join(member, 'Cargo.toml')), 'r') as file:
                cargo_toml = toml.load(file)
                cargo_toml['package']['version'] = version

            with open(str(os.path.join(member, 'Cargo.toml')), 'w') as file:
                toml.dump(cargo_toml, file)

    def test_modify_cargo_tomls(self):
        """Test getting the cargo manigest's version"""
        workspace_members = get_workspace_members(CARGO_MANIFEST_DIR)
        members_workspace_dirs = list(map(
            lambda crate: os.path.join(CARGO_MANIFEST_DIR, crate),
            workspace_members
        ))
        cur_version = get_current_version(CARGO_MANIFEST_DIR, workspace_members)
        prerelease = 'abc'
        modify_cargo_tomls(members_workspace_dirs, prerelease, append_prerelease_to_cargo_version)
        self.assert_members_version(members_workspace_dirs, cur_version + '-' + prerelease)
        self.version_reverter(members_workspace_dirs, cur_version)

if __name__ == '__main__':
    unittest.main()
