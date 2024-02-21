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
        self.cstrans = []
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
    def get_position(self, c, n):
        for (c1,n1,p) in self.position:
            if c1 ==c and n1 == n:
                return p
    def append_position(self,ps):
        self.position = self.position + ps
    def add_position(self,p):
        self.position.append(p)

    def set_lane(self,ls):
        self.lane = ls
    def get_lane(self):
        return self.lane
    def get_lane(self, c, n):
        for (c1,n1,l) in self.lane:
            if c1 == c and n1 == n:
                return l

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
    def remove_ntrans(self,t):
        self.ntrans.remove(t)

    def set_ctrans(self,ts):
        self.ctrans = ts
    def get_ctrans(self):
        return self.ctrans
    def append_ctrans(self,ts):
        self.ctrans = self.ctrans + ts
    def add_ctrans(self,t):
        self.ctrans.append(t)

    # t: (c1,n1,c2,n2,[(cn,nn)])
    def set_netrans(self,ts):
        self.netrans = ts
    def get_netrans(self):
        return self.netrans
    def get_netrans4(self, c1, n1, c2, n2):
        for (c3, n3, c4, n4, cbx) in self.netrans:
            if c1 == c3 and n1 == n3 and c2 == c4 and n2 == n4:
                return (c3, n3, c4, n4, cbx)
    def append_netrans(self,ts):
        self.netrans = self.netrans + ts
    def add_netrans(self,t):
        self.netrans.append(t)
    def remove_netrans(self,t):
        self.netrans.remove(t)
    def check_netrans4(self, c1, n1, c2, n2):
        flag = False
        for (c3, n3, c4, n4, cbx) in self.netrans:
            if c1 == c3 and n1 == n3 and c2 == c4 and n2 == n4:
                flag = True
        return flag
        
    # t: (c1,n1,c2,n2,f)
    def set_cstrans(self,ts):
        self.cstrans = ts
    def get_cstrans(self):
        return self.cstrans
    def append_cstrans(self,ts):
        self.cstrans = self.cstrans + ts
    def add_cstrans(self,t):
        self.cstrans.append(t)

    def set_strans(self,ts):
        self.strans = ts
    def get_strans(self):
        return self.strans
    def append_strans(self,ts):
        self.strans = self.strans + ts
    def add_strans(self,t):
        self.strans.append(t)

    def check_loc (self, c, l, p):
        flag = False
        for (b1, n1, x) in self.lane:
            for (b2, n2, y) in self.position:
                if ( c == b1 and c == b2 and n1 == n2 and x == l and y == p):
                    flag = True
                    break
        return flag

    def get_loc (self, c, l, p):
        for (b1, n1, x) in self.lane:
            for (b2, n2, y) in self.position:
                if ( c == b1 and c == b2 and n1 == n2 and x == l and y == p):
                    return (b1, n2)

    def check_ntrans(self, c1, n1, c2, n2):
        flag = False
        for (c3,n3,c4,n4) in self.ntrans:
            if (c1 == c3 and c2 == c4 and n1 == n3 and n2 == n4):
                flag = True
        return flag

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
    for (c1,n1,c2,n2,cbx) in ts:
        props = []
        props.append(Box (c2i[c1], n1, s))
        props.append(Not (Box(c2i[c1], n1, s+1)))
        props.append(Box (c2i[c2], n2, s+1))
        for (c,n) in cbx:
            props.append(Not(Box (c2i[c], n, s)))
        for (c, n) in bx:
            if not ((c1, n1) == (c,n) or (c2,n2) == (c,n)):
                props.append(Box (c2i[c],n,s) == Box (c2i[c],n,s+1))
        ps.append(And (props))
    return ps

