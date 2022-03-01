# $Coffee Machine
"""functionality that simulates a real coffee machine

Stage 6/6. Possible operations are: buy, fill, take, remaining, exit.
If the coffee machine doesn't have enough resources to make coffee,
the program should output 'can't make a cup of coffee' and what is missing.
if the user types "buy"  and then changes his mind
he can type "back" to return into the main cycle.
The class should not use system input at all; it will only handle the input
that comes to it via special method and its string argument.
"""
import logging

logging.basicConfig(filename='coffee-machine.log', level=logging.DEBUG, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(10)

# logging.debug('DEBUG message')
# logging.info('INFO message')
# logging.warning('WARNING message')
# logging.error('ERROR message')
# logging.critical('CRITICAL message')


class WrongCommandError(Exception):
    def __str__(self):
        return "Unknown command!"


class RecipeError(Exception):
    def __str__(self):
        return "Recipe should be like {'water': 10, 'milk': 0, 'coffee beans': 2, 'price': 1}"


class CoffeeMachine:
    n_ph = 0
    fill_commands = {
        'water': 'Write how many ml of water do you want to add:',
        'milk': 'Write how many ml of milk do you want to add:',
        'coffee beans': 'Write how many grams of coffee beans do you want to add:',
        'cups': 'Write how many disposable cups of coffee do you want to add',
    }
    
    def __init__(self):
        """The initializer of the class.

        Arguments:
        initial_store: dict
        current_store: dict
        """
        self.initial_store = {'money': 550, 'water': 400, 'milk': 540, 'coffee beans': 120, 'cups': 9}
        self.current_store = self.initial_store
        self.current_state = 'choosing an action'
    
    def __new__(cls, *args, **kwargs):
        if cls.n_ph == 0:
            cls.n_ph += 1
            return object.__new__(cls)
        return None
    
    def __repr__(self):
        return f'CoffeeMachine object with:\n' \
               f'initial stock: {self.initial_store}\n'
    
    def __str__(self):
        return self.__repr__()
    
    @staticmethod
    def ask_user():
        aaa = input()
        logging.debug(f'user answer action= {aaa}')
        return aaa
    
    def calculate_store(self, data: 'dict with data about sales or added supplies') -> dict:
        """Take dict with data about sales or added supplies"""
        current_result = {'money': 0, 'water': 0, 'milk': 0, 'coffee beans': 0, 'cups': 0}
        for key in list(self.current_store.keys()):
            current_result[key] = self.current_store[key] - data[key]
        return current_result
    
    def remaining(self):
        """Print current stock"""
        print('The coffee machine has:')
        print(f'{self.current_store["water"]} ml of water',
              f'{self.current_store["milk"]} ml of milk',
              f'{self.current_store["coffee beans"]} g of coffee beans',
              f'{self.current_store["cups"]} of disposable cups',
              f'${self.current_store["money"]} of money',
              sep='\n')
        print()
    
    def fill(self) -> 'added supplies dict':
        """Replenish supplies."""
        try:
            supplies = {'money': 0}
            for key in list(CoffeeMachine.fill_commands.keys()):
                print(CoffeeMachine.fill_commands[key])
                supplies.update({key: -int(CoffeeMachine.ask_user())})
            # self.current_store = CoffeeMachine.calculate_store(self, supplies)
            return supplies
        except ValueError:
            raise WrongCommandError
    
    def take(self):
        print(f'I gave you ${self.current_store["money"]}')
        self.current_store.update({'money': 0})
        print()
    
    def choose_coffee(self):
        """Return coffee_chosen as dict."""
        recipes = {'espresso': {'water': 250, 'milk': 0, 'coffee beans': 16, 'price': 4},
                   'latte': {'water': 350, 'milk': 75, 'coffee beans': 20, 'price': 7},
                   'cappuccino': {'water': 200, 'milk': 100, 'coffee beans': 12, 'price': 6},
                   }
        coffee_types = {'1': 'espresso', '2': 'latte', '3': 'cappuccino'}
        if self.current_state == 'choosing a type of coffee':
            print('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, '
                  'back - to main menu:')
            coffee_chosen = CoffeeMachine.ask_user()
            if coffee_chosen in coffee_types.keys():
                return recipes[coffee_types[coffee_chosen]]
            elif coffee_chosen == 'back':
                logging.debug('coffee_chosen == back')
                return dict()
            else:
                raise WrongCommandError
    
    def resources_not_enough(self, recipe):
        # recipe = {'water': 250, 'milk': 0, 'coffee beans': 16, 'price': 4}
        if isinstance(recipe, dict):
            if list(recipe.keys()) == ['water', 'milk', 'coffee beans', 'price']:
                for key, value in self.current_store.items():
                    try:
                        if key == 'cups' and value == 0:
                            print(f'Sorry, not enough {key}!')
                            return True
                        elif value < recipe[key]:
                            print(f'Sorry, not enough {key}!')
                            return True
                        # else:
                        #     continue
                    except KeyError:
                        continue
            else:
                raise RecipeError
        else:
            raise TypeError('recipe should be dict class obj')
    
    def buy(self):
        """User must choose one of three types of coffee"""
        sales = {'money': 0, 'water': 0, 'milk': 0, 'coffee beans': 0, 'cups': 0}
        coffee = CoffeeMachine.choose_coffee(self)
        if coffee == dict():
            return 'back'
        coffee_possible = CoffeeMachine.resources_not_enough(self, coffee)
        if coffee_possible:
            return sales
        else:
            print('I have enough resources, making you a coffee!')
            sales['money'] += (-coffee['price'])
            sales['water'] += coffee['water']
            sales['milk'] += coffee['milk']
            sales['coffee beans'] += coffee['coffee beans']
            sales['cups'] += 1
            return sales
    
    def exit(self):
        self.current_state = 'terminated'
        logging.info('END')
        exit()
    
    actions = {
        'buy': buy,
        'fill': fill,
        'take': take,
        'remaining': remaining,
        'exit': exit
    }
    
    possible_states = {
        'buy': 'choosing a type of coffee',
        'fill': 'defining amounts',
        'take': 'choosing an action',
        'remaining': 'choosing an action',
        'exit': 'terminated'
    }
    
    def give_command(self):
        while True:
            try:
                self.current_state = 'choosing an action'
                logging.debug(f'current_state: {self.current_state}')
                print('Write action (buy, fill, take, remaining, exit):')
                user_answer = CoffeeMachine.ask_user()
                self.current_state = CoffeeMachine.possible_states[user_answer]
                logging.debug(f'current_state: {self.current_state}')
                print()
                if user_answer == 'buy':
                    sales = CoffeeMachine.actions[user_answer](self)  # CoffeeMachine.buy(self)
                    # CoffeeMachine.current_state = 'choosing an action'
                    if sales == 'back':
                        # let's go back to machine menu
                        CoffeeMachine.give_command(self)
                        print()
                    else:
                        self.current_store = CoffeeMachine.calculate_store(self, sales)
                        print()
                elif user_answer == 'fill':
                    added_supplies = CoffeeMachine.actions[user_answer](self)  # dict
                    self.current_store = CoffeeMachine.calculate_store(self, added_supplies)
                    logging.debug(f'added_supplies {added_supplies}')
                    print()
                elif user_answer in ('take', 'remaining', 'exit'):
                    CoffeeMachine.actions[user_answer](self)
                    
                else:
                    raise WrongCommandError
            except KeyError:
                raise WrongCommandError


def main():
    try:
        logging.info('START')
        new_operation = CoffeeMachine()
        CoffeeMachine.give_command(new_operation)
    except WrongCommandError as err:
        print('Unknown command!')
        logging.error(err)
        logging.info('END')


if __name__ == '__main__':
    main()
