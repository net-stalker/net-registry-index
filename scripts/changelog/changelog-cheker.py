#!/usr/bin/env python
import os
import sys
import re

def verify_changelog_changes(manifest_dir):
    pattern = r"(### [A-z]+)"
    changelog_dir = os.path.join(manifest_dir, 'CHANGELOG.md')
    changelog = open(changelog_dir)
    unreleased = False
    cheking_line = "" 
    for line in changelog:
        if unreleased and line != '\n':
            cheking_line = line
            break
        if not unreleased and line != '## [Unreleased] - ReleaseDate\n':
            continue
        unreleased = True
    if re.match(pattern, cheking_line) == None:
        raise RuntimeError("Changelog isn't updated properly")

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        raise RuntimeError("wrong number of args. 1 is required")
    manifest_dir = args[0]
    verify_changelog_changes(manifest_dir)

if __name__ == "__main__":
    main()
