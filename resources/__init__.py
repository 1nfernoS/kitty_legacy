from json import loads
from data_typings import Puzzles

with open('resources/const_strings.json', 'r') as f:
    puzzles: Puzzles = loads(f.read())
