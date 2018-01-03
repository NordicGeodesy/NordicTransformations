# PROJ.4 parameters for transformations defined by the Nordic Geodetic Commision

The Nordic Geodetic Commision (NKG) defines transformations betweeen the
national realisations of the ETRS89 and the various realisations of the
global reference system ITRS. This repository is a collection of
transformation parameters and gridded deformation models that can be used with
the transformation software PROJ.4.

## Concept

All NKG-transformations are defined such that the common Nordic reference
frame, *NKG_ETRF00*, functions as a transformation hub. That is, all
transformations from e.g. ITRFxx to the national realisations of ERTS89 go through
NKG_ETRF00. We use this to our advantage when setting up the parameter files
for PROJ.4. By leveraging init-files in PROJ.4 a system is set up that delivers
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

## Transforming coordinates

In the following examples of various transformations are given in the form of
PROJ.4 proj-strings. Users unfamiliar with PROJ.4 should consult the
[documentation of the software](http://www.PROJ4.org) for an introduction.

### Global reference frames and the common Nordic frame

Below is a few examples of proj-strings that is used for the
NKG-transformations.

ITRF2014 to NKG_ETRF00 (the common NKG reference frame):
```
+proj=pipeline +step +init=NKG:ITRF2014 +t_obs=2017.25 +inv
```

ITRF2014 to the Danish realisation of ETRS89:
```
+proj=pipeline
  +step +init=NKG:ITRF2014 +t_obs=2017.25 +inv      # ITRF2014@2017.25 -> NKG_ETRF00
  +step +init=NKG:DK                                # NKG_ERTF00 -> ETRS89(DK)
```

### National coordinate reference systems

When coordinates relate to the common Nordic frame it is possible to
transform them to the various national coordinate reference systems.

For instance a transformation between the Danish systems *System34 Jylland* and
*UTM32/ETRS89+DVR90* is performed with:

```
+proj=pipeline
  +step +init=DK:s34j +inv      # System34 Jylland -> ETRS89(DK)
  +step +init=DK:UTM32_DVR90    # ETRS89(DK) -> ETRS89(DK) / UTM Zone 32
```

Below is an example of transforming coordinates from the common Nordic frame
to the Danish compound system of UTM32 and the local vertical reference, DVR90:

```
+proj=pipeline
  +step +init=NKG:DK            # NKG_ETRF00 -> ETRS89(DK)
  +step +init=DK:UTM32_DVR90    # ETRS89(DK) -> ETRS89(DK)/UTM Zone 32
```

Transforming between coordinate reference systems across national borders is
also possible. Here Swedish UTM coordinates are transformed to Norwegian UTM
coordinates, both of course referenced to the local realisations of ETRS89:

```
+proj=pipeline
  +step +init=SE:UTM32 +inv     # ETRS89(SE)/UTM Zon32 -> ETRS89(SE)
  +step +init=NKG:SE +inv       # ETRS89(SE) -> NKG_ETRF00
  +step +init=NKG:NO            # NKG_ETRF00 -> ETRS89(NO)
  +step +init=NO:UTM32          # ETRS89(NO) -> ETRS89(NO)/UTM Zone 32
```

### From global frame to local coordinate reference system

Transforming coordinates from a global frame to a local coordinate
reference system involved two hub datums. First the common Nordic frame
and second one of the national realisations of ERTS89. For instance,
ITRF2014-coordinates from a GNSS-station in Denmark can be transformed to a
local UTM-coordinates with:

```
+proj=pipeline
  +step +init=NKG:ITRF2014 +t_obs=2017.25 +inv  # ITRF2014@2017.25 -> NKG_ETRF00
  +step +init=NKG:DK                            # NKG_ETRF00 -> ETRS89(DK)
  +step +init=DK:UTM32                          # ETRS89(DK) -> ETRS89(DK)/UTM Zone 32
```

## "Installing" the PROJ.4 resource files

PROJ.4 looks for resource files in a few standard locations as well as a user
specified libarary, that can be controlled with the environment variable
``PROJ_LIB``. On Windows systems PROJ.4 only looks for resource files in the
folder specified in ``PROJ_LIB`` and the current directory. On UNIX(-like)
systems PROJ.4 also looks in ``/usr/local/share/proj``. With this in mind,
the NKG PROJ.4 resource files should be copied to one of those locations.

Most Windows-users will probably be using the OSGeo4W distribution of PROJ.4,
which usually has ``PROJ_LIB`` set to ``C:\OSGeo4W64\share\proj``.


## Parameter files

### NKG

Transformation parameters for transformations going to and from the common
Nordic frame NKG_ETRF00. Includes transformations to and from global frames such as
ITRFxx and the national realisations of ETRS89.

At the moment the NKG file is not yet created, but eventually the following
transformation entries can be used in conjunction with the ``NKG`` parameter
file:

| Entry    | Required options | Description                                         |
|----------|------------------|-----------------------------------------------------|
| ITRF2000 | ``+t_obs``       |                                                     |
| ITRF2005 | ``+t_obs``       |                                                     |
| ITRF2008 | ``+t_obs``       |                                                     |
| ITRF2014 | ``+t_obs``       |                                                     |
| DK       |                  | Danish realisation of ETRS89 (ETRF92@1994.704)      |
| EE       |                  | Estonian realisation of ETRS89 (ETRF96@1997.56)     |
| FO       |                  | Faroese realisation of ETRS89 (ETRF2000@2008.75)    |
| FI       |                  | Finish realisation of ETRS89 (ETRF96@1997.0)        |
| LV       |                  | Latvian realisation of ETRS89 (ETRF89@1992.75)      |
| LT       |                  | Lithuanian realisation of ETRS89 (ETRF2000@2003.75) |
| NO       |                  | Norwegian realisation of ETRS89 (ETRF93@1995.0)     |
| SE       |                  | Swedish realisation of ETRS89 (ETRF97@1999.5)       |


### DK

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

| Entry             |  Description
|-------------------|-----------------------------------------------|
| FOTM              | FOTM                                          |
| FOTM_FVR09        | FOTM + FVR09 heights                          |
| UTM29N            | UTM Zone 29N                                  |
| UTM29N_FVR09      | UTM Zone 29N + FVR09 heights                  |
| FD54              | Faroese Datum of 1954                         |
| FVR09             | Faroese Vertical Reference of 2009            |


### GL

Definitions of Greenlandic systems. Uses GR96 as pivot datum.

| Entry             |  Description
|-------------------|-----------------------------------------------|
| ITRF2014          | Transformation from GR96 to ITRF2014          |
| ITRF2008          | Transformation from GR96 to ITRF2008          |

