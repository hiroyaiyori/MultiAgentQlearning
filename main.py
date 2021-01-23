import random
import matplotlib.pyplot as plt


from setting import *
from field import Field
from qvalue import Hunter


def qlearn_step(f: Field, h0: Hunter, h1: Hunter):
    # move hunter0
    m0 = h0.decide_movement(f)
    pre_s0 = h0.h_recognize(f)
    f.move_agent(0, m0)

    # move hunter1
    m1 = h1.decide_movement(f)
    pre_s1 = h1.h_recognize(f)
    f.move_agent(1, m1)

    # move target
    f.move_agent(2, random.randrange(0, 4))

    # ask reward
    neighbor_hunter_n = f.catch_detection()
    if neighbor_hunter_n == 2:
        reward = CATCH_REWARD
    else:
        reward = MOVEMENT_REWARD

    # update q_value
    h0.update_qvalue(f, pre_s0, m0, reward)
    h1.update_qvalue(f, pre_s1, m1, reward)
    return neighbor_hunter_n == 2


if __name__ == "__main__":
    h0 = Hunter(0)
    h1 = Hunter(1)

    epi_itern_l = []
    for i in range(EPISODE_N):
        f = Field()
        itern = 0
        while True:
            fin = qlearn_step(f, h0, h1)
            itern += 1
            if fin:
                break
        epi_itern_l.append(itern)
        print(i, itern)
    plt.plot(list(range(EPISODE_N)), epi_itern_l, linewidth=1)
    plt.xlabel("Number of Trials")
    plt.ylabel("Steps to Catch")
    plt.savefig("figure")
