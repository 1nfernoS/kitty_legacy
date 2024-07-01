from json import loads
from data_typings import Puzzles


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
