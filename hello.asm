B4 09
BA 0b 01 ; move "Hello!" into reg A
CD 21 ; call to msdos api

B4 01 ; <character input>
CD 21 ; msdos api

B4 4C ; <terminate>
CD 21 ; msdos api

48 65 6C 6C 6F 21 24 ; Hello world!