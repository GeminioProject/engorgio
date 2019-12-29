from dataclasses import dataclass


@dataclass
class Scan:
    path: str


@dataclass
class Decompress:
    path: str
