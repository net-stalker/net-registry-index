"""Module providing unit tests for core.py"""
# pylint: disable=import-error, wrong-import-position
import sys
import unittest
import os

cur_dir = os.path.dirname(__file__)
core_module_dir = os.path.join(cur_dir, '..')
sys.path.append(core_module_dir)

from core import get_workspace_members
from get_manifest_version import get_current_version

CARGO_MANIFEST_DIR = os.path.join(cur_dir, "rust-test-workspace")

class TestGetManifestVersion(unittest.TestCase):
    """Class providing unit tests for get_manifest_version.py"""
    def test_get_manifest_version(self):
        """Test getting the cargo manigest's version"""
        expected = '0.1.0'
        workspace_members = get_workspace_members(CARGO_MANIFEST_DIR)
        manifest_version = get_current_version(CARGO_MANIFEST_DIR, workspace_members)
        self.assertEqual(expected, manifest_version, f"Should be {expected}")

if __name__ == '__main__':
    unittest.main()
