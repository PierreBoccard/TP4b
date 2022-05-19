#!/usr/bin/env python3

from curses import pair_content
import numpy as np
import matplotlib
matplotlib.use('Agg')


from numba import jit
from time import perf_counter

@jit(nopython=True)
def vitesser(galaxies, voids, s):
    s[:, 0] = np.linspace(0.5, 119.5, 120)

    for i in range(len(galaxies)):
        for j in range(len(voids)):
            rij = np.sqrt((galaxies[i, 0] - voids[j, 0]) ** 2 + (galaxies[i, 1] - voids[j, 1]) ** 2 + (galaxies[i, 2] - voids[j, 2]) ** 2)
            for k in range(len(s[:, 0])):
                if (rij< s[k, 0] + 0.5) and (rij >= s[k, 0] - 0.5):
                    s[k, 1] = s[k, 1] + ((galaxies[i, 3] * voids[j, 0]) + (galaxies[i, 4] * voids[j, 1]) + (galaxies[i, 5] * voids[j, 2])) / rij

def vitesser_nonumba(galaxies, voids, s):
    s[:, 0] = np.linspace(0.5, 119.5, 120)

    for i in range(len(galaxies)):
        for j in range(len(voids)):
            rij = np.sqrt((galaxies[i, 0] - voids[j, 0]) ** 2 + (galaxies[i, 1] - voids[j, 1]) ** 2 + (galaxies[i, 2] - voids[j, 2]) ** 2)
            for k in range(len(s[:, 0])):
                if (rij < s[k, 0] + 0.5) and (rij >= s[k, 0] - 0.5):
                    s[k, 1] = s[k, 1] + ((galaxies[i, 3] * voids[j, 0]) + (galaxies[i, 4] * voids[j, 1]) + (galaxies[i, 5] * voids[j, 2])) / rij


if __name__ == "__main__":

    # load data
    galaxies = np.loadtxt('galaxies.txt')
    voids = np.loadtxt('voids.txt')

    # filter data
    voids_filtered = voids[(voids[:, 3] > 16) & (voids[:, 3] < 50)]

    # allocate memory
    s = np.zeros((120, 2))

    # analyze data (in-place) with numba
    tic = perf_counter()
    vitesser(galaxies, voids, s)
    toc = perf_counter()
    print(f"Analysis with numba: {toc - tic}s")

    # analyze data (in-place) without numba
    tic = perf_counter()
    vitesser_nonumba(galaxies, voids, s)
    toc = perf_counter()
    print(f"Analysis without numba: {toc - tic}s")
