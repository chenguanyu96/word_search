PUZZLE1 = '''
glkutqyu
onnkjoaq
uaacdcne
gidiaayu
urznnpaf
ebnnairb
xkybnick
ujvaynak
'''

PUZZLE2 = '''
fgbkizpyjohwsunxqafy
hvanyacknssdlmziwjom
xcvfhsrriasdvexlgrng
lcimqnyichwkmizfujqm
ctsersavkaynxvumoaoe
ciuridromuzojjefsnzw
bmjtuuwgxsdfrrdaiaan
fwrtqtuzoxykwekbtdyb
wmyzglfolqmvafehktdz
shyotiutuvpictelmyvb
vrhvysciipnqbznvxyvy
zsmolxwxnvankucofmph
txqwkcinaedahkyilpct
zlqikfoiijmibhsceohd
enkpqldarperngfavqxd
jqbbcgtnbgqbirifkcin
kfqroocutrhucajtasam
ploibcvsropzkoduuznx
kkkalaubpyikbinxtsyb
vjenqpjwccaupjqhdoaw
'''


def rotate_puzzle(puzzle):
    '''(str) -> str
    Return the puzzle rotated 90 degrees to the left.
    '''
    raw_rows = puzzle.split('\n')
    rows = []
    # If blank lines or trailing spaces are present, remove them
    for row in raw_rows:
        row = row.strip()
        if row:
            rows.append(row)
    # Calculate number of rows and columns in original puzzle
    num_rows = len(rows)
    num_cols = len(rows[0])
    # An empty row in the rotated puzzle
    empty_row = [''] * num_rows

    # Create blank puzzle to store the rotation
    rotated = []
    for row in range(num_cols):
        rotated.append(empty_row[:])
    for x in range(num_rows):
        for y in range(num_cols):
            rotated[y][x] = rows[x][num_cols - y - 1]

    # Construct new rows from the lists of rotated
    new_rows = []
    for rotated_row in rotated:
        new_rows.append(''.join(rotated_row))

    rotated_puzzle = '\n'.join(new_rows)

    return rotated_puzzle


def lr_occurrences(puzzle, word):
    '''(str, str) -> int
    Return the number of times word is found in puzzle in the
    left-to-right direction only.
    >>> lr_occurrences('xaxy\nyaaa', 'xy')
    1
    '''
    return puzzle.count(word)


def total_occurrences(puzzle, word):
    '''(str, str) -> int
    Return total occurrences of word in puzzle.
    All four directions are counted as occurrences:
    left-to-right, top-to-bottom, right-to-left, and bottom-to-top.
    >>> total_occurrences('xaxy\nyaaa', 'xy')
    2
    '''
    # Check in puzzle for left-to-right for the word
    total = lr_occurrences(puzzle, word)

    # Check in all directions by rotating the puzzle 90 degrees to the left
    puzzle = rotate_puzzle(puzzle)

    # Add the new number of occurrences to the ongoing total number of
    # occurrences of the word
    total += lr_occurrences(puzzle, word)
    puzzle = rotate_puzzle(puzzle)
    total += lr_occurrences(puzzle, word)
    puzzle = rotate_puzzle(puzzle)
    total += lr_occurrences(puzzle, word)
    return total


def in_puzzle_horizontal(puzzle, word):
    '''(str, str) -> bool
    Return True iff the given word can be found in puzzle in one or both
    horizontal directions, otherwise returns False.
    >>> in_puzzle_horizontal(PUZZLE1, 'brian')
    True
    '''
    # Find the words that does from left-to-right and assigns the number to the
    # variable total_track
    total_track = lr_occurrences(puzzle, word)

    # Rotate the puzzle so that the words from right-to-left can be found by
    # scanning left-to-right and added on to the ongoing total count of
    # occurrences (total_track)
    puzzle = rotate_puzzle(puzzle)
    puzzle = rotate_puzzle(puzzle)
    total_track += lr_occurrences(puzzle, word)

    # Return True if the word does go horizontally, otherwise return False
    return total_track > 0


def in_puzzle_vertical(puzzle, word):
    '''(str, str) -> bool
    Return True iff the given word can be found in puzzle in one or both
    vertical directions (top-to-bottom or bottom-to-top), otherwise return
    False.
    >>> in_puzzle_vertical(PUZZLE1, 'nick')
    True
    '''
    # Rotate the puzzle in order to check from top-to-bottom
    puzzle = rotate_puzzle(puzzle)
    total_track = lr_occurrences(puzzle, word)

    # Rotate the puzzle twice in roder to check from bottom-to-top and adds
    # the number of occurrences to the ongoing total number of occurrences
    puzzle = rotate_puzzle(puzzle)
    puzzle = rotate_puzzle(puzzle)
    total_track += lr_occurrences(puzzle, word)
    return total_track > 0


