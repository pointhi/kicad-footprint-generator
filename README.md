
This repository contains scripts to generate custom KiCAD footprints using python, and a framework which allows us to create custom KiCAD footprint

# KicadModTree

**Licence:** GNU GPLv3+

**Maintainer:** Thomas Pointhuber

[![Build Status](https://travis-ci.org/pointhi/kicad-footprint-generator.svg?branch=master)](https://travis-ci.org/pointhi/kicad-footprint-generator)
[![Code Climate](https://codeclimate.com/github/pointhi/kicad-footprint-generator/badges/gpa.svg)](https://codeclimate.com/github/pointhi/kicad-footprint-generator)

**WARNING:** currently under development, but already usable for some footprints. But note that API changes are possible due to refactoring.


## About

I started drawing a bunch of similar footprints for KiCAD, like connectors which are mainly one base shape, and different amount of pins.
To be able to update/improve those footprints quickly I decided to write my own footprint generator Framework, to allow simple creation of easy as well complex shapes.

This is my second approach (the first one is visible below). This solution should be able to be easy to use, to read and also be easy expand with custom nodes.


## Overview

This framework is mainly based on the idea of scripted CAD systems (for example OpenSCAD). This means, everything is a node, and can be structured like a tree.
In other words, you can group parts of the footprint, and translate them in any way you want. Also cloning & co. is no Problem anymore because of this concept.

To be able to create custom Nodes, I separated the system in two parts. Base nodes, which represents simple structures and also be used by KiCAD itself,
and specialized nodes which alter the behaviour of base nodes (for example positioning), or represent a specialized usage of base nodes (for example RectLine).

When you serialize your footprint, the serialize command only has to handle base nodes, because all other nodes are based upon the base nodes.
This allows us to write specialized nodes without worrying about the FileHandlers or other core systems.
You simply create you special node, and the framework knows how to handle it seamlessly.


### Base Nodes

| Function          | Description                                      |
| ----------------- | ------------------------------------------------ |
| **Arc**           | Draws an arc                                     |
| **Circle**        | Draws a circle                                   |
| **Line**          | Draws a line                                     |
| **Model**         | A 3D model representing the footprint            |
| **Pad**           | Add a pad to the footprint                       |
| **Text**          | Draws text                                       |


### Currently available special Nodes

This nodes alter base nodes, or are based on base Nodes to create special functionality

| Function          | Description                                      |
| ----------------- | ------------------------------------------------ |
| **Rotation**      | Rotate all child nodes                           |
| **Translation**   | Translate all child nodes                        |
| **PolygoneLine**  | Draws a polygone line                            |
| **RectLine**      | Draws a rect                                     |
| **RectFill**      | Draws the filling of a rect (not the outline)    |
| **FilledRect**    | Draws a filled rect                              |


### Development

#### Install development Dependencies

```sh
manage.sh update_dev_packages
```

#### run tests

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
kicad_mod.append(RectLine(start=[-2, -2], end=[5, 2], layer='F.SilkS))

# create courtyard
kicad_mod.append(RectLine(start=[-2.25, -2.25], end=[5.25, 2.25], layer='F.CrtYd'))

# create pads
kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
                     at=[0, 0], size=[2, 2], drill=1.2, layers=['*.Cu', '*.Mask', 'F.SilkS']))
kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                     at=[3, 0], size=[2, 2], drill=1.2, layers=['*.Cu', '*.Mask', 'F.SilkS']))

# add model
kicad_mod.append(Model(filename="example.3dshapes/example_footprint.wrl",
                       at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

# output kicad model
file_handler = KicadFileHandler(kicad_mod)
file_handler.writeFile('example_footprint.kicad_mod')
```


--
# kicad_mod (old generator script)

**WARNING:** usable, but will be replaced by KicadModTree. Only for documentation reason


### example

```python
from kicad_mod import KicadMod, createNumberedPadsTHT

footprint_name = "example_footprint"

# init kicad footprint
kicad_mod = KicadMod(footprint_name)
kicad_mod.setDescription("A example footprint")
kicad_mod.setTags('example')

# set general values
kicad_mod.addReference('REF**', {'x':0, 'y':-3}, 'F.SilkS')
kicad_mod.addValue(footprint_name, {'x':1.5, 'y':3}, 'F.Fab')

# create silscreen
kicad_mod.addRectLine({'x':-2, 'y':-2}, {'x':5, 'y':2}, 'F.SilkS', 0.15)

# create courtyard
kicad_mod.addRectLine({'x':-2.25, 'y':-2.25}, {'x':5.25, 'y':2.25}, 'F.CrtYd', 0.05)

# create pads
createNumberedPadsTHT(kicad_mod, 2, 3, 1.2, {'x':2, 'y':2.6})

# output kicad model
print(kicad_mod)
```
