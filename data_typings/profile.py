from typing import TypedDict, List


class Skill(TypedDict):
    name: str
    level: int


class Skills(TypedDict):
    active: List[Skill]
    passive: List[Skill]


class Stats(TypedDict):
    level: int
    attack: int
    defence: int
    strength: int
    agility: int
    endurance: int
    luck: int
    accuracy: int
    concentration: int

class Profile(TypedDict):
    stats: Stats
    items: List[int]


class Build(TypedDict):
    books: List[int]
    adms: List[int]
