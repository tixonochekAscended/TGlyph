"""
OFFICIAL T^ (T-GLYPH) PROGRAMMING LANGUAGE INTERPRETER
P.S.: REMADE WITH CLASSES, AUTHOR: TIXONOCHEK, CONTRIBUTION: TEMA5002
GPL-3.0 LICENSE, CHECK GITHUB FOR MORE INFORMATION !!!
"""
import sys, os, re, random
from enum import Enum
from typing import NoReturn, Optional, Any
from itertools import product as itertools_product
from string import ascii_uppercase
from copy import deepcopy as copy_deepcopy

class Utils:
    class Colors:
        _HEADER = '\033[95m'
        _BLUE = '\033[94m'
        _CYAN = '\033[96m'
        _GREEN = '\033[92m'
        _WARNING = '\033[93m'
        _FAIL = '\033[91m'
        _ENDC = '\033[0m'
        _BOLD = '\033[1m'
        _UNDERLINE = '\033[4m'
    
    _VALID_ARGS = ('-B', '-BYPASS')

    @classmethod
    def check_app_args(cls, arguments: list[str]) -> Optional[str]:
        arguments.pop(0)
        match len(arguments):
            case 0:
                # Throw an error that there isn't a file provided
                # that needs to be executed.
                ErrorHandler.throw_error(2)
            case 1:
                # Check the ending of the file name provided.
                file_name: str = arguments.pop(0)
                if os.path.isfile(file_name):
                    if file_name.endswith(".tgl"): 
                        return file_name
                    ErrorHandler.throw_error(0)
                ErrorHandler.throw_error(1)
            case _:
                # Check the ending of the file name provided, then
                # check all of the remaining arguments, and handle
                # special ones like -B (a.k.a. -bypass).
                # If an invalid additional argument is found, throw
                # an error that states this.
                file_name: str = arguments.pop(0)
                arguments = map(lambda x: x.upper(), arguments)
                bypass: bool = any(x in ["-B", "-BYPASS"] for x in arguments) # ?: Should bypass file extension
                for arg in arguments:
                    if arg not in cls._VALID_ARGS:
                        ErrorHandler.throw_error(53, arg)
                if os.path.isfile(file_name):
                    if bypass or file_name.endswith(".tgl"): 
                        return file_name
                    ErrorHandler.throw_error(0)
                ErrorHandler.throw_error(1)
