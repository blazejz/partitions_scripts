#!/usr/bin/env python3

import argparse
import numpy as np
import itertools as it

TYPE = np.int64


def gen_levels(mod):
    old = np.array([[1]], dtype=TYPE)
    whole = old
    yield whole

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
        whole = np.pad(whole, ((h, 0), (1, 0)), mode='constant')
        whole[:h] += new
        yield whole


def main(mod):
    for lvl in gen_levels(mod):
        failed = False
        print("=== test ===")
        print(lvl.shape)
        # print(lvl)

        h, w = lvl.shape
        for py_v in it.product(range(mod), repeat=w):
            v = np.array(py_v, dtype=TYPE)

            multiplied = (((lvl * v) % mod).sum(axis=1) % mod)
            result = np.any(multiplied == 0)
            print(v)
            print(lvl[multiplied == 0])

            if not result:
                failed = True
                break

        if not failed:
            print("=== result ===")
            print(lvl)
            return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mod', type=int, required=True)
    main(**vars(parser.parse_args()))
