#!/usr/bin/env python3

import argparse
import numpy as np

TYPE = np.int64


def gen_levels(mod):
    old = np.array([[1]], dtype=TYPE)
    yield old

    while True:
        old_h, old_w = old.shape

        h = 1 + old_h + old_h
        w = old_w + 1

        new = np.zeros((h, w), dtype=TYPE)
        new[:, 0] += 1
        for i, row in enumerate(old):
            new[2*i+1:, 1:] += row
            new[2*i+2:, 1:] += row

        new %= mod

        old = new
        yield old


def check(lvl, prev, mod, levels):
    if lvl >= len(levels):
        return None

    result = lvl

    if prev is None:
        prev = np.zeros(1)
    else:
        prev = np.pad(prev, (1, 0), mode='constant')

    for k in range(mod):
        prev[0] = k
        if np.any(((levels[lvl] * prev).sum(axis=1) % mod) == 0):
            continue
        else:
            r = check(lvl + 1, prev, mod, levels)
            if r is None:
                return None
            else:
                result = max(result, r)

    return result


def main(mod, levels):
    levels_list = []

    for i, lvl in enumerate(gen_levels(mod)):
        levels_list.append(lvl)
        if i >= levels - 1:
            break

    print(check(0, None, mod, levels_list))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mod', type=int, required=True)
    parser.add_argument('--levels', type=int, required=True)
    main(**vars(parser.parse_args()))