from dataclasses import dataclass


@dataclass
class Version:
    major: int
    minor: int
    patch: int

    @property
    def current(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def bump(
        self, major: bool = False, minor: bool = False, patch: bool = False
    ) -> None:
        if major:
            self.major += 1
            self.minor = 0
            self.patch = 0
        elif minor:
            self.minor += 1
            self.patch = 0
        elif patch:
            self.patch += 1
        else:
            raise AttributeError("must provide one of ['major', 'minor', 'patch']")
