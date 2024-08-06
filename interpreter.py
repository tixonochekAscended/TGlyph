# OFFICIAL T^ (T-GLYPH) PROGRAMMING LANGUAGE INTERPRETER
# P.S.: REMADE WITH CLASSES, AUTHOR: TIXONOCHEK, CONTRIBUTION: TEMA5002 (OR 5003)
import sys, os, re
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
                bypass: bool = False # ?: Should bypass file extension
                for arg in arguments:
                    arg: str = arg.upper()
                    if not (arg in cls._VALID_ARGS):
                        ErrorHandler.throw_error(53, arg)
                    match arg:
                        case "-B" | "-BYPASS":
                            bypass = True
                if os.path.isfile(file_name):
                    if bypass:
                        return file_name
                    if file_name.endswith(".tgl"): 
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
      54: "Unknown error. If you see this, please contact the developer."
    }
    
    @classmethod
    def throw_error(cls, error_id: int, *args: str) -> NoReturn:
        if ("~~~" in cls._ERRORS[error_id]) and (len(args) >= 1):
            cls._ERRORS[error_id] = cls._ERRORS[error_id].replace("~~~", args[0])
        print(f"\n{Utils.Colors._FAIL}[fatal error]{Utils.Colors._ENDC} Error ID: {error_id}")
        print(f"{Utils.Colors._CYAN}[i]{Utils.Colors._ENDC} {cls._ERRORS[error_id]}")
        sys.exit(-1)

class Token: 
   def __init__(self, type: str, value: Any) -> None:
      self.type: str = type
      self.value: Any = value
      self.full: tuple[str, Any] = (type, value)

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
          if glyph in f"\"'":
            token, j = cls._handle_string(script_text, j + 1)
            tokens.append(("string", token))
          elif glyph == ",":
            token, j = cls._handle_number(script_text, j + 1)
            tokens.append(("number", token))
          elif glyph == "[" and script_text[j:j+2] == "[*":
            m = COMMENT_RE.match(script_text, j)
            if m is None:
              ErrorHandler.throw_error(52)
            j = m.end()
          elif glyph == "*" and script_text[j:j+2] == "*]":
            ErrorHandler.throw_error(52)
          elif glyph not in "\n\r\t ":
            tokens.append(("glyph", glyph))
            j += 1
          else:
            j += 1
        return_tokens: list[Token] = []
        for tkn in tokens:
           return_tokens.append(Token(tkn[0], tkn[1]))
        return return_tokens

