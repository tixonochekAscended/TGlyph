<p align="center">
<a href="https://imgbb.com/"><img src="https://i.ibb.co/dkBB1nM/TG-Logo.png" alt="TG-Logo" border="0" width=250 height=250/></a><br>
<i>↓ ↓ You can find explanations in English below ↓ ↓</i>
</p>


------------------------
## T^ (Ти-Глиф)
T^ _(читай как: ти-глиф)_ это эзотерический, интерпретируемый язык программирования который базирован на "глифах" которые исполняют команды. Результат данных команд зависит от аргументов переданных глифе и от значения "регистров" (регистры это много уже созданных переменных, которые можно использовать как и программисту так и используются глифами для математический операций, работы с текстом, условиями итд.). 75% вещей которые присутствуют в данном языке были взяты из других языков в которых я когда-либо программировал. Это легкий проект, не несущий в себе большого смысла. Этот язык не предназначен для использования ни в какой сфере, он не оптимизирован и даже не близко (Скажу больше, интерпретатор языка написан на Пайтоне). Смысл это просто быть прикольным, растряпаным и интересным языком с которым каждый может поигратся. __Это язык созданный за ради идеи, не для настоящего использования.__ Любые фиксы и поправки в коде приветствуются ❤️<br>
Вы можете узнать больше информации из данного ютуб-видео на моем канале: https://youtu.be/PmIvz5kOFyY?si=NurrvhbkJxktOmBo
Если у вас есть какие то вопросы, можете спросить тут: https://discord.gg/NSK7YJ2R6j