#
def ps_cstrans(ts,bx,s):
    ps = []
    for (c1,n1,c2,n2, f) in ts:
        props = []
        props.append(Box (c2i[c1], n1, s))
        props.append(f (s) )
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
def p_disable (ts, cs, nes, cst, sss, bx, s):
    props1 = []
    for (c1,n1,c2,n2) in ts:
        props1.append(Not(Box(c2i[c1],n1,s)))
    for (c1,n1,c2,n2,c3,n3) in cs:
        props1.append(Not(And(Box(c2i[c1],n1,s), Box(c2i[c3],n3,s))))
    for (c1,n1,c2,n2,cbx) in nes:
        ps = [Box(c2i[c1],n1,s)]
        for (c,n) in cbx:
            ps.append(Not(Box(c2i[c],n,s)))
        props1.append(Not(And(ps)))
    for (c1,n1,c2,n2, f) in cst:
        props1.append(Not(And(Box(c2i[c1],n1,s), f (s))))
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
        solver.add(Or (ps_ntrans(m.ntrans,m.boxes,i) + ps_ctrans(m.ctrans, m.boxes,i) + ps_netrans(m.netrans,m.boxes,i) + ps_cstrans(m.cstrans,m.boxes,i) + ps_strans(m.strans,m.boxes,i) + [p_disable(m.ntrans, m.ctrans, m.netrans, m.cstrans, m.strans, m.boxes, i)]))

def all_disable(m, s):
    prop = []
    for (c, n) in m.boxes:
        prop.append(Box (c2i[c],n,s) == Box (c2i[c],n,s+1))
    return (And(prop))
        
def add_trans_tm(m,cnd):
    for i in range(m.max_step):
        trans = Or (ps_ntrans(m.ntrans,m.boxes,i) + ps_ctrans(m.ctrans, m.boxes,i) + ps_netrans(m.netrans,m.boxes,i) + ps_cstrans(m.cstrans,m.boxes,i) + ps_strans(m.strans,m.boxes,i) + [p_disable(m.ntrans, m.ctrans, m.netrans, m.cstrans, m.strans, m.boxes, i)])
        c_trans = And(Not(cnd(m.boxes, i)), trans)
        n_trans = And(cnd(m.boxes, i), all_disable(m,i))
        solver.add(Or(c_trans, n_trans))

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

#collision primitives
def ps_col(c1, c2, bx, t):
    ps = []
    for b1 in [b for (c,b) in bx if c == c1]:
        for b2 in [b for (c,b) in bx if c == c2]:
            ps.append(And(Box(c2i[c1], b1, t), Box(c2i[c2], b2, t), Pos(c2i[c1], b1) == Pos(c2i[c2], b2), Lane(c2i[c1], b1) == Lane(c2i[c2], b2)))
    return Or (ps)

def ps_lp(c1, bx, l, p, t):
    ps = []
    for b1 in [b for (c,b) in bx if c == c1]:
        ps.append(And(Box(c2i[c1], b1, t), Pos(c2i[c1], b1) == p, Lane(c2i[c1], b1) == l))
    return Or(ps)
        
def ps_front(c1, bx, t):
    ps = []
    for b1 in [b for (c,b) in bx if c == c1]:
        for b2 in [b for (c,b) in bx if c == c1]:
            if not (b1 == b2):
                ps.append(And(0 < t, Box(c2i[c1], b1, t - 1), Box(c2i[c1], b2, t), Pos(c2i[c1], b1) < Pos(c2i[c1],b2)))
    return (Or (ps))

def ps_rear(c1, bx, t):
    ps = []
    for b1 in [b for (c,b) in bx if c == c1]:
        for b2 in [b for (c,b) in bx if c == c1]:
            if not (b1 == b2):
                ps.append(And(0 < t, Box(c2i[c1], b1, t - 1), Box(c2i[c1], b2, t), Pos(c2i[c1], b1) > Pos(c2i[c1],b2)))
    return (Or (ps))