class Register:
    def __init__(self, name: str, data_type: str, default_value: Any):
        self._name: str = name
        self._data_type: str = data_type
        if data_type == "any":
            self._real_type = None
        self._value: Any = default_value
    
    def type(self) -> str:
        match self._data_type:
            case "any":
                if self._real_type is None:
                    return "any"
                return self._real_type
            case _:
                return self._data_type
    
    def value(self) -> Any:
        return self._value
    
    def set(self, new_value: Any, error_id: int = 54, bypass: bool = False) -> NoReturn:
        if isinstance(new_value, int):
            new_value = float(new_value)
        
        if isinstance(new_value, float):
            if self.type() == "any":
                self._real_type = "number"
                self._value = new_value
            elif self.type() == "const":
                if bypass:
                    self._value = new_value
                else:
                    ErrorHandler.throw_error(14)
            elif self.type() == "number":
                self._value = new_value
            else:
                ErrorHandler.throw_error(error_id)

        if isinstance(new_value, str):
            if self.type() == "any":
                self._real_type = "string"
                self._value = new_value
            elif self.type() == "string":
                self._value = new_value
            elif self.type() == "const":
               ErrorHandler.throw_error(14)
            else:
                ErrorHandler.throw_error(error_id)

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
       "@": 1,
       "+": 0,
       "-": 0,
       "/": 0,
       "*": 0,
       "`": 1,
       "~": 0,
       ":": 0,
       ">": 1,
       "<": 0
    }
    _regs: list[Register] = []
    _orig_regs: list[Register] = [] # Stores a deepcopy of the registers
    stack: list[(str, Any)] = []
    bookmarks: list[(str, int)] = []

    def __init__(self):
        # Create & append all of the TGlyph registers,
        # to the _regs list of Parser class;
        # create the stack & the bookmarks.
        self._regs.append(Register(name="MA", data_type="number", default_value=0.0))
        self._regs.append(Register(name="MB", data_type="number", default_value=0.0))
        self._regs.append(Register(name="TA", data_type="string", default_value=''))
        self._regs.append(Register(name="TB", data_type="string", default_value='\n'))
        self._regs.append(Register(name="FA", data_type="const", default_value=0.0))
        # The code below creates 26 universal registers (AA, AB .. AZ)
        for reg_name in [''.join(pair) for pair in itertools_product(ascii_uppercase, repeat=2) if pair[0] == 'A']:
            self._regs.append(Register(name=reg_name, data_type="any", default_value=0.0))
        self._orig_regs = copy_deepcopy(self._regs)

    def get_register(self, name: str, error_id: int = 54) -> Register:
        # This method finds & returns a Register
        # object by the Register's name.
        name = name.upper()
        found_register: Register = None
        for register in self._regs:
            if name == register._name:
                found_register = register
                break
        if found_register is None:
           ErrorHandler.throw_error(error_id)
        return found_register

    def _orig_get_register(self, name: str, error_id: int = 54) -> Register:
        # This method finds & returns an "ORIGINAL" Register
        # object by the Register's name.
        name = name.upper()
        found_register: Register = None
        for register in self._orig_regs:
            if name == register._name:
                found_register = register
                break
        if found_register is None:
           ErrorHandler.throw_error(error_id)
        return found_register
    
    def parse(self, tokens: list[Token]) -> NoReturn:
        j: int = 0
        ignore_mode: bool = False
        while j < len(tokens):

            current: Token = tokens[j]
            arguments: list[Token] = []
            if current.type == "glyph": # Get & append the arguments if they exist, if they dont throw an error that states this.
                if ignore_mode:
                    if current.value == ";":
                        ignore_mode = False
                        j += 1 
                        continue
                    j += 1 
                    continue      
                if not (current.value in self._NEEDED_ARGS.keys()):
                    ErrorHandler.throw_error(3)
                for k in range(1, self._NEEDED_ARGS[current.value]+1):
                    if not ((j+k) >= len(tokens)):
                        arguments.append(tokens[j+k])
                    else:
                        ErrorHandler.throw_error(4, current.value)
                # Execute each glyph (the actual interpretation of the code)
                match current.value:
                    case '^':
                        if not (arguments[0].type == "string"):
                            ErrorHandler.throw_error(5)
                        desired_register: Register = self.get_register(arguments[0].value, 7)
                        desired_register.set(arguments[1].value, 6)
                    case "&":
                        if not (arguments[0].type == "string") or not (arguments[1].type == "string"):
                            ErrorHandler.throw_error(21)
                        to_register: Register = self.get_register(arguments[0].value, 22)
                        from_register: Register = self.get_register(arguments[1].value, 22)
                        if to_register.type() != from_register.type():
                           ErrorHandler.throw_error(23)
                        to_register.set(from_register.value(), 23)
                    case '$':
                        print(self.get_register("TA").value(), end=self.get_register("TB").value())
                    case '#':
                        if not (arguments[0].type == "string"):
                            ErrorHandler.throw_error(8)
                        self.bookmarks.append((arguments[0].value.upper(), j))
                    case '!':
                        if not (arguments[0].type == "string"):
                            ErrorHandler.throw_error(10)
                        found_bk_j: int = None
                        for bookmark in self.bookmarks:
                           if arguments[0].value.upper() == bookmark[0]:
                              found_bk_j = bookmark[1]
                              break
                        if found_bk_j is None:
                           ErrorHandler.throw_error(12)
                        j = found_bk_j
                        continue
                    case ';':
                        ignore_mode = True
                    case '=':
                        if not (arguments[0].type == "string") or not (arguments[1].type == "string"):
                            ErrorHandler.throw_error(18)
                        first_to_compare: Register = self.get_register(arguments[0].value, 19)
                        second_to_compare: Register = self.get_register(arguments[1].value, 19)
                        flag_register: Register = self.get_register("FA")
                        flag_register.set(int((first_to_compare.type(), first_to_compare.value()) == (second_to_compare.type(), second_to_compare.value())), bypass=True)
                    case '(':
                        if not (arguments[0].type == "string") or not (arguments[1].type == "string"):
                            ErrorHandler.throw_error(36)
                        first_to_compare: Register = self.get_register(arguments[0].value, 37)
                        second_to_compare: Register = self.get_register(arguments[1].value, 37)
                        flag_register: Register = self.get_register("FA")
                        flag_register.set(int(first_to_compare.type() == second_to_compare.type()), bypass=True)
                    case ')':
                        if not (arguments[0].type == "string") or not (arguments[1].type == "string"):
                            ErrorHandler.throw_error(40)
                        first_to_compare: Register = self.get_register(arguments[0].value, 41)
                        second_to_compare: Register = self.get_register(arguments[1].value, 41)
                        flag_register: Register = self.get_register("FA")
                        flag_register.set(int(first_to_compare.value() == second_to_compare.value()), bypass=True)
                    case '@':
                        if not (arguments[0].type == "glyph"):
                            ErrorHandler.throw_error(16)
                        if not self.get_register("FA").value():
                           j += 2
                           continue
                    case '+':
                        self.get_register("MA").set((
                           self.get_register("MA").value() + self.get_register("MB").value()
                        ))
                    case '-':
                        self.get_register("MA").set((
                           self.get_register("MA").value() - self.get_register("MB").value()
                        ))
                    case '*':
                        self.get_register("MA").set((
                           self.get_register("MA").value() * self.get_register("MB").value()
                        ))
                    case '/':
                        self.get_register("MA").set((
                           self.get_register("MA").value() / self.get_register("MB").value()
                        ))
                    case '~':
                      self.get_register("TA").set(str(self.get_register("MA").value()))
                    case ':':
                        try: self.get_register("MA").set(float(self.get_register("TA").value()))
                        except: ErrorHandler.throw_error(44)
                    case '`':
                        if not (arguments[0].type == "string"):
                            ErrorHandler.throw_error(34)
                        self.get_register(arguments[0].value, 35).set(copy_deepcopy(
                           self._orig_get_register(arguments[0].value, 35).value()
                        ))
                    case '>':
                        if not (arguments[0].type == "string"):
                            ErrorHandler.throw_error(46)
                        register_to_push = self.get_register(arguments[0].value, 47)
                        if register_to_push.type() == "const":
                           ErrorHandler.throw_error(48)
                        self.stack.append((arguments[0].value, register_to_push.value()))
                    case '<':
                        popped = self.stack.pop(0)
                        related_register: Register = self.get_register(popped[0])
                        related_register.set(popped[1])
            j += 1

def main() -> NoReturn:
    script_name = Utils.check_app_args(sys.argv)
    script_text: str
    with open(script_name, encoding="UTF-8") as file:
        script_text = file.read()
    tokens = Lexer.divide_glyphs(script_text)
    tglyph_parser = Parser()
    tglyph_parser.parse(tokens)

if __name__ == "__main__":
    main()
