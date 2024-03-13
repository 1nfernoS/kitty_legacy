from json import loads
from data_typings import Puzzles

with open('resources/puzzle_answers.json', 'r') as f:
    puzzles: Puzzles = loads(f.read())
