import sys
import copy
import os
import re
from typing import NoReturn, Any

ERRORS: dict[int, str] = {
  0: "Unsupported file type. If you would like to bypass the file type, provide \"-B\" or \"-bypass\" in (application) arguments.",
  1: "File you provided as a script does not exist. Perhaps you made a typo?",
  2: "You haven't provided any (application) arguments, therefore there is no file to run and process.",
  3: "Unknown glyph contained in the code.",
  4: "Not enough values provided for the bind glyph (^).",
  5: "The first value provided to the bind glyph (^) must be a string symbolising the name of a certain register.",
  6: "You provided a wrong type of value to the register via the bind glyph (^).",
  7: "Register you provided via the bind glyph (^) does not exist.",
  8: "The value provided to the bookmark glyph (#) must be a string symbolising a bookmark name.",
  9: "Not enough values provided for the bookmark glyph (#).",
  10: "The value provided to the jump glyph (!) must be a string symbolising a bookmark name that the program will jump to.",
  11: "Not enough values provided for the jump glyph (!).",
  12: "The bookmark you tried to jump to does not exist.",
  13: "Not enough values provided for the direct comparison glyph (=).",
  14: "You can't assign values to constant, read-only registers (f.e. flags).",
  15: "Not enough values provided for the when glyph (@)",
  16: "After a when glyph (@) there should be another glyph, not something else.",
  17: "The expression inside one of the commas cannot be evaluated as a number, and might be a text. Usage of any mathematical operations inside also leads to this error. Perhaps you made a typo?",
  18: "The values provided to the direct comparison glyph (=) must be strings, symbolising name of the registers that the glyph should compare.",
  19: "Register you tried to compare via the direct comparison glyph (=) does not exist (at least one of the provided ones).",
  20: "Not enough values provided for the register match glyph (&)",
  21: "The values provided to the register match glyph (&) must be strings, symbolising the names of the registers to perform the assign operation on.",
  22: "Register you tried to operate on via the register match glyph (&) does not exist (at least one of the provided ones).",
  23: "You tried to provide a wrong type of value to the register via the register match glyph (&).",
  24: "The value provided to the add glyph (+) must be a number, so it can be added to the MA register.",
  25: "Not enough values provided for the add glyph (+).",
  26: "The value provided to the subtract glyph (-) must be a number, so it can be subtracted from the MA register.",
  27: "Not enough values provided for the subtract glyph (-).",
  28: "The value provided to the divide glyph (/) must be a number, so the division can be done.",
  29: "Not enough values provided for the divide glyph (/).",
  30: "The value provided to the multiply glyph (*) must be a number, so the multiplication can be done.",
  31: "Not enough values provided for the multiply glyph (*).",
  32: "Math evaluation error. This error may happen if you divide by 0, or the numbers you tried to perform operations on got too large for the language to handle. There are more possible causes for this error.",
  33: "Not enough values provided for the register reset glyph (`).",
  34: "The value provided for the register reset glyph (`) must be a string, symbolising the name of a register that needs to be reset.",
  35: "The register you tried to reset via the register reset glyph (`) does not exist.",
  36: "The values provided for the type comparison glyph \"(\" must be strings, symbolising the names of the registers.",
  37: "The register you tried to compare via the type comparison glyph \"(\" does not exist (at least one of the provided ones).",
  38: "Not enough values provided for the type comparison glyph \"(\".",
  39: "You can't compare a constant, read-only flag via the type comparison glyph \"(\". ",
  40: "The values provided for the value comparison glyph \")\" must be strings, symbolising the names of the registers.",
  41: "The register you tried to compare via the value comparison glyph \")\" does not exist (at least one of the provided ones).",
  43: "You can't compare a constant, read-only flag via the value comparison glyph \")\".",
  44: "Couldn't convert the provided text in the TA register into a float and store it in the MA register via STN-convert glyph (:)",
  45: "Not enough values provided for the push glyph (>).",
  46: "The value provided to the push glyph (>) must be a string, symbolising a name of the register that is being pushed to the stack.",
  47: "The register you tried to push onto the stack does not exist.",
  48: "You can't push a constant, read-only flag onto the stack."
}


