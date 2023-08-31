"""Module providing unit tests for core.py"""
# pylint: disable=import-error, wrong-import-position, unspecified-encoding
import sys
import unittest
import os

cur_dir = os.path.dirname(__file__)
core_module_dir = os.path.join(cur_dir, '..')
sys.path.append(core_module_dir)

from core import get_workspace_members
from changelog_preparator import move_log_out_of_comments

CARGO_MANIFEST_DIR = os.path.join(cur_dir, "rust-test-workspace")

class TestChangelogPreparator(unittest.TestCase):
    """Class providing unit tests for changelog_preparator.py"""
    def create_changelog_backup(self):
        """Create a copy of CHANGELOG.md file for future test rerunnnig"""
        os.rename(os.path.join(CARGO_MANIFEST_DIR, 'CHANGELOG.md'), os.path.join(CARGO_MANIFEST_DIR, 'test.md'))
        changelog_dir = os.path.join(CARGO_MANIFEST_DIR, 'CHANGELOG.md')
        test_dir = os.path.join(CARGO_MANIFEST_DIR, 'test.md')
        with open(changelog_dir, 'w') as new_changelog:
            with open(test_dir, 'r') as changelog:
                for line in changelog:
                    new_changelog.write(line)    
        
    def test_move_log_out_of_comments(self):
        """Test modifing changelog"""
        self.create_changelog_backup()
        move_log_out_of_comments(CARGO_MANIFEST_DIR, 'test.md')
        expected = open(os.path.join(CARGO_MANIFEST_DIR, "EXPECTED-CHANGELOG.md")).readlines()
        actual = open(os.path.join(CARGO_MANIFEST_DIR, "test.md")).readlines()
        os.remove(os.path.join(CARGO_MANIFEST_DIR, "test.md"))
        self.assertEqual(expected, actual, f"{expected} is expected")

        

if __name__ == '__main__':
    unittest.main()
