from z3 import *
import time

def n_queen_smt(n = 8):
    Q = [Int('Q_%i' % (i + 1)) for i in range(n)]
    val_c = [And(1 <= Q[i], Q[i] <= n) for i in range(n)]
    col_c = [Distinct(Q)]
    diag_c = [If(i == j, True, And(i+Q[j]!=j+Q[i], i-Q[j]!=j-Q[i])) for i in range(n) for j in range(i)]

    time_start=time.perf_counter()
    solve(val_c + col_c + diag_c)
    time_end=time.perf_counter()
    print('time cost for smt:',time_end-time_start,'s')

def n_queen_sat(n = 8):
    Q = [Bool('Q_%i%i' % (i + 1, j + 1)) for i in range (n) for j in range(n)]
    row_c = And([Or([Not(Or([If(i==k, Not(Q[j*n+i]), Q[j*n+i]) for i in range(n)])) for k in range(n)]) for j in range(n)])  #每一行有且仅有一个为True
    col_c = And([Or([Not(Or([If(j==k, Not(Q[j*n+i]), Q[j*n+i]) for j in range(n)])) for k in range(n)]) for i in range(n)])  #每一列有且仅有一个为True
    outer1 = []
    outer2 = []
    for j in range(2*n-1):#0-6
        inner = []
        literal = []
        for i in range(n):
            if(j-i < n and j-i >=0):
                literal += [Q[(j-i)*n+i]]
        outer_list = [Not(Or(literal))]
        for a in range(len(literal)):
            inner_list = []
            for b in range(len(literal)):
                if(b == a):
                    inner_list += [Not(literal[b])]
                else:
                    inner_list += [literal[b]]
            outer_list += [Not(Or(inner_list))]
        outer1 += [Or(outer_list)]
    for j in range(-n+1,n):#0-3
        inner = []
        literal = []
        for i in range(n):
            if(j+i < n and j+i >= 0):
                literal += [Q[(j+i)*n+i]]
        outer_list = [Not(Or(literal))]
        # print(literal)
        for a in range(len(literal)):
            inner_list = []
            for b in range(len(literal)):
                if(b == a):
                    inner_list += [Not(literal[b])]
                else:
                    inner_list += [literal[b]]
            outer_list += [Not(Or(inner_list))]
        outer2 += [Or(outer_list)]
    diag_c = And(And(outer1), And(outer2))

    time_start=time.perf_counter()
    solve(row_c + col_c + diag_c)
    time_end=time.perf_counter()
    print('time cost for smt:',time_end-time_start,'s')