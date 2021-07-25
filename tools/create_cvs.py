import pandas
import random

name = []
int = []
pre = 0
subtr = 0
features = 26

'''
 creates mininfo.csv.  Convention - we have 26*1000 stl-files, so it is hardcoded now
'''

for x in range(features * 1000):
    if x % 1000 == 0 and x != 0:
        pre += 1
        subtr += 1000

    number = x - subtr + 1
    int.append(random.randint(0, 53))

    string = "data/FNSet/" + str(pre) + "_" + str(number) + ".binvox"
    name.append(string)

df = pandas.DataFrame(data={"a": name, "b": int})
df.to_csv("..\data\minfo.csv", sep=',', index=False, header=False)
