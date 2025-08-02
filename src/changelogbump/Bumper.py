#!/usr/bin/env python3

import toml

from changelogbump.PyProject import PyProject


class Bumper:
    @property
    def current(self) -> str:
        content = toml.load(PyProject.path)
        return content["project"]["version"]

    def bump(
        self, major: bool = False, minor: bool = False, patch: bool = False
    ) -> str:
        major_num, minor_num, patch_num = self.current.split(".")
        major_num = int(major_num)
        minor_num = int(minor_num)
        patch_num = int(patch_num)
        if major:
            major_num += 1
            minor_num = 0
            patch_num = 0
        elif minor:
            minor_num += 1
            patch_num = 0
        elif patch:
            patch_num += 1
        else:
            raise AttributeError("must provide one of ['major', 'minor', 'patch']")
        return f"{major_num}.{minor_num}.{patch_num}"
