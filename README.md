# PROJ parameters for transformations defined by the Nordic Geodetic Commision

The Nordic Geodetic Commision (NKG) defines transformations betweeen the
national realisations of the ETRS89 and the various realisations of the
global reference system ITRS. This repository is a collection of
transformation parameters and gridded deformation models that can be used with
the transformation software PROJ.

## License

All files in this repository are licensed under the Creative Commons Attribution 4.0 license,
or as it is commonly referred to, CC-BY 4.0. The license allows redistribution and modification
of the files as long as the original rights holder is credited. In this case the proper rights
holder to credit is either NKG or one of the individual members of NKG, typically the local
National Mapping Authority that has the jurisdiction in the country for which the file is
related to. For the Danish geoid grid the proper attribution is therefore "Agency
for Data Supply and Efficiency". Below the correct authority to attribute for a given files
is specified.

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Concept

All NKG-transformations are defined such that the common Nordic reference
frame, *NKG_ETRF00*, functions as a transformation hub. That is, all
transformations from e.g. ITRFxx to the national realisations of ERTS89 go through
NKG_ETRF00. We use this to our advantage when setting up the parameter files
for PROJ. By leveraging init-files in PROJ a system is set up that delivers
an easy-to-use shorthand notation for day to day use of PROJ.4 that hides most
of the complexity of the transformations for the user.

In addition to using the common Nordic frame as a hub datum for transformations
across national border, we use the national realisations of ERTS89 as hub
datums within those countries. That is, transformations between local coordinate
reference systems always go through the local realisation of ETRS89. This concept
of having a common Nordic hub datum and a set of national hub datums enables us
to perform a wide range of transformations between various local and Nordic
systems, without having to define transformation parameters for all of the
possible paths between systems.

## Usage in PROJ

