from z3 import *
import time

def add(a = 20, b = 7):
    max_len = max(len("{0:b}".format(a)), len("{0:b}".format(b)))+1
    format_str = '{0:0'+str(max_len)+'b}'
    a_bin = format_str.format(a)
    b_bin = format_str.format(b)
    # 数据预处理，将A B补足到相同位数
    A = [Bool('a_%i' % (i + 1)) for i in range (max_len)]
    B = [Bool('b_%i' % (i + 1)) for i in range (max_len)]
    C = [Bool('c_%i' % i) for i in range (max_len + 1)]
    D = [Bool('d_%i' % (i + 1)) for i in range (max_len)]
    # 采用舍去D的最高位的方式计算
    # 变量定义
    A_c = And([If(a_bin[i] == '0', Not(A[i]), A[i]) for i in range(max_len)])	# 将A的二进制数字形式化为表达式
    B_c = And([If(b_bin[i] == '0', Not(B[i]), B[i]) for i in range(max_len)])	# 将B的二进制数字形式化为表达式
    D_c = And([D[i]==(A[i]==(B[i]==C[i+1])) for i in range(max_len)])	# 约束A[i],B[i],C[i],D[i]间关系
    Carry_c = And([C[i]==Or(And(A[i], B[i]), And(A[i], C[i+1]), And(B[i], C[i+1])) for i in range(max_len)])	# 约束进位关系
    s = Solver()
    s.add(A_c, B_c, D_c, Carry_c, Not(C[0]), Not(C[max_len]))
    result = s.check()
    # 输出计算结果
    if result == sat:
        d = ""
        for i in range(max_len):
            if s.model()[D[i]] == True:
                d += '1'
            else:
                d += '0'
        print(int(d, 2))
        return int(d, 2)
   	return None

def minus(a = 20, b = 7):
    # a - b = d implies a = b + d
    max_len = max(len("{0:b}".format(a)), len("{0:b}".format(b)))
    format_str = '{0:0'+str(max_len)+'b}'
    a_bin = format_str.format(a)
    b_bin = format_str.format(b)
    A = [Bool('a_%i' % (i + 1)) for i in range (max_len)]
    B = [Bool('b_%i' % (i + 1)) for i in range (max_len)]
    C = [Bool('c_%i' % i) for i in range (max_len + 1)]
    D = [Bool('d_%i' % (i + 1)) for i in range (max_len)]
    A_c = And([If(a_bin[i] == '0', Not(A[i]), A[i]) for i in range(max_len)])
    B_c = And([If(b_bin[i] == '0', Not(B[i]), B[i]) for i in range(max_len)])
    # 以上内容和加法相同
    # 以下内容唯一不同在于由于d=a-b⇔a=b+d，所以需要把加法中的a换成b，d换成a
    D_c = And([A[i]==(D[i]==(B[i]==C[i+1])) for i in range(max_len)])
    Carry_c = And([C[i]==Or(And(D[i], B[i]), And(D[i], C[i+1]), And(B[i], C[i+1])) for i in range(max_len)])
    s = Solver()
    s.add(A_c, B_c, D_c, Carry_c, Not(C[0]), Not(C[max_len]))
    result = s.check()
    if result == sat:
        d = ""
        for i in range(max_len):
            if s.model()[D[i]] == True:
                d += '1'
            else:
                d += '0'
        print(int(d, 2))
        return int(d, 2)
	return None