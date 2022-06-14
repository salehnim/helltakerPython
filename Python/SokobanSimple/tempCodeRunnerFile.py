actions = {d : Action('move',d) for d in 'udrl'} | {d.upper() : Action('push',d) for d in 'udrl'}
s0 = {'me': (3, 3),
'boxes': {(3, 4), (3, 2)}}
map_rules = {'goals': {(3, 1), (3,5)}, 
'walls': {},'actions': actions}