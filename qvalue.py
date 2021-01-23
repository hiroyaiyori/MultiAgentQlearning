import random

import numpy as np

from setting import *
from field import Field


class Hunter:
    def __init__(self, hunter_id):
        self.qvalue = np.zeros([P_SEARCH_AREA ** 2 + 1, P_SEARCH_AREA ** 2 + 1, LMD])
        self.hunter_id = hunter_id
        self.ii = 2 * hunter_id
        self.ij = 2 * hunter_id + 1
        self.oi = 2 * (1 - hunter_id)
        self.oj = 2 * (1 - hunter_id) + 1
        return

    def h_recognize(self, f: Field):
        hti = (f.target_i[0] - f.hunter_i[self.ii]) % FIELD_SIZE
        htj = (f.target_i[1] - f.hunter_i[self.ij]) % FIELD_SIZE
        hoi = (f.hunter_i[self.oi] - f.hunter_i[self.ii]) % FIELD_SIZE
        hoj = (f.hunter_i[self.oj] - f.hunter_i[self.ij]) % FIELD_SIZE
        tsn = self.calc_sn(hti, htj)
        osn = self.calc_sn(hoi, hoj)
        return tsn, osn

    def calc_sn(self, i, j):

        i_s = -1
        if i >= FIELD_SIZE - P_SEARCH_DIST:
            i_s = i - (FIELD_SIZE - P_SEARCH_DIST)
        elif i <= P_SEARCH_DIST:
            i_s = i + P_SEARCH_DIST

        j_s = -1
        if j >= FIELD_SIZE - P_SEARCH_DIST:
            j_s = j - (FIELD_SIZE - P_SEARCH_DIST)
        elif j <= P_SEARCH_DIST:
            j_s = j + P_SEARCH_DIST
        if i_s >= 0 and j_s >= 0:
            sn = i_s * P_SEARCH_AREA + j_s
        else:
            sn = P_SEARCH_AREA ** 2
        return sn

    def get_q_value(self, f: Field):
        tsn, osn = self.h_recognize(f)
        return self.qvalue[tsn][osn]

    def decide_movement(self, f: Field):
        '''
        decide movement by epsilon greedy
        :param f: Field instance
        :return: decided movement direction index
        '''
        q_l = self.get_q_value(f)
        max_p_m = np.argmax(q_l)
        weights = [1 - EPSILON if i == max_p_m else EPSILON / (LMD - 1) for i in range(LMD)]
        decided_m = random.choices(list(range(LMD)), weights=weights)
        return decided_m[0]

    def update_qvalue(self, f: Field, pres: tuple, m: int, r):
        '''
        update q value
        :param f: the instance of Field class
        :param pres: (pre_tsn, pre_osn)
        :param m: movement direction index
        :param r: reward which the agent got
        :return:
        '''
        post_q_max = self.get_q_value(f).max()
        self.qvalue[pres[0]][pres[1]][m] = (1 - ALPHA) * self.qvalue[pres[0]][pres[1]][m] + ALPHA * (
                    r + GAMMA * post_q_max)
