"""Module providing unit tests for registry_maintainer.py"""
# pylint: disable=import-error, wrong-import-position, line-too-long, unspecified-encoding,duplicate-code
import sys
import unittest
import os
import shutil
import json
import pathlib as pl

cur_dir = os.path.dirname(__file__)
core_module_dir = os.path.join(cur_dir, '..')
sys.path.append(core_module_dir)

from registry_maintainer import cargo_index, get_metainfo, update_or_create_index, move_crate_binaries
from create_packages import create_packages
from core import get_registry_ignore

CARGO_MANIFEST_DIR = os.path.join(cur_dir, "rust-test-workspace")

FIRST_METAINFO = '{"name":"first","vers":"0.1.0","deps":[],"features":{},"cksum":"","yanked":false,"links":null}'
SECOND_METAINFO = '{"name":"second","vers":"0.1.0","deps":[],"features":{},"cksum":"","yanked":false,"links":null}'
THIRD_METAINFO = '{"name":"third","vers":"0.1.0","deps":[],"features":{},"cksum":"","yanked":false,"links":null}'


class TestCaseBase(unittest.TestCase):
    """Extending unittest.TestCase with an additional assertion"""
    # pylint: disable=invalid-name
    def assertIsFile(self, path):
        """Assert for checking if file exists"""
        if not pl.Path(path).resolve().is_file():
            raise AssertionError(f"File does not exist: {str(path)}")

    def assertIsDirectory(self, path):
        """Assert for checking if directory exists"""
        if not pl.Path(path).resolve().is_dir():
            raise AssertionError(f"Directory does not exist: {str(path)}")

class TestCreatePackages(TestCaseBase):
    """Class providing unit tests for registry_maintainer.py"""
    def create_packages_for_test(self):
        """Method for packaging workspace members"""
        registry_ignore_0 = os.path.join(
            CARGO_MANIFEST_DIR, '.registryignore-0')
        registry_ignore = os.path.join(CARGO_MANIFEST_DIR, '.registryignore')
        os.rename(registry_ignore_0, registry_ignore)
        ignored_members = get_registry_ignore(CARGO_MANIFEST_DIR)
        os.rename(registry_ignore, registry_ignore_0)
        create_packages(CARGO_MANIFEST_DIR, ignored_members)


    def test_cargo_index(self):
        """Test forming cargo index string for getting metainfo"""
        expected = 'cargo index metadata --crate path --index-url url | grep "{*}"'
        self.assertEqual(expected, cargo_index('', 'path'), f"{expected} is expected")

    def test_get_metainfo(self):
        """Test getting metainfo for packages"""
        expected = {
            'first': ['first-0.1.0.crate', FIRST_METAINFO],
            'second': ['second-0.1.0.crate', SECOND_METAINFO],
            'third': ['third-0.1.0.crate' ,THIRD_METAINFO],
        }
        self.create_packages_for_test()

        packages_dir = os.path.join(CARGO_MANIFEST_DIR, 'target', 'package')
        for name, info in get_metainfo(packages=packages_dir).items():
            self.assertIn(name, expected.keys(), f"{name} is expected to be in result")
            info_json = json.loads(info[1])
            expected_json = json.loads(expected[name][1])
            self.assertEqual(info_json['name'], expected_json['name'], f"{info_json['name']} != {expected_json['name']}")
            self.assertEqual(info_json['vers'], expected_json['vers'], f"{info_json['vers']} != {expected_json['vers']}")
            self.assertEqual(info_json['deps'], expected_json['deps'], f"{info_json['deps']} != {expected_json['deps']}")
            self.assertEqual(info_json['features'], expected_json['features'], f"{info_json['features']} != {expected_json['features']}")
            self.assertEqual(info_json['yanked'], expected_json['yanked'], f"{info_json['yanked']} != {expected_json['yanked']}")
            self.assertEqual(info_json['links'], expected_json['links'], f"{info_json['links']} != {expected_json['links']}")

        shutil.rmtree(packages_dir)

    def test_update_or_create_index(self):
        """Test for checking updating cargo registry index"""
        self.create_packages_for_test()

        packages_dir = os.path.join(CARGO_MANIFEST_DIR, 'target', 'package')
        metainfo = get_metainfo(packages=packages_dir)

        shutil.rmtree(packages_dir)

        registry = os.path.join(cur_dir, 'test-registry')
        os.mkdir(registry)

        update_or_create_index(metainfo, registry)
        actual_ans = {
            'first': os.path.join(registry, 'fi', 'rs', 'first'),
            'second': os.path.join(registry, 'se', 'co', 'second'),
            'third': os.path.join(registry, 'th', 'ir', 'third')
        }

        for name, info in metainfo.items():
            self.assertIsFile(actual_ans[name])
            with open(actual_ans[name], 'r') as file:
                actual_info = file.read()
                excepted_info = info[1]
                self.assertEqual(actual_info, excepted_info, f'{excepted_info} is expected')

        update_or_create_index(metainfo, registry)

        for name, info in metainfo.items():
            self.assertIsFile(actual_ans[name])
            with open(actual_ans[name], 'r') as file:
                actual_info = file.read()
                excepted_info = info[1] + info[1]
                self.assertEqual(actual_info, excepted_info, f'{excepted_info} is expected')

        shutil.rmtree(registry)

    def test_move_crate_binaries(self):
        """Test moving crate binaries"""
        self.create_packages_for_test()

        registry = os.path.join(cur_dir, 'test-registry')
        packages_dir = os.path.join(CARGO_MANIFEST_DIR, 'target', 'package')
        metainfo = get_metainfo(packages=packages_dir)

        os.mkdir(registry)
        update_or_create_index(metainfo, registry)
        move_crate_binaries(packages=packages_dir, metainfo=metainfo, registry=registry)

        actual_ans = [
            os.path.join(registry, 'crates', 'first', '0.1.0', 'download', 'first-0.1.0.crate'),
            os.path.join(registry, 'crates', 'second', '0.1.0', 'download', 'second-0.1.0.crate'),
            os.path.join(registry, 'crates', 'third', '0.1.0', 'download', 'third-0.1.0.crate')
        ]
        for crate in actual_ans:
            self.assertIsFile(crate)

        move_crate_binaries(packages=packages_dir, metainfo=metainfo, registry=registry)
        for crate in actual_ans:
            self.assertIsFile(crate)
        shutil.rmtree(registry)



if __name__ == '__main__':
    unittest.main()
