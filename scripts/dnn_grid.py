import numpy as np

from osgeo import gdal
from osgeo import osr

import TrLib

# Adjust accordingly...
TrLib.InitLibrary(r"C:\Data\Geoids2013","trlib.dll",r"C:\dev\TRLIB_v110\win64")
TrLib.SetMaxMessages(0)

LONMIN = 7.9
LONMAX = 15.3
LATMIN = 54.5
LATMAX = 57.8
DLON = 0.0020
DLAT = 0.0020

NODATA = -88.888  # GTX format NODATA value

def main():
    tr = TrLib.CoordinateTransformation('geoEetrs89', 'geoHetrs89_h_dnn')

    lons = np.arange(LONMIN, LONMAX+DLON, DLON)
    lats = np.arange(LATMIN, LATMAX+DLAT, DLAT)

    cols = len(lons)
    rows = len(lats)

    grid = np.ndarray((rows, cols))

    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            I = rows-i-1
            try:
                grid[I,j] = -tr.Transform(lon, lat, z=0.0)[2]
                if grid[I,j] > 1000.0:
                    grid[I,j] = NODATA
            except:
                grid[I,j] = NODATA

    ds = gdal.GetDriverByName('GTX').Create('dnn.gtx', cols, rows, 1, gdal.GDT_Float32)
    ds.SetGeoTransform((LONMIN, DLON, 0, LATMAX, 0, -DLAT))
    band = ds.GetRasterBand(1)
    band.SetNoDataValue(NODATA)
    band.WriteArray(grid)

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4258)
    ds.SetProjection(srs.ExportToWkt())
    band.FlushCache()

if __name__ == '__main__':
    main()
