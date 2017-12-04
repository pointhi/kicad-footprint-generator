#
# SCRIPT to generate 3D models
#



 # R_Axial_DIN0204_L3.6mm_D1.6mm_P1.90mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '3.6')
# d
App.ActiveDocument.Spreadsheet.set('B2', '1.6')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '1.9')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.4')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0204_L3.6mm_D1.6mm_P1.90mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0204_L3.6mm_D1.6mm_P1.90mm_Vertical.FCStd")
print("created R_Axial_DIN0204_L3.6mm_D1.6mm_P1.90mm_Vertical")


 # R_Axial_DIN0204_L3.6mm_D1.6mm_P2.54mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '3.6')
# d
App.ActiveDocument.Spreadsheet.set('B2', '1.6')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '2.54')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.4')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0204_L3.6mm_D1.6mm_P2.54mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0204_L3.6mm_D1.6mm_P2.54mm_Vertical.FCStd")
print("created R_Axial_DIN0204_L3.6mm_D1.6mm_P2.54mm_Vertical")


 # R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '3.6')
# d
App.ActiveDocument.Spreadsheet.set('B2', '1.6')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '5.08')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.4')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Vertical.FCStd")
print("created R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Vertical")


 # R_Axial_DIN0207_L6.3mm_D2.5mm_P2.54mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '6.3')
# d
App.ActiveDocument.Spreadsheet.set('B2', '2.5')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '2.54')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.5')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0207_L6.3mm_D2.5mm_P2.54mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0207_L6.3mm_D2.5mm_P2.54mm_Vertical.FCStd")
print("created R_Axial_DIN0207_L6.3mm_D2.5mm_P2.54mm_Vertical")


 # R_Axial_DIN0207_L6.3mm_D2.5mm_P5.08mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '6.3')
# d
App.ActiveDocument.Spreadsheet.set('B2', '2.5')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '5.08')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.5')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0207_L6.3mm_D2.5mm_P5.08mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0207_L6.3mm_D2.5mm_P5.08mm_Vertical.FCStd")
print("created R_Axial_DIN0207_L6.3mm_D2.5mm_P5.08mm_Vertical")


 # R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '9')
# d
App.ActiveDocument.Spreadsheet.set('B2', '3.2')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '2.54')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.5')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical.FCStd")
print("created R_Axial_DIN0309_L9.0mm_D3.2mm_P2.54mm_Vertical")


 # R_Axial_DIN0309_L9.0mm_D3.2mm_P5.08mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '9')
# d
App.ActiveDocument.Spreadsheet.set('B2', '3.2')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '5.08')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.5')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0309_L9.0mm_D3.2mm_P5.08mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0309_L9.0mm_D3.2mm_P5.08mm_Vertical.FCStd")
print("created R_Axial_DIN0309_L9.0mm_D3.2mm_P5.08mm_Vertical")


 # R_Axial_DIN0411_L9.9mm_D3.6mm_P5.08mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '9.9')
# d
App.ActiveDocument.Spreadsheet.set('B2', '3.6')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '5.08')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.9')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0411_L9.9mm_D3.6mm_P5.08mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0411_L9.9mm_D3.6mm_P5.08mm_Vertical.FCStd")
print("created R_Axial_DIN0411_L9.9mm_D3.6mm_P5.08mm_Vertical")


 # R_Axial_DIN0411_L9.9mm_D3.6mm_P7.62mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '9.9')
# d
App.ActiveDocument.Spreadsheet.set('B2', '3.6')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '7.62')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.9')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0411_L9.9mm_D3.6mm_P7.62mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0411_L9.9mm_D3.6mm_P7.62mm_Vertical.FCStd")
print("created R_Axial_DIN0411_L9.9mm_D3.6mm_P7.62mm_Vertical")


 # R_Axial_DIN0414_L11.9mm_D4.5mm_P5.08mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '11.9')
# d
App.ActiveDocument.Spreadsheet.set('B2', '4.5')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '5.08')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.9')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0414_L11.9mm_D4.5mm_P5.08mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0414_L11.9mm_D4.5mm_P5.08mm_Vertical.FCStd")
print("created R_Axial_DIN0414_L11.9mm_D4.5mm_P5.08mm_Vertical")


 # R_Axial_DIN0414_L11.9mm_D4.5mm_P7.62mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '11.9')
