# !/usr/bin/python
# -*- coding: utf-8
# $Static Code Analyzer
import ast
import logging
import os
import re
import string
import sys
from pprint import pprint

logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')

# logging.disable(20)

# os.chdir(r'C:\Users\Тоша\PycharmProjects\Static Code Analyzer\Static Code Analyzer\task')
# os.chdir(r'C:\Users\Тоша\PycharmProjects\FirstProject')

target = sys.argv[1]
logging.debug(f'sys.argv[1]: {target}')


class StaticCodeAnalyzer:
    
    def __init__(self, _target: str):
        self.target = _target
        self.mistakes = dict()  # {'line' : [errors]}
        self.messages = {'S001': 'T00 long',
                         'S002': 'Indentation is not a multiple of four',
                         'S003': 'Unnecessary semicolon',
                         'S004': 'Less than two spaces before inline comments',
                         'S005': 'TODO found',
                         'S006': 'More than two blank lines preceding a code line',
                         'S007': "Too many spaces after \"$name\"",
                         'S008': 'Class name \"$name\" should be in CamelCase',
                         'S009': 'Function name \"$name\" should be in snake_case',
                         'S010': 'Argument name \"$name\" should be in snake_case',
                         'S011': 'Variable \"$name\" should be written in snake_case',
                         'S012': 'The default argument value is mutable',
                         }
    
    def get_abs_names(self) -> list:
        """Walking a directory tree and printing the names of the directories and files"""
        logging.debug('get_abs_names...')
        abs_names = []
        for dirpath, dirnames, files_ in os.walk(self.target, topdown=True):
            logging.debug(dirpath)
            for file_name in files_:
                if file_name.endswith('.py'):
                    logging.debug((dirpath, '\\' + file_name))
                    abs_names.append(os.path.join(dirpath, file_name))
        return abs_names
    
    @staticmethod
    def check_s001(text):
        """check_length"""
        if len(text) > 79:
            return 'T00 long'
    
    @staticmethod
    def check_s002(expr: str):
        """Check if Indentation is a multiple of 4."""
        if expr.startswith(' '):
            parse = re.match(r'\ +', expr)
            return 'Ok' if len(parse.group()) % 4 == 0 else 'Not Ok'
    
    @staticmethod
    def check_s003(expr: str):
        """check_semicolon"""
        # logging.info('check_s003...')
        if expr.startswith('#'):
            return False
        elif expr.find(';'):
            # logging.debug(f'expr: {expr}')
            # case with inline comment expr = 'pass; # comment;'
            parse = re.match(r'([\S\D]+)(#[\S\D]+)', expr)  # match='pass; # comment;
            # logging.debug(f'parse= {parse}')
            if parse:
                statement = parse.group(1).strip()
            # case without inline comment
            else:
                statement = expr.strip()
            # logging.debug(f'statement= {statement}')
            # logging.debug(statement.endswith(';'))
            return statement.endswith(';')
    
    @staticmethod
    def check_s004(expr: str):
        """check_inline_comment
        Return True if there are less than 2 spaces between statement and # """
        # logging.debug('check_s004...')
        # logging.debug(expr)
        if expr.find('#') > 0:
            # logging.debug(expr.find('#'))
            comment_start = expr.index('#')
            # logging.debug(expr.index('#'))
            return expr[comment_start - 2:comment_start:1] != '  '
        else:
            return None
    
    @staticmethod
    def check_s005(expr: str):
        """check todo
        [S005] TODO found (in comments only and case-insensitive);"""
        # logging.info('check_s005')
        if expr.startswith('#'):
            # logging.debug(f'expr: {expr}')
            parse = re.match(r'#.?[tT][Oo][Dd][Oo]', expr)
            # logging.debug(f'parse: {parse}')
            if parse:
                return True
        elif expr.find('#'):
            # logging.debug(f'expr: {expr}')
            parse = re.findall(r'# ?[tT][Oo][Dd][Oo]', expr)
            # logging.debug(f'parse: {parse}')
            if parse:
                return True
    
    @staticmethod
    def check_s007(expr: str):
        """1 space between the construction name and the object name"""
        search_construction = re.findall('(class |def )', expr, flags=re.I)
        if search_construction:
            # logging.info(search_construction)
            s007 = re.search(r'(class|def) [^\s]+', expr, flags=re.I)
            if not s007:
                # logging.debug(line)
                return search_construction[0].strip()
    
    @staticmethod
    def check_s008(expr):
        # match expr for class in groups
        s008 = re.match(r"^(class[ ]+)([A-z]+)", expr)
        if bool(s008):
            # if it's a match, we have class_name in .group(2)
            logging.info('def check_s008')
            class_name = s008.group(2)
            logging.debug(class_name)
            # match class_name for correct format
            if not bool(re.match(r"^([A-Z][a-z]+)([A-Z][a-z]+)*", class_name)):
                # if class_name doesn't match correct format for class name,
                # we consider class_name is wrong, we captured style error S008
                logging.debug(f's008: {class_name}')
                return class_name
        else:
            return False
    
    @staticmethod
    def check_s009(expr: str):
        """Function name function_name should be written in snake_case"""
        search_def = re.findall('(def )', expr, flags=re.I)
        if search_def:
            # logging.info('def check_s009...')
            # match expr for def in groups
            match = re.match(r"^(.*def[ ]+)([_A-z0-9]+)", expr)
            # if it's a match, we have method's name in .group(2)
            method_name = match.group(2)
            logging.debug(method_name)
            # match method_name for correct format
            if bool(re.match(r"^__init__", method_name)):
                pass
            elif not bool(re.match(r"^[_a-z0-9]+$", method_name)):
                # if method_name doesn't match correct format for class name,
                # we consider method_name is wrong, we captured style error S009
                logging.debug(f's009: {method_name}')
                return method_name
    
    @staticmethod
    def check_snake_case(expr: str):
        """Return True if variable/argument name is written in snake_case"""
        logging.info(f'check_snake_case for... {expr}')
        # check_ = re.match(r'([a-z_][a-z0-9_]+)$', expr)
        # check_ = re.match(r'([a-z0-9]+(?:_[a-z0-9]+)*)$', expr)
        if expr == '__init__':
            return True
        else:
            check_ = re.match(r'[_a-z0-9]+(?:_[a-z0-9]+)*$', expr)
            logging.debug(f'check_: {check_}')
            return bool(check_)
    
    @staticmethod
    def check_immutability(tested_obj):
        """Check type of tested_obj.
        Return True if tested_obj is hashable and -> immutable"""
        # Constants are immutable.
        # Immutable containers (like tuples) are hashable if their elements are hashable
        # and -> immutable
        # frozensets are immutable and hashable.
        logging.info('check_immutability ...')
        logging.debug(type(tested_obj))
        if isinstance(tested_obj, ast.Tuple):
            if hash(tested_obj.elts):
                logging.debug('tested_obj is Tuple, but immutable and hashable')
                return True
        elif isinstance(tested_obj, ast.Constant):
            logging.debug('tested_obj is Constant, immutable and hashable')
            return True
        elif isinstance(tested_obj, int) or isinstance(tested_obj, str):
            return True
    
    def check_ast_nodes(self, filename):
        """find ast.FunctionDef node and analyze that node: make 3 checks"""
        logging.info('check_ast_nodes...')
        logging.debug(f'filename: {filename}')
        with open(filename, 'r', encoding='utf-8') as file:
            code = file.read()
            # try:
            tree = ast.parse(code)
            # lines = [None] + code.splitlines()  # None at [0] so we can index lines from 1
            for node_ in tree.body:
                logging.debug(node_.lineno)
                if isinstance(node_, ast.ClassDef):
                    tree = node_
                    for node in tree.body:
                        logging.debug(node.lineno)
                        if isinstance(node, ast.FunctionDef):
                            logging.info('node: ast.FunctionDef')
                            function_node = node
                            self.mistakes[function_node.lineno] = set()
                            logging.debug(self.mistakes)
                            function_name = node.name
                            logging.debug(f'function_name: {function_name}')
                            # check for error S010
                            function_args = [a.arg for a in function_node.args.args]
                            logging.debug(f'function_args: {function_args}')
                            if not self.check_snake_case(function_name):
                                logging.debug(f'{function_name} !!! error S009')
                                self.mistakes[function_node.lineno].add(('S009', function_name))
                            for arg in function_args:
                                if not self.check_snake_case(arg):
                                    self.mistakes[function_node.lineno].add(('S010', arg))
                            # check for error S011
                            logging.info('check for error S011')
                            function_tree = function_node
                            for inner_node in function_tree.body:
                                if isinstance(inner_node, ast.Assign):
                                    assign_node = inner_node
                                    logging.info('ast.Assign node')
                                    self.mistakes[assign_node.lineno] = set()
                                    logging.debug(assign_node.lineno)
                                    if isinstance(assign_node.targets[0], ast.Attribute):
                                        logging.debug(assign_node.targets[0])  # <_ast.Attribute object at ...>
                                        logging.debug(assign_node.targets[0].attr)
                                        var_name = assign_node.targets[0].attr
                                    else:
                                        # print(assign_node.targets[0])  # <_ast.Name object at 0x0000000001E9B2B0>
                                        var_name = assign_node.targets[0].id  # variable name by it's id
                                        var_value = assign_node.value.id  # assigned value
                                        logging.debug(f'var_value: {var_value}')
                                    logging.debug(f'var_name: {var_name}')
                                    # for obj in function_node.body:
                                    #     if isinstance(obj, ast.Assign):
                                    #         self.mistakes[obj.lineno] = set()
                                    #         logging.debug(self.mistakes)
                                    #         logging.debug(obj.targets)
                                    #         var_name = [name for name in obj.targets][0]
                                    #         logging.debug(var_name)
                                    if not self.check_snake_case(var_name):
                                        self.mistakes[inner_node.lineno].add(('S011', var_name))
                            # check for error S012
                            function_args_defaults = [d for d in function_node.args.defaults]
                            logging.debug(f'args_default: {function_args_defaults}')
                            for default_value in function_args_defaults:
                                logging.debug(default_value)
                                if not self.check_immutability(default_value):
                                    self.mistakes[function_node.lineno].add(('S012',))
            # except IndentationError as err:
            #     logging.error(err)
            # except SyntaxError as err:
            #     logging.error(err)
    
    def check_file(self, filename):
        logging.info('check_file...')
        logging.debug(f'filename: {filename}')
        with open(filename, 'r', encoding='utf-8') as file:
            empty_line_count = 0
            for number, line in enumerate(file):
                # try:
                if (number + 1) not in self.mistakes.keys():
                    self.mistakes[number + 1] = set()
                # self.mistakes[number + 1] = []
                if self.check_s001(line):
                    self.mistakes[number + 1].add(('S001',))
                if self.check_s002(line) == 'Not Ok':
                    self.mistakes[number + 1].add(('S002',))
                if self.check_s003(line):
                    self.mistakes[number + 1].add(('S003',))
                if self.check_s004(line):
                    self.mistakes[number + 1].add(('S004',))
                if self.check_s005(line):
                    self.mistakes[number + 1].add(('S005',))
                if self.check_s007(line):
                    self.mistakes[number + 1].add(('S007', self.check_s007(line)))
                if self.check_s008(line):
                    self.mistakes[number + 1].add(('S008', self.check_s008(line)))
                if self.check_s009(line):
                    self.mistakes[number + 1].add(('S009', self.check_s009(line)))
                # check_s006 inplace - without separate method
                if line == '\n':
                    logging.warning(r"line == '\n'")
                    logging.warning(number + 1)
                    empty_line_count += 1
                    logging.warning(f'empty_line_count: {empty_line_count}')
                    if empty_line_count > 2:
                        try:
                            logging.warning('empty_line_count > 2')
                            self.mistakes[number + 2].add(('S006',))
                            logging.debug(self.mistakes)
                            empty_line_count = 0
                        except KeyError as err:
                            logging.warning(err)
                            self.mistakes[number + 2] = set()
                            self.mistakes[number + 2].add(('S006',))
                            logging.debug(self.mistakes)
                            empty_line_count = 0
                else:
                    if 0 < empty_line_count < 3:
                        empty_line_count = 0
    
    def process_result(self):
        new_m = dict()
        for key, value in self.mistakes.items():
            if value:
                # new_m[key] = sorted(list(set(value)))
                new_m[key] = sorted(list(value))
        logging.debug(new_m)
        return new_m
    
    def print_sorted_results(self, file_):
        """File: Line X: Code Message"""
        logging.info("print_sorted_results")
        for lineno in sorted(self.mistakes.keys()):
            for error in self.mistakes[lineno]:
                if len(error) == 2:
                    logging.info('len(error) == 2:')
                    logging.debug(f'{file_}: Line {lineno}: {error}')
                    template = string.Template(self.messages[error[0]])
                    logging.debug(self.messages[error[0]])
                    logging.debug(template)
                    msg = template.substitute(name=error[1])
                    logging.info('template.substitute(name=error[1])')
                    logging.debug(f'msg: {msg}')
                    print(f'{file_}: Line {lineno}: {error[0]} {msg}')
                else:
                    print(f'{file_}: Line {lineno}: {error[0]} {self.messages[error[0]]}')
    
    def start(self) -> None:
        # PREPARATION
        if self.target.endswith('.py'):
            logging.info('case 1: file')
            files = [self.target, ]
        else:
            logging.info('case 2: directory')  # directory
            files = self.get_abs_names()
        logging.debug(f'files: {files}')
        # ANALYZING
        logging.info('ANALYZING')
        for file in sorted(files):
            logging.debug(file)
            self.check_file(file)
            self.check_ast_nodes(file)
            self.mistakes = self.process_result()
            # pprint(self.mistakes)
            self.print_sorted_results(file)
            self.mistakes = dict()


# TESTING input
# input_path = 'test\test_1.py'
# input_path = r'C:\Users\Тоша\PycharmProjects\FirstProject\test'
# input_path = '\test'
# input_path = '\task'
# target = input_path
logging.info('START')
# logging.debug(f'input: {input_path}')

target = target.replace('\t', '\\t')
target = target.replace('\a', '\\a')
logging.debug(f'target: {target}')

new = StaticCodeAnalyzer(target)

if __name__ == '__main__':
    new.start()
