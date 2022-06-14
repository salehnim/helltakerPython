from collections import namedtuple

Action = namedtuple('action',('verb','direction'))
State = namedtuple('state',('me','boxes'))

actions = {d : Action('move',d) for d in 'udrl'} | {d.upper() : Action('push',d) for d in 'udrl'}
s0 = {'me': (2, 2),
'boxes': {(4, 4), (3, 4), (6, 5), (6, 1), (6, 4), (2, 3), (6, 3)}}
map_rules = {'goals': {(7, 4), (2, 1), (6, 6), (5, 4), (6, 3), (4, 1), (3, 5)}, 
'walls': {(4, 0), (4, 3), (3, 1), (4, 6), (5, 7), (8, 0),
(0, 2), (8, 3), (0, 5), (8, 6), (1, 0), (1, 6), (7, 7), (4, 2),
(3, 0), (5, 0), (5, 6), (3, 6), (8, 2), (8, 5), (1, 2), (0, 4),
(7, 0), (6, 7), (3, 2), (5, 2), (8, 4), (8, 1), (8, 7), (1, 1),
(0, 3), (2, 0), (0, 6), (2, 6), (6, 0)},'actions': actions}

""" actions = {d : Action('move',d) for d in 'udrl'} | {d.upper() : Action('push',d) for d in 'udrl'}
s0 = {'me': (3, 3),
'boxes': {(3, 4), (3, 2)}}
map_rules = {'goals': {(3, 1), (3,5)}, 
'walls': {},'actions': actions} """

def one_step(position, direction) :
    i, j = position
    return {'r' : (i,j+1), 'l' : (i,j-1), 'u' : (i-1,j), 'd' : (i+1,j)}[direction]

def free(position, map_rules) :
    return not(position in map_rules['walls'])
def free_factory(map_rules) :
    def free(position) :
        return not(position in map_rules['walls'])
    return free

""" def do_inplace(action, state) :
   X0 = state['me']
   boxes = state['boxes']
   X1 = one_step(X0, action.direction)
   print(type(action))
   if action.verb == 'move' :
       if free(X1, map_rules) and not (X1 in boxes) :
           state['me'] = X1
       else :
           return None
   if action.verb == 'push' :
       X2 = one_step(X1, action.direction)
       if X1 in boxes and free(X2, map_rules) and not (X2 in boxes) :
           state['me'] = X1
           state['boxes'].add(X2)
           state['boxes'].remove(X1)
       else :
           return None
   return None

state = {k : v for k,v in s0.items()}
# la ligne qui précède permet de cloner s0
# pour ne pas l'écraser
print(0,state)
for a in 'RurrddddlDRuuuuLLLrdRDrddlLdllUUdR' :
   do_inplace(actions[a],state)
   print(a,state) 

print(state['boxes']==map_rules['goals']) """

def state2frozenState(state):
    temp = {'me' : state['me'], 'boxes' : frozenset(state['boxes'])}
    return State(**temp)

def do_fn(action, state) :
    X0 = state['me']
    boxes = state['boxes']
    X1 = one_step(X0, action.direction)
    if action.verb == 'move' :
        if free(X1, map_rules) and not (X1 in boxes) :
            return {'me' : X1, 'boxes' : boxes}
        else :
            return None
    if action.verb == 'push' :
        X2 = one_step(X1, action.direction)
        if X1 in boxes and free(X2, map_rules) and not (X2 in boxes) :
            temp = {'boxes' : {X2} | boxes - {X1} ,'me' : X1}
            return temp
        else :
            return None
    
    return None

""" state = s0
print(0,state)
for a in 'RurrddddlDRuuuuLLLrdRDrddlLdllUUdR' :
   state = do_fn(actions[a],state)
   print(a,state)

print(state['boxes']==map_rules['goals']) """

""" temp = {'me' : s0['me'], 'boxes' : frozenset(s0['boxes'])}
#print(type(temps0), temps0)
#state = State(**s0)
state = State(**temp)
#print(type(state), state)
#print(0,state)
save = {}
for a in 'RurrddddlDRuuuuLLLrdRDrddlLdllUUdR' :
    #temp = do_fn(actions[a],state._asdict())
    temp = do_fn(actions[a],state._asdict())
    temp = {'me' : temp['me'], 'boxes' : frozenset(temp['boxes'])}
    newstate = State(**temp)
    #temp = State(state['me'], newstate['boxes'])
    #print(type(save), save)
    #print(type(state), state)
    #print(type(newstate), newstate)
    save[state] = newstate
    state = newstate
    print(a,state)

print(state[1])
print(map_rules['goals'])

print(state[1] ==map_rules['goals'])   """


def search_with_parent(s0, goals, succ, remove, insert, debug=True) :
    i = 0
    l = [s0]
    #print(s0)
    save = {s0 : None}
    s = s0
    #print(save)
    while l:
        if debug:
            print("l =", l)
        s, l = remove(l)
        #print(s, l)
        for s2,a in succ(s).items():
            if not s2 in save:
                save[s2] = (s,a) 
                #print(goals(s2))
                i += 1
                print("Etape : ", i)
                if goals(s2):
                    return s2, save
                insert(s2, l)
    return None, save
def insert_tail(s, l):
    l.append(s)
    return l

def remove_head(l):
    return l.pop(0), l

def remove_tail(l):
    return l.pop(), l

def dict2path(s, d):
    l = [(s,None)]
    while not d[s] is None:
        parent, a = d[s]
        l.append((parent,a))
        s = parent
    l.reverse()
    return l

def goal_factory(rules) :
    def goals(state) :
        return state.boxes == rules['goals']
    return goals

def succ_factory(rules) :
    def succ(state) :
        l = [(do_fn(actions[a] ,state._asdict()),a) for a in actions]
        #print(l)
        
        """ res = {}
        for x,a in l :
            if x : 
                print("__________________")
                print(res)
                print(State(**x))
                res[state2frozenState(x)] = a
        print(res) """
        return {state2frozenState(x) : a for x,a in l if x}
    return succ

mygoals = goal_factory(map_rules)
mysucc = succ_factory(map_rules)
print(mygoals)
print("__________________________")
print(mysucc)
print(s0)
s_end, save = search_with_parent(state2frozenState(s0), mygoals, mysucc, remove_head, insert_tail, debug=False)
print(save)
print(s_end)

plan = ' '.join([a for s,a in dict2path(s_end,save) if a])
print(plan)
#On trouve un plan de longueur 34, presque identique à celui mis en oeuvre dans le gif, après avoir visité 481 975 états intermédiaires.
