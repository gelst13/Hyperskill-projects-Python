import random

roll = ['python', 'java', 'kotlin', 'javascript']
word = random.choice(roll)
guess = list("-" * len(word))  # create a list of characters for placing guessed letters
mistakes = 0  # counter of mistakes
already_entered = []
status = ""
L = ""
lower_case = 'abcdefghijklmnopqrstuvwxyz'


def menu():
    global status
    c = input('Type "play" to play the game, "exit" to quit: ')
    if c == "play":
        status = "on"
    elif c == "exit":
        status = "end"
    else:
        menu()


def get_valid_letter():
    global L
    print()
    print(''.join(guess))
    L = input("Input a letter: ")
    if len(L) != 1:
        print("You should input a single letter")
        get_valid_letter()
    elif L not in lower_case:
        print("Please enter a lowercase English letter")
        get_valid_letter()
    elif L not in already_entered:
        already_entered.append(L)
    else:
        print("You've already guessed this letter")
        get_valid_letter()


def check_for_win():
    global status
    if mistakes < 8 and ''.join(guess) == word:
        print("You guessed the word!")
        print("You survived!")
        status = "end"
    elif mistakes >= 8 and ''.join(guess) != word:
        print("You lost!")
        status = "end"
        #print()
        #menu()


print("H A N G M A N")
menu()
while status != "end":
    get_valid_letter()
    if L not in word:
        print("That letter doesn't appear in the word")
        mistakes += 1
        check_for_win()
    elif L in word:
        for x in range(len(word)):
            if word[x] == L:
                guess[x] = L
        check_for_win()
