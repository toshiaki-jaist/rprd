#
# Copyright (c) 2021 Toshiaki Aoki. All rights reserved.
#
from z3 import *

# Box (Car, Box, Step): Bool
# Pos (Car, Box): Int
# Lane (Car, Box): Int
Box = Function ('Box', IntSort(), IntSort(), IntSort(), BoolSort())
Pos = Function ('Pos', IntSort(), IntSort(), IntSort())
Lane = Function ('Lane', IntSort(), IntSort(), IntSort())
c2i = {}
solver = Solver()

class Model:
    def __init__(self):
        self.cars = []
        self.boxes = []
        self.position = []
        self.lane = []
        self.inits = []
        self.ntrans = []
        self.ctrans = []
        self.netrans = []
        self.strans = []
        self.max_step = 0
        self.num_model = 0
        self.debug_const = False
        self.debug_count = False

    def set_car(self,cs):
        self.cars = cs
    def get_car(self):
        return self.cars
    def append_car(self,cs):
        self.cars = self.cars + cs
    def add_car(self,c):
        self.cars.append(c)

    def set_box(self,bs):
        self.boxes = bs
    def get_box(self):
        return self.boxes
    def append_box(self,bs):
        self.boxes = self.boxes + bs
    def add_box(self,b):
        self.boxes.append(b)
        
    def set_position(self,ps):
        self.position = ps
    def get_position(self):
        return self.position
    def append_position(self,ps):
        self.position = self.position + ps
    def add_position(self,p):
        self.position.append(p)

    def set_lane(self,ls):
        self.lane = ls
    def get_lane(self):
        return self.lane
    def append_lane(self,ls):
        self.lane = self.lane + ls
    def add_lane(self,l):
        self.lane.append(l)

    def set_init(self,bs):
        self.inits = bs
    def get_init(self):
        return self.inits
    def append_init(self,bs):
        self.inits = self.inits + bs
    def add_init(self,b):
        self.inits.append(b)

    def set_ntrans(self,ts):
        self.ntrans = ts
    def get_ntrans(self):
        return self.ntrans
    def append_ntrans(self,ts):
        self.ntrans = self.ntrans + ts
    def add_ntrans(self,t):
        self.ntrans.append(t)

    def set_ctrans(self,ts):
        self.ctrans = ts
    def get_ctrans(self):
        return self.ctrans
    def append_ctrans(self,ts):
        self.ctrans = self.ctrans + ts
    def add_ctrans(self,t):
        self.ctrans.append(t)

    def set_netrans(self,ts):
        self.netrans = ts
    def get_netrans(self):
        return self.netrans
    def append_netrans(self,ts):
        self.netrans = self.netrans + ts
    def add_netrans(self,t):
        self.netrans.append(t)
        
    def set_strans(self,ts):
        self.strans = ts
    def get_strans(self):
        return self.strans
    def append_strans(self,ts):
        self.strans = self.strans + ts
    def add_strans(self,t):
        self.strans.append(t)

def init(m):
    i = 0
    for c in m.cars:
        c2i[c] = i
        i = i + 1

#add initial boxes
def add_init(m):
    for (c,n) in m.inits:
        solver.add (Box(c2i[c], n, 0))
    for (c,n) in m.boxes:
        if not ((c,n) in m.inits):
            solver.add(Not(Box (c2i[c], n, 0)))

# generating constaints for normal transitions
def ps_ntrans(ts, bx, s):
    ps = []
    for (c1,n1,c2,n2) in ts:
        props = []
        props.append(Box (c2i[c1], n1, s))
        props.append(Not (Box(c2i[c1], n1, s+1)))
        props.append(Box (c2i[c2], n2, s+1))
        for (c, n) in bx:
            if not ((c1, n1) == (c,n) or (c2,n2) == (c,n)):
                props.append(Box (c2i[c],n,s) == Box (c2i[c],n,s+1))
        ps.append(And (props))
    return ps

# generating constaints for conditonal transitions
def ps_ctrans(ts,bx,s):
    ps = []
    for (c1,n1,c2,n2,c3,n3) in ts:
        props = []
        props.append(Box (c2i[c1], n1, s))
        props.append(Box (c2i[c3], n3, s))
        props.append(Not (Box(c2i[c1], n1, s+1)))
        props.append(Box (c2i[c2], n2, s+1))
        for (c, n) in bx:
            if not ((c1, n1) == (c,n) or (c2,n2) == (c,n)):
                props.append(Box (c2i[c],n,s) == Box (c2i[c],n,s+1))
        ps.append(And (props))
    return ps