### Объяснения каждой глифы:
| Глифа    | Имя (Англ.) | Кол-во нужных аргументов | Предназначение |
| -------- | ------- | ------- | ------- |
| ^  | Bind Glyph    | 2    | Первым аргументом является имя регистра записанное как текст (например: "TA"), в которое хотим положить значение. Вторым аргументом является значение, которое будет положено в заданный регистр. С помощью данной глифы можно установить значение регистра на конкретное (текст, число). Значение которые мы хотим положить должно соответствовать типу данных регистра.    |
| &  | Register Match Glyph    |2    | Первый аргумент это имя регистра записанное как текст (например: "TA"), значение которого будет изменено. Вторым аргументом является имя регистра записанное как текст. С помощью данной глифы можно установить значение регистра из первого аргумента на значение регистра из второго аргумента, "сравнивая" их.   |
| $  | Output Glyph    | 0    | Данная глифа выводит то что помещено в регистре TA _плюс_ то что помещено в TB.   |
| #  | Bookmark Glyph    | 1    | Аргументом является имя новой закладки записанное как текст (например: "bk1"). Создает так называемую "закладку", к которой можно вернутся позже с помощью глифы прыжка (Jump glyph `!`) по имени закладки. Может быть использовано для создания циклов.|
| !  | Jump Glyph   | 1    | Аргументом является имя закладки записанное как текст (например: "bk1"), к которому нужно переместиться. С помощью данной глифы можно вернутся к ранее созданной закладке. Может быть использовано для создания циклов.|
| ;  | Ignore Glyph   | 0    | Включает "режим игнорирования". Когда программа находится в режиме игнорирования, все последующие глифы будут пропущены, до момента пока не будет найдена еще одна глифа игнорирования (`;`), в таком случае режим игнорирования будет выключен. Может быть использовано для создания циклов (в цели выхода из них).|
| =  | Direct Comparsion Glyph   | 2    | Первым аргументом является имя регистра записанное как текст (например: "TA"). Вторым аргументом является имя регистра записанное как текст. Данная глифа сравнивает, равны ли оба регистра (и тип данных, и значение). После этого записывает результат сравнения в регистр FA, записывая 0 если регистры не равны, и записывая 1 если регистры равны.|
| (  | Type Comparsion Glyph    | 2    |Первым аргументом является имя регистра записанное как текст (например: "TA"). Вторым аргументом является имя регистра записанное как текст. Данная глифа сравнивает, равны ли типы данных обоих регистров. После этого записывает результат сравнения в регистр FA, записывая 0 если типы данных регистров не равны, и записывая 1 если типы данных регистров равны.|
| )  | Value Comparsion Glyph   | 2    |Первым аргументом является имя регистра записанное как текст (например: "TA"). Вторым аргументом является имя регистра записанное как текст. Данная глифа сравнивает, равны ли значения обоих регистров. После этого записывает результат сравнения в регистр FA, записывая 0 если значения регистров не равны, и записывая 1 если значения регистров равны. Может сравнивать значения текстовых и числовых регистров.|
| \|  | < (less than) Comparsion Glyph   | 2    |Первым аргументом является имя регистра записанное как текст (например: "TA"). Вторым аргументом является имя регистра записанное как текст. Данная глифа сравнивает значения двух регистров, и если они равны или значение первого меньше записывает 0 в регистр FA, в других случаях записывает 1. Можно использовать только с регистрами которые в данный момент сохраняют в себе число. |
| @  | When Glyph    | 1    | Аргументом является любая глифа. Проверяет, какому значению равен регистр FA. Если же это 0, то пропускает глифу которую передано как аргумент (следующую после глифы "когда"). Если же это 1, исполняет следующую глифу, как бы "ничего не делая". Может быть использовано для создания циклов. |
| +  | Add Glyph    | 0    |Добавляет значение регистра MB к значению регистра MA. |
| -  | Substract Glyph    | 0    |Отнимает значение регистра MB от значения регистра MA.|
| /  | Divide Glyph    | 0    |Делит значение регистра MA на значение регистра MB.|
| *  | Multiply Glyph    | 0    |Умножает значение регистра MA на значение регистра MB.|
| %  | Mod Glyph    | 0    |Делит значение регистра MA на значение регистра MB, и записывает остаток в МА (Mod, Modulus).|
| r  | Root Glyph    | 0    |Берет (ЗНАЧЕНИЕ РЕГИСТРА MB)ый корень из числа (ЗНАЧЕНИЕ РЕГИСТРА MA), результат записывается в МА.|
| l  | Log Glyph    | 0    |Записывает результат логарифма в МА, где база это число которое находится в регистре MB а аргументом логарифма число находящееся в регистре МА.|
| s  | Sin Glyph    | 0    |Результат записывается в МА. Берет синус числа которое находится в MA.|
| c  | Cos Glyph    | 0    |Результат записывается в МА. Берет косинус числа которое находится в MA.|
| t  | Tan Glyph    | 0    |Результат записывается в МА. Берет тангенс числа которое находится в MA.|
| `  | Register Reset Glyph    | 1    | Аргументом является имя регистра записанное как текст (например: "TA"). Сбрасывает значение указанного регистра до изначального.|
| ~  | NTS-conversion Glyph    | 0    | Переделывает число находящееся в регистре MA на текст и устанавливает значение регистра TA на данный конвертированный текст. MA -> TA.|
| :  | STN-conversion Glyph    | 0    | Переделывает текст находящийся в регистре TA на число и устанавливает значение регистра MA на данное конвертированное число. TA -> MA. Также изменяет регистр FA в зависимости от результата конвертации: если получилось то выставляет 1, а если не вышло то 0. |
| >  | Push Glyph    | 1 | Аргументом является имя регистра записанное как текст (например: "TA"). Пушит (добавляет в КОНЕЦ) регистр в Стак. Значение регистра при этом не меняется.|
| <  | Pop Glyph    | 0   |Попает первый регистр находящийся в Стаке (с НАЧАЛА, не с КОНЦА), возвращая регистру значение которое у него было на момент пуша (добавления) регистра в Стак.|
| ?  | Input Glyph    | 0   |Запрашивает ввод от пользователя из консоли и сохраняет результат в регистре TA.|
| `[* ... *]` | Комментарии | 0 | Всё что находится между ними игнорируются лексером, могут быть многострочными. |

### Объяснения каждого регистра:
| Имя Регистра    | Тип Данных | Изначальное Значение | Предназначение |
| -------- | ------- | ------- | ------- |
| MA  | Число | 0| Регистр который используется для математических операций. Глифы `+ - / * ~ :` изменяют или берут значение из данного регистра (взаимодействуют с ним).|
| MB  |  Число |0| Регистр который используется для математических операций. Глифы `+ - / * ~ :` изменяют или берут значение из данного регистра (взаимодействуют с ним).|
| TA  | Текст | "" (Пустой string) | Регистр который используется для текстовых манипуляций. Его значение может быть изменено или взято глифами `$ ~ :`.|
| TB  | Текст  | "\n" (Новая строка) | Регистр который используется для текстовых манипуляций. |
| FA  | Константа (В реальности: Число) | 0 |Используется для условий и работы с ними. Это регистр-константа, то есть его значение нельзя изменить самостоятельно. Значение данного регистра может быть изменено глифами `= ( )`. При сравнении данного регистра с другими, принимает тип данных `number` (число). |
| FB  | Константа (В реальности: Число) | 1 |Используется для рандомизации. Это регистр-константа, то есть его значение нельзя изменить самостоятельно. Значение данного регистра меняется каждый раз, когда исполняется какая-либо глифа. Таким образом, каждый раз значение регистра рандомизируется от 1-100 (учитывая 1 и 100, 100 чисел в общем) |
| AA, AB ... AY, AZ | Любой | 0| Данные 26 регистров начиная с АА, АB и заканчивая AX, AY & AZ не изменяются никакими глифами и их можно свободно использовать в любых целях. В такие регистры можно положить любое значение: будь то число или текст. |
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
