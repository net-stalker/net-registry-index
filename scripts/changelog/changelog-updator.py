#!/usr/bin/env python
import os
import sys
from datetime import datetime

def update_changelog(manifest_dir, git_tag):
    current_date = datetime.now().date().strftime('%Y-%m-%d')
    changelog_dir = os.path.join(manifest_dir, 'CHANGELOG.md')
    old_dir = os.path.join(manifest_dir, 'old.md')
    os.rename('CHANGELOG.md', 'old.md')
    with open(changelog_dir, 'w') as changelog:
        with open(old_dir, 'r') as old_changelog:
            for line in old_changelog:
                if line == '## [Unreleased] - ReleaseDate\n':
                    line += "\n## [" + git_tag + "] - " + current_date + "\n" 
                changelog.write(line)
    os.remove(old_dir)
    

def main():
    args = sys.argv[1:]
    if len(args) != 2:
        raise RuntimeError("wrong number of args. 2 is required")
    manifest_dir = args[0]
    git_tag = args[1]
    update_changelog(manifest_dir, git_tag)

if __name__ == "__main__":
    main()
