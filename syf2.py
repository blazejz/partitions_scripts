#!/usr/bin/env python3

import argparse
import numpy as np

TYPE = np.int64


# Level Generator
#
# arguments:
#   mod: modulo
#   arity
def gen_levels(mod, arity):
    # level is initially 2-D array $[1]$
    old = np.array([[1]], dtype=TYPE)

    # yield the result keeping state of the generator
    yield old

    # infinite loop
    while True:
        # set old_h and old_w to height and width of previous level
        old_h, old_w = old.shape

        # compute new dimensions $\text{h} := 1 + \text{old\_h} \cdot \text{arity}$
        h = 1 + old_h * arity
        # $\text{w} := \text{old\_w} + 1$
        w = old_w + 1

        # initialize new level with zeros
        new = np.zeros((h, w), dtype=TYPE)
        # add $1$ to first column
        new[:, 0] += 1
        # for each $row$ in the array $i$ is number of the $row$
        for i, row in enumerate(old):
            # for $j$ in range $[0, arity)$
            for j in range(arity):
                # for each row in the new level with index $\ge 2 i + 1 + j$ add $[0, \text{row from the old level}]$
                new[2*i+1+j:, 1:] += row

        # apply modulo on new level
        new %= mod

        # we need to remember only the last level
        old = new
        # yield generated level
        yield old


# Recursive Level Checker
#
# arguments:
#   lvl: currently beeing checked level
#   prev: previous table
#   mod: modulo
#   levels: total number of generated levels
#   step: step of algorithm
def check(lvl, prev, mod, levels, step):
    # if we checked the whole generated depth, return failure
    if lvl >= len(levels):
        return None

    # set $\text{result}$ initially to level number
    result = lvl

    if prev is None:
        # if we have no previous, define $\text{prev} := [0]$
        prev = np.zeros(1)
    else:
        # else add $1$-row padding from the left using value $0$
        prev = np.pad(prev, (1, 0), mode='constant')

    # for $k$ in $0, \text{step}, 2\text{step}, 3\text{step}, \ldots, \text{mod}-1$
    for k in range(0, mod, step):
        prev[0] = k
        # Let's multiply each row of considered level and multiply it elementwise by prev.  If sum of the received row is equivalent to $0$ modulo $mod$, continue the search
        if np.any(((levels[lvl] * prev).sum(axis=1) % mod) == 0):
            continue
        # the oposite case
        else:
            # check next level recursively
            r = check(lvl + 1, prev, mod, levels, step)
            if r is None:
                # if algorithm wasn't able to find satisfying result, return failure
                return None
            else:
                # in the oposite case, remember only the greatest result
                result = max(result, r)

    return result


# Main method
#
# arguments:
#   mod: modulo
#   levels: total number of generated levels
#   arity
#   step: step of algorithm
def main(mod, levels, arity, step):
    # list of precomputed levels
    levels_list = []

    # generate levels for given modulo and arity upto given depth
    for i, lvl in enumerate(gen_levels(mod, arity)):
        # store the level
        levels_list.append(lvl)
        # stop the process if we generated required number of levels
        if i >= levels - 1:
            break

    # check, whether generated case is valid
    result = check(0, None, mod, levels_list, step)

    # we count levels from zero, so add 1 to the result
    if result is not None:
        result += 1

    # print the result
    print(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mod', type=int, required=True)
    parser.add_argument('--step', type=int, default=1)
    parser.add_argument('--levels', type=int, default=10)
    parser.add_argument('--arity', type=int, default=2)
    main(**vars(parser.parse_args()))
