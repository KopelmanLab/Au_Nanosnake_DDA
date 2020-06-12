#Graph Fitter

#Imports
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

#Pt 1
#Interpolate the qTables so that we can use them to solve for the spacing later

#wavelengths = [x for x in range(350,951)] #This program only uses wavelenght in range(350,800)
final = np.empty((20, 41)) #Changed on 1-29-20 from 0 to 20
ALLX = np.empty((451, 42, 0)) #Changed on 1-29-20 from 62 to 42
ALLYZ = np.empty((451, 42, 0)) #Changed on 1-29-20 from 62 to 42

for length in range(2,30+1): #The range indicates the range of chain lengths
    finalx = np.empty((20, 41)) #Changed on 1-29-20 from 0 to 20
    finalyz = np.empty((20, 41)) #Changed on 1-29-20 from 0 to 20
    list_of_qextx = np.empty((0,451))
    list_of_qextyz = np.empty((0,451))
    for spacing in range(1,3+1): #Iterates through the 4 spacings at 1dpnm (0nm, 1nm, 2nm, 3nm) #Changed to iterate only through (1, 2, and 3 nm)
        x_name = "x/" + str(length) + "/" + str(length) + str(spacing) + "qtable"
        yz_name = "yz/" + str(length) + "/" + str(length) + str(spacing) +"qtable"
        #We read the files to get a list of the qExt for each chain length/spacing
        with open(x_name) as fp:
            #The first 14 lines of the qTable do not contain spectrum data
            for blank in range(1,30+1):
                fp.readline()
            qexts = np.empty((1,0))
            for k in range(350,801):
                line = fp.readline()
                ary = line.split(" ")
                qext = np.array([[ary[3]]])
                qexts = np.append(qexts, qext, axis=1)
            list_of_qextx = np.vstack((list_of_qextx, qexts))
        with open(yz_name) as fp:
            #The first 14 lines of the qTable do not contain spectrum data
            for blank in range(1,30+1):
                fp.readline()
            qexts = np.empty((1,0))
            for k in range(350,801):
                line = fp.readline()
                ary = line.split(" ")
                qext = np.array([[ary[3]]])
                qexts = np.append(qexts, qext, axis=1)
            list_of_qextyz = np.append(list_of_qextyz, qexts,axis=0)
    #Only 450 wavelengths since range is [350,801)
    for wave in range(0,451):
        x1 = [1,2,3] ##Changed 1-29-20 from [0,1,2,3]
        y1 = list_of_qextx[:,wave]
        y1 = y1.tolist()
        #We are gonna try to interpolate, but this may fail if we are missing values
        #We miss values because sometimes DDSCAT isnt able to calculate them
       # try:
        f = interp1d(x1,y1, kind='quadratic') #Changed on 1-29-20 from cubic to qudratic
        #If we are missing values, we interpolate using a quadratic instead of a cubic
        #We may also need to extrapolate because of this
        #except ValueError:
         #   print(x, y2, wave+350)
          #  while ("" in y1):
           #     ind = y1.index("")
            #    y1.pop(ind)
             #   x1.pop(ind)
            #f = interp1d(x1,y1, kind='qudratic', fill_value="extrapolate")
        xnew = np.linspace(1, 3, num=41, endpoint=True) #Changed on 1-29-20 from 0,3 to 1,3; num from 61 to 41
        fnew = f(xnew)
        finalx = np.append(finalx, [fnew], axis=0)
    allx = np.column_stack((wavelengths,finalx))
    #Same as above but for the yz orientation
    #Only 450 wavelengths since range is [350,801)
    for wave in range(0,451):
        x2 = [1,2,3] ##Changed 1-29-20 from [0,1,2,3]
        y2 = list_of_qextyz[:,wave]
        y2 = y2.tolist()
        #We are gonna try to interpolate, but this may fail if we are missing values
        #We miss values because sometimes DDSCAT isnt able to calculate them
        #try:
        f = interp1d(x2,y2, kind='qudratic') #Changed on 1-29-20 from cubic to quadratic
        #If we are missing values, we interpolate using a quadratic instead of a cubic
        #We may also need to extrapolate because of this
        #except ValueError:
         #   print(x, y2, wave+350)
          #  while ("" in y2):
           #     ind = y2.index("")
            #    y2.pop(ind)
             #   x2.pop(ind)
            #f = interp1d(x2,y2, kind='qudratic')
        xnew = np.linspace(1, 3, num=41, endpoint=True) #Changed on 1-29-20 from 0,3 to 1,3; num from 61 to 41
        fnew = f(xnew)
        finalyz = np.append(finalyz, [fnew], axis=0)
    allyz = np.column_stack((wavelengths,finalyz))
    #Now we save the interpolated texts as csv files so we can check them out if we want (get plots)
    gaps = list(map(str,xnew))
    gaps.insert(0,'')
    head = ','.join(gaps)
    namex = str(x) + "x_interp.csv"
    nameyz = str(x) + "yz_interp.csv"
    np.savetxt(namex, allx,header=head,comments='',delimiter=',')
    np.savetxt(nameyz, allyz, header=head, comments='', delimiter=',')
    ALLX = np.append(ALLX, np.atleast_3d(allx), axis=2)
    ALLYZ = np.append(ALLYZ, np.atleast_3d(allyz), axis=2)

