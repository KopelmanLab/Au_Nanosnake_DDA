import numpy as np



Ls = 10 #sphere radius for calculations
#spheres = 9 #number of spheres

for num in range(31,35+1):
    spheres = num
    for spacing in range(21,25):
        #offX = np.array([0,21,42,63,84,105,126,147,168])#x
        #offY = np.array([0,0,0,0,0,0,0,0,0]) #y
        #offZ = np.array([0,0,0,0,0,0,0,0,0]) #z
        offX = np.array([x*spacing for x in range(0, num)])
        offY = np.array([0 for x in range(0, num)])
        offZ = np.array([0 for x in range(0, num)])

        ## calculation parameters for output file documentation
        X = Ls #sphere radius
        Y = Ls
        Z = Ls
        Xd = X*2 #diameter
        Yd = Y*2
        Zd = Z*2

        coords = np.array([], ndmin=2)
        for off in range(0, spheres):
            xco = np.arange(-X+offX[off], X+1+offX[off]) #add 1 to account for float
            yco = np.arange(-Y+offY[off], Y+1+offY[off])
            zco = np.arange(-Z+offZ[off], Z+1+offZ[off])

            # creates a list of all coordinates in the x,y,z cube that the sphere can exist in
            coord_list = np.array(np.meshgrid(xco,yco,zco)).T.reshape(-1,3)
            # conditional list to check which locations have distance from origin less than or equal to Ls
            conds = (np.square(coord_list[:,0] - offX[off]) + np.square(coord_list[:,1] - offY[off]) + np.square(coord_list[:,2] - offZ[off])) ** 0.5 <= Ls
            # extracts valid sphere coordinates
            sphere_coords = coord_list[conds]
            # appends to list of all sphere coords
            coords = np.append(coords, sphere_coords)

        coords = coords.reshape(-1, 3)


        # In[12]:


        num_coords = coords.size / 3

        NX = offX.max() - offX.min() + 2 * Ls
        NY = offY.max() - offY.min() + 2 * Ls
        NZ = offZ.max() - offY.min() + 2 * Ls

        f_name = "shape_" + str(num) + "x_" +  str(spacing-20) + "nm_" + "1dpnm.dat"
        with open(f_name, 'w') as fp:
            fp.write(' >PIPOBJ: point-in-polyhedron; NX,NY,NZ= %d %d %d ' % (NX, NY, NZ))
            fp.write('\r\n %8.0f %8.0f = NAT, NIN' % (num_coords, 1))
            fp.write('\r\n 1.000000 0.000000 0.000000 = A_1 vector\r\n 0.000000 1.000000 0.000000 = A_2 vector')
            fp.write('\r\n 1.000000 1.000000 1.000000 = lattice spacings(d_x,d_y,d_z)/d')
            fp.write('\r\n 0.0 0.0 0.0 = lattice offset x0(1-3) =(x_TF,y_TF,z_TF)/d for dipole 0 0 0')
            fp.write('\r\n       JA    IX    IY    IZ  ICOMP(x,y,z)')
            for idx, coord in enumerate(coords):
                fp.write('\r\n    {:>4}   {:>4}  {:>4}  {:>4}     {} {} {}'.format(idx + 1, int(coord[0]), int(coord[1]), int(coord[2]), 1, 1, 1))
