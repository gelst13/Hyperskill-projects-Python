m = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
row, column = 0, 0
v = ["X", "O"] * 4 + ["X"]
status = "on"


def print_grid():
    print('-' * 9)
    print(f'| {m[0][0]} {m[0][1]} {m[0][2]} |')
    print(f'| {m[1][0]} {m[1][1]} {m[1][2]} |')
    print(f'| {m[2][0]} {m[2][1]} {m[2][2]} |')
    print('-' * 9)


def check_for_win():
    global status, m
    line1 = m[0]
    line2 = m[1]
    line3 = m[2]
    st1 = [m[0][0], m[1][0], m[2][0]]
    st2 = [m[0][1], m[1][1], m[2][1]]
    st3 = [m[0][2], m[1][2], m[2][2]]
    d1 = [m[0][0], m[1][1], m[2][2]]
    d2 = [m[2][0], m[1][1], m[0][2]]
    c = [line1, line2, line3, st1, st2, st3, d1, d2]
    if ['X', 'X', 'X'] in c:
        if ['O', 'O', 'O'] in c:
            print('Impossible')
            status = "end"
        else:
            print('X wins')
            status = "end"
    elif ['O', 'O', 'O'] in c:
        print('O wins')
        status = "end"
    elif " " in m[0] or " " in m[1] or " " in m[2]:
        #  print('Game not finished')
        status = "on"
    else:
        print("Draw")
        status = "end"


def coordinates():
    global row, column, m
    move = input('Enter the coordinates: ')
    try:
        row, column = move.split()
        if 1 <= int(row) <= 3 and 1 <= int(column) <= 3 and m[int(row) - 1][int(column) - 1] == " ":
            row = int(row)
            column = int(column)
            return row, column
        elif 1 <= int(row) <= 3 and 1 <= int(column) <= 3:
            print("This cell is occupied! Choose another one!")
            return coordinates()
        else:
            print('Coordinates should be from 1 to 3!')
            return coordinates()
    except ValueError:
        print("You should enter numbers!")
        return coordinates()


def play_game():
    global v, m, row, column, status
    while status != "end" and len(v) > 0:
        coordinates()
        m[row - 1][column - 1] = v[0]
        del v[0]
        print_grid()
        check_for_win()


print_grid()

play_game()
