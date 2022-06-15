from collections import namedtuple
from helltaker_utils import grid_from_file
from pprint import pprint
import config

Action = namedtuple('action',('verb','direction'))
State = namedtuple('state',('hero','blocks','mobs', 'last_spike', 'key', 'lock', 'active_traps', 'unactive_traps'))
actions = {d : Action('move',d) for d in 'udrl'} | \
{d.upper() : Action('push',d) for d in 'udrl'} | \
{'m'+d : Action('push_mob', d) for d in 'udrl'} |\
{'s' : Action('spikked', '_')}

DicoDirection = {'u' : 'haut', 'd' : 'bas', 'l' : 'gauche', 'r' : 'right'}

actions2output = {d : "deplacement : " + DicoDirection[d] for d in 'udrl'} | \
{d : "Poussage de bloc : " + DicoDirection[d.lower()] for d in 'UDRL'} | \
{'m'+d : "Poussage de mob : " + DicoDirection[d] for d in 'udrl'} |\
{'s': "Empiquage"}

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
        if char == "L" : 
            res_spawn['lock'] = (x,y)
        if char == "K" : 
            res_spawn['key'] = (x,y)
        if char == "B" : 
            if res_spawn['blocks'] == None :
                res_spawn['blocks'] = {(x,y)}
            else : 
                res_spawn['blocks'].add((x,y))
        if char == "O" : 
            if res_map['spikes'] == None :
                res_map['spikes'] = {(x,y)}
            else : 
                res_map['spikes'].add((x,y))
            if res_spawn['blocks'] == None : 
                res_spawn['blocks'] = {(x,y)}
            else : 
                res_spawn['blocks'].add((x,y))
        if char == "T" : 
            if res_spawn['unactive_traps'] == None :
                res_spawn['unactive_traps'] = {(x,y)}
            else : 
                res_spawn['unactive_traps'].add((x,y))
        if char == "O" : 
            if res_spawn['active_traps'] == None :
                res_spawn['active_traps'] = {(x,y)}
            else : 
                res_spawn['active_traps'].add((x,y))
        if char == "P" : 
            if res_spawn['unactive_traps'] == None :
                res_spawn['unactive_traps'] = {(x,y)}
            else : 
                res_spawn['unactive_traps'].add((x,y))
            if res_spawn['blocks'] == None : 
                res_spawn['blocks'] = {(x,y)}
            else : 
                res_spawn['blocks'].add((x,y))
        if char == "Q" : 
            if res_spawn['active_traps'] == None :
                res_spawn['active_traps'] = {(x,y)}
            else : 
                res_spawn['active_traps'].add((x,y))
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
        if char == "S" : 
            if res_map['spikes'] == None :
                res_map['spikes'] = {(x,y)}
            else : 
                res_map['spikes'].add((x,y)) 
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
    spawn = {'hero' : None, 'blocks' : None, 'mobs' : None, 'last_spike' : None, 'key' : None, 
    'lock' : None, 'active_traps' : None, 'unactive_traps' : None}
    map_rules = {'demon' : None, 'walls' : None, 'spikes' : None}
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
    demon = map_rules['demon']
    spikes = map_rules['spikes']
    last_spike = state['last_spike']
    key = state['key']
    lock= state['lock']
    mobs = state['mobs']
    active_traps = state['active_traps']
    unactive_traps = state['unactive_traps']
    if (active_traps != None and mobs != None) :
        mobs = mobs - active_traps
    X1 = one_step(X0, action.direction)
    if action.verb == 'spikked':
        if (spikes != None and X0 in spikes or active_traps != None and X0 in active_traps) : 
            return {'hero' : X0, 'blocks' : blocks, 'mobs' : mobs, 
            'last_spike' : None, 'key' : key, 'lock' : lock, 
            'active_traps' : active_traps, 'unactive_traps' : unactive_traps}
        else :
            return None
    if last_spike == None :  
        if action.verb == 'move' :
            if spikes != None and X1 in spikes or unactive_traps != None and X1 in unactive_traps: 
                last_spike = X1
            if key != None and X1 == key : 
                key = None
            if free(X1, map_rules) and (blocks == None or not (X1 in blocks)) and (mobs == None or not (X1 in mobs)) :
                if lock != X1 or (lock == X1 and key == None) :  
                    temp = {'hero' : X1, 'blocks' : blocks, 'mobs' : mobs, 
                    'last_spike' : last_spike, 'key' : key, 'lock' : lock, 
                    'active_traps' : unactive_traps, 'unactive_traps' : active_traps}
                    return temp
                else : 
                    return None
            else :
                return None
        if action.verb == 'push' :
            X2 = one_step(X1, action.direction) 
            if blocks != None : 
                if (X1 in blocks) :
                    if free(X2, map_rules) and not (blocks != None and X2 in blocks) and not (X2 == demon) and \
                    not (mobs != None and X2 in mobs) and lock != X2:
                        if spikes != None and X0 in spikes or unactive_traps != None and X0 in unactive_traps: 
                            last_spike = X0   
                        temp = {'blocks' : {X2} | blocks - {X1} ,'hero' : X0, 
                        'mobs' : mobs, 'last_spike' : last_spike, 'key' : key, 
                        'lock' : lock, 'active_traps' : unactive_traps, 'unactive_traps' : active_traps}
                        return temp
                    else : 
                        return {'hero' : X0, 'blocks' : blocks, 
                        'mobs' : mobs, 
                        'last_spike' : last_spike, 
                        'key' : key, 'lock' : lock, 
                        'active_traps' : unactive_traps, 'unactive_traps' : active_traps}
                else :
                    return None
        if action.verb == 'push_mob' : 
            X2 = one_step(X1, action.direction)
            if mobs != None : 
                if (X1 in mobs) :
                    if spikes != None and X0 in spikes or unactive_traps != None and X0 in unactive_traps : 
                        last_spike = X0
                    if (not free(X2, map_rules)) or (X2 in mobs or (blocks != None and X2 in blocks)
                    or (unactive_traps != None and X2 in unactive_traps) or (spikes != None and X2 in spikes)) :
                        return {'hero' : X0, 'blocks' : blocks, 
                        'mobs' : mobs - {X1}, 'last_spike' : last_spike, 
                        'key' : key, 'lock' : lock, 
                        'active_traps' : unactive_traps, 'unactive_traps' : active_traps}
                    else : 
                        return {'hero' : X0, 'blocks' : blocks, 
                        'mobs' : {X2} | mobs - {X1}, 
                        'last_spike' : last_spike, 
                        'key' : key, 'lock' : lock, 
                        'active_traps' : unactive_traps, 'unactive_traps' : active_traps}
                else : 
                    return None 
    return None 

