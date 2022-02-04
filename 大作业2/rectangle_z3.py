from z3 import *

def readfile():
    with open("rectangle.txt", 'r', encoding='utf-8') as f:
        # txt文件第一行是最外框大小
        line = f.readline().strip('\n\t').split(',')
        outer_rec = {"h": int(line[0]), "w": int(line[1])}
        rec = {}
        i = 0
        # 一次读取每个矩形
        for line_raw in f:
            line = line_raw.strip('\n\t').split(',')
            rec[i] = {"h": int(line[0]), "w": int(line[1])}
            i = i + 1
        return outer_rec, rec

# 约束每个矩形的height和width
def constrain_rec(W, H, rec_dict):
    constrain = []
    for i, info in rec_dict.items():
        constrain.append(Or(
            And(W[i]==info["w"], H[i]==info['h']),
            And(W[i]==info['h'], H[i]==info['w'])
            ))
    return And(constrain)

# 约束每个矩形的位置,确保不出最外框的大小
def constrain_loc(X, Y, W, H, outer_rec):
    constrain = []
    for i in range(len(H)):
        constrain.append(And(
            And(X[i]>=0, X[i]+W[i]<=outer_rec['w']),
            And(Y[i]>=0, Y[i]+H[i]<=outer_rec['h']),
            ))
    return And(constrain)

# 约束矩形互相位置,确保不重叠
def constrain_overlap(X, Y, W, H):
    constrain = []
    for i in range(len(H)):
        for j in range((len(H))):
            if i != j:
                constrain.append(Or(
                    X[j]>=X[i]+W[i],
                    X[i]>=X[j]+W[j],
                    Y[j]>=Y[i]+H[i],
                    Y[i]>=Y[j]+H[j]
                    ))
    return And(constrain)

# 从文件中读取各个矩形的大小,以及最外框的大小
outer_rec, rec = readfile()
# 定义每个矩形的左下角点的坐标及height和width值
X = [Int('X_%i' % (i + 1)) for i in range(len(rec))]
Y = [Int('Y_%i' % (i + 1)) for i in range(len(rec))]
W = [Int('W_%i' % (i + 1)) for i in range(len(rec))]
H = [Int('H_%i' % (i + 1)) for i in range(len(rec))]
# 约束每个矩形的height和width
constrain1 = constrain_rec(W, H, rec)
# 约束每个矩形的位置,确保不出最外框的大小
constrain2 = constrain_loc(X, Y, W, H, outer_rec)
# 约束矩形互相位置,确保不重叠
constrain3 = constrain_overlap(X, Y, W, H)
# 求解结果
import time
t1 = time.time()
for i in range(100):
    solve(constrain1, constrain2, constrain3)
t2 = time.time()
print(t2-t1)