def in_puzzle(puzzle, word):
    '''(str, str) -> bool
    Return True iff the word is in the puzzle (any of the 4 directions),
    otherwise return False.
    >>> in_puzzle(PUZZLE1, 'brian')
    True
    >>> in_puzzle(PUZZLE2, 'nick')
    True
    >>> in_puzzle(PUZZLE1, 'big')
    False
    >>> in_puzzle(PUZZLE2, 'dad')
    False
    '''
    # Check if the word is in the puzzle in any of the 4 directions, if it is
    # return True, otherwise return False
    return((in_puzzle_horizontal(puzzle, word))
           or (in_puzzle_vertical(puzzle, word)))


def in_exactly_one_dimension(puzzle, word):
    '''(str, str) -> bool
    Return True iff the word is found the puzzle only in one direction
    (horizontal or vertical); cannot be both, otherwise return False.
    >>> in_exactly_one_dimension(PUZZLE1, 'dan')
    True
    >>> in_exactly_one_dimension(PUZZLE1, 'brian')
    False
    '''
    # Compute the total number of occurrences of the word in the puzzle
    expected_total = total_occurrences(puzzle, word)

    # Checks both horizontal and vertical to make sure that
    bool_ver = in_puzzle_vertical(puzzle, word)
    bool_hor = in_puzzle_horizontal(puzzle, word)

    # Check the 2 bool variables (bool_ver and bool_hor) to return True if
    # the word is exactly one dimension or False if the word is not in exactly
    # one dimension
    return(((bool_ver is True) and (bool_hor is False))
           or ((bool_ver is False) and (bool_hor is True))
           or (expected_total == 0))


def all_horizontal(puzzle, word):
    '''(str, str) -> bool
    Return True iff all occurrences of the supplied word are horizontal in the
    puzzle. If word is not in the puzzle, return True, otherwise return False.
    >>> all_horizontal(PUZZLE2, 'brian')
    False
    >>> all_horizontal(PUZZLE1, 'glkutqyu')
    True
    >>> all_horizontal(PUZZLE2, 'kevin')
    True
    >>> all_horizontal(PUZZLE1, 'nick')
    False
    '''
    # Compute the total amount of occurrences of the word
    expected_total = total_occurrences(puzzle, word)

    # Checks in both directions (horizontal and vertical), and will only return
    # True if bool_hor is True and bool_ver is False or if the word is not in
    # the puzzle at all
    bool_ver = in_puzzle_vertical(puzzle, word)
    bool_hor = in_puzzle_horizontal(puzzle, word)
    return(((bool_ver is False) and (bool_hor is True))
           or (expected_total == 0))


def at_most_one_vertical(puzzle, word):
    '''(str, str) -> bool
    Return True iff the word appears at most once in the puzzle and that
    occurrence is vertical, otherwise it will return False.
    >>> at_most_one_vertical(PUZZLE1, 'brian')
    False
    >>> at_most_one_vertical(PUZZLE2, 'paco')
    True
    '''
    # Compute the total amount of occurrences of the word in the puzzle
    expected_total = total_occurrences(puzzle, word)

    # Checks in both directions (horizontal and vertical), will return True iff
    # the word occurs at most once in the puzzle and that occurrence is
    # vertical
    bool_ver = in_puzzle_vertical(puzzle, word)
    bool_hor = in_puzzle_horizontal(puzzle, word)
    return((expected_total <= 1) and (bool_ver is True)
           and (bool_hor is False))


def do_tasks(puzzle, name):
    '''(str, str) -> NoneType
    puzzle is a word search puzzle and name is a word.
    Carry out the tasks specified here and in the handout.
    '''
    print('Number of times', name, 'occurs left-to-right: ', end='')
    print(lr_occurrences(puzzle, name))

    # Rotate the puzzle 90 degrees to the left to face the top side to the left
    # in order to check from top-to-bottom
    puzzle = rotate_puzzle(puzzle)
    print('Number of times', name, 'occurs top-to-bottom: ', end='')
    print(lr_occurrences(puzzle, name))

    # Rotate the puzzle 90 degrees to the left in order to get the
    # right-side of the original puzzle on the left side in order to check for
    # the word
    puzzle = rotate_puzzle(puzzle)
    print('Number of times', name, 'occurs right-to-left: ', end='')
    print(lr_occurrences(puzzle, name))

    # Rotate the puzzle 90 degrees to the left in order to get the bottom-side
    # of the original puzzle on the left-side to check for the word
    puzzle = rotate_puzzle(puzzle)
    print('Number of times', name, 'occurs bottom-to-top: ', end='')
    print(lr_occurrences(puzzle, name))
    print(total_occurrences(puzzle, name))
    print(in_puzzle_horizontal(puzzle, name))
