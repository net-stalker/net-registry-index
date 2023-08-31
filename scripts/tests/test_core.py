"""Module providing unit tests for core.py"""
# pylint: disable=wrong-import-position
import sys
import unittest
import os

cur_dir = os.path.dirname(__file__)
core_module_dir = os.path.join(cur_dir, '..')
sys.path.append(core_module_dir)

from core import get_registry_ignore, get_workspace_members, filter_workspace_members_by_ignored

CARGO_MANIFEST_DIR = os.path.join(cur_dir, "rust-test-workspace")

class TestCore(unittest.TestCase):
    """Class providing unit tests for core.py"""
    def test_get_registry_ignore_0(self):
        """Test for get_registry_ignore with .registryignore-0 file"""

        expected = []
        registry_ignore_0 = os.path.join(CARGO_MANIFEST_DIR, '.registryignore-0')
        registry_ignore = os.path.join(CARGO_MANIFEST_DIR, '.registryignore')
        os.rename(registry_ignore_0, registry_ignore)
        ignored_members = get_registry_ignore(CARGO_MANIFEST_DIR)
        os.rename(registry_ignore, registry_ignore_0)
        self.assertEqual(expected, ignored_members, f"Should be {expected}")

    def test_get_registry_ignore_1(self):
        """Test for get_registry_ignore with .registryignore-1 file"""

        expected = ['first']
        registry_ignore_1 = os.path.join(CARGO_MANIFEST_DIR, '.registryignore-1')
        registry_ignore = os.path.join(CARGO_MANIFEST_DIR, '.registryignore')
        os.rename(registry_ignore_1, registry_ignore)
        ignored_members = get_registry_ignore(CARGO_MANIFEST_DIR)
        os.rename(registry_ignore, registry_ignore_1)
        self.assertEqual(expected, ignored_members, f"Should be {expected}")

    def test_get_registry_ignore_all(self):
        """Test for get_registry_ignore with .registryignore-all file"""

        expected = ['first', 'second', 'third']
        registry_ignore_all = os.path.join(CARGO_MANIFEST_DIR, '.registryignore-all')
        registry_ignore = os.path.join(CARGO_MANIFEST_DIR, '.registryignore')
        os.rename(registry_ignore_all, registry_ignore)
        ignored_members = get_registry_ignore(CARGO_MANIFEST_DIR)
        os.rename(registry_ignore, registry_ignore_all)
        self.assertEqual(expected, ignored_members, f"Should be {expected}")

    def test_get_workspace_members(self):
        """Test for get_workspace_members"""

        expected = ['first', 'second', 'third']
        workspace_members = get_workspace_members(CARGO_MANIFEST_DIR)
        self.assertEqual(expected, workspace_members, f"Should be {expected}")

    def test_filter_workspace_members_by_ignored_0(self):
        """Test for get_registry_ignore with .registryignore-0 file"""

        expected = ['first', 'second', 'third']
        registry_ignore_0 = os.path.join(CARGO_MANIFEST_DIR, '.registryignore-0')
        registry_ignore = os.path.join(CARGO_MANIFEST_DIR, '.registryignore')
        os.rename(registry_ignore_0, registry_ignore)
        ignored_members = get_registry_ignore(CARGO_MANIFEST_DIR)
        os.rename(registry_ignore, registry_ignore_0)
        workspace_members = get_workspace_members(CARGO_MANIFEST_DIR)
        filtered_workspace_members = filter_workspace_members_by_ignored(workspace_members,
                                                                          ignored_members)
        self.assertEqual(expected, filtered_workspace_members, f"Should be {expected}")

    def test_filter_workspace_members_by_ignored_1(self):
        """Test for get_registry_ignore with .registryignore-1 file"""

        expected = ['second', 'third']
        registry_ignore_1 = os.path.join(CARGO_MANIFEST_DIR, '.registryignore-1')
        registry_ignore = os.path.join(CARGO_MANIFEST_DIR, '.registryignore')
        os.rename(registry_ignore_1, registry_ignore)
        ignored_members = get_registry_ignore(CARGO_MANIFEST_DIR)
        os.rename(registry_ignore, registry_ignore_1)
        workspace_members = get_workspace_members(CARGO_MANIFEST_DIR)
        filtered_workspace_members = filter_workspace_members_by_ignored(workspace_members,
                                                                         ignored_members)
        self.assertEqual(expected, filtered_workspace_members, f"Should be {expected}")

    def test_filter_workspace_members_by_ignored_all(self):
        """Test for get_registry_ignore with .registryignore-all file"""

        expected = []
        registry_ignore_all = os.path.join(CARGO_MANIFEST_DIR, '.registryignore-all')
        registry_ignore = os.path.join(CARGO_MANIFEST_DIR, '.registryignore')
        os.rename(registry_ignore_all, registry_ignore)
        ignored_members = get_registry_ignore(CARGO_MANIFEST_DIR)
        os.rename(registry_ignore, registry_ignore_all)
        workspace_members = get_workspace_members(CARGO_MANIFEST_DIR)
        filtered_workspace_members = filter_workspace_members_by_ignored(workspace_members,
                                                                         ignored_members)
        self.assertEqual(expected, filtered_workspace_members, f"Should be {expected}")


if __name__ == '__main__':
    unittest.main()