# d
App.ActiveDocument.Spreadsheet.set('B2', '4.5')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '7.62')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.9')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0414_L11.9mm_D4.5mm_P7.62mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0414_L11.9mm_D4.5mm_P7.62mm_Vertical.FCStd")
print("created R_Axial_DIN0414_L11.9mm_D4.5mm_P7.62mm_Vertical")


 # R_Axial_DIN0516_L15.5mm_D5.0mm_P5.08mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '15.5')
# d
App.ActiveDocument.Spreadsheet.set('B2', '5')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '5.08')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.9')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0516_L15.5mm_D5.0mm_P5.08mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0516_L15.5mm_D5.0mm_P5.08mm_Vertical.FCStd")
print("created R_Axial_DIN0516_L15.5mm_D5.0mm_P5.08mm_Vertical")


 # R_Axial_DIN0516_L15.5mm_D5.0mm_P7.62mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '15.5')
# d
App.ActiveDocument.Spreadsheet.set('B2', '5')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '7.62')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.9')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0516_L15.5mm_D5.0mm_P7.62mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0516_L15.5mm_D5.0mm_P7.62mm_Vertical.FCStd")
print("created R_Axial_DIN0516_L15.5mm_D5.0mm_P7.62mm_Vertical")


 # R_Axial_DIN0614_L14.3mm_D5.7mm_P5.08mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '14.3')
# d
App.ActiveDocument.Spreadsheet.set('B2', '5.7')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '5.08')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '1.1')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0614_L14.3mm_D5.7mm_P5.08mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0614_L14.3mm_D5.7mm_P5.08mm_Vertical.FCStd")
print("created R_Axial_DIN0614_L14.3mm_D5.7mm_P5.08mm_Vertical")


 # R_Axial_DIN0614_L14.3mm_D5.7mm_P7.62mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '14.3')
# d
App.ActiveDocument.Spreadsheet.set('B2', '5.7')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '7.62')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '1.1')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0614_L14.3mm_D5.7mm_P7.62mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0614_L14.3mm_D5.7mm_P7.62mm_Vertical.FCStd")
print("created R_Axial_DIN0614_L14.3mm_D5.7mm_P7.62mm_Vertical")


 # R_Axial_DIN0617_L17.0mm_D6.0mm_P5.08mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '17')
# d
App.ActiveDocument.Spreadsheet.set('B2', '6')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '5.08')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.9')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0617_L17.0mm_D6.0mm_P5.08mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0617_L17.0mm_D6.0mm_P5.08mm_Vertical.FCStd")
print("created R_Axial_DIN0617_L17.0mm_D6.0mm_P5.08mm_Vertical")


 # R_Axial_DIN0617_L17.0mm_D6.0mm_P7.62mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '17')
# d
App.ActiveDocument.Spreadsheet.set('B2', '6')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '7.62')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.9')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0617_L17.0mm_D6.0mm_P7.62mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0617_L17.0mm_D6.0mm_P7.62mm_Vertical.FCStd")
print("created R_Axial_DIN0617_L17.0mm_D6.0mm_P7.62mm_Vertical")


 # R_Axial_DIN0918_L18.0mm_D9.0mm_P7.62mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '18')
# d
App.ActiveDocument.Spreadsheet.set('B2', '9')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '7.62')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.9')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0918_L18.0mm_D9.0mm_P7.62mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0918_L18.0mm_D9.0mm_P7.62mm_Vertical.FCStd")
print("created R_Axial_DIN0918_L18.0mm_D9.0mm_P7.62mm_Vertical")


 # R_Axial_DIN0922_L20.0mm_D9.0mm_P7.62mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '20')
# d
App.ActiveDocument.Spreadsheet.set('B2', '9')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '0')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '7.62')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.9')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0922_L20.0mm_D9.0mm_P7.62mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_DIN0922_L20.0mm_D9.0mm_P7.62mm_Vertical.FCStd")
print("created R_Axial_DIN0922_L20.0mm_D9.0mm_P7.62mm_Vertical")