def ps_right(c1, bx, t):
    ps = []
    for b1 in [b for (c,b) in bx if c == c1]:
        for b2 in [b for (c,b) in bx if c == c1]:
            if not (b1 == b2):
                ps.append(And(0 < t, Box(c2i[c1], b1, t - 1), Box(c2i[c1], b2, t), Lane(c2i[c1], b1) < Lane(c2i[c1],b2)))
    return (Or (ps))

def ps_left(c1, bx, t):
    ps = []
    for b1 in [b for (c,b) in bx if c == c1]:
        for b2 in [b for (c,b) in bx if c == c1]:
            if not (b1 == b2):
                ps.append(And(0 < t, Box(c2i[c1], b1, t - 1), Box(c2i[c1], b2, t), Lane(c2i[c1], b1) > Lane(c2i[c1],b2)))
    return (Or (ps))

# exists c1 c2 t. f(c1, c2, bx, t)
def eval_col (m, f):
    ps = []
    for c1 in m.cars:
        for c2 in m.cars:
            if not (c1 == c2):
                for t in range (m.max_step + 1):
                    ps.append(f(c1, c2, m.boxes, t))
    return Or(ps)

# exists t. f(bx, t)
def eval_col_t (m, f):
    ps = []
    for t in range (m.max_step + 1):
        ps.append(f(m.boxes, t))
    return Or(ps)

def eval_all_t (m, f):
    ps = []
    for t in range (m.max_step + 1):
        ps.append(f(m.boxes, t))
    return (And(ps))

# exists c t. f(c, bx, t)
def eval_col_c (m, f):
    ps = []
    for c in m.cars:
        for t in range (m.max_step + 1):
            ps.append(f(c, m.boxes, t))
    return (Or(ps))

def add_solver (c):
    solver.add(c)

def add_col(m):
    add_solver(eval_col(m, lambda c1, c2, bx, t: ps_col(c1, c2, bx, t)))

def add_noncol(m):
    add_solver(Not(eval_col(m, lambda c1, c2, bx, t: ps_col(c1, c2, bx, t))))

# collision of c1 and c2
def add_colc(m, c1, c2):
    add_solver(eval_col_t(m, lambda bx, t: ps_col(c1, c2, bx, t)))

def add_noncolc(m, c1, c2):
    add_solver(Not(eval_col_t(m, lambda bx, t: ps_col(c1, c2, bx, t))))

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

def print_model(m):
    print ("Cars")
    print (m.cars)
    print ("Boxes")
    print (m.boxes)
    print ("Position")
    print (m.position)
    print ("Lane")
    print (m.lane)
    print ("Inits")
    print (m.inits)
    print ("Ntrans")
    print (m.ntrans)
    print ("Ctrans")
    print (m.ctrans)
    print ("Netrans")
    print (m.netrans)
    print ("Strans")
    print (m.strans)
    print ("Max Step")
    print (m.max_step)
    print ("Num Model")
    print (m.num_model)


#c: cars, p: pos, l: lane, ib: init_box, bx: box
#nt:ntrans, ct:ctrans, net; netrans, st:strans
#nm: NUM_MODEL, ms: MAX_STEP
#def road_gen(c,p,l,ib,bx,nt,ct,net,st,nm,ms):
def s_gen(m):
    init(m)
    add_pos(m)
    add_lane(m)
    add_init(m)
    add_trans(m)
# for debug
#    print_constraints()
    return (enum_ss(m))

def s_count(m):
    init(m)
    add_pos(m)
    add_lane(m)
    add_init(m)
    add_trans(m)
    return (enum_count(m))

#def add_constraints(c,p,l,ib,bx,nt,ct,net,st,ms):
def add_constraints(m):
    init(m)
    add_pos(m)
    add_lane(m)
    add_init(m)
    add_trans(m)

# terminates if cnd becomes true
def add_constraints_tm(m,cnd):
    init(m)
    add_pos(m)
    add_lane(m)
    add_init(m)
    add_trans_tm(m,cnd)
