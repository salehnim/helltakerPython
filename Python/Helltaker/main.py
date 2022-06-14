from collections import namedtuple
from helltaker_utils import grid_from_file

Action = namedtuple('action',('verb','direction'))
State = namedtuple('state',('hero','blocks','mobs'))

actions = {d : Action('move',d) for d in 'udrl'} | \
{d.upper() : Action('push',d) for d in 'udrl'} | \
{'m'+d : Action('push_mob', d) for d in 'udrl'} |\
{'b'+d : Action('push_block', d) for d in 'udrl'} |\
{'s' : Action('spikked', '_')}


""" def complete(m: List[List[str]], n: int):
    for l in m:
        for _ in range(len(l), n):
            l.append(" ")
    return m """


def is_fluent(char) : 
    return (char in "MHBKLTUOPQ") 

def complete(spawn, map_rules, char, x, y) : 
    res_spawn = spawn
    res_map = map_rules
    if (is_fluent(char)) : 
        if char == "M" : 
            if not 'mobs' in res_spawn.keys()  :
                res_spawn['mobs'] = {(x,y)}
            else : 
                res_spawn['mobs'].add((x,y))
        if char == "H" : 
            res_spawn['hero'] = (x,y)
        if char == "B" : 
            if not 'blocks' in res_spawn.keys() :
                res_spawn['blocks'] = {(x,y)}
            else : 
                res_spawn['blocks'].add((x,y))
    else : 
        if char == "D" : 
            res_map['demon'] = (x,y)
        if char == "#" : 
            if not "walls" in res_map.keys()  : 
                res_map["walls"] = {(x,y)}
            else : 
                res_map["walls"].add((x,y))
    return res_spawn, res_map

def completeV2(spawn, map_rules, char, x, y) : 
    res_spawn = spawn
    res_map = map_rules
    if (is_fluent(char)) : 
        if char == "M" : 
            if res_spawn['mobs'] == None  :
                res_spawn['mobs'] = {(x,y)}
            else : 
                res_spawn['mobs'].add((x,y))
        if char == "H" : 
            res_spawn['hero'] = (x,y)
        if char == "B" : 
            if res_spawn['blocks'] == None :
                res_spawn['blocks'] = {(x,y)}
            else : 
                res_spawn['blocks'].add((x,y))
    else : 
        if char == "D" : 
            res_map['demon'] = (x,y)
        if char == "#" : 
            if res_map['walls'] == None : 
                res_map["walls"] = {(x,y)}
            else : 
                res_map["walls"].add((x,y))
    return res_spawn, res_map

def grid2spawn(grid) :
    res = dict()
    map_rules = dict()
    spawn = dict()
    for i in range(len(grid)) : 
        for j in range(len(grid[i])) : 
            spawn, map_rules = complete(spawn, map_rules, grid[i][j], i, j)
    return spawn, map_rules

def grid2spawnV2(grid) :
    spawn = {'hero' : None, 'blocks' : None, 'mobs' : None}
    map_rules = {'demon' : None, 'walls' : None}
    for i in range(len(grid)) : 
        for j in range(len(grid[i])) : 
            spawn, map_rules = completeV2(spawn, map_rules, grid[i][j], i, j)
    return spawn, map_rules

def one_step(position, direction) :
    i, j = position
    return {'r' : (i,j+1), 'l' : (i,j-1), 'u' : (i-1,j), 'd' : (i+1,j), '_' : (i,j)}[direction]

def free(position, map_rules) :
    return not(position in map_rules['walls'])
def free_factory(map_rules) :
    def free(position) :
        return not(position in map_rules['walls'])
    return free

def do_fn(action, state) :
    X0 = state['hero']
    blocks = state['blocks']
    mobs = state['mobs']
    demon = map_rules['demon']
    print(demon)
    X1 = one_step(X0, action.direction)
    if action.verb == 'move' :
        if free(X1, map_rules) and (blocks == None or not (X1 in blocks)) and (mobs == None or not (X1 in mobs)) :
            return {'hero' : X1, 'blocks' : blocks, 'mobs' : mobs}
        else :
            return None
    if action.verb == 'push' :
        X2 = one_step(X1, action.direction) 
        if blocks != None : 
            print(X2 in demon)
            if (X1 in blocks) and free(X2, map_rules) and not (X2 in blocks) and not (X2 == demon) :
                print(X2, demon)
                temp = {'blocks' : {X2} | blocks - {X1} ,'hero' : X1, 'mobs' : mobs}
                print(temp)
                return temp
            else :
                return None
    if action.verb == 'push_mob' : 
        X2 = one_step(X1, action.direction)
        if mobs != None : 
            if (X1 in mobs) :
                if (not free(X2, map_rules)) or (X2 in mobs or (blocks != None and X2 in blocks)) :
                    return {'hero' : X0, 'blocks' : blocks, 'mobs' : mobs - {X1}}
                else : 
                    return {'hero' : X0, 'blocks' : blocks, 'mobs' : {X2} | mobs - {X1}}
            else : 
                return None 
    return None

test, test2 = grid2spawn([
    [' ', ' ', ' ', ' ', ' ', '#', '#', '#', ' '], 
[' ', ' ', '#', '#', '#', ' ', 'H', '#', ' '], 
[' ', '#', ' ', ' ', 'M', ' ', ' ', '#', ' '], 
[' ', '#', ' ', 'M', ' ', 'M', '#', ' ', ' '], 
['#', ' ', ' ', '#', '#', '#', '#', ' ', ' '], 
['#', ' ', 'B', ' ', ' ', 'B', ' ', '#', ' '], 
['#', ' ', 'B', ' ', 'B', ' ', ' ', 'D', '#'], 
['#', '#', '#', '#', '#', '#', '#', '#', '#']]) 
print(test)
print(test2)

grid = grid_from_file("tests/level2.txt")['grid']
print(grid)
spawn ,map_rules = grid2spawnV2(grid)
print(spawn)
print(map_rules)
map_rules["actions"] = actions
print(map_rules)

def state2frozenState(state):
    res = {}
    print()
    print(state)
    res['hero'] = state['hero']
    if state['blocks'] != None :
        res['blocks'] = frozenset(state['blocks'])
    else : 
        res['blocks'] = None 
    if state['mobs'] != None :
        res['mobs'] = frozenset(state['mobs'])  
    else : 
        res['mobs'] = None
    #temp = {'hero' : state['hero'], 'blocks' : frozenset(state['blocks']), 'mobs' : frozenset(state['mobs'])}
    print(State(**res))
    return State(**res)

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
        for letter in "urdl" : 
            if state.hero == one_step(rules['demon'], letter) : 
                return True
        return False
    return goals

def succ_factory(rules) :
    def succ(state) :
        l = [(do_fn(actions[a] ,state._asdict()),a) for a in actions]
        print("----------")
        print(l)
        
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
print(spawn)
s_end, save = search_with_parent(state2frozenState(spawn), mygoals, mysucc, remove_head, insert_tail, debug=False)

plan = ' '.join([a for s,a in dict2path(s_end,save) if a])
print(plan)
#On trouve un plan de longueur 34, presque identique à celui mis en oeuvre dans le gif, après avoir visité 481 975 états intermédiaires.
