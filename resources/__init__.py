from json import loads
from typing import Dict

from data_typings import Puzzles


help_groups: Dict[str, str]


def get_puzzles() -> Puzzles:
    puzzles: Puzzles = {}

    from ORM import session, PuzzleType
    with session() as db:
        data = db.query(PuzzleType).all()
    for puzzle in data:
        puzzles[puzzle.type_name] = {str(answer.puzzle_question): str(answer.puzzle_answer) for answer in puzzle.puzzle_type_answers}
    with open('resources/const_strings.json', 'r') as f:
        buffs = loads(f.read())
        puzzles.update({'buffs': buffs['buffs']})
        return puzzles


with open('resources/help_descriptions.json', 'r') as f:
    help_groups = loads(f.read())

