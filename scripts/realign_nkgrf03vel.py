# -*- coding: utf-8 -*-
'''
Realign the 2003 NKG velocity model to the ETRF2000 frame as described in
"The NKG2008 GPS campaign - final transformation results and a new common
Nordic reference frame" by Häkli et al.

Outputs two grids, one for the horizontal components and one for the
vertical component. The horizontal grid is in CTable2 format and the
vertical grid is in GTX format. In both grids the units of the grid values
are mm/year
'''
import math
import sys

import numpy as np
from astropy.coordinates import EarthLocation
from kmsgrid import KMSGrid # version 1.1.0

from math import sin
from math import cos

def mas2rad(x):
    ''' Miliarcseconds to radians. '''
    return x*math.pi/(1000*3600*180)

def realign(V, C):
    '''
    Re-aligning a single velocity vector by a Helmert shift.

    Input:

        V: Vector of velocities in mm/yr
        C: Cartesian coordinates

    Returns:

        Vector of realigned velocities in m/yr
    '''

    (Vx, Vy, Vz) = V
    (X, Y, Z) = C

    # input velocities are in mm/year, we want m/year for the re-alignment
    Vx /= 1000
    Vy /= 1000
    Vz /= 1000

    Vx += Tx + D*X + (      - Rz*Y + Ry*Z)
    Vy += Ty + D*Y + ( Rz*X        - Rx*Z)
    Vz += Tz + D*Z + (-Ry*X + Rx*Y       )

    # the values in the grid should be stored as mm/year
    Vx *= 1000
    Vy *= 1000
    Vz *= 1000

    return (Vx, Vy, Vz)

def neu2xyz(dN, dE, dU, lat, lon):
    '''
    Convert from NEU-space to cartesian XYZ-space.

    NEU -> XYZ formula described in

    Nørbech, T., et al, 2003(?), "Transformation from a Common Nordic Reference
    Frame to ETRS89 in Denmark, Finland, Norway, and Sweden – status report"
    '''
    dX = -sin(lat)*cos(lon)*dN - sin(lon)*dE + cos(lat)*cos(lon)*dU
    dY = -sin(lat)*sin(lon)*dN + cos(lon)*dE + cos(lat)*sin(lon)*dU
    dZ = cos(lat)*dN + sin(lat)*dU

    return (dX, dY, dZ)

def xyz2neu(dX, dY, dZ, lat, lon):
    '''
    Convert from cartesian XYZ-space to NEU-space.

    Solves the inverse set of equations described in (Nørbech, 2003(?))
    numerically.
    '''
    # b = Ax, solve for x
    b = np.array([dX, dY, dZ])
    A = np.array([[-sin(lat)*cos(lon), -sin(lon), cos(lat)*cos(lon)],
                  [-sin(lat)*sin(lon),  cos(lon), cos(lat)*sin(lon)],
                  [ cos(lat),                  0, sin(lat)]])

    x = np.linalg.solve(A, b)

    return (x[0], x[1], x[2])

# realignment parameters
Tx = 0.00211  # m/yr
Ty = 0.00056  # m/yr
Tz = 0.00127  # m/yr
D  = -0.465*1e-9   # ppb/yr
Rx = mas2rad(0.016120) # rad/yr
Ry = mas2rad(-0.03066) # rad/yr
Rz = mas2rad(0.01435) # rad/yr

# read model and make working copies
grid = KMSGrid(r'data\nkgrf03vel.01')

# Data is aligned as North, East, Up
VN = np.zeros(shape=grid.data[0].shape, dtype='f4')
VE = np.zeros(shape=grid.data[1].shape, dtype='f4')
VU = np.zeros(shape=grid.data[2].shape, dtype='f4')

minlat = 9999
minlon = 9999
maxlat = -9999
maxlon = -9999

# realign model
#for i, lat in enumerate(np.arange(grid.latmin, grid.latmax+grid.dlat, grid.dlat)):
for i, lat in enumerate(np.arange(grid.latmax+grid.dlat, grid.latmin, -grid.dlat)):
    for j, lon in enumerate(np.arange(grid.lonmin, grid.lonmax+grid.dlat, grid.dlon)):

        # geodetic -> cartesian conversion
        P = EarthLocation(lat=lat, lon=lon, height=0, ellipsoid='GRS80')
        C = (P.x.value, P.y.value, P.z.value)

        # Data is aligned as North, East, Up
        (dN, dE, dU) = (grid.data[0][i,j], grid.data[1][i,j], grid.data[2][i,j])

        # dNEU -> dXYZ conversion
        lat_rad = lat * math.pi / 180
        lon_rad = lon * math.pi / 180

        # convert from NEU-space to XYZ-space
        (dX, dY, dZ) = neu2xyz(dN, dE, dU, lat_rad, lon_rad)

        # re-align velocities in 2003 model
        V = (dX, dY, dZ)
        (VX, VY, VZ) = realign(V, C)

        # convert back to NEU-space
        (VN[i,j], VE[i,j], VU[i,j]) = xyz2neu(VX, VY, VZ, lat_rad, lon_rad)

# override original griddata and take advantage of existing KMSGrid metadata
# when saving the grids in PROJ.4-readable formats
grid.data[0] = VN
grid.data[1] = VE
grid.data[2] = VU

print(np.min(VN[:]), np.max(VN[:]), np.mean(VN[:]))
print(np.min(VE[:]), np.max(VE[:]), np.mean(VE[:]))
print(np.min(VU[:]), np.max(VU[:]), np.mean(VU[:]))

# CTable2 files are physicalled ordered E first,N second, but the GDAL CTable2
# driver, for consistency with NTv2, exposes the bands in the N,E
# order. See https://github.com/OSGeo/gdal/blob/7673db05ef592e706662c085e736f5ca3bf7da67/gdal/frmts/raw/ctable2dataset.cpp#L224
grid.export(r'../resources/nkgrf03vel_realigned_xy.ct2', (1, 2), 'CTable2')
grid.export(r'../resources/nkgrf03vel_realigned_z.gtx', (3,), 'GTX')
