#
# SCRIPT to generate 3D models
#



 # R_Axial_Power_L20.0mm_W6.4mm_P5.08mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '20')
# d
App.ActiveDocument.Spreadsheet.set('B2', '6.4')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '6.4')
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

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_Power_L20.0mm_W6.4mm_P5.08mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_Power_L20.0mm_W6.4mm_P5.08mm_Vertical.FCStd")
print("created R_Axial_Power_L20.0mm_W6.4mm_P5.08mm_Vertical")


 # R_Axial_Power_L20.0mm_W6.4mm_P7.62mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '20')
# d
App.ActiveDocument.Spreadsheet.set('B2', '6.4')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '6.4')
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

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_Power_L20.0mm_W6.4mm_P7.62mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_Power_L20.0mm_W6.4mm_P7.62mm_Vertical.FCStd")
print("created R_Axial_Power_L20.0mm_W6.4mm_P7.62mm_Vertical")


 # R_Axial_Power_L25.0mm_W9.0mm_P7.62mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '25')
# d
App.ActiveDocument.Spreadsheet.set('B2', '9')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '9')
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

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_Power_L25.0mm_W9.0mm_P7.62mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_Power_L25.0mm_W9.0mm_P7.62mm_Vertical.FCStd")
print("created R_Axial_Power_L25.0mm_W9.0mm_P7.62mm_Vertical")


 # R_Axial_Power_L25.0mm_W9.0mm_P10.16mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '25')
# d
App.ActiveDocument.Spreadsheet.set('B2', '9')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '9')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '10.16')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.9')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_Power_L25.0mm_W9.0mm_P10.16mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_Power_L25.0mm_W9.0mm_P10.16mm_Vertical.FCStd")
print("created R_Axial_Power_L25.0mm_W9.0mm_P10.16mm_Vertical")


 # R_Axial_Power_L48.0mm_W12.5mm_P7.62mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '48')
# d
App.ActiveDocument.Spreadsheet.set('B2', '12.5')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '12.5')
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

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_Power_L48.0mm_W12.5mm_P7.62mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_Power_L48.0mm_W12.5mm_P7.62mm_Vertical.FCStd")
print("created R_Axial_Power_L48.0mm_W12.5mm_P7.62mm_Vertical")


 # R_Axial_Power_L48.0mm_W12.5mm_P10.16mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '48')
# d
App.ActiveDocument.Spreadsheet.set('B2', '12.5')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '12.5')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '10.16')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.9')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_Power_L48.0mm_W12.5mm_P10.16mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_Power_L48.0mm_W12.5mm_P10.16mm_Vertical.FCStd")
print("created R_Axial_Power_L48.0mm_W12.5mm_P10.16mm_Vertical")


 # R_Axial_Power_L60.0mm_W14.0mm_P10.16mm_Vertical
import FreeCAD
import os
import os.path

# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.02')
App.ActiveDocument.recompute()
# L
App.ActiveDocument.Spreadsheet.set('B1', '60')
# d
App.ActiveDocument.Spreadsheet.set('B2', '14')
# d2
App.ActiveDocument.Spreadsheet.set('C2', '14')
# RM
App.ActiveDocument.Spreadsheet.set('B3', '10.16')
# d_wire
App.ActiveDocument.Spreadsheet.set('B4', '0.9')
App.ActiveDocument.recompute()
doc = FreeCAD.activeDocument()
__objs__=[]
for obj in doc.Objects:	
    if obj.ViewObject.Visibility:
        __objs__.append(obj)

FreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+"R_Axial_Power_L60.0mm_W14.0mm_P10.16mm_Vertical.wrl")
doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+"R_Axial_Power_L60.0mm_W14.0mm_P10.16mm_Vertical.FCStd")
print("created R_Axial_Power_L60.0mm_W14.0mm_P10.16mm_Vertical")
