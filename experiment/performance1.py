from z3 import *
from gcpd import *
import time
import math

def tnum(x):
    return (math.factorial(2 * x))/(math.factorial(x)*math.factorial(x))

print ("steps, models, time to add, time to enumerate, check")
for i in range (1, 11):
    perf1 = Model()
    perf1.set_car ( ["LCar", "RCar"])
    perf1.append_box ([("LCar", n) for n in range(i+1)] + [("RCar", n) for n in range(i+1)])
    perf1.append_position ([("LCar", n, n) for n in range(i+1)] + [("RCar", n, n) for n in range(i+1)])
    perf1.append_lane ([("LCar", n, 0) for n in range(i+1)] + [("RCar", n, 1) for n in range(i+1)])
    perf1.set_init  ([("LCar", 0), ("RCar", 0)])
    perf1.append_ntrans ([("LCar", n, "LCar", n+1) for n in range (i)])
    perf1.append_ntrans ([("RCar", n, "RCar", n+1) for n in range (i)])
    solver.reset()
    s_time = time.time()
    perf1.max_step = i*2
    add_constraints(perf1)
    e_time1 = time.time()
    num = s_count(perf1)
    e_time2= time.time()
    print (("%d, %d, %f, %f, %d") % (i, num, e_time1 - s_time, e_time2 - e_time1, tnum(i)))
