<p align="center">
<img src="https://i.ibb.co/dkBB1nM/TG-Logo.png" alt="TG-Logo" border="0" width=250 height=250/><br>
WIKI: https://esolangs.org/wiki/T%5E
</p>

------------------------------------------------

## T^ (T-Glyph)
T^ _(read as: tea-glyph)_ is an esoteric interpreted programming language that is based around 'glyphs' that execute some code based on the arguments given and based on the values of the "registers" (registers are pre-defined variables that can be used for calculations, string-manipulation, conditions etc.). 75% of things this language is made of were borrowed from other languages I have programmed in. It's a lightweight project - it's not supposed to actually be used in any sphere, it's not optimized or even close (More to say, the interpreter is made in Python). The point of the language is to just be a fun, messy thing that you can play around with. __It's a language that is made solely for the idea, not for real usage.__ Any tweaks are fully accepted and welcomed, you can open an issue or whatever ❤️

### Explaination of each glyph:
| Glyph | Name | Number of required arguments | Purpose |
| -------- | ------- | ------- | ------- |
| ^ | Bind Glyph | 2 | Sets the value of a register (specified as text, e.g., "TA") (first argument) to a given value (second argument). The value must match the register's data type. |
| & | Register Match Glyph | 2 | Sets the value of one register (first argument) to the value of another (second argument). Both arguments must be specified as text, e.g., "TA" |
| $ | Output Glyph | 0 | Outputs the combined values of registers TA and TB. |
| # | Bookmark Glyph | 1 | Creates a "bookmark" that can be jumped to later using the Jump glyph (`!`), may be used for making loops. Argument is a name of new bookmark (specified as text, e.g., "bk1"). |
| ! | Jump Glyph | 1 | Jumps to a previously created bookmark. Argument is a name of bookmark (specified as text, e.g., "bk1") |
| ; | Ignore Glyph | 0 | Enables "Ignore Mode". Makes all following glyphs ignored until another Ignore glyph is encountered. May be used to break from loops. |
| = | Direct Comparsion Glyph | 2 | Compares two registers for both data type and value. Sets FA to 1 if equal, 0 otherwise. Both arguments must be specified as text, e.g., "TA" |
| ( | Type Comparsion Glyph | 2 | Compares two registers for data type. Sets FA to 1 if equal, 0 otherwise. Both arguments must be specified as text, e.g., "TA" |
| ) | Value Comparsion Glyph | 2 | Compares two registers for value. Sets FA to 1 if equal, 0 otherwise. Both arguments must be specified as text, e.g., "TA". Can compare number and text registers |
| \| | < (less than) Comparsion Glyph | 2 | Compares two registers for both data type and value. Sets FA to 0 if the first register has a lower value than the second register or if they are equal, 1 otherwise. Both arguments must be specified as text, e.g., "TA". Can compare only number registers|
| @ | When Glyph | 1 | Executes the following glyph only if FA is 1, skips the glyph otherwise. May be used for loops |
| + | Add Glyph | 0 | Adds the value of register MB to the value of register MA. |
| - | Substract Glyph | 0 | Subtracts the value of register MB from the value of register MA. |
| / | Divide Glyph | 0 | Divides the value of register MA by the value of register MB. |
| * | Multiply Glyph | 0 | Multiplies the value of register MA by the value of register MB. |
| % | Mod Glyph | 0 | Divides the value of register MA by the value of register MB, and then sets the value of the register MA to what is left after the division (This is a mod, modulus operator). |
| r  | Root Glyph    | 0    |Takes (VALUE OF MB REGISTER)th root of (VALUE OF REGISTER MA), result of the operation is written in the register МА.|
| l  | Log Glyph    | 0    |The result of the log operation is stored in MA, where the log base is the value of the registerr MB, and the log's argument is the value of the register MA.|
| s  | Sin Glyph    | 0    |The result of the operation is stored in МА. Takes sin of a number that is located in the register MA.|
| c  | Cos Glyph    | 0    |The result of the operation is stored in МА. Takes cosine of a number that is located in the register MA.|
| t  | Tan Glyph    | 0    |The result of the operation is stored in МА. Takes tangent of a number that is located in the register MA.|
| ` | Register Reset Glyph | 1 | Resets the value of a specified register to its initial value. Argument must be name of regiser specified as text, e.g., "TA" |
| ~ | NTS-conversion Glyph | 0 | Converts the number in MA to a text string and stores it in TA. |
| : | STN-conversion Glyph | 0 | Converts the text in TA to a number and stores it in MA. Based on the result, sets the register FA to either 1 if success and 0 if couldn't convert.|
| > | Push Glyph | 1 | Pushes the value of a register onto the stack. Argument must be name of regiser specified as text, e.g., "TA" |
| < | Pop Glyph | 0 | Pops the top value from the stack and assigns it to a register it was pushed by. |
| ? | InputGlyph | 0 | Asks for the input from the user in the console and stores the input in the register TA. |
| g  | Get File Glyph    | 1   |Argument is the name of an existing file (f.e.: "blahblahblah.*"). Reads the contents of the file and puts them into the register TA.|
| w  | Write File Glyph    | 1   |АргуArgument is the name of an existing file (f.e.: "blahblahblah.*"). If the file with the given name doesn't exist, creates one. Writes whatever is written in the register TA into the file with the given name.|
| G  | Exclusive Get File Glyph    | 1   |Argument is the name of a register written as a string (f.e.: "AA"). Reads the contents of the file called (VALUE OF THE PROVIDED REGISTER) and puts them into the register TA. |
| W  | Exclusive Write File Glyph    | 1   |Argument is the name of a register written as a string (f.e.: "AA"). If the file doesnt exist already, create a file with the name (VALUE OF THE PROVIDED REGISTER) and write whatever is in the register TA into that file.|
| `[* ... *]` | Comments | 0 | Everything that is between them is ignored by the lexer, can be multi-line |

### Register Explanations
| Register Name | Data Type | Initial Value | Purpose |
| -------- | ------- | ------- | ------- |
| MA | Number | 0| Used for mathematical operations. Affected by `+ - / * ~ :` glyphs. |
| MB | Number |0| Used for mathematical operations. Affected by `+ - / * ~ :` glyphs. |
| TA | Text | "" (Empty string) | Used for text manipulations. Affected by `$ ~ :` glyphs|
| TB | Text | "\n" (Newline symbol) | Used for text manipulations. |
| FA | Constant (Actually: Number) | 0 | Used for condiations. Affected by `= ( )` glyphs. |
| FB | Constant (Actually: Number) | 1 | Used for randomization. Each time a glyph is executed, changes value of itself in a range from 1-100 (random, this range includes 1 and 100, so 100 numbers in total). |
| AA, AB ... AY, AZ | Any | 0 | General-purpose registers. |
------------------------------------------------
