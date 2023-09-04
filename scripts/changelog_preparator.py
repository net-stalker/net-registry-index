#!/usr/bin/env python
# pylint: disable=unspecified-encoding
"""
Module proving preparation for changelog updation by using update-file ci flow
https://github.com/marketplace/actions/update-file
"""
import os
import sys

## FROM THIS
# <!-- [START AUTO UPDATE] -->
# <!-- Please keep comment here to allow auto-update -->
# INFO ABOUT CHANGES
# <!-- [END AUTO UPDATE] -->

## TO THIS
# <!-- [START AUTO UPDATE] -->
# <!-- Please keep comment here to allow auto-update -->
# <!-- [END AUTO UPDATE] -->
# INFO ABOUT CHANGES

def move_log_out_of_comments(manifest_dir, file_name):
    """A function for moving all the info out of comments"""
    changelog_dir = os.path.join(manifest_dir, file_name)
    old_dir = os.path.join(manifest_dir, 'old.md')
    os.rename(changelog_dir, old_dir)
    with open(changelog_dir, 'w') as changelog:
        with open(old_dir, 'r') as old_changelog:
            started_capturing_log = False
            log_container = []
            for line in old_changelog:
                if line == '<!-- Please keep comment here to allow auto-update -->\n':
                    changelog.write(line)
                    started_capturing_log = True
                    continue

                if line == '<!-- [END AUTO UPDATE] -->\n' or line == '<!-- [END AUTO UPDATE] -->':
                    changelog.write(line)
                    started_capturing_log = False
                    continue

                if started_capturing_log:
                    log_container.append(line)
                    continue

                if not started_capturing_log and len(log_container) != 0:
                    for log_line in log_container:
                        changelog.write(log_line)
                    log_container = []

                changelog.write(line)

            if not started_capturing_log and len(log_container) != 0:
                for log_line in log_container:
                    changelog.write(log_line)
                log_container = []

    os.remove(old_dir)

def main():
    """Main function"""
    args = sys.argv[1:]
    if len(args) != 1:
        raise RuntimeError("wrong number of args. 1 is required")
    manifest_dir = args[0]
    move_log_out_of_comments(manifest_dir, "CHANGELOG.md")

if __name__ == "__main__":
    main()
