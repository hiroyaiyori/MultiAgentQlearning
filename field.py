import random

from setting import *


class Field:
    '''
    self.field: 2d list (FIELD_SIZE+P_SEARCH_AREA*2,FIELD_SIZE+P_SEARCH_AREA*2)
    -1:not in field
    0: in field
    1: hunter
    2: target

    '''

    def __init__(self):
        self.hunter_i = [random.randrange(0, FIELD_SIZE), random.randrange(0, FIELD_SIZE),
                         random.randrange(0, FIELD_SIZE), random.randrange(0, FIELD_SIZE)]
        self.target_i = [random.randrange(0, FIELD_SIZE), random.randrange(0, FIELD_SIZE)]
        return


    def catch_detection(self):
        '''
        :return: the number of hunter which exists neighbor of target
        '''
        neighbor_hunter_n = 0
        for m in MOVABLE_DIRECTION:
            movedi = (self.target_i[0] + m[0]) % FIELD_SIZE
            movedj = (self.target_i[1] + m[1]) % FIELD_SIZE
            if (movedi == self.hunter_i[0] and movedj == self.hunter_i[1]) or \
                    (movedi == self.hunter_i[2] and movedj == self.hunter_i[3]):
                neighbor_hunter_n += 1
        return neighbor_hunter_n

    def move_agent(self, id, m):
        '''
        move agent
        :param id: 0:hunter0, 1:hunter1, 2:target
        :param m: move direction index
        :return:
        '''
        if id != 2:
            ii = 2 * id
            ij = 2 * id + 1
            oi = 2 * (1 - id)
            oj = 2 * (1 - id) + 1
            movedi = (self.hunter_i[ii] + MOVABLE_DIRECTION[m][0]) % 10
            movedj = (self.hunter_i[ij] + MOVABLE_DIRECTION[m][1]) % 10
            if (movedi != self.hunter_i[oi] or movedj != self.hunter_i[oj]) and \
                    (movedi != self.target_i[0] or movedj != self.target_i[1]):
                self.hunter_i[ii] = movedi
                self.hunter_i[ij] = movedj
        else:
            self.target_i[0] = (self.target_i[0] + MOVABLE_DIRECTION[m][0]) % 10
            self.target_i[1] = (self.target_i[1] + MOVABLE_DIRECTION[m][1]) % 10
        return
