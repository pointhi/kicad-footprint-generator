#!/usr/bin/env python

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
from KicadModTree.klc import *

from math import floor,ceil

# http://www.jst-mfg.com/product/pdf/eng/eZE.pdf

#ZE connector, top-entry SMD

pitch = 1.5

for pincount in range(2,17):

    jst = "SM{pincount:02}B-ZESS-TB".format(pincount=pincount)

    # Through-hole type shrouded header, side entry type
    fp_name = "JST_ZE_" + jst + "_{pincount:02}x{pitch:02}mm_Angled".format(pincount=pincount, pitch=pitch)
    
    footprint = Footprint(fp_name)
    
    print(fp_name)
    
    desc = "JST ZE series connector, " + jst + ", 1.50mm pitch, side entry surface mount"
    footprint.setDescription(desc)
    footprint.setTags('connector jst ze top horizontal angled smt surface mount')
    footprint.setAttribute("smd")
    
    # set general values
    footprint.append(Text(type='reference', text='REF**', at=[0,-5], layer='F.SilkS'))
    footprint.append(Text(type='value', text=fp_name, at=[0,7], layer='F.Fab'))

    #dimensions
    A = (pincount - 1) * 1.5
    B = A + 6
    W = 7.5 # width of the connector body
    
    #position of pads (from datasheet)
    ym = 1.45 + 3.8 / 2
    yp = 6.60 + 2.9 / 2
    ymid = (ym + yp) / 2
    
    # pad positions (offset)
    m_y = ymid - ym
    pad_y = ymid - yp

    # housing positions
    y2 = m_y + 3.8/2 + 1.45
    y1 = y2 - W
    
    # pad size
    pad_w = 0.8
    pad_h = 3.0
    
    # Create the pads
    footprint.append(PadArray(pincount=pincount,
                  x_spacing=pitch,
                  type=Pad.TYPE_SMT,
                  shape=Pad.SHAPE_RECT,
                  layers=Pad.LAYERS_SMT,
                  size=[pad_w, pad_h],
                  center=[0,pad_y]
                  ))
            
    # mechanical pad size
    m_w = 1.8
    m_h = 3.8
    m_x = A/2 + 1.7 + m_w/2
    
    footprint.append(Pad(at=[m_x, m_y], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT, size=[m_w, m_h]))
    
    footprint.append(Pad(at=[-m_x, m_y], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT, size=[m_w, m_h]))
    
    # position of housing
    
    # add connector outline to fab layer
    footprint.append(RectLine(start=[-B/2, y1], end=[B/2, y2], layer='F.Fab', width=KLC_FAB_WIDTH))
    
    # silkscreen offset
    o = 0.2
    
    # add silkscreen around bottom of housing
    bottom = [
    {'x': -B/2-o,'y': m_y + m_h/2 + 0.3},
    {'x': -B/2-o,'y': y2 + o},
    {'x': B/2+o,'y': y2 + o},
    {'x': B/2+o,'y': m_y + m_h/2 + 0.3},
    ]
    
    footprint.append(PolygoneLine(polygone=bottom, layer='F.SilkS', width=KLC_SILK_WIDTH))
    
    # add silkscreen around top of housing
    top = [
    {'x': -B/2-o,'y': m_y-m_h/2-0.3},
    {'x': -B/2-o,'y': y1-o},
    {'x': -A/2-pad_w/2-0.3,'y': y1-o},
    ]
    
    footprint.append(PolygoneLine(polygone=top, layer='F.SilkS', width=KLC_SILK_WIDTH))
    footprint.append(PolygoneLine(polygone=top, layer='F.SilkS', width=KLC_SILK_WIDTH, x_mirror=0))
    
    # add pin-1 indication on silk
    footprint.append(Line(start=[-A/2-pad_w/2-0.3, y1-o], end=[-A/2-pad_w/2-0.3, pad_y-pad_h/2]))
    
    # add pin-1 marking on F.Fab
    
    xm = -A/2
    ym = pad_y + pad_h/2 + 0.25
    mm = 0.3
    
    p1 = [
    {'x': xm, 'y': ym},
    {'x': xm-mm, 'y': ym+2*mm},
    {'x': xm+mm, 'y': ym+2*mm},
    {'x': xm, 'y': ym},
    ]
    
    footprint.append(PolygoneLine(polygone=p1, layer='F.Fab', width=KLC_FAB_WIDTH))
    
    # add courtyard
    off = 0.5 # offset
    crtyd = [
    {'x': -m_x - m_w/2 - off ,'y': y1 - off},
    {'x': -m_x - m_w/2 - off ,'y': y2 + off},
    {'x': m_x + m_w/2 + off ,'y': y2 + off},
    {'x': m_x + m_w/2 + off ,'y': y1 - off},
    {'x': A/2 + pad_w/2 + off ,'y': y1 - off},
    {'x': A/2 + pad_w/2 + off ,'y': pad_y - pad_h/2 - off},
    {'x': -A/2 - pad_w/2 - off ,'y': pad_y - pad_h/2 - off},
    {'x': -A/2 - pad_w/2 - off ,'y': y1 - off},
    {'x': -m_x - m_w/2 - off ,'y': y1 - off},
    ]
    footprint.append(PolygoneLine(polygone=crtyd,layer='F.CrtYd',width=KLC_CRTYD_WIDTH))
    
    """
    # Create mechanical pads    
                  
    
    #y-coords calculated based on drawing in datasheet
    #middle point of pads
    py = -6.7
    #middle point of mechanical pads
    my = -1.65
    
    #size of mechanical pads
    mw = 2.0
    mh = 3.3
    #x-pos of mechanical pads
    mx = A/2 + 1.7 + 1.8/2
    
    #middle point of connector
    ymid = (py + my) / 2
    
    kicad_mod.setCenterPos({'x': 0,'y': ymid})
    
    
    #outline
    x1 = -B / 2
    x2 =  B / 2
    
    y2 = -0.4
    y1 = y2 - 5.8
    
    #add outline to F.Fab
    kicad_mod.addRectLine(
        {'x': x1, 'y': y1},
        {'x': x2, 'y': y2},
        'F.Fab', 0.15
        )

    #expand the outline a little bit
    out = 0.2
    x1 -= out
    x2 += out
    y1 -= out
    y2 += out

    #pad size
    pw = 0.9
    ph = 2.5
    
    #create dem pads
    createNumberedPadsSMD(kicad_mod, pincount, -pitch, {'x': pw,'y': ph}, py)

    #create some sweet, sweet mechanical pads
    kicad_mod.addMountingPad(
    {'x': mx, 'y': my},
    {'x': mw, 'y': mh}
    )
    
    kicad_mod.addMountingPad(
    {'x': -mx, 'y': my},
    {'x': mw, 'y': mh}
    )
    
    #add pin-1 designation
    xm = A/2
    ym = py - ph/2 - 0.5
    
    m = 0.3
    
    kicad_mod.addPolygoneLine([
    {'x': xm,'y': ym},
    {'x': xm + m,'y': ym - 2*m},
    {'x': xm - m,'y': ym - 2*m},
    {'x': xm,'y': ym},
    ])
    
    #wall thickness t
    t = 0.8
    #line offset from pads o
    o = 0.5
    xo = A/2 + pw/2 + o #horizontal distance from numbered pads
    yo = my - mh/2 - o
    #draw left-hand line
    kicad_mod.addPolygoneLine([
    {'x': -xo,'y': y1},
    {'x': x1,'y': y1},
    {'x': x1,'y': yo},
    {'x': x1+t,'y': yo},
    {'x': x1+t,'y': y1+t},
    {'x': -xo,'y': y1+t},
    {'x': -xo,'y': y1},
    ])
    #draw right-hand line
    kicad_mod.addPolygoneLine([
    {'x': xo,'y': y1},
    {'x': x2,'y': y1},
    {'x': x2,'y': yo},
    {'x': x2-t,'y': yo},
    {'x': x2-t,'y': y1+t},
    {'x': xo,'y': y1+t},
    {'x': xo,'y': y1},
    ])
    
    #draw bottom line
    xa = -A/2 + o
    xb =  A/2 - o
    
    xo = mx - mw/2 - o
    
    #boss thickness b
    b = 1.5
    
    kicad_mod.addRectLine(
    {'x': -xo, 'y': y2 - b},
    {'x':  xo, 'y': y2}
    )
    
    #inner rect
    #rect thickness r
    r = 0.4
    kicad_mod.addRectLine(
    {'x': xa+r,'y': y2-b+r},
    {'x': xb-r,'y': y2-r})
    
    #left hand wall
    kicad_mod.addLine(
    {'x':  xa,'y': y2-b},
    {'x':  xa,'y': y2}
    )
    
    #right hand wall
    kicad_mod.addLine(
    {'x':  xb,'y': y2-b},
    {'x':  xb,'y': y2}
    )
    
    #add a "slot" for each of the pins
    for i in range(pincount):
        x = -A/2 + i * pitch
        
        #width of each pin
        w = 0.15
        
        ya = py + ph/2 + 0.6
        yb = y2 - b - 0.5
        
        kicad_mod.addRectLine(
        {'x': x-w,'y': ya},
        {'x': x+w,'y': yb}
        )
    
    
    #draw the courtyard
    cx2 = mx + mw/2 + 0.5
    cx1 = -cx2
    cy1 = -8.3 + 0.025
    cy2 = 0.5 - 0.025
    
    cy=0.5
    kicad_mod.addRectLine(
        {'x':cx1,'y':cy1},
        {'x':cx2,'y':cy2},
        "F.CrtYd", 0.05)
        
    
    """

    # output kicad model
    #Add a model
    footprint.append(Model(filename="Connectors_JST.3dshapes/" + fp_name + ".wrl"))
    
    #filename
    filename = output_dir + fp_name + ".kicad_mod"
    
    file_handler = KicadFileHandler(footprint)
    file_handler.writeFile(filename)
