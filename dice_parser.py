"""This module includes all of the tools used to interpret dice statements.
With this, you should be able to interpret complex dice roll statements.
"""
from random import randint


INTEGER = 'INTEGER'
EOF = 'EOF'
ADD, SUB = 'ADD', 'SUB'
KEEP, DROP = 'KEEP', 'DROP'
LOW, HIGH = 'LOW', 'HIGH'
REPEAT = 'REPEAT'
DICE = 'DICE'

SYMBOLS = {
    '+': ADD,
    '-': SUB,
    'k': KEEP,
    'x': DROP,
    'l': LOW,
    'h': HIGH,
    'r': REPEAT,
    'd': DICE
}


class Token:
    """Class to represent a single token in the statement.
    This can be a value or an operator, and it has a type and a value.
    For operators, this value is just the symbol used to represent it.
    """

    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __str__(self):
        return f"{self.type}: {self.value}"

    def __repr__(self):
        return self.__str__()


class Lexer:
    """The lexer converts all lexemes in the given string to tokens.
    This includes operators and values. This also strips whitespace and such.
    """

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self, message):
        raise Exception(
            f"Lexer error: '{message}' in statement `{self.text}` at position {self.pos}")

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char in SYMBOLS.keys():
                tok = Token(SYMBOLS[self.current_char], self.current_char)
                self.advance()
                return tok

            self.error(f"Unexpected character {self.current_char}")

        return Token(EOF, EOF)


class Parser:
    """This parses the statement and executes it, step by step.
    It uses the Lexer class to tokenize the expression, and then uses the tokens to execute the statement.
    """

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message):
        raise Exception(
            f'Parsing error: {message} around {self.current_token}')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(
                f"Unexpected token {self.current_token}, expected {token_type}")

    def num(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def dice(self):
        self.eat(DICE)
        return self.num()

    def roll(self):
        number = 1
        if self.current_token.type == INTEGER:
            number = self.num()
        return (self.dice(), number)

    def keep_drop(self):
        operation = ""
        if self.current_token.type == KEEP:
            operation = KEEP
            self.eat(KEEP)
        elif self.current_token.type == DROP:
            operation = DROP
            self.eat(DROP)
        side = ""
        if self.current_token.type == LOW:
            side = LOW
            self.eat(LOW)
        elif self.current_token.type == HIGH:
            side = HIGH
            self.eat(HIGH)
        number = self.num()
        return (operation, side, number)

    def add_sub(self):
        operation = ""
        if self.current_token.type == ADD:
            operation = ADD
            self.eat(ADD)
        elif self.current_token.type == SUB:
            operation = SUB
            self.eat(SUB)
        number = self.num()
        return (operation, number)

    def mod(self):
        mod = None
        if self.current_token.type in (KEEP, DROP):
            mod = self.keep_drop()
        elif self.current_token.type in (ADD, SUB):
            mod = self.add_sub()
        return mod

    def set(self):
        roll = self.roll()
        mods = []
        while self.current_token.type in (KEEP, DROP, ADD, SUB):
            mods.append(self.mod())
        return (roll, mods)

    def expr(self):
        set = self.set()
        repeat = 1
        if self.current_token.type == REPEAT:
            self.eat(REPEAT)
            repeat = self.num()
        self.eat(EOF)
        return (set, repeat)


class Interpreter:
    def __init__(self, text):
        self.parser = Parser(Lexer(text))

    def interpret(self):
        expr = self.parser.expr()
        return self.exec_expr(expr)

    def exec_expr(self, expr):
        return [self.exec_term(expr[0]) for _ in range(0, expr[1])]

    def exec_term(self, term):
        rolls = sorted(self.exec_roll(term[0]))
        dropped = []
        total_to_add = 0
        for mod in term[1]:
            if mod[0] == DROP:
                if mod[1] == LOW:
                    dropped += rolls[:mod[2]]
                    rolls = rolls[mod[2]:]
                elif mod[1] == HIGH:
                    dropped += rolls[len(rolls)-mod[2]:]
                    rolls = rolls[:len(rolls)-mod[2]]
            elif mod[0] == KEEP:
                if mod[1] == LOW:
                    dropped += rolls[mod[2]:]
                    rolls = rolls[:mod[2]]
                elif mod[1] == HIGH:
                    dropped += rolls[:len(rolls)-mod[2]]
                    rolls = rolls[len(rolls)-mod[2]:]
            elif mod[0] == ADD:
                total_to_add += mod[1]
            elif mod[0] == SUB:
                total_to_add -= mod[1]
        result = sum(rolls) + total_to_add
        return (rolls, dropped, total_to_add, result)

    def exec_roll(self, roll):
        sides, num = roll
        return [randint(1, sides) for _ in range(0, num)]


if __name__ == "__main__":
    print(Interpreter("4d6xl1r6").interpret())
