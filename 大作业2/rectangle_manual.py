remain_rec = {}

def readfile():
    with open("rectangle.txt", 'r', encoding='utf-8') as f:
        # txt文件第一行是最外框大小
        line = f.readline().strip('\n\t').split(',')
        outer_rec = {"h": int(line[0]), "w": int(line[1])}
        rec = []
        # 一次读取每个矩形
        for line_raw in f:
            line = line_raw.strip('\n\t').split(',')
            rec.append((int(line[0]), int(line[1])))
        return outer_rec, rec

def fitting(x, y, h, w, recset):
    # 已经没有可摆放的空间
    assert recset is not None
    if x == w or y == h:
        return [], recset
    elif len(recset) == 0:
        return [], None
    for i in recset:
        # 横放
        if x + i[1] <= w and y + i[0] <= h:
            # fitting第一种空间
            res = recset.copy()
            res.pop(res.index(i))
            ans1, res = fitting(x, y+i[0], h, w, res)
            # 如果放置完毕
            if res is None:
                return ans1 + [(x, y, i[1], i[0])], None
            # 对未放放置完毕的rectangle继续放置
            else:
                # print(x+i[1], y)
                ans2, res = fitting(x+i[1], y, y+i[0], w, res.copy())
                # 即使没有放置完毕也可以返回
                return ans1 + ans2 + [(x, y, i[1], i[0])], res

            # fitting第二种空间
            res = recset.copy()
            res.pop(res.index(i))
            ans1, res = fitting(x, y+i[0], h, x+i[1], res)
            # 如果放置完毕
            if res is None:
                return ans1 + [(x, y, i[1], i[0])], None
            # 对未放放置完毕的rectangle继续放置
            else:
                ans2, res = fitting(x+i[1], y, h, w, res.copy())
                # 即使没有放置完毕也可以返回
                return ans1 + ans2 + [(x+i[1], y, i[1], i[0])], res
        # 竖放
        elif x + i[0] <= w and y + i[1] <= h:
            # fitting第一种空间
            res = recset.copy()
            res.pop(res.index(i))
            ans1, res = fitting(x, y+i[1], h, w, res)
            # 如果放置完毕
            if res is None:
                return ans1 + [(x, y, i[0], i[1])], None
            # 对未放放置完毕的rectangle继续放置
            else:
                # print(x+i[0], y)
                ans2, res = fitting(x+i[0], y, y+i[1], w, res.copy())
                # 即使没有放置完毕也可以返回
                return ans1 + ans2 + [(x, y, i[0], i[1])], res

            # fitting第二种空间
            res = recset.copy()
            res.pop(res.index(i))
            ans1, res = fitting(x, y+i[1], h, x+i[0], res)
            # 如果放置完毕
            if res is None:
                return ans1 + [(x, y, i[0], i[1])], None
            # 对未放放置完毕的rectangle继续放置
            else:
                ans2, res = fitting(x+i[0], y, h, w, res.copy())
                # 即使没有放置完毕也可以返回
                return ans1 + ans2 + [(x+i[0], y, i[0], i[1])], res
    return [], recset

# 从文件中读取各个矩形的大小,以及最外框的大小
outer_rec, remain_rec = readfile()
# 按照面积大小对矩形进行排序
remain_rec = sorted(remain_rec, reverse=True, key=lambda r: r[0]*r[1])
# print(sum(remain_rec))
# ans, _ = fitting(0,0,outer_rec['h'],outer_rec["w"],remain_rec)
import time
t1 = time.time()
for i in range(100000):
    ans, _ = fitting(0,0,outer_rec['h'],outer_rec["w"],remain_rec)
t2 = time.time()
print(t2-t1)
print("x, y, h, w")
for item in ans:
    print(item)