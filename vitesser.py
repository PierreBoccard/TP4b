

from curses import pair_content
import numpy as np
import matplotlib
import pandas as pd
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from IPython.display import display

from numba import jit
import random

# voids = pd.read_csv('/home/astro/pboccard/TP4b/DIVE-main/test.txt',sep=" ", header=None,squeeze = True,nrows = 1000,engine='python')
# #print(voids.head())
# galaxies = pd.read_csv('/home/astro/pboccard/TP4b/FCFC/Box.dat',sep="  ", usecols = [0,1,2,3,4,5],header=None,squeeze = True,nrows = 1000,engine='python')
# #print(galaxies.head())

galaxies = np.loadtxt('galaxies.txt')
voids = np.loadtxt('voids.txt')

voids2 = voids[(voids.iloc[:,3] > 16) & (voids.iloc[:,3] < 50)]
rij = np.zeros([len(galaxies),len(voids2)])
vij = np.zeros([len(galaxies),len(voids2)])

s = np.zeros((120,2))
s[:,0] = np.linspace(0.5,119.5,120)


# np.savetxt('galaxies.txt', galaxies)
# np.savetxt('voids.txt', galaxies)

#np.savetxt('galaxies.txt', galaxies.values, fmt='%d')

galaxies.to_csv('galaxies.txt', header=None, index=None, sep=' ')
voids.to_csv('voids.txt', header=None, index=None, sep=' ')
voids2.to_csv('voids2.txt', header=None, index=None, sep=' ')

# print(len(galaxies))
# print(len(voids))

# @jit(nopython=True)
# def inner_loop(i, nvoids):
#     for j in range(nvoids):
#          rij[i,j] = np.sqrt((galaxies.iloc[i,0] - voids2.iloc[j,0])**2 + (galaxies.iloc[i,1] - voids2.iloc[j,1])**2 + (galaxies.iloc[i,2] - voids2.iloc[j,2])**2)

#          for k in range(len(s[:,0])) :

#              if (rij[i,j] < s[k,0] + 0.5) and (rij[i,j] >= s[k,0] - 0.5):

#                  #vij[i,j] = ((galaxies.iloc[i,3]*voids2.iloc[j,0]) + (galaxies.iloc[i,4]*voids2.iloc[j,1]) + (galaxies.iloc[i,5]*voids2.iloc[j,2]))/rij[i,j]

#                  s[k,1] = s[k,1] + ((galaxies.iloc[i,3]*voids2.iloc[j,0]) + (galaxies.iloc[i,4]*voids2.iloc[j,1]) + (galaxies.iloc[i,5]*voids2.iloc[j,2]))/rij[i,j]


# @jit(nopython=True)
# def outer_loop(ngalaxies):
#     for i in range(ngalaxies):
#         inner_loop(i, len(voids2))

for i in range(len(galaxies)):
    for j in range(len(voids2)):
         rij[i,j] = np.sqrt((galaxies.iloc[i,0] - voids2.iloc[j,0])**2 + (galaxies.iloc[i,1] - voids2.iloc[j,1])**2 + (galaxies.iloc[i,2] - voids2.iloc[j,2])**2)

         for k in range(len(s[:,0])) :

             if (rij[i,j] < s[k,0] + 0.5) and (rij[i,j] >= s[k,0] - 0.5):

                 #vij[i,j] = ((galaxies.iloc[i,3]*voids2.iloc[j,0]) + (galaxies.iloc[i,4]*voids2.iloc[j,1]) + (galaxies.iloc[i,5]*voids2.iloc[j,2]))/rij[i,j]

                 s[k,1] = abs(s[k,1] + ((galaxies.iloc[i,3]*voids2.iloc[j,0]) + (galaxies.iloc[i,4]*voids2.iloc[j,1]) + (galaxies.iloc[i,5]*voids2.iloc[j,2]))/rij[i,j])

#outer_loop(len(galaxies))

np.savetxt('rij.txt', rij)
np.savetxt('vij.txt', vij)
np.savetxt('final.txt',np.vstack([s[:,0], s[:,1]]).T)
