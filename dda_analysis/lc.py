#Pt 2
# Spacing Solver
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


#Calculates absorption wavelength by using a critical point
def calculate(effective_ls):
    diff_prev = -1
    #We start at a wavelength of 540 (350+190) because we are only interested in the second peak (>530nm)
    for x in range(190,450):
        diff = effective_ls[x+1]-effective_ls[x]
        if ((diff_prev > 0) and (diff < 0)):
            return x + 350
        diff_prev = diff
#Not helpful
def calculate_2nd(effective_ls):
    MAX = 1000
    for x in range(190,300):
        diff = effective_ls[x+1]-effective_ls[x]
        if (abs(diff)<MAX):
            MAX = abs(diff)
            wave = x+350
    return wave
#
# Sample Data
# This data is organized by a list where the index+1 is equal to the chain length
# And the number at the represents the number of the chains at that size
# Uncomment the sample you need, and recomment a sample if its uncommented
#

#Exp 1 size data is below
results = [317, 353, 270, 208, 125, 73, 31, 15, 7, 6, 5, 3, 2, 0, 0, 1] #Sample 10#
#results = [259, 92, 62, 55, 36, 15, 12, 5, 9, 4, 8, 2, 2, 4, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
#results = [57, 71, 96, 95, 74, 59, 42, 28] #Sample 8
#results = [59, 64, 91, 90, 79, 55, 45, 31, 31, 16, 17, 12, 7, 3, 3, 2, 7, 4, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
#results = [32, 9, 15, 18, 23, 15, 17, 11, 10, 10, 7, 4, 3, 1, 2, 3, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0, 1] #Sample 7
#results = [30, 28, 32, 45, 41, 36, 22, 21, 26, 19, 19, 17, 9, 14, 12, 11, 13, 7, 6, 4, 9, 2, 4, 2, 1, 4, 2, 3, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1] #Sample 6A
#results = [63, 40, 56, 71, 69, 58, 48, 34, 45, 36, 37, 30, 22, 27, 21, 31, 24, 15, 14, 12, 10, 9, 9, 3, 4, 7, 4, 4, 5, 4, 2, 2, 2, 3, 0, 0, 2, 1, 1, 0, 3, 0, 0, 1, 2, 2, 0, 0, 0, 0, 1, 0, 0, 1, 1] #Sample 6b

#Exp 2
#results = [1480, 918, 627, 439, 303, 177, 148, 90, 64, 44, 43, 28, 25, 21, 12, 11, 3, 5, 5, 2] #600
#results = [767, 424, 327, 287, 199, 148, 101, 49, 43, 24, 20, 12, 9, 5, 2, 1, 1, 0, 2, 0, 0, 0, 0, 2] #605
#results = [606, 350, 262, 203, 163, 138, 99, 70, 40, 29, 25, 25, 18, 22, 12, 4, 6, 3, 4, 1, 2, 1, 0, 0, 0, 1, 1, 0, 1, 1, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1] #610

#610 CellProf V2 (Slightly modified to check for dirt)
#results = [564, 364, 263, 178, 186, 133, 99, 67, 45, 31, 30, 27, 20, 16, 15, 6, 8, 2, 4, 4, 2, 1, 1, 3, 0, 0, 1, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
#615
#results = [592, 271, 186, 155, 94, 94, 74, 37, 24, 16, 14, 13, 11, 4, 4, 2, 3, 2, 1, 1, 2, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
#620
#results = [924, 305, 172, 132, 113, 68, 71, 47, 36, 35, 23, 19, 17, 16, 7, 7, 3, 4, 4, 1, 5, 2, 2, 1, 3, 2, 0, 0, 1, 0, 0, 0, 2, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]

#Weights sample
weighted= [x/sum(results) for x in results]
weighted = [weighted[x] for x in range(0,30+1)] #Changed on 01-29-20

monomer = []
effective = []
#Do weight of monomer separately
with open("10qtable") as fp:
    for z in range(1,30+1):  ##Changed 01-29-20
        fp.readline()
    for k in range(350,801):
        line=fp.readline()
        ary = line.split(" ")
        qext = ary[3]
        monomer.append(float(qext)*weighted[0])
closest_ls = []

#Now for each spacing combination
for spacing in range(20,61): #Changed on 1-29-20 20-61
    effective = monomer[:]
    for chain_sz in range(0,30+1): #Changed on 1-29-20
        for wavelength in range(0,451):
            effective[wavelength] += ALLX[wavelength,spacing,chain_sz]*weighted[chain_sz+1]/3
            effective[wavelength] += ALLYZ[wavelength,spacing,chain_sz]*weighted[chain_sz+1]*2/3
    #Find peak absorption (Ignore calculate 2nd, was there for early experimenting)
    wavelength_abs = calculate(effective)
    wavelength_abs2 = calculate_2nd(effective)
    spacing_in_nm = spacing*.05
    closest_ls.append((spacing_in_nm, wavelength_abs,wavelength_abs2))
    if spacing == 22: #Change the number for spacing == # to adjust the output file
        maX = max(effective)
        effective = [eff/maX for eff in effective]
        with open("to_plot", "w") as fp: #This creates a file where you can plot the spectra for a spacing
            for i,num in enumerate(effective):
                print(i+350, num, file=fp)

#This prints basic data for each spacing
for tup in closest_ls:
    print(tup[0], tup[1], tup[2], tup[0]*20)

#This helps give an idea about how much of the sample was used to generate the data
print(sum(results))
results = [results[x] for x in range(1,30+1)] #Changed on 1-30-20
print(sum(results))
