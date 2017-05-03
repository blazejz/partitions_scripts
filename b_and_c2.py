#!/usr/bin/env python3

import argparse


def is_prime(k):
    p = 2
    while p * p <= k:
        if k % p == 0:
            return False
        p += 1
    return True


def find_primes(p, q):
    for k in range(p, q):
        if is_prime(k):
            yield k


def find_cm(m):
    # $\text{bound} := m^2 + m + 1$
    bound = m * m + m + 1
    # $\text{primes} := \text{set of primes from range } [m+2, \text{bound}+1)$
    primes = set(find_primes(m + 2, bound + 1))

    # results dictionary
    results = {}

    # initialize main table
    b = [1, 1]
    # counter
    i = 2

    # while any prime remains
    while len(primes):
        # if $i \equiv 1 \pmod{m}$
        if i % m == 1:
            # $t := b_{\lfloor (i - 1) / 5\rfloor} + b_{i - 5}$
            t = b[(i - 1) // 5] + b[i - 5]
        else:
            # $t := b_{i - 1}$
            t = b[i - 1]
        b.append(t)

        # foreach prime $p$ remaining
        for p in primes.copy():
            # if $t \equiv 0 \pmod{p}$
            if t % p == 0:
                # remove $p$ from set
                primes.remove(p)
                # set result for the prime $p$
                results[p] = {'n': i, 'b': t}
        i += 1

    return results


def find_bm(m):
    # $\text{bound} := m^2 + m + 1$
    bound = m * m + m + 1
    # $\text{primes} := \text{set of primes from range } [m+2, \text{bound}+1)$
    primes = set(find_primes(m + 2, bound + 1))

    # results dictionary
    results = {}

    # initialize main table
    b = [1]
    # counter
    i = 1

    # while any prime remains
    while len(primes):
        # if $i \equiv 1 \pmod{m}$
        if i % m == 0:
            # $t := b_{\lfloor i / 5\rfloor} + b_{i - 5}$
            t = b[i // 5] + b[i - 5]
        else:
            # $t := b_{i - 1}$
            t = b[i - 1]
        b.append(t)
        # foreach prime $p$ remaining
        for p in primes.copy():
            # if $t \equiv 0 \pmod{p}$
            if t % p == 0:
                # remove $p$ from set
                primes.remove(p)
                # set result for the prime $p$
                results[p] = {'n': i, 'b': t}
        i += 1

    return results


def main(min_m, max_m, func):
    lines = []
    for m in range(min_m, max_m + 1):
        if func == 'b':
            results = find_bm(m)
        elif func == 'c':
            results = find_cm(m)

        print("")
        print("m p n_1")
        for p in sorted(results):

            print("{} {} {}".format(m, p, results[p]['n']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--func', required=True)
    parser.add_argument('--min-m', type=int, required=True)
    parser.add_argument('--max-m', type=int, default=1000000000)
    main(**vars(parser.parse_args()))

