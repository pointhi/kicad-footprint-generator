#http://katalog.we-online.com/en/pbs/WE-MAPI]

#sizes,shapes,etc]
#name, L, W, pad-w, pad-gap, pad-h
inductors = [
[1610,1.6,1.6,1.8,0.4,1.8],
[2010,2.0,1.6,2.3,0.6,1.9],
[2506,2.5,2.0,2.8,1.1,2.3],
[2508,2.5,2.0,2.8,1.1,2.3],
[2510,2.5,2.0,2.8,1.1,2.3],
[2512,2.5,2.0,2.8,1.1,2.3],
[3010,3.0,3.0,3.4,0.8,3.4],
[3012,3.0,3.0,3.4,0.8,3.4],
[3015,3.0,3.0,3.4,0.8,3.4],
[3020,3.0,3.0,3.5,0.8,3.4],
[4020,4.0,4.0,3.35,1.39,3.7],
]

import sys
import os

output_dir = os.getcwd()

#if specified as an argument, extract the target directory for output footprints
if len(sys.argv) > 1:
    out_dir = sys.argv[1]
    
    if os.path.isabs(out_dir) and os.path.isdir(out_dir):
        output_dir = out_dir
    else:
        out_dir = os.path.join(os.getcwd(),out_dir)
        if os.path.isdir(out_dir):
            output_dir = out_dir

if output_dir and not output_dir.endswith(os.sep):
    output_dir += os.sep
        
#import KicadModTree files
sys.path.append("..\\..")
from KicadModTree import *
from KicadModTree.nodes.specialized.PadArray import PadArray

prefix = "Inductor_"
part = "Wurth_MAPI-{pn}"
dims = "{l:0.1f}mmx{w:0.1f}mm"

desc = "Inductor, Wurth Elektronik, {pn}"
tags = "inductor wurth smd"

for inductor in inductors:
    name,l,w,x,g,y = inductor
    
    fp_name = prefix + part.format(pn=str(name))
    
    fp = Footprint(fp_name)
    
    description = desc.format(pn = part.format(pn=str(name))) + ", " + dims.format(l=l,w=w)
    
    fp.setTags(tags)
    fp.setAttribute("smd")
    fp.setDescription(description)
    
    # set general values
    fp.append(Text(type='reference', text='REF**', at=[0,-y/2 - 1], layer='F.SilkS'))
    fp.append(Text(type='value', text=fp_name, at=[0,y/2 + 1.5], layer='F.Fab'))
    
    #calculate pad center
    #pad-width pw
    pw = (x-g) / 2
    c = g/2 + pw/2
    
    #add the component outline
    fp.append(RectLine(start=[-l/2,-w/2],end=[l/2,w/2],layer='F.Fab',width=0.15))
    
    layers = ["F.Cu","F.Paste","F.Mask"]
    
    #add pads
    fp.append(Pad(number=1,at=[-c,0],layers=layers,shape=Pad.SHAPE_RECT,type=Pad.TYPE_SMT,size=[pw,y]))
    fp.append(Pad(number=2,at=[c,0],layers=layers,shape=Pad.SHAPE_RECT,type=Pad.TYPE_SMT,size=[pw,y]))
    
    #add inductor courtyard
    cx = c + pw/2
    cy = y / 2
    
    fp.append(RectLine(start=[-cx,-cy],end=[cx,cy],offset=0.35,width=0.05,grid=0.05,layer="F.CrtYd"))
    
    #add lines
    fp.append(Line(start=[-g/2+0.2,-w/2-0.1],end=[g/2-0.2,-w/2-0.1]))
    fp.append(Line(start=[-g/2+0.2,w/2+0.1],end=[g/2-0.2,w/2+0.1]))
    
    #Add a model
    fp.append(Model(filename="Inductors.3dshapes/" + fp_name + ".wrl"))
    
    #filename
    filename = output_dir + fp_name + ".kicad_mod"
    
    file_handler = KicadFileHandler(fp)
    file_handler.writeFile(filename)
    