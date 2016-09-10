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


def find_b5(m):
    bound = m*m + m + 1
    primes = set(find_primes(m + 2, bound + 1))
    results = {}

    b = [1]
    i = 1

    while len(primes):
        if i % m == 0:
            t = b[(i - 5) // 5 + 1] + b[i - 5]
        else:
            t = b[i - 1]
        b.append(t)
        for p in primes.copy():
            if t % p == 0:
                primes.remove(p)
                results[p] = {'n': i, 'b': t}
        i += 1

    return results


def print_minipage(lines):
    print("\\begin{minipage}[t]{.23\\textwidth}")
    print("\\begin{displaymath}")
    print("\\begin{array}{|c|c|c|}")
    print("\\hline")
    print("m & p & n_{1} \\\\ \\hline")

    for i, line in enumerate(lines):
        if i == 0 or lines[i - 1][0] != lines[i][0]:
            print("\\hline")

        print("{} & {} & {} \\\\ \\hline".format(*line))

    print("\\end{array}")
    print("\\end{displaymath}")
    print("\\end{minipage}")


def print_minipages(lines, k):
    print("\\begin{center}")
    for i in range(0, len(lines), k):
        print_minipage(lines[i:i+k])
    print("\\end{center}")


def main(min_m, max_m):
    print("\\documentclass[a4paper, 10pt]{article}")
    print("\\usepackage[a4paper, top=3.5cm, bottom=3.5cm]{geometry}")
    print("\\begin{document}")

    lines = []
    for m in range(min_m, max_m + 1):
        results = find_b5(m)
        for p in sorted(results):
            lines.append((m, p, results[p]['n'], ))

    print_minipages(lines, 45)

    print("\\end{document}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--min-m', type=int, required=True)
    parser.add_argument('--max-m', type=int, required=True)
    main(**vars(parser.parse_args()))