class ErrorHandler:
    _ERRORS: dict[int, str] = {
        0: "Unsupported file type. If you would like to bypass the file type, provide \"-B\" or \"-bypass\" in the application arguments.",
        1: "File you provided as a script does not exist. Perhaps you made a typo?",
        2: "You haven't provided any application arguments, therefore there is no file to run and process.\n"
           "Usage: py interpreter.py <tgl file> (-B/-bypass)",
        3: "Unknown glyph contained in the code.",
        4: "Not enough values provided for the ~~~ glyph. Check github page for more information about the needed amount and the types.",
        5: "The first value provided to the bind glyph (^) must be a string symbolising the name of a certain register.",
        6: "You provided a wrong type of value to the register via the bind glyph (^).",
        7: "Register you provided via the bind glyph (^) does not exist.",
        8: "The value provided to the bookmark glyph (#) must be a string symbolising a bookmark name.",
        10: "The value provided to the jump glyph (!) must be a string symbolising a bookmark name that the program will jump to.",
        12: "The bookmark you tried to jump to does not exist.",
        14: "You can't assign values to constant, read-only registers (f.e. flags).",
        16: "After a when glyph (@) there should be another glyph, not something else.",
        17: "The expression inside one of the commas cannot be evaluated as a number, and might be a text. Usage of any mathematical operations inside also leads to this error. Perhaps you made a typo?",
        18: "The values provided to the direct comparison glyph (=) must be strings, symbolising name of the registers that the glyph should compare.",
        19: "Register you tried to compare via the direct comparison glyph (=) does not exist (at least one of the provided ones).",
        21: "The values provided to the register match glyph (&) must be strings, symbolising the names of the registers to perform the assign operation on.",
        22: "Register you tried to operate on via the register match glyph (&) does not exist (at least one of the provided ones).",
        23: "You tried to provide a wrong type of value to the register via the register match glyph (&).",
        24: "The value provided to the add glyph (+) must be a number, so it can be added to the MA register.",
        26: "The value provided to the subtract glyph (-) must be a number, so it can be subtracted from the MA register.",
        28: "The value provided to the divide glyph (/) must be a number, so the division can be done.",
        30: "The value provided to the multiply glyph (*) must be a number, so the multiplication can be done.",
        32: "Math evaluation error. This error may happen if you divide by 0, or the numbers you tried to perform operations on got too large for the language to handle. There are more possible causes for this error.",
        34: "The value provided for the register reset glyph (`) must be a string, symbolising the name of a register that needs to be reset.",
        35: "The register you tried to reset via the register reset glyph (`) does not exist.",
        36: "The values provided for the type comparison glyph \"(\" must be strings, symbolising the names of the registers.",
        37: "The register you tried to compare via the type comparison glyph \"(\" does not exist (at least one of the provided ones).",
        39: "You can't compare a constant, read-only flag via the type comparison glyph \"(\". ",
        40: "The values provided for the value comparison glyph \")\" must be strings, symbolising the names of the registers.",
        41: "The register you tried to compare via the value comparison glyph \")\" does not exist (at least one of the provided ones).",
        44: "Couldn't convert the provided text in the TA register into a float and store it in the MA register via STN-convert glyph (:)",
        46: "The value provided to the push glyph (>) must be a string, symbolising a name of the register that is being pushed to the stack.",
        47: "The register you tried to push onto the stack does not exist.",
        48: "You can't push a constant, read-only flag onto the stack.",
        49: "Invalid escape sequence in a string",
        50: "Unterminated string literal.",
        51: "Unterminated number literal.",
        52: "Unterminated comment.",
        53: "This application argument you provided does not exist: ~~~",
        54: "Unknown error. If you see this, please contact the developer.",
        55: "The values provided for < (less than) comparison glyph (|) must be strings, symbolising the names of the registers.",
        56: "The register you tried to compare via the < (less than) comparison glyph (|) does not exist (at least one of the provided ones).",
        57: "The registers you tried to compare via the < (less than) comparison glyph (|) must both be registers that are numerical (store numbers currently)."
    }
    
    @classmethod
    def throw_error(cls, error_id: int, *args: str) -> NoReturn:
        if error_id == -1:
            print(f"{Utils.Colors._BOLD}{Utils.Colors._GREEN}Keyboard Interrupt, exiting the program...{Utils.Colors._ENDC}")
            sys.exit(-1)
        if ("~~~" in cls._ERRORS[error_id]) and (len(args) >= 1):
            cls._ERRORS[error_id] = cls._ERRORS[error_id].replace("~~~", args[0])
        print(f"\n{Utils.Colors._FAIL}[fatal error]{Utils.Colors._ENDC} Error ID: {error_id}")
        print(f"{Utils.Colors._CYAN}[i]{Utils.Colors._ENDC} {cls._ERRORS[error_id]}")
        sys.exit(-1)

class TokenType(Enum):
    STRING = 0
    NUMBER = 1
    GLYPH = 2

class Token: 
    def __init__(self, type: TokenType, value: Any) -> None:
        self.type: TokenType = type
        self.value: Any = value

    def __repr__(self) -> str:
        return f"Token({self.type}) = {self.value}"

