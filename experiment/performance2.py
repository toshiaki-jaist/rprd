from z3 import *
from gcpd import *
import time


print ("steps, time to add, time to solve, boolean vars, clauses, memory, max-memory")
for i in range (1, 101):
    perf2 = Model()
    perf2.set_car (["LCar", "RCar"])
    perf2.append_box ([("LCar", n) for n in range(i+1)] + [("RCar", n) for n in range(i+1)])
    perf2.append_position ([("LCar", n, n) for n in range(i+1)] + [("RCar", n, n) for n in range(i+1)])
    perf2.append_lane ([("LCar", n, 0) for n in range(i+1)] + [("RCar", n, 1) for n in range(i+1)])
    perf2.set_init ([("LCar", 0), ("RCar", 0)])
    perf2.append_ntrans ([("LCar", n, "LCar", n+1) for n in range (i)])
    perf2.append_ntrans ([("RCar", n, "RCar", n+1) for n in range (i)])
    solver.reset()
    perf2.max_step = i*2
    s_time = time.time()
    add_constraints(perf2)
    e_time1 = time.time()
    solver.check()
    e_time2 = time.time()
    stat = solver.statistics()
    nb = 0
    nc = 0
    mm = 0
    mxm = 0
    for (k,v) in stat:
        if k == "mk bool var":
            nb = v
        if k == "mk clause":
            nc = v
        if k == "memory":
            mm = v
        if k == "max memory":
            mxm = v
    print (("%d, %f, %f, %d, %d, %f, %f") % (i, e_time1 - s_time, e_time2 - e_time1, nb, nc, mm, mxm))