# generating constraints for conditional (not exist) transitions
def ps_netrans(ts,bx,s):
    ps = []
    for (c1,n1,c2,n2,c3,n3) in ts:
        props = []
        props.append(Box (c2i[c1], n1, s))
        props.append(Not(Box (c2i[c3], n3, s)))
        props.append(Not (Box(c2i[c1], n1, s+1)))
        props.append(Box (c2i[c2], n2, s+1))
        for (c, n) in bx:
            if not ((c1, n1) == (c,n) or (c2,n2) == (c,n)):
                props.append(Box (c2i[c],n,s) == Box (c2i[c],n,s+1))
        ps.append(And (props))
    return ps

# generating constaints for synchronized transitions
def ps_strans(tss, bx, s):
    ps = []
    for ts in tss:
        props = []
        ds = []
        for (c1,n1,c2,n2) in ts:
            props.append(Box (c2i[c1], n1, s))
            props.append(Not (Box(c2i[c1], n1, s+1)))
            props.append(Box (c2i[c2], n2, s+1))
        for (c, n) in bx:
            if all (not ((c,n) == (c3,n3) or (c,n) == (c4,n4)) for (c3,n3,c4,n4) in ts):
                props.append(Box (c2i[c],n,s) == Box (c2i[c],n,s+1))
        ps.append(And (props))
    return ps
    
# generating constraints for no transition
def p_disable (ts, cs, nes, sss, bx, s):
    props1 = []
    for (c1,n1,c2,n2) in ts:
        props1.append(Not(Box(c2i[c1],n1,s)))
    for (c1,n1,c2,n2,c3,n3) in cs:
        props1.append(Not(And(Box(c2i[c1],n1,s), Box(c2i[c3],n3,s))))
    for (c1,n1,c2,n2,c3,n3) in nes:
        props1.append(Not(And(Box(c2i[c1],n1,s), Not(Box(c2i[c3],n3,s)))))
    for ss in sss:
        ps = []
        for (c1,n1,c2,n2) in ss:
            ps.append (Not(Box(c2i[c1],n1,s)))
        props1.append (Or (ps))
    props2 = []
    for (c,n) in bx:
        props2.append(Box (c2i[c],n,s) == Box (c2i[c],n,s+1))
    return (And(props2 + props1))

#def add_trans(ts, cs, nes, ss, bx, n):
def add_trans(m):
    for i in range(m.max_step):
        solver.add(Or (ps_ntrans(m.ntrans,m.boxes,i) + ps_ctrans(m.ctrans, m.boxes,i) + ps_netrans(m.netrans,m.boxes,i) + ps_strans(m.strans,m.boxes,i) + [p_disable(m.ntrans, m.ctrans, m.netrans, m.strans, m.boxes, i)]))

#add position constraints
def add_pos(m):
    for (c, n, p) in m.position:
        solver.add(Pos (c2i[c], n) == p)
    if m.debug_const:
        result = solver.check()        
        if result == sat:
            print ("position constraints are satisfiable")
        else:
            print ("position constraints are unsatisfiable")
    
#add position precedence constraint
def add_prec(bx1,bx2,ms):
    ps = []
    nps = []
    for t in range(ms + 1):
        ps.append(And(Box(c2i[bx1[0]], bx1[1], t), Box(c2i[bx2[0]], bx2[1], t), Pos(c2i[bx1[0]], bx1[1]) < Pos(c2i[bx2[0]], bx2[1])))
        nps.append(And(Not(Box(c2i[bx1[0]], bx1[1], t)), Not(Box(c2i[bx2[0]], bx2[1], t))))
    ps.append(And(nps))
    solver.add(Or(ps))
#        ps.append(Implies(And(Box(c2i[bx1[0]], bx1[1], t), Box(c2i[bx2[0]], bx2[1], t)), Pos(c2i[bx1[0]], bx1[1]) < Pos(c2i[bx2[0]], bx2[1])))

#add lane constraints
def add_lane(m):
    for (c, n, l) in m.lane:
        solver.add(Lane (c2i[c], n) == l)
    if m.debug_const:
        result = solver.check()
        if result == sat:
            print ("position and lane constraints are satisfiable")
        else:
            print ("position or lane constraints are unsatisfiable")

#add collision constraints
def ps_col(bx, ms):
    ps = []
    for t in range(ms + 1):
        for (c1,b1) in bx:
            for (c2,b2) in bx:
                if not (c1 == c2 and b1 == b2):
                    ps.append(And(Box(c2i[c1], b1, t), Box(c2i[c2], b2, t), Pos(c2i[c1], b1) == Pos(c2i[c2], b2), Lane(c2i[c1], b1) == Lane(c2i[c2], b2)))
    return ps

