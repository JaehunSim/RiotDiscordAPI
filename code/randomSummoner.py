# -*- coding: utf-8 -*-
import pandas as pd
import sys, os
PATH = os.path.dirname(os.path.realpath(sys.argv[0]))[:-5] + "\\db"
data = pd.read_excel(PATH+"\\koreapasSummoner.xlsx")

for j in range(20):
    sampled = data.sample(10)
    print("!team ",end="")
    for i in sampled.values:
        print(i[0],end=" ")
    print("\n")