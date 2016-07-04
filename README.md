# pmasm.py
pmasm stands for Python Machine code Assembler (and editor)

## Example
File: hello.asm:
```
B4 09
BA 0b 01
CD 21

B4 4C
CD 21

48 65 6C 6C 6F 21 0A 24
```

Cmd: pmasm(.py) hello --edit
```
  0x0100: B4 09
  0x0102: BA 0b 01
  0x0105: CD 21
  0x0107:
  0x0107: B4 4C
  0x0109: CD 21
  0x010b:
  0x010b: 48 65 6C 6C 6F 21 0A 24
```

As you can see, it is clear that BA 0b01h refers to location 0x010b in memory. If it was just a single line such as
```
B4 09 BA 0B 01 CD 21 B4 4C CD 21 48 65 6C 6C 6F 21 0D 0A 24
```
it would have been much harder to find the location of 48 65 ... 0A 24 ('Hello!\n$').

Say, for example, you wanted to add a pause after calling MS-DOS api function 0x09 by calling 0x01. It would look like this:
```
  0x0100: B4 09
  0x0102: BA 0b 01
  0x0105: CD 21
  0x0107:
  0x0107: B4 01
  0x0109: CD 21
  0x010b:
  0x010b: B4 4C
  0x010d: CD 21
  0x010f:
  0x010f: 48 65 6C 6C 6F 21 0A 24
```
Note how the memory address of "Hello!" moved to 0x010f. In order for the string to be displayed properly, instead of some junk, we edit the second line such that:
```
  0x0102: BA 0b 01 -->   0x0102: BA 0f 01
```


## pmasm -h
pmasm <file> -- convert .asm hex code file into binary 
