# kicad-footprint-generator

This repository contains a script to generate kicad footprints using python

# kicad_mod (first generator script)

**WARNING:** usable, but will be replaced by KicadModTree soon.

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

# KicadModTree (next gen kicad module generator)

**WARNING:** currently under development, but already usable for some footprints

Currently, I'm working at KicadModTree which is using a render tree to construct the model.

Advantage for example is simple usage of transformation operations like rotation and translation on the full (or a part) of the footprint.
Furthermore, we are able to copy complex structures of the footprint and later transform them in any way you want.

### example

```python
from KicadModTree import *

footprint_name = "example_footprint"

# init kicad footprint
kicad_mod = KicadModTree(footprint_name)
kicad_mod.setDescription("A example footprint")
kicad_mod.setTags("example")

# set general values
kicad_mod.append(Text(type='reference', text='REF**', at=[0,-3], layer='F.SilkS'))
kicad_mod.append(Text(type='value', text=footprint_name, at=[1.5,3], layer='F.Fab'))

# create silscreen
kicad_mod.append(RectLine(start=[-2,-2], end=[5,2], layer='F.SilkS', width=0.15))

# create courtyard
kicad_mod.append(RectLine(start=[-2.25,-2.25], end=[5.25,2.25], layer='F.CrtYd', width=0.05))

# create pads
kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[0,0], size=[2,2], drill=1.2, layers=['*.Cu', '*.Mask', 'F.SilkS']))
kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, at=[3,0], size=[2,2], drill=1.2, layers=['*.Cu', '*.Mask', 'F.SilkS']))

# add model
kicad_mod.append(Model(filename="example.3dshapes/example_footprint.wrl"
                      ,at=[0,0,0]
                      ,scale=[1,1,1]
                      ,rotate=[0,0,0]))

# output kicad model
file_handler = KicadFileHandler(kicad_mod)
file_handler.writeFile('example_footprint.kicad_mod')
```

### running unit tests

#### Install dependencies

```sh
pip install unittest2
```

#### run tests

```sh
python KicadModTree/tests/test.py
```
