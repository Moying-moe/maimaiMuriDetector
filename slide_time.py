"""
Author: moying
Date: 2021-08-17 01:37:37
LastEditTime: 2021-08-17 01:59:33
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \maimai无理检测\slide_time.py
"""
SLIDE_TIME = {
    "-": {
        2: [{"area": 2, "time": 0.7678}],
        3: [{"area": 3, "time": 0.83415}],
        4: [{"area": 4, "time": 0.84112}],
        5: [{"area": 5, "time": 0.83415}],
        6: [{"area": 6, "time": 0.7678}],
    },
    "v": {
        1: [{"area": 1, "time": 0.84244}],
        2: [{"area": 2, "time": 0.84244}],
        3: [{"area": 3, "time": 0.84244}],
        5: [{"area": 5, "time": 0.84244}],
        6: [{"area": 6, "time": 0.84244}],
        7: [{"area": 7, "time": 0.84244}],
    },
    "p": {
        0: [{"area": 0, "time": 0.90878}],
        1: [{"area": 1, "time": 0.90049}],
        2: [{"area": 2, "time": 0.8839}],
        3: [{"area": 3, "time": 0.87561}],
        4: [{"area": 4, "time": 0.85902}],
        5: [{"area": 5, "time": 0.92537}],
        6: [{"area": 6, "time": 0.92537}],
        7: [{"area": 7, "time": 0.91707}],
    },
    "q": {
        0: [{"area": 0, "time": 0.90878}],
        7: [{"area": 7, "time": 0.90049}],
        6: [{"area": 6, "time": 0.8839}],
        5: [{"area": 5, "time": 0.87561}],
        4: [{"area": 4, "time": 0.85902}],
        3: [{"area": 3, "time": 0.92537}],
        2: [{"area": 2, "time": 0.92537}],
        1: [{"area": 1, "time": 0.91707}],
    },
    "s": {4: [{"area": 4, "time": 0.86732}]},
    "z": {4: [{"area": 4, "time": 0.86732}]},
    "w": {4: [{"area": 4, "time": 0.85073}]},
    "pp": {
        0: [
            {"area": 2, "time": 0.54836},
            {"area": 1, "time": 0.75745},
            {"area": 0, "time": 0.94982},
        ],
        1: [{"area": 2, "time": 0.68925}, {"area": 1, "time": 0.93281}],
        2: [{"area": 2, "time": 0.86562}],
        3: [
            {"area": 2, "time": 0.38689},
            {"area": 1, "time": 0.53807},
            {"area": 3, "time": 0.94121},
        ],
        4: [
            {"area": 2, "time": 0.38689},
            {"area": 1, "time": 0.53807},
            {"area": 4, "time": 0.94121},
        ],
        5: [
            {"area": 2, "time": 0.40369},
            {"area": 1, "time": 0.53807},
            {"area": 5, "time": 0.94121},
        ],
        6: [
            {"area": 2, "time": 0.42048},
            {"area": 1, "time": 0.56326},
            {"area": 6, "time": 0.93281},
        ],
        7: [
            {"area": 2, "time": 0.45408},
            {"area": 1, "time": 0.63045},
            {"area": 7, "time": 0.92441},
        ],
    },
    "qq": {
        0: [
            {"area": 6, "time": 0.54836},
            {"area": 7, "time": 0.75745},
            {"area": 0, "time": 0.94982},
        ],
        7: [{"area": 6, "time": 0.68925}, {"area": 7, "time": 0.93281}],
        6: [{"area": 6, "time": 0.86562}],
        5: [
            {"area": 6, "time": 0.38689},
            {"area": 7, "time": 0.53807},
            {"area": 5, "time": 0.94121},
        ],
        4: [
            {"area": 6, "time": 0.38689},
            {"area": 7, "time": 0.53807},
            {"area": 4, "time": 0.94121},
        ],
        3: [
            {"area": 6, "time": 0.40369},
            {"area": 7, "time": 0.53807},
            {"area": 3, "time": 0.94121},
        ],
        2: [
            {"area": 6, "time": 0.42048},
            {"area": 7, "time": 0.56326},
            {"area": 2, "time": 0.93281},
        ],
        1: [
            {"area": 6, "time": 0.45408},
            {"area": 7, "time": 0.63045},
            {"area": 1, "time": 0.92441},
        ],
    },
    "V": {
        (2, 4): [
            {"area": 2, "time": 0.37439},
            {"area": 3, "time": 0.64375},
            {"area": 4, "time": 0.87835},
        ],
        (2, 5): [{"area": 2, "time": 0.32225}, {"area": 5, "time": 0.90442}],
        (2, 6): [{"area": 2, "time": 0.30488}, {"area": 6, "time": 0.89573}],
        (2, 7): [{"area": 2, "time": 0.31948}, {"area": 7, "time": 0.89663}],
        (6, 4): [
            {"area": 6, "time": 0.37439},
            {"area": 5, "time": 0.64375},
            {"area": 4, "time": 0.87835},
        ],
        (6, 3): [{"area": 6, "time": 0.32225}, {"area": 3, "time": 0.90442}],
        (6, 2): [{"area": 6, "time": 0.30488}, {"area": 2, "time": 0.89573}],
        (6, 1): [{"area": 6, "time": 0.31948}, {"area": 1, "time": 0.89663}],
    },
    ">": {
        0: [
            {"area": 1, "time": 0.08142},
            {"area": 2, "time": 0.21027},
            {"area": 3, "time": 0.33496},
            {"area": 4, "time": 0.45966},
            {"area": 5, "time": 0.58851},
            {"area": 6, "time": 0.71736},
            {"area": 7, "time": 0.84205},
            {"area": 0, "time": 0.96675},
        ],
        1: [{"area": 1, "time": 0.7132}],
        2: [{"area": 1, "time": 0.33496}, {"area": 2, "time": 0.86699}],
        3: [
            {"area": 1, "time": 0.21858},
            {"area": 2, "time": 0.56772},
            {"area": 3, "time": 0.91271},
        ],
        4: [
            {"area": 1, "time": 0.16523},
            {"area": 2, "time": 0.42401},
            {"area": 3, "time": 0.67444},
            {"area": 4, "time": 0.93322},
        ],
        5: [
            {"area": 1, "time": 0.13129},
            {"area": 2, "time": 0.33496},
            {"area": 3, "time": 0.53863},
            {"area": 4, "time": 0.74645},
            {"area": 5, "time": 0.95012},
        ],
        6: [
            {"area": 1, "time": 0.11051},
            {"area": 2, "time": 0.27677},
            {"area": 3, "time": 0.44719},
            {"area": 4, "time": 0.6176},
            {"area": 5, "time": 0.78802},
            {"area": 6, "time": 0.95844},
        ],
        7: [
            {"area": 1, "time": 0.09388},
            {"area": 2, "time": 0.23936},
            {"area": 3, "time": 0.38484},
            {"area": 4, "time": 0.53032},
            {"area": 5, "time": 0.67164},
            {"area": 6, "time": 0.81711},
            {"area": 7, "time": 0.96259},
        ],
    },
    "<": {
        0: [
            {"area": 7, "time": 0.08142},
            {"area": 6, "time": 0.21027},
            {"area": 5, "time": 0.33496},
            {"area": 4, "time": 0.45966},
            {"area": 3, "time": 0.58851},
            {"area": 2, "time": 0.71736},
            {"area": 1, "time": 0.84205},
            {"area": 0, "time": 0.96675},
        ],
        7: [{"area": 7, "time": 0.7132}],
        6: [{"area": 7, "time": 0.33496}, {"area": 6, "time": 0.86699}],
        5: [
            {"area": 7, "time": 0.21858},
            {"area": 6, "time": 0.56772},
            {"area": 5, "time": 0.91271},
        ],
        4: [
            {"area": 7, "time": 0.16523},
            {"area": 6, "time": 0.42401},
            {"area": 5, "time": 0.67444},
            {"area": 4, "time": 0.93322},
        ],
        3: [
            {"area": 7, "time": 0.13129},
            {"area": 6, "time": 0.33496},
            {"area": 5, "time": 0.53863},
            {"area": 4, "time": 0.74645},
            {"area": 3, "time": 0.95012},
        ],
        2: [
            {"area": 7, "time": 0.11051},
            {"area": 6, "time": 0.27677},
            {"area": 5, "time": 0.44719},
            {"area": 4, "time": 0.6176},
            {"area": 3, "time": 0.78802},
            {"area": 2, "time": 0.95844},
        ],
        1: [
            {"area": 7, "time": 0.09388},
            {"area": 6, "time": 0.23936},
            {"area": 5, "time": 0.38484},
            {"area": 4, "time": 0.53032},
            {"area": 3, "time": 0.67164},
            {"area": 2, "time": 0.81711},
            {"area": 1, "time": 0.96259},
        ],
    },
    "^": {
        1: [{"area": 1, "time": 0.7132}],
        2: [{"area": 1, "time": 0.33496}, {"area": 2, "time": 0.86699}],
        3: [
            {"area": 1, "time": 0.21858},
            {"area": 2, "time": 0.56772},
            {"area": 3, "time": 0.91271},
        ],
        7: [{"area": 7, "time": 0.7132}],
        6: [{"area": 7, "time": 0.33496}, {"area": 6, "time": 0.86699}],
        5: [
            {"area": 7, "time": 0.21858},
            {"area": 6, "time": 0.56772},
            {"area": 5, "time": 0.91271},
        ],
    },
}

'''

def rev(k):
    return {0: 0, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}[k]


SLIDE_TIME["<"] = {}
for k in SLIDE_TIME[">"]:
    SLIDE_TIME["<"][rev(k)] = []
    for o in SLIDE_TIME[">"][k]:
        to = o.copy()
        to["area"] = rev(to["area"])
        SLIDE_TIME["<"][rev(k)].append(to)
print(SLIDE_TIME)
'''