def tglError(_id: int) -> NoReturn:
  print()
  print("program ended with an error (ID: %s): " % _id)
  print(ERRORS[_id])
  sys.exit(-1)


def runCode(args: list[str]):
  args.pop(0)
  if not args[0].endswith(".tgl") and "-B" not in args and "-bypass" not in args:
    tglError(0)
  if not (os.path.exists(args[0]) and os.path.isfile(args[0])):
    tglError(1)
  with open(args[0], encoding="UTF-8") as f:
    allGlyphs = f.read()
  dividedGlyphs: list[tuple[str, Any]] = []
  scIndex = 0
  glyphLookS = False
  glyphLookI = False
  for j, glyph in enumerate(allGlyphs):
    if glyph in "\"'" and not glyphLookI and not glyphLookS:
      scIndex = j
      glyphLookS = True
    elif glyph == "," and not glyphLookS and not glyphLookI:
      scIndex = j
      glyphLookI = True

    elif glyphLookI:
      if glyph == ",":
        glyphLookI = False
        try:
          dividedGlyphs.append(("number", float(allGlyphs[scIndex + 1:j])))
        except:
          tglError(17)
        scIndex = 0
    elif glyphLookS and glyph in "\"'":
      glyphLookS = False
      dividedGlyphs.append(("string", allGlyphs[scIndex + 1:j]))
      scIndex = 0
    elif not (glyphLookS or glyphLookI) and glyph not in "\n\r\t ":
      dividedGlyphs.append(("glyph", glyph))

  # ----------------------------------
  # Declaration of important variables
  registers: dict[str, list[str, int]] = {
    "MA": ["number", 0],
    "MB": ["number", 0],
    "TA": ["string", ''],
    "TB": ["string", '\n'],
    "FA": ["const", 0],
    "AA": ["any", 0], "AB": ["any", 0], "AC": ["any", 0], "AD": ["any", 0],
    "AE": ["any", 0], "AF": ["any", 0], "AG": ["any", 0], "AH": ["any", 0],
    "AI": ["any", 0], "AJ": ["any", 0], "AK": ["any", 0], "AL": ["any", 0],
    "AM": ["any", 0], "AN": ["any", 0], "AO": ["any", 0], "AP": ["any", 0],
    "AQ": ["any", 0], "AR": ["any", 0], "AS": ["any", 0], "AT": ["any", 0],
    "AU": ["any", 0], "AV": ["any", 0], "AW": ["any", 0], "AX": ["any", 0],
    "AY": ["any", 0], "AZ": ["any", 0]
  }
  origRegisters = copy.deepcopy(registers)
  bookmarks = {}
  stack = []
  # ----------------------------------
  j = 0
  ignoreMode = False
  while j < len(dividedGlyphs):
    actionType = dividedGlyphs[j][0]
    actionValue = dividedGlyphs[j][1]
    if ignoreMode:
      if actionType == "glyph" and actionValue == ";":
        ignoreMode = False
        j += 1
        continue
      else:
        j += 1
        continue
    nextActionType = None
    nextActionValue = None
    doubleActionType = None
    doubleActionValue = None
    if not (j + 1 >= len(dividedGlyphs)):
      nextActionType = dividedGlyphs[j + 1][0]
      nextActionValue = dividedGlyphs[j + 1][1]
    if not (j + 2 >= len(dividedGlyphs)):
      doubleActionType = dividedGlyphs[j + 2][0]
      doubleActionValue = dividedGlyphs[j + 2][1]

    if actionType not in ["string", "number"]:
      match actionValue:
        case "^":
          if nextActionValue is None or doubleActionValue is None:
            tglError(4)
          if nextActionType != "string":
            tglError(5)
          nextActionValue = nextActionValue.upper()
          if nextActionValue not in registers:
            tglError(7)
          if registers[nextActionValue][0] == "const":
            tglError(14)
          if registers[nextActionValue][0] == "any":
            registers[nextActionValue][1] = (doubleActionType, doubleActionValue)
          else:
            if doubleActionType != registers[nextActionValue][0]:
              tglError(6)

            # ----------------------------------
            # Assign value to a register via equal sign
            registers[nextActionValue][1] = doubleActionValue
            # ----------------------------------
        case "&":
          if nextActionValue is None or doubleActionValue is None:
            tglError(20)
          if nextActionType != "string" or doubleActionType != "string":
            tglError(21)
          nextActionValue = nextActionValue.upper()
          doubleActionValue = doubleActionValue.upper()
          if nextActionValue not in registers or doubleActionValue not in registers:
            tglError(22)
          destRegister = registers[nextActionValue]
          fromRegister = registers[doubleActionValue]
          destRegisterType = destRegister[0]
          fromRegisterType = fromRegister[0]
          fromRegisterValue = fromRegister[1]

          if destRegister[0] == "const":
            tglError(14)
          if destRegister[0] == "any" and destRegister[1] != 0:
            destRegisterType = destRegister[1][0]
          if fromRegister[0] == "any" and fromRegister[1] != 0:
            fromRegisterType = fromRegister[1][0]
            fromRegisterValue = fromRegister[1][1]

          if fromRegisterType != destRegisterType:
            if destRegisterType == "any" and fromRegisterType != "any":
              destRegister[1] = [fromRegisterType, fromRegister[1]]
            else:
              tglError(23)
          destRegister[1] = fromRegisterValue
        case "$":
          print(registers['TA'][1], end=registers['TB'][1])
        case "#":
          if nextActionValue is None:
            tglError(9)
          if nextActionType != "string":
            tglError(8)
          nextActionValue = nextActionValue.upper()
          # ----------------------------------
          # Create a new bookmark under a specific name containing a J-value
          bookmarks[nextActionValue] = j
          # ----------------------------------
        case "!":
          if nextActionValue is None:
            tglError(11)
          if nextActionType != "string":
            tglError(10)
          nextActionValue = nextActionValue.upper()
          if nextActionValue not in bookmarks:
            tglError(12)
          j = bookmarks[nextActionValue]
          continue
        case ";":
          ignoreMode = True
        case "=":
          if nextActionValue is None or doubleActionValue is None:
            tglError(13)
          if nextActionType != "string" or doubleActionType != "string":
            tglError(18)
          nextActionValue = nextActionValue.upper()
          doubleActionValue = doubleActionValue.upper()
          if nextActionValue not in registers or doubleActionValue not in registers:
            tglError(19)

          if registers[nextActionValue][0] == "any":
            firstVTC = registers[nextActionValue][1]
          elif registers[nextActionValue][0] == "const":
            secondVTC = ('number', registers[nextActionValue][1])
          else:
            firstVTC = (registers[nextActionValue][0], registers[nextActionValue][1])
          if registers[doubleActionValue][0] == "any":
            secondVTC = registers[doubleActionValue][1]
          elif registers[doubleActionValue][0] == "const":
            secondVTC = ('number', registers[doubleActionValue][1])
          else:
            secondVTC = (registers[doubleActionValue][0], registers[doubleActionValue][1])

          registers["FA"][1] = int(
            firstVTC == secondVTC
          )
        case "(":
          if nextActionValue is None or doubleActionValue is None:
            tglError(38)
          if nextActionType != "string" or doubleActionType != "string":
            tglError(36)
          nextActionValue = nextActionValue.upper()
          doubleActionValue = doubleActionValue.upper()

          if nextActionType not in registers or doubleActionValue not in registers:
            tglError(37)

          if registers[nextActionValue][0] == "any" and registers[nextActionValue][1] != 0:
            firstVTC = registers[nextActionValue][1][0]
          elif registers[nextActionValue][0] == "any" and registers[nextActionValue][1] == 0:
            firstVTC = "number"
          elif registers[nextActionValue][0] == "const":
            tglError(39)
          else:
            firstVTC = registers[nextActionValue][0]

          if registers[doubleActionValue][0] == "any" and registers[doubleActionValue][1] != 0:
            secondVTC = registers[doubleActionValue][1][0]
          elif registers[doubleActionValue][0] == "any" and registers[doubleActionValue][1] == 0:
            secondVTC = "number"
          elif registers[doubleActionValue][0] == "const":
            tglError(39)
          else:
            secondVTC = registers[doubleActionValue][0]

          registers["FA"][1] = int(
            firstVTC == secondVTC
          )
        case ")":
          if nextActionValue is None or doubleActionValue is None:
            tglError(41)
          if nextActionType != "string" or doubleActionType != "string":
            tglError(40)
          nextActionValue = nextActionValue.upper()
          doubleActionValue = doubleActionValue.upper()

          if nextActionValue not in registers or doubleActionValue not in registers:
            tglError(42)

          if registers[nextActionValue][0] == "any" and registers[nextActionValue][1] != 0:
            firstVTC = registers[nextActionValue][1][1]
          elif registers[nextActionValue][0] == "any" and registers[nextActionValue][1] == 0:
            firstVTC = 0
          elif registers[nextActionValue][0] == "const":
            tglError(43)
          else:
            firstVTC = registers[nextActionValue][1]

          if registers[doubleActionValue][0] == "any" and registers[doubleActionValue][1] != 0:
            secondVTC = registers[doubleActionValue][1][1]
          elif registers[doubleActionValue][0] == "any" and registers[doubleActionValue][1] == 0:
            secondVTC = 0
          elif registers[doubleActionValue][0] == "const":
            tglError(43)
          else:
            secondVTC = registers[doubleActionValue][1]

          if isinstance(firstVTC, float):
            if str(firstVTC).endswith('.0'):
              firstVTC = int(firstVTC)
          if isinstance(secondVTC, float):
            if str(secondVTC).endswith('.0'):
              secondVTC = int(secondVTC)
          registers["FA"][1] = int(
            str(firstVTC) == str(secondVTC)
          )
        case "@":
          if nextActionValue is None:
            tglError(15)
          if nextActionType != "glyph":
            tglError(16)
          if not registers["FA"][1]:
            j += 2
            continue
        case "+":
          if nextActionValue is None:
            tglError(25)
          if nextActionType != "number":
            tglError(24)
          try:
            registers['MA'][1] + nextActionValue
          except:
            tglError(32)
          registers['MA'][1] += nextActionValue
        case "-":
          if nextActionValue is None:
            tglError(27)
          if nextActionType != "number":
            tglError(26)
          try:
            registers['MA'][1] -= nextActionValue
          except:
            tglError(32)
        case "/":
          if nextActionValue is None:
            tglError(29)
          if nextActionType != "number":
            tglError(28)
          try:
            registers['MA'][1] /= nextActionValue
          except:
            tglError(32)
        case "*":
          if nextActionValue is None:
            tglError(31)
          if nextActionType != "number":
            tglError(30)
          try:
            registers['MA'][1] *= nextActionValue
          except:
            tglError(32)
        case "`":
          if nextActionValue is None:
            tglError(33)
          if nextActionType != "string":
            tglError(34)
          if nextActionValue not in registers:
            tglError(35)
          registers[nextActionValue] = copy.deepcopy(origRegisters[nextActionValue])
        case "~":
          registers['TA'][1] = str(registers['MA'][1])
        case ":":
          try:
            registers['MA'][1] = float(registers['TA'][1])
          except ValueError:
            tglError(44)
        case ">":
          if nextActionValue is None:
            tglError(45)
          if nextActionType != "string":
            tglError(46)
          nextActionValue = nextActionValue.upper()
          if nextActionValue not in registers:
            tglError(47)
          vta = registers[nextActionValue][1]
          if registers[nextActionValue][0] == "const":
            tglError(48)
          if registers[nextActionValue][0] == "any" and registers[nextActionValue][1] != 0:
            vta = registers[nextActionValue][1][1]
          if registers[nextActionValue][0] == "any" and registers[nextActionValue][1] == 0:
            vta = 0
          stack.append(
            (nextActionValue, vta)
          )
        case "<":
          vton = stack.pop(0)
          if registers[vton[0]][0] == "any" and registers[vton[0]][1] == 0:
            registers[vton[0]][1] = (vton[1])
          elif registers[vton[0]][0] == "any" and registers[vton[0]][1] != 0:
            if isinstance(vton[1], float):
              registers[vton[0]][1] = ("number", vton[1])
            elif isinstance(vton[1], str):
              registers[vton[0]][1] = ("string", vton[1])
          else:
            registers[vton[0]][1] = vton[1]
        case _:
          tglError(3)

    j += 1


def main():
  if len(sys.argv) < 2:
    tglError(2)
  runCode(sys.argv)


if __name__ == "__main__":
  main()