It is out of the scope of this collection of grids and parameter files
to also describe all the nitty details of the usage of PROJ but a short
introduction is warranted nonetheless. We refer to the [PROJ documentation](http://proj4.org) 
for specific details. It is also worth noting that the project's
[mailing list](http://lists.maptools.org/mailman/listinfo/proj) is a
valuable resource for the PROJ user. Use it when you have questions you
can't find answers to in the documentation.


All of the transformation setups in the sections below can be used
with the `cct` application, e.g.

```
cct +proj=... <file>
```

For coordinates without an epoch the `-t` option of `cct` can be used, e.g.

```
cct -t 2015.830 +proj=... <file>
```

Consult the documentation for [`cct`](http://proj4.org/apps/cct.html) for
further details on the use of `cct`. `cct` is the go-to application for
spatio-temporal (4D) coordinates.

All transformation setups used `cct` with `cct` are describing the
transformation between two systems. In PROJ the `cs2cs` application can be
used to transform between to named coordinate systems without knowing the
specifics of the transformation between those two systems. This functionality
also works with the NKG transformations, at least for the national transformations
described below. An example of such transformation is given below where we
transform Danish UTM32 coordinates to System34 with `cs2cs`:

```
cs2cs +init=DK:UTM32 +to +init=DK:S34S <file>
```

`cs2cs` does only work with 2D and 3D coordinates. So for more advanced 4D
transformations using `cct` is necessary.


## Transforming coordinates

In the following examples of various transformations are given in the form of
PROJ proj-strings. See the above section for a few examples of how the can be
used. Consult the PROJ documentation for further details and examples.


### Global reference frames and the common Nordic frame

Below is a few examples of proj-strings that is used for the
NKG-transformations.

NKG_ETRF00 (the common NKG reference frame) to ITRF2014:
```
+init=NKG:ITRF2014
```

ITRF2014 to the Danish realisation of ETRS89:
```
+proj=pipeline
  +step +init=NKG:ITRF2014 +inv  # ITRF2014 -> NKG_ETRF00 (observation epoch given in coordinate input)
  +step +init=NKG:DK             # NKG_ERTF00 -> ETRS89(DK)
```

### National coordinate reference systems

When coordinates relate to the common Nordic frame it is possible to
transform them to the various national coordinate reference systems.

For instance a transformation between the Danish systems *System34 Jylland* and
*UTM32/ETRS89+DVR90* is performed with:

```
+proj=pipeline
  +step +init=DK:S34J +inv      # System34 Jylland -> ETRS89(DK)
  +step +init=DK:UTM32N_DVR90   # ETRS89(DK) -> ETRS89(DK) / UTM Zone 32
```

Below is an example of transforming coordinates from the common Nordic frame
to the Danish compound system of UTM32 and the local vertical reference, DVR90:

```
+proj=pipeline
  +step +init=NKG:DK            # NKG_ETRF00 -> ETRS89(DK)
  +step +init=DK:UTM32N_DVR90   # ETRS89(DK) -> ETRS89(DK)/UTM Zone 32
```

Transforming between coordinate reference systems across national borders is
also possible. Here Swedish UTM coordinates are transformed to Norwegian UTM
coordinates, both of course referenced to the local realisations of ETRS89:

```
+proj=pipeline
  +step +init=SE:UTM32N +inv    # ETRS89(SE)/UTM Zon32 -> ETRS89(SE)
  +step +init=NKG:SE +inv       # ETRS89(SE) -> NKG_ETRF00
  +step +init=NKG:NO            # NKG_ETRF00 -> ETRS89(NO)
  +step +init=NO:UTM32N         # ETRS89(NO) -> ETRS89(NO)/UTM Zone 32
```

### From global frame to local coordinate reference system

Transforming coordinates from a global frame to a local coordinate
reference system involved two hub datums. First the common Nordic frame
and second one of the national realisations of ERTS89. For instance,
ITRF2014-coordinates from a GNSS-station in Denmark can be transformed to a
local UTM-coordinates with:

```
+proj=pipeline
  +step +init=NKG:ITRF2014 +inv  # ITRF2014 -> NKG_ETRF00
  +step +init=NKG:DK             # NKG_ETRF00 -> ETRS89(DK)
  +step +init=DK:UTM32N          # ETRS89(DK) -> ETRS89(DK)/UTM Zone 32
```

## "Installing" the PROJ resource files

PROJ looks for resource files in a few standard locations as well as a user
specified libarary, that can be controlled with the environment variable
``PROJ_LIB``. On Windows systems PROJ only looks for resource files in the
folder specified in ``PROJ_LIB`` and the current directory. On UNIX(-like)
systems PROJ also looks in ``/usr/local/share/proj``. With this in mind,
the NKG PROJ resource files should be copied to one of those locations.

Most Windows-users will probably be using the OSGeo4W distribution of PROJ,
which usually has ``PROJ_LIB`` set to ``C:\OSGeo4W64\share\proj``.


## Parameter files

### NKG

*Attribution*: [The Nordic Geodetic Commision](http://www.nordicgeodeticcommission.com/).

Transformation parameters for transformations going to and from the common
Nordic frame NKG_ETRF00. Includes transformations to and from global frames such as
ITRFxx and the national realisations of ETRS89.

At the moment the NKG file is not yet created, but eventually the following
transformation entries can be used in conjunction with the ``NKG`` parameter
file:

| Entry    | Description                                         |
|----------|-----------------------------------------------------|
| ITRF2000 |                                                     |
| ITRF2005 |                                                     |
| ITRF2008 |                                                     |
| ITRF2014 |                                                     |
| DK       | Danish realisation of ETRS89 (ETRF92@1994.704)      |
| EE       | Estonian realisation of ETRS89 (ETRF96@1997.56)     |
| FO       | Faroese realisation of ETRS89 (ETRF2000@2008.75)    |
| FI       | Finish realisation of ETRS89 (ETRF96@1997.0)        |
| LV       | Latvian realisation of ETRS89 (ETRF89@1992.75)      |
| LT       | Lithuanian realisation of ETRS89 (ETRF2000@2003.75) |
| NO       | Norwegian realisation of ETRS89 (ETRF93@1995.0)     |
| SE       | Swedish realisation of ETRS89 (ETRF97@1999.5)       |


### DK

*Attribution*: [Agency for Data Supply and Efficiency](http://sdfe.dk).

| Entry             |  Description
|-------------------|-----------------------------------------------|
| S34J              | System34 Jylland                              |
| S34S              | System34 Sjælland                             |
| S45B              | System45 Bornholm                             |
| KP2000J           | KP2000 Jylland                                |
| KP2000J_DVR90     | KP2000 Jylland + DVR90 heights                |
| KP2000S           | KP2000 Sjælland                               |
| KP2000S_DVR90     | KP2000 Sjælland + DVR90 heights               |
| KP2000B           | KP2000 Bornholm                               |
| KP2000B_DVR90     | KP2000 Bornholm + DVR90 heights               |
| DKTM1             | DKTM1                                         |
| DKTM1_DVR90       | DKTM1 + DVR90 heights                         |
| DKTM2             | DKTM2                                         |
| DKTM2_DVR90       | DKTM2 + DVR90 heights                         |
| DKTM3             | DKTM3                                         |
| DKTM3_DVR90       | DKTM3 + DVR90 heights                         |
| DKTM4             | DKTM4                                         |
| DKTM4_DVR90       | DKTM4 + DVR90 heights                         |
| UTM32N            | UTM Zone 32N                                  |
| UTM32N_DVR90      | UTM Zone 32N + DVR90 heights                  |
| UTM33N            | UTM Zone 33N                                  |
| UTM33N_DVR90      | UTM Zone 33N + DVR90 heights                  |
| DVR90             | Danish Vertical Reference of 1990             |

### FO

*Attribution*: [Agency for Data Supply and Efficiency](http://sdfe.dk).

| Entry             |  Description
|-------------------|-----------------------------------------------|
| FOTM              | FOTM                                          |
| FOTM_FVR09        | FOTM + FVR09 heights                          |
| UTM29N            | UTM Zone 29N                                  |
| UTM29N_FVR09      | UTM Zone 29N + FVR09 heights                  |
| FD54              | Faroese Datum of 1954                         |
| FK89              |                                               |
| FVR09             | Faroese Vertical Reference of 2009            |


### GL

*Attribution*: [Agency for Data Supply and Efficiency](http://sdfe.dk).

Definitions of Greenlandic systems. Uses GR96 as pivot datum.

| Entry             |  Description
|-------------------|-----------------------------------------------|
| ITRF2014          | Transformation from GR96 to ITRF2014          |
| ITRF2008          | Transformation from GR96 to ITRF2008          |
| GVR2000           | Greenlandic Vertical Reference of 2000        |
| GVR2016           | Greenlandic Vertical Reference of 2016        |
| UTM18N            | UTM Zone 18N                                  |
| UTM18N_GVR2000    | UTM Zone 18N + GVR2000 heights                |
| UTM18N_GVR2016    | UTM Zone 18N + GVR2016 heights                |
| UTM19N            | UTM Zone 19N                                  |
| UTM19N_GVR2000    | UTM Zone 19N + GVR2000 heights                |
| UTM19N_GVR2016    | UTM Zone 19N + GVR2016 heights                |
| UTM20N            | UTM Zone 20N                                  |
| UTM20N_GVR2000    | UTM Zone 20N + GVR2000 heights                |
| UTM20N_GVR2016    | UTM Zone 20N + GVR2016 heights                |
| UTM21N            | UTM Zone 21N                                  |
| UTM21N_GVR2000    | UTM Zone 21N + GVR2000 heights                |
| UTM21N_GVR2016    | UTM Zone 21N + GVR2016 heights                |
| UTM22N            | UTM Zone 22N                                  |
| UTM22N_GVR2000    | UTM Zone 22N + GVR2000 heights                |
| UTM22N_GVR2016    | UTM Zone 22N + GVR2016 heights                |
| UTM23N            | UTM Zone 23N                                  |
| UTM23N_GVR2000    | UTM Zone 23N + GVR2000 heights                |
| UTM23N_GVR2016    | UTM Zone 23N + GVR2016 heights                |
| UTM24N            | UTM Zone 24N                                  |
| UTM24N_GVR2000    | UTM Zone 24N + GVR2000 heights                |
| UTM24N_GVR2016    | UTM Zone 24N + GVR2016 heights                |
| UTM25N            | UTM Zone 25N                                  |
| UTM25N_GVR2000    | UTM Zone 25N + GVR2000 heights                |
| UTM25N_GVR2016    | UTM Zone 25N + GVR2016 heights                |
| UTM26N            | UTM Zone 26N                                  |
| UTM26N_GVR2000    | UTM Zone 26N + GVR2000 heights                |
| UTM26N_GVR2016    | UTM Zone 26N + GVR2016 heights                |
| UTM27N            | UTM Zone 27N                                  |
| UTM27N_GVR2000    | UTM Zone 27N + GVR2000 heights                |
| UTM27N_GVR2016    | UTM Zone 27N + GVR2016 heights                |
| UTM28N            | UTM Zone 28N                                  |
| UTM28N_GVR2000    | UTM Zone 28N + GVR2000 heights                |
| UTM28N_GVR2016    | UTM Zone 28N + GVR2016 heights                |
| UTM28N            | UTM Zone 29N                                  |
| UTM29N_GVR2000    | UTM Zone 29N + GVR2000 heights                |
| UTM29N_GVR2016    | UTM Zone 29N + GVR2016 heights                |

## Grids

Descriptions of the grids available in the NordicTransformations repository.

### nkgrf03vel_realigned_xy.ct2

*Attribution*: [The Nordic Geodetic Commision](http://www.nordicgeodeticcommission.com/).

The horizontal component of the readjusted NKG velocity model from 2003. The readjustment
is performed as described in [Häkli et al. (2016)](https://www.researchgate.net/profile/Pasi_Haekli/publication/298807458_The_NKG2008_GPS_campaign_-_final_transformation_results_and_a_new_common_Nordic_reference_frame/links/5728674d08aee491cb4262e8/The-NKG2008-GPS-campaign-final-transformation-results-and-a-new-common-Nordic-reference-frame.pdf)
The velocity model is used in transformations going from global reference frames to
the individual national realizations of ETRS89.

### nkgrf03vel_realigned_z.gtx

*Attribution*: [The Nordic Geodetic Commision](http://www.nordicgeodeticcommission.com/).

The vertical component of the readjusted NKG velocity model from 2003. The readjustment
is performed as described in [Häkli et al. (2016)](https://www.researchgate.net/profile/Pasi_Haekli/publication/298807458_The_NKG2008_GPS_campaign_-_final_transformation_results_and_a_new_common_Nordic_reference_frame/links/5728674d08aee491cb4262e8/The-NKG2008-GPS-campaign-final-transformation-results-and-a-new-common-Nordic-reference-frame.pdf)
The velocity model is used in transformations going from global reference frames to
the individual national realizations of ETRS89.

### dvr90.gtx

*Attribution*: [Agency for Data Supply and Efficiency](http://sdfe.dk).

Geoid model for the Danish height reference DVR90. The grid implements the
transformation between GRS80 ellipsoid heights and heights in the DVR90 system.
Grid coordinates are referenced to ETRS89.

### fvr09.gtx

*Attribution*: [Agency for Data Supply and Efficiency](http://sdfe.dk).

Geoid model for the Faroese height reference FVR09. The grid implements the
transformation between GRS80 ellipsoid heights and heights in the FVR09 system.
Grid coordinates are referenced to ETRS89.

### gvr2016.gtx

*Attribution*: [Agency for Data Supply and Efficiency](http://sdfe.dk).

Geoid model for the Greenlandic height reference GVR2016. The grid implements the
transformation between GRS80 ellipsoid heights and heights in the GVR2016 system.
Grid coordinates are referenced to GR96.
