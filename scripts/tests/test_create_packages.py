"""Module providing unit tests for core.py"""
# pylint: disable=import-error, wrong-import-position,duplicate-code
import sys
import unittest
import os
import shutil

cur_dir = os.path.dirname(__file__)
core_module_dir = os.path.join(cur_dir, '..')
sys.path.append(core_module_dir)

from core import get_registry_ignore
from create_packages import create_packages

CARGO_MANIFEST_DIR = os.path.join(cur_dir, "rust-test-workspace")

class TestCreatePackages(unittest.TestCase):
    """Class providing unit tests for get_manifest_version.py"""
    def assert_created_packages(self, expected):
        """Function for assertion newly created packages"""
        packages = os.path.join(CARGO_MANIFEST_DIR, 'target', 'package')
        amount_of_packages = 0
        for package in os.listdir(packages):
            if not package.endswith(".crate"):
                continue
            amount_of_packages += 1
            self.assertIn(package, expected, f"{package} isn't in packages")
        self.assertEqual(
            len(expected),
            amount_of_packages,
            f"{len(expected)} amount of packages is expected"
        )
        shutil.rmtree(packages)

    def test_create_packages_ignore_0(self):
        """Test getting the cargo manigest's version .registryognore-0"""
        expected = ['first-0.1.0.crate', 'second-0.1.0.crate', 'third-0.1.0.crate']
        registry_ignore_0 = os.path.join(CARGO_MANIFEST_DIR, '.registryignore-0')
        registry_ignore = os.path.join(CARGO_MANIFEST_DIR, '.registryignore')
        os.rename(registry_ignore_0, registry_ignore)
        ignored_members = get_registry_ignore(CARGO_MANIFEST_DIR)
        os.rename(registry_ignore, registry_ignore_0)
        create_packages(CARGO_MANIFEST_DIR, ignored_members)
        self.assert_created_packages(expected)

    def test_create_packages_ignore_1(self):
        """Test getting the cargo manigest's version .registryognore-1"""

        expected = ['second-0.1.0.crate', 'third-0.1.0.crate']
        registry_ignore_1 = os.path.join(CARGO_MANIFEST_DIR, '.registryignore-1')
        registry_ignore = os.path.join(CARGO_MANIFEST_DIR, '.registryignore')
        os.rename(registry_ignore_1, registry_ignore)
        ignored_members = get_registry_ignore(CARGO_MANIFEST_DIR)
        os.rename(registry_ignore, registry_ignore_1)
        create_packages(CARGO_MANIFEST_DIR, ignored_members)
        self.assert_created_packages(expected)

    def test_create_packages_ignore_all(self):
        """Test getting the cargo manigest's version .registryognore-all"""

        expected = []
        registry_ignore_all = os.path.join(CARGO_MANIFEST_DIR, '.registryignore-all')
        registry_ignore = os.path.join(CARGO_MANIFEST_DIR, '.registryignore')
        os.rename(registry_ignore_all, registry_ignore)
        ignored_members = get_registry_ignore(CARGO_MANIFEST_DIR)
        os.rename(registry_ignore, registry_ignore_all)
        create_packages(CARGO_MANIFEST_DIR, ignored_members)
        with self.assertRaises(FileNotFoundError):
            self.assert_created_packages(expected)


if __name__ == '__main__':
    unittest.main()
