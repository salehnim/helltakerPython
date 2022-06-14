            if (X1 in blocks) and free(X2, map_rules) and not (X2 in blocks) :
                temp = {'blocks' : {X2} | blocks - {X1} ,'hero' : X1, 'mobs' : mobs}
                return temp
            else :
                return None