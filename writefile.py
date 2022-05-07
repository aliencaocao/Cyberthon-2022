import random
import os

f = os.fdopen(os.open('reallybig', os.O_RDWR | os.O_CREAT), 'rb+')

flag = __REDACTED__
spacer = __REDACTED__
curpos = __REDACTED__

f.seek(curpos)
f.write(bytes([random.randint(1,255)]))
for c in flag:
    curpos += c*spacer
    f.seek(curpos)
    f.write(bytes([random.randint(1,255)]))