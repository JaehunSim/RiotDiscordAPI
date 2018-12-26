# -*- coding: utf-8 -*
import random

def min_diff_sets(data):
    import itertools
    if len(data) == 1:
        return data[0]
    s = sum(data)
    a = []
    for i in range(1, len(data)):
        if i == len(data)/2:
            a.extend(list(itertools.combinations(data, i)))
            break
    b = itertools.combinations(a, 2)
    c = filter(lambda x: sum(x[0])+sum(x[1])==s, b)
    c = filter(lambda x: sorted([i for sub in x for i in sub])==sorted(data), c)

    res = sorted([(abs(sum(i[0]) - sum(i[1])), i) for i in c],
            key=lambda x: x[0])
    min1 = min([i[0] for i in res])
    temp = []
    for i in res:
        if i[0] == min1:
            temp.append(i[1])
    return temp

def getUniqueDivSets(divSets):
    uniqueDivSets = []
    for comb in divSets:
        team1_list = list(comb[0])
        team2_list = list(comb[1])
        team1_list.sort()
        team2_list.sort()
        comb2 = [team1_list,team2_list]
        if comb2 not in uniqueDivSets:
            uniqueDivSets.append(comb2)
    return uniqueDivSets

def divideTeam(rankScoreList):
    l = rankScoreList
    t = l[:3]
    j = l[3:6]
    m = l[6:9]
    a = l[9:12]
    s = l[12:15]
    while True:
        wrong = False
        t1 = []
        t2 = []
        t3 = []
        teams = [t1,t2,t3]
        random.shuffle(t)
        random.shuffle(j)
        random.shuffle(m)
        random.shuffle(a)
        random.shuffle(s)
        for index,value in enumerate(teams):
            value.append(t[index])
            value.append(j[index])
            value.append(m[index])
            value.append(a[index])
            value.append(s[index])
        sumList= []
        for i in teams:
            tempList = []
            for j1 in i:
                tempList.append(j1[1])
            sumList.append(sum(tempList))
        tempList = []
        for i in rankScoreList:
            tempList.append(i[1])
        mean = round(sum(tempList)/3)
        for i in sumList:
            if i>= (mean+2) or i <= (mean-2):
                wrong = True
                break
        if not wrong:
            break
    return t1,t2,t3, sumList
#rankScoreOnly = [21, 14, 11, 11, 7, 18, 19, 12, 11, 11]
#w = min_diff_sets(rankScoreOnly)