def state2frozenState(state):
    res = {}
    res['hero'] = state['hero']
    res['lock'] = state['lock']
    res['key'] = state['key']
    res['last_spike'] = state['last_spike']
    if state['blocks'] != None :
        res['blocks'] = frozenset(state['blocks'])
    else : 
        res['blocks'] = None 
    if state['mobs'] != None :
        res['mobs'] = frozenset(state['mobs'])  
    else : 
        res['mobs'] = None
    if state['active_traps'] != None :
        res['active_traps'] = frozenset(state['active_traps'])  
    else : 
        res['active_traps'] = None
    if state['unactive_traps'] != None :
        res['unactive_traps'] = frozenset(state['unactive_traps'])  
    else : 
        res['unactive_traps'] = None
    
    #temp = {'hero' : state['hero'], 'blocks' : frozenset(state['blocks']), 'mobs' : frozenset(state['mobs'])}
    return State(**res)

def search_with_parent(s0, goals, succ, remove, insert, debug=True) :
    i = 0
    l = [s0]
    save = {s0 : None}
    s = s0
    while l:
        if debug:
            print("l =", l)
        s, l = remove(l)
        for s2,a in succ(s).items():
            if not s2 in save:
                save[s2] = (s,a) 
                i += 1
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



def dict2path(s, d, Lexique):
    l = [(s,None)]
    """ if s == None :
        return [] """
    if d[s] is None : 
        return 
    while not d[s] is None:
        parent, a = d[s]
        l.append((parent,Lexique[a]))
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
        temp = {state2frozenState(x) : a for x,a in l if x}
        return temp
    return succ


grid = grid_from_file(config.file_name)['grid']
#grid = grid_from_file("homemade_tests/impossible.txt")['grid']
spawn ,map_rules = grid2spawnV2(grid)
map_rules["actions"] = actions
mygoals = goal_factory(map_rules)
mysucc = succ_factory(map_rules)
s_end, save = search_with_parent(state2frozenState(spawn), mygoals, mysucc, remove_head, insert_tail, debug=False)
if s_end == None : 
    print("niveau impossible")
else : 
    plan = '\n'.join([a for s,a in dict2path(s_end,save, actions2output) if a])
    pprint(grid)
    print(plan)
    print("nombre d'actions : ", plan.count('\n') + 1)
#On trouve un plan de longueur 34, presque identique à celui mis en oeuvre dans le gif, après avoir visité 481 975 états intermédiaires.