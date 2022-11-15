# $Memorization Tool
# Stage 4
"""Change practice()
new methods: learn()"""

import db_worker as dw
import flashcard_states as fs
import logging
from typing import Type, List

logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')

logging.disable(40)


class Game:
    def __init__(self):
        self.calls = 0

    @staticmethod
    def start():
        """Entry point of the program."""
        end_game: bool = False
        logging.debug(f'end_game = {end_game}')
        state: Type[fs.State] = fs.MainMenu
        logging.debug(f'state = {state}')
        while not end_game:
            if state == fs.MainMenu:
                logging.debug(f'state = {state}')
                state = Game.main_menu()
            elif state == fs.AddCard:
                logging.debug(f'state = {state}')
                state = Game.add_card()
            elif state == fs.Practice:
                logging.debug(f'state = {state}')
                state = Game.practice()
            elif state == fs.End:
                logging.debug(f'state = {state}')
                state = Game.end()
                logging.debug('end_game = True')
                end_game = True
            else:
                state = fs.End

    @staticmethod
    def main_menu() -> Type[fs.State]:
        command: str = input('1. Add flashcards\n'
                             '2. Practice flashcards\n'
                             '3. Exit\n')
        print()  # !
        if command == '1':
            return fs.AddCard
        elif command == '2':
            return fs.Practice
        elif command == '3':
            return fs.End
        else:
            print(f'{command} is not an option\n')
            return fs.MainMenu

    @staticmethod
    def add_card() -> Type[fs.State]:
        """add a card - create a new flashcard with "question"/"answer.
        # questions and answers must be non-empty values. Otherwise, wait for the input."""
        logging.info(' def add_card()')
        command = input('1. Add a new flashcard\n'
                        '2. Exit\n')
        print()  # !
        if command == '1':
            dw.store_card(Game.input_correct('Question:'), Game.input_correct('Answer:'), 1)
            print()
            return fs.AddCard
        elif command == '2':
            return fs.MainMenu
        else:
            print(f'{command} is not an option\n')
            return fs.AddCard

    @staticmethod
    def practice() -> Type[fs.State]:
        """
        press "y" to see the answer:
        press "n" to skip:
        press "u" to update:
        - If n is entered, skip to the next flashcard.
        - If there are no flashcards to show, return to the main menu (1)
        """
        flashcards: List[dw.FlashCard] = dw.get_cards()
        if not flashcards:
            print('There is no flashcard to practice!')
            return fs.MainMenu
        else:
            for card in flashcards:
                print(f'Question: {card.question}')
                practice_menu = ('press "y" to see the answer:',
                                 'press "n" to skip:',
                                 'press "u" to update:')
                command = Game.input_correct(practice_menu, cases=('y', 'n', 'u'))
                if command == 'y':
                    Game.learn(card)
                    print()  # !
                elif command == 'n':
                    print()  # !
                    continue
                elif command == 'u':
                    Game.update_(card)
                else:
                    print(f'{command} is not an option ')
                    continue
        return fs.MainMenu

    @staticmethod
    def learn(card: dw.FlashCard):
        print(f'Answer: {card.answer}')
        learning_menu = ('press "y" if your answer is correct:',
                         'press "n" if your answer is wrong:')
        learning_answer = Game.input_correct(learning_menu, cases=('y', 'n'))
        if learning_answer == 'y':
            # If you get the card right, you move it to the next box
            dw.change_box(card.id, card.box + 1)
        elif learning_answer == 'n':
            # every time you get a card wrong, you move it to Box 1
            dw.change_box(card.id, 1)

    @staticmethod
    def update_(card: dw.FlashCard):
        update_menu = ('press "d" to delete the flashcard:',
                       'press "e" to edit the flashcard:')
        command = Game.input_correct(update_menu, cases=('d', 'e'))
        if command == 'd':
            dw.delete_card(card.id)
            print()  # !
        elif command == 'e':
            # If the user leaves the question or the answer field empty,
            # keep the original question or answer value unchanged.  !!!
            print()  # !
            print(f'current question: {card.question}')
            question_new = input('please write a new question:\n')
            print()  # !
            if question_new:
                dw.edit_card(card.id, 'question', question_new)
            print(f'current answer: {card.answer}')
            answer_new = input('please write a new answer:\n')
            if answer_new.strip():
                dw.edit_card(card.id, 'answer', answer_new)
            print()  # !

    @staticmethod
    def end() -> Type[fs.State]:
        print('Bye!')
        return fs.End

    @staticmethod
    def input_correct(request=None, cases=None):
        """Return correct input depending on the request and valid answers"""
        while True:
            if isinstance(request, str):
                print(request)
            elif isinstance(request, tuple):
                print(*request, sep='\n')
            user_input = input()
            if len(user_input.strip()) < 1 or (cases is not None and user_input not in cases):
                print(f'{user_input} is not an option')
                continue
            return user_input


def main():
    logging.info('def main ...')
    # dw.print_db_info()
    new = Game()
    new.start()
    dw.session.close()
    logging.debug('dw.session.close()')


if __name__ == '__main__':
    main()
    logging.debug('THE END')
