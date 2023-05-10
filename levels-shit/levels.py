import json

datafile = open("levels.json", "a+")

xp=0
xpincrease=0
level=0

data = []
for i in range(2005):
    xp = xp + xpincrease
    xpincrease += 5
    level += 1
    lvl = ({level:[level,xp,xpincrease]}) ,"\n"
    datafile.write(str(lvl))