class Lexer:
    _BACKSLASH = {
        "\"": "\"", "'": "'", "\\": "\\", "/": "/",
        "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t"
    }
    
    def _decode_uXXXX(s: str, pos: int) -> int:
        esc = s[pos + 1:pos + 5]
        if len(esc) == 4 and esc[1].lower() != "x":
            try:
                return int(esc, 16)
            except ValueError:
                pass
        ErrorHandler.throw_error(49)
    
    @classmethod
    def _handle_string(cls, s: str, index: int) -> tuple[str, int]:
        new_text = ""
        STRINGCHUNK = re.compile(f"(.*?)([\"'\\\\\\x00-\\x1f])", re.VERBOSE | re.MULTILINE | re.DOTALL)
        while True:
            chunk = STRINGCHUNK.match(s, index)
            if chunk is None:
                ErrorHandler.throw_error(50)
            index = chunk.end()
            content, terminator = chunk.groups()
            if content:
                new_text += content
            if terminator in "\"'":
                break
            if terminator != "\\":
                ErrorHandler.throw_error(49)
            if index > len(s):
                ErrorHandler.throw_error(49)
            esc = s[index]

            if esc != "u":
                if esc not in cls._BACKSLASH:
                    ErrorHandler.throw_error(49)
                new_text += cls._BACKSLASH[esc]
                index += 1
            else:
                uni = cls._decode_uXXXX(s, index)
                index += 5
                if 0xd800 <= uni <= 0xdbff and s[index:index + 2] == '\\u':
                    uni2 = cls._decode_uXXXX(s, index + 1)
                    if 0xdc00 <= uni2 <= 0xdfff:
                        uni = 0x10000 + (((uni - 0xd800) << 10) | (uni2 - 0xdc00))
                        index += 6
                new_text += chr(uni)
        return new_text, index

    def _handle_number(s: str, index: int) -> tuple[float, int]:
        NUMBER_RE = re.compile(
            r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
            (re.VERBOSE | re.MULTILINE | re.DOTALL)
        )
        m = NUMBER_RE.match(s, index)
        if m is None:
            ErrorHandler.throw_error(17)
        index = m.end()
        if s[index:index+1] != ",":
            ErrorHandler.throw_error(51)
        integer, frac, exp = m.groups()
        return float(integer + (frac or '') + (exp or '')), index + 1

    @classmethod
    def divide_glyphs(cls, script_text: str) -> list[Token]:
        COMMENT_RE = re.compile(f"(.*?)(\\*])", re.VERBOSE | re.MULTILINE | re.DOTALL)
        tokens: list[tuple[str, Any]] = []
        j = 0
        while j < len(script_text):
            glyph = script_text[j]
            if glyph in "\"'":
                token, j = cls._handle_string(script_text, j + 1)
                tokens.append((TokenType.STRING, token))
            elif glyph == ",":
                token, j = cls._handle_number(script_text, j + 1)
                tokens.append((TokenType.NUMBER, token))
            elif glyph == "[" and script_text[j:j+2] == "[*": # slices instead of index to prevent IndexError
                m = COMMENT_RE.match(script_text, j)
                if m is None:
                    ErrorHandler.throw_error(52)
                j = m.end()
            elif glyph == "*" and script_text[j:j+2] == "*]":
                ErrorHandler.throw_error(52)
            elif glyph not in "\n\r\t ":
                tokens.append((TokenType.GLYPH, glyph))
                j += 1
            else:
                j += 1
        return_tokens: list[Token] = [Token(type, value) for type, value in tokens]
        return return_tokens

class RegisterType(Enum):
    STRING = 1
    NUMBER = 2
    ANY = 3
    CONST = 4

class Register:
    def __init__(self, name: str, data_type: RegisterType, default_value: Any):
        self._name: str = name
        self._data_type: str = data_type
        if data_type == RegisterType.ANY:
            self._real_type = RegisterType.NUMBER
        self._value: Any = default_value
        self._default_value: Any = default_value
    
    @property
    def type(self) -> str:
        match self._data_type:
            case RegisterType.ANY:
                return self._real_type or RegisterType.ANY
            case _:
                return self._data_type
    
    @property
    def value(self) -> Any:
        return self._value
    
    def set(self, new_value: Any, error_id: int = 54, bypass: bool = False) -> None:
        if isinstance(new_value, (int, float)):
            new_value = float(new_value)
            if self.type == RegisterType.ANY:
                self._real_type = RegisterType.NUMBER
                self._value = new_value
            elif self.type == RegisterType.CONST:
                if not bypass:
                    ErrorHandler.throw_error(14)
                self._value = new_value               
            elif self.type == RegisterType.NUMBER:
                self._value = new_value
            else:
                ErrorHandler.throw_error(error_id)

        elif isinstance(new_value, str):
            if self.type == RegisterType.ANY:
                self._real_type = RegisterType.STRING
                self._value = new_value
            elif self.type == RegisterType.STRING:
                self._value = new_value
            elif self.type == RegisterType.CONST:
                ErrorHandler.throw_error(14)
            else:
                ErrorHandler.throw_error(error_id)

    def reset(self):
        self._value = self._default_value

    def __eq__(self, v):
        return self.type == v.type and self.value == v.value

