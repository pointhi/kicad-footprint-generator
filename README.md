This repository contains scripts to generate custom KiCAD footprints using python, and a framework which allows us to
create custom KiCAD footprint. A big bunch of footprints of the KiCad library was developed using this framework.

# KicadModTree

**Licence:** GNU GPLv3+

**Maintainer:** Thomas Pointhuber

[![Build Status](https://travis-ci.org/pointhi/kicad-footprint-generator.svg?branch=master)](https://travis-ci.org/pointhi/kicad-footprint-generator)
[![Code Climate](https://codeclimate.com/github/pointhi/kicad-footprint-generator/badges/gpa.svg)](https://codeclimate.com/github/pointhi/kicad-footprint-generator)
[![Documentation Status](https://readthedocs.org/projects/kicad-footprint-generator/badge/?version=latest)](http://kicad-footprint-generator.readthedocs.io/en/latest/?badge=latest)

**Supports:** Python 2.7 and 3.3+

## About

I started drawing a bunch of similar footprints for KiCAD, like connectors which are mainly one base shape, and different
amount of pins. To be able to update/improve those footprints quickly I decided to write my own footprint generator Framework,
to allow simple creation of easy as well complex shapes.

This is my second approach (the first one is visible below). This solution should be able to be easy to use, to read and
also be easy expand with custom nodes.


## Overview

This framework is mainly based on the idea of scripted CAD systems (for example OpenSCAD). This means, everything is a
node, and can be structured like a tree. In other words, you can group parts of the footprint, and translate them in any
way you want. Also cloning & co. is no problem anymore because of this concept.

To be able to create custom Nodes, I separated the system in two parts. Base nodes, which represents simple structures
and also be used by KiCAD itself, and specialized nodes which alter the behaviour of base nodes (for example positioning),
or represent a specialized usage of base nodes (for example RectLine).

When you serialize your footprint, the serialize command only has to handle base nodes, because all other nodes are based
upon the base nodes. This allows us to write specialized nodes without worrying about the FileHandlers or other core systems.
You simply create your special node, and the framework knows how to handle it seamlessly.

Please look into the **[Documentation](http://kicad-footprint-generator.readthedocs.io/en/latest/)** for further details

```
KicadModTree        - The KicadModTree framework which is used for footprint generation
docs                - Files required to generate a sphinx documentation
kicad_mod           - my old framework, which should be considered as legacy now
scripts             - scripts which are generating footprints based on this library
```

## Development

### Install development Dependencies

```sh
manage.sh update_dev_packages
```

### run tests

```sh
manage.sh tests
```

## Example Script

```python
from KicadModTree import *

footprint_name = "example_footprint"

# init kicad footprint
kicad_mod = Footprint(footprint_name)
kicad_mod.setDescription("A example footprint")
kicad_mod.setTags("example")

# set general values
kicad_mod.append(Text(type='reference', text='REF**', at=[0, -3], layer='F.SilkS'))
kicad_mod.append(Text(type='value', text=footprint_name, at=[1.5, 3], layer='F.Fab'))

# create silscreen
kicad_mod.append(RectLine(start=[-2, -2], end=[5, 2], layer='F.SilkS'))

# create courtyard
kicad_mod.append(RectLine(start=[-2.25, -2.25], end=[5.25, 2.25], layer='F.CrtYd'))

# create pads
kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
                     at=[0, 0], size=[2, 2], drill=1.2, layers=Pad.LAYERS_THT))
kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                     at=[3, 0], size=[2, 2], drill=1.2, layers=Pad.LAYERS_THT))

# add model
kicad_mod.append(Model(filename="example.3dshapes/example_footprint.wrl",
                       at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

# output kicad model
file_handler = KicadFileHandler(kicad_mod)
file_handler.writeFile('example_footprint.kicad_mod')
```