def ps_colc(bx, ms, c1, c2):
    ps = []
    for t in range(ms + 1):
        for (c3,b3) in bx:
            for (c4,b4) in bx:
                if (c1 == c3 and c2 == c4):
                    ps.append(And(Box(c2i[c3], b3, t), Box(c2i[c4], b4, t), Pos(c2i[c3], b3) == Pos(c2i[c4], b4), Lane(c2i[c3], b3) == Lane(c2i[c4], b4)))
    return ps

def add_col(m):
    solver.add(Or(ps_col(m.boxes, m.max_step)))

def add_noncol(m):
    solver.add(Not(Or(ps_col(m.boxes, m.max_step))))

# collision of c1 and c2
def add_colc(m, c1, c2):
    solver.add(Or(ps_colc(m.boxes, m.max_step, c1, c2)))    

def add_noncolc(m, c1, c2):
    solver.add(Not(Or(ps_colc(m.boxes, m.max_step, c1, c2))))

#count the number of scenarios
def enum_count(m):
    cnt = 0
    while True:
        result = solver.check()
        if result == sat:
            cnt = cnt + 1
            if m.debug_count:
                print(cnt)
            model = solver.model()
            #add negation of model
            or_list = []
            for j in range (m.max_step + 1):
                for (c,n) in m.boxes:
                    if model.evaluate(Box(c2i[c],n,j)):
                        or_list.append(Not(Box(c2i[c],n,j)))
                    else:
                        or_list.append(Box(c2i[c],n,j))
            if or_list != []:
                solver.add(Or (or_list))
        else:
            break
    return cnt

#enumerate snap shots
def enum_ss(m):
    history = []
    for i in range(m.num_model):
        result = solver.check()
        if result == sat:
            model = solver.model()
            history.append([])
            #make history
            for j in range (m.max_step + 1):
                ss = []
                for (c,n) in m.boxes:
                    if model.evaluate(Box(c2i[c],n,j)):
                        p = (model.evaluate(Pos(c2i[c], n))).as_long()
                        l = (model.evaluate(Lane(c2i[c], n))).as_long()
                        history[i].append((c,n,l,p,j))
            #add negation of model
            or_list = []
            for j in range (m.max_step + 1):
                for (c,n) in m.boxes:
                    if model.evaluate(Box(c2i[c],n,j)):
                        or_list.append(Not(Box(c2i[c],n,j)))
                    else:
                        or_list.append(Box(c2i[c],n,j))
            if or_list != []:
                solver.add(Or (or_list))
        else:
            break
    return history

def pretty_print(hs):
    cnt = 1
    for h in hs:
        print ("------------- %d ----------------" % cnt)
        cs = h[0][4]
        for (c, n, l, p, s) in h:
            if not(cs == s):
                print ("")
                cs = s
            print ("(%s %d) @ (%d, %d) at %d" % (c, n, l, p, s))
        cnt = cnt + 1

def col_print(hs):
    cnt = 0
    for h in hs:
        cnt = cnt + 1
        print ("--------------%d-------------" %cnt)
        prev = 0
        for (c,n,l,p,s) in h:
            flag = False
            if not (s == prev):
                prev = s
                print ("")
            for (c1,n1,l1,p1,s1) in h:
                if (p == p1) and (l == l1) and (s == s1) and not (c == c1) and not(n == n1 and c == c1):
                    print ("<<<(%s %d) @ (%d, %d) at %d>>>" % (c, n, l, p, s))
                    flag = True
            if not flag:
                print ("(%s %d) @ (%d, %d) at %d" % (c, n, l, p, s))

def print_constraints():
    for c in solver.assertions():
        print (c)

#c: cars, p: pos, l: lane, ib: init_box, bx: box
#nt:ntrans, ct:ctrans, net; netrans, st:strans
#nm: NUM_MODEL, ms: MAX_STEP
#def road_gen(c,p,l,ib,bx,nt,ct,net,st,nm,ms):
def road_gen(m):
    init(m)
    add_pos(m)
    add_lane(m)
    add_init(m)
    add_trans(m)
# for debug
#    print_constraints()
    return (enum_ss(m))

#def add_constraints(c,p,l,ib,bx,nt,ct,net,st,ms):
def add_constraints(m):
    init(m)
    add_pos(m)
    add_lane(m)
    add_init(m)
    add_trans(m)