class Parser:
    _NEEDED_ARGS = {
       "^": 2,
       "&": 2,
       "$": 0,
       "#": 1,
       "!": 1,
       ";": 0,
       "=": 2,
       "(": 2,
       ")": 2,
       "|": 2,
       "@": 1,
       "+": 0,
       "-": 0,
       "/": 0,
       "*": 0,
       "%": 0,
       "`": 1,
       "~": 0,
       ":": 0,
       ">": 1,
       "<": 0
    }
    _regs: list[Register] = []
    stack: list[(str, Any)] = []
    bookmarks: dict[str, int] = {}

    def __init__(self):
        """
        Create & append all of the TGlyph registers,
        to the _regs list of Parser class
        """
        # This code creates 26 universal registers
        self._regs = [Register("A" + letter, RegisterType.ANY, 0.0) for letter in ascii_uppercase]
        self._regs.append(Register("MA", RegisterType.NUMBER, 0.0))
        self._regs.append(Register("MB", RegisterType.NUMBER, 0.0))
        self._regs.append(Register("TA", RegisterType.STRING, ''))
        self._regs.append(Register("TB", RegisterType.STRING, '\n'))
        self._regs.append(Register("FA", RegisterType.CONST, 0.0))
        self._regs.append(Register("FB", RegisterType.CONST, 1.0))

    def get_register(self, name: str, error_id: int = 54) -> Register:
        """
        Finds & returns Register by the Register's name.
        """
        name = name.upper()
        for register in self._regs:
            if name == register._name:
                return register
        ErrorHandler.throw_error(error_id)

    def parse(self, tokens: list[Token]) -> None:
        j: int = 0
        ignore_mode: bool = False
        while j < len(tokens):
            self.get_register("FB").set(random.randint(1, 100), bypass=True)
            current: Token = tokens[j]
            if current.type == TokenType.GLYPH: # Get & append the arguments if they exist, if they dont throw an error that states this.
                if ignore_mode:
                    ignore_mode = current.value != ";"
                    j += 1
                    continue     
                if current.value not in self._NEEDED_ARGS:
                    ErrorHandler.throw_error(3)
                arguments: list[Token] = tokens[j+1:j+1+self._NEEDED_ARGS[current.value]] # Get arguments using slices to prevent IndexError
                if len(arguments) < self._NEEDED_ARGS[current.value]:
                    ErrorHandler.throw_error(4, current.value)
                # Execute each glyph (the actual interpretation of the code)
                match current.value:
                    case '^':
                        if arguments[0].type != TokenType.STRING:
                            ErrorHandler.throw_error(5)
                        desired_register: Register = self.get_register(arguments[0].value, 7)
                        desired_register.set(arguments[1].value, 6)
                    case "&":
                        if any(arg.type != TokenType.STRING for arg in [arguments[0], arguments[1]]):
                            ErrorHandler.throw_error(21)
                        to_register: Register = self.get_register(arguments[0].value, 22)
                        from_register: Register = self.get_register(arguments[1].value, 22)
                        to_register.set(from_register.value, 23)
                    case '$':
                        print(self.get_register("TA").value, end=self.get_register("TB").value)
                    case '#':
                        if arguments[0].type != TokenType.STRING:
                            ErrorHandler.throw_error(8)
                        self.bookmarks[arguments[0].value.upper()] = j
                    case '!':
                        if arguments[0].type != TokenType.STRING:
                            ErrorHandler.throw_error(10)
                        bookmark_name: str = arguments[0].value.upper()
                        if bookmark_name not in self.bookmarks:
                            ErrorHandler.throw_error(12)
                        j = self.bookmarks[bookmark_name]
                    case ';':
                        ignore_mode = True
                    case '=':
                        if any(arg.type != TokenType.STRING for arg in [arguments[0], arguments[1]]):
                            ErrorHandler.throw_error(18)
                        first_to_compare: Register = self.get_register(arguments[0].value, 19)
                        second_to_compare: Register = self.get_register(arguments[1].value, 19)
                        flag_register: Register = self.get_register("FA")
                        flag_register.set(int(first_to_compare == second_to_compare), bypass=True)
                    case '(':
                        if any(arg.type != TokenType.STRING for arg in [arguments[0], arguments[1]]):
                            ErrorHandler.throw_error(36)
                        first_to_compare: Register = self.get_register(arguments[0].value, 37)
                        second_to_compare: Register = self.get_register(arguments[1].value, 37)
                        flag_register: Register = self.get_register("FA")
                        flag_register.set(int(first_to_compare.type == second_to_compare.type), bypass=True)
                    case ')':
                        if any(arg.type != TokenType.STRING for arg in [arguments[0], arguments[1]]):
                            ErrorHandler.throw_error(40)
                        first_to_compare: Register = self.get_register(arguments[0].value, 41)
                        second_to_compare: Register = self.get_register(arguments[1].value, 41)
                        flag_register: Register = self.get_register("FA")
                        flag_register.set(int(first_to_compare.value == second_to_compare.value), bypass=True)
                    case '|':
                        if any(arg.type != TokenType.STRING for arg in [arguments[0], arguments[1]]):
                            ErrorHandler.throw_error(55)
                        first_to_compare: Register = self.get_register(arguments[0].value, 56)
                        second_to_compare: Register = self.get_register(arguments[1].value, 56)
                        if not (first_to_compare.type == RegisterType.NUMBER) or not (second_to_compare.type == RegisterType.NUMBER):
                            ErrorHandler.throw_error(57)
                        flag_register: Register = self.get_register("FA")
                        flag_register.set(int(first_to_compare.value < second_to_compare.value), bypass=True)
                    case '@':
                        if arguments[0].type != TokenType.GLYPH:
                            ErrorHandler.throw_error(16)
                        if not self.get_register("FA").value:
                           j += 2
                           continue
                    case '+':
                        self.get_register("MA").set(
                           self.get_register("MA").value + self.get_register("MB").value
                        )
                    case '-':
                        self.get_register("MA").set(
                           self.get_register("MA").value - self.get_register("MB").value
                        )
                    case '*':
                        self.get_register("MA").set(
                           self.get_register("MA").value * self.get_register("MB").value
                        )
                    case '/':
                        self.get_register("MA").set(
                           self.get_register("MA").value / self.get_register("MB").value
                        )
                    case '%':
                        self.get_register("MA").set(
                           self.get_register("MA").value % self.get_register("MB").value
                        )
                    case '~':
                        self.get_register("TA").set(str(self.get_register("MA").value).removesuffix(".0"))
                    case ':':
                        try:
                            self.get_register("MA").set(float(self.get_register("TA").value))
                        except ValueError:
                            ErrorHandler.throw_error(44)
                    case '`':
                        if arguments[0].type != TokenType.STRING:
                            ErrorHandler.throw_error(34)
                        self.get_register(arguments[0].value, 35).reset()
                    case '>':
                        if arguments[0].type != TokenType.STRING:
                            ErrorHandler.throw_error(46)
                        register_to_push = self.get_register(arguments[0].value, 47)
                        if register_to_push.type == RegisterType.CONST:
                            ErrorHandler.throw_error(48)
                        self.stack.append((arguments[0].value, register_to_push.value))
                    case '<':
                        popped = self.stack.pop(0)
                        self.get_register(popped[0]).set(popped[1])
            j += 1

def main() -> None:
    script_name = Utils.check_app_args(sys.argv)
    try:
        with open(script_name, encoding="UTF-8") as file:
            script_text: str = file.read()
    except OSError as e:
        print(f"Can't read file: {e}")
    tokens = Lexer.divide_glyphs(script_text)
    try:
        Parser().parse(tokens)
    except KeyboardInterrupt:
        ErrorHandler.throw_error(-1)
    except Exception as e:
        raise e

if __name__ == "__main__":
    main()
