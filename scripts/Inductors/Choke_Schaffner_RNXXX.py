#http://katalog.we-online.com/en/pbs/WE-MAPI]

#sizes,shapes,etc]
#name, Type, #pins, A, B, H, L, W, , P, PDiam, PadSize
inductors = [
["RN102",  0, 4, 10.0, 10.0,  9.0, 14.0, 14.0,  4.0,  0.6,  2.0 ],
["RN112",  1, 4, 15.0, 10.0, 12.6, 17.7, 17.1,  4.0,  0.8,  2.0 ],
["RN114",  1, 4, 20.1, 12.5, 13.2, 22.5, 21.5,  4.0,  0.8,  2.0 ],
["RN116",  1, 4, 20.1, 12.5, 13.2, 22.5, 21.5,  4.0,  0.8,  2.0 ],
["RN122",  1, 4, 25.0, 15.0, 16.5, 28.0, 27.0,  4.0,  0.8,  2.0 ],
["RN142",  1, 4, 30.0, 20.0, 19.7, 33.1, 32.5,  4.3,  0.8,  2.0 ],
["RN143",  1, 4, 30.0, 20.0, 19.7, 33.1, 32.5,  4.3,  0.8,  2.0 ],
["RN152",  2, 4, 40.0, 15.0, 25.0, 43.0, 41.8,  4.5,  1.2,  2.5 ],
["RN202",  3, 4,  5.1, 15.2, 13.5,  8.8, 18.2,  4.5,  0.8,  2.0 ],
["RN204",  3, 4,  7.6, 10.0, 14.3,  9.0, 14.0,  4.0,  0.5,  2.0 ],
["RN212",  3, 4, 10.0, 15.0, 20.0, 12.5, 18.0,  4.0,  0.8,  2.0 ],
["RN214",  3, 4, 12.5, 10.0, 25.0, 15.5, 23.0,  4.0,  0.8,  2.0 ],
["RN216",  3, 4, 12.5, 10.0, 25.0, 15.5, 23.0,  4.0,  0.8,  2.0 ],
["RN218",  3, 4, 10.0, 12.5, 20.0, 12.5, 18.0,  4.0,  0.8,  2.0 ],
["RN222",  3, 4, 15.0, 12.5, 29.3, 18.0, 31.0,  4.0,  0.8,  2.0 ],
["RN232",  3, 4, 15.0, 12.5, 34.3, 18.0, 31.0,  4.2,  0.8,  2.0 ],
["RN242",  3, 4, 15.0, 12.5, 34.3, 18.0, 31.0,  4.2,  0.8,  2.0 ]
]

import sys
import os
import math

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
sys.path.append(os.path.join(sys.path[0], "..", ".."))
from KicadModTree import *
from KicadModTree.nodes.specialized.PadArray import PadArray

prefix = "Choke_Schaffner_"
part = "{serie}-0{pn}"
dims  = "{l:0.1f}mmx{w:0.1f}mm"
dims2 = "{l:0.1f}x{w:0.1f}mm"

desc = "Current-compensated Chokes, Schaffner, {pn}"
tags = "chokes schaffner tht"
TargetDir = "Inductor_THT.3dshapes"
Datasheet = "https://www.schaffner.com/products/download/product/datasheet/rn-series-common-mode-chokes-new/"

for inductor in inductors:
    Serie,Type,PN,A,B,H,L,W,P,PDiam,PadSize=inductor
    
    Pin1x1 = 0
    Pin1y1 = 0
    Pin1dx = 1.0
    RefX1 = 0
    RefY1 = round((0 - ((W - B) / 2) - 1.5), 2)

    cx = round(A / 2, 2)
    cy = round(B / 2, 2)

    fp_name = prefix + part.format(serie=str(Serie), pn=str(PN)) + "-" + dims2.format(l=L,w=W)
    fp = Footprint(fp_name)
    description = desc.format(pn = part.format(serie=str(Serie), pn=str(PN))) + ", " + dims.format(l=L,w=W) + " " + Datasheet
    
#    fp.append(Line(start=[cx - (L / 2), cy - (W / 2)], end=[cx + (L / 2), cy - (W / 2)],layer='F.Fab', width=0.01))
#    fp.append(Line(start=[cx + (L / 2), cy - (W / 2)], end=[cx + (L / 2), cy + (W / 2)],layer='F.Fab', width=0.01))
#    fp.append(Line(start=[cx + (L / 2), cy + (W / 2)], end=[cx - (L / 2), cy + (W / 2)],layer='F.Fab', width=0.01))
#    fp.append(Line(start=[cx - (L / 2), cy + (W / 2)], end=[cx - (L / 2), cy - (W / 2)],layer='F.Fab', width=0.01))

    if Type == 0:
        #
        # This have the shape of a box with rounded corners
        #
        #
        # Add the component outline
        #
        # Top line
        Layer = ['F.Fab', 'F.SilkS', 'F.CrtYd']
        LayerW = [0.1, 0.12, 0.05]
        LayerD = [0, 0.12, 0.25]
        for i in range(0, 3):
            myLayer = Layer[i]
            myLayerW = LayerW[i]
            myLayerD = LayerD[i]
            #
            # Top line
            x1 = 0
            y1 = 0 - (((W - B) / 2) + myLayerD)
            x2 = A
            y2 = y1
            fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer=myLayer,width=myLayerW))
            # Top right arc
            fp.append(Arc(center=[round(A, 2), round(0, 2)], start=[round(x2, 2), round(y2, 2)], angle=90.0, layer=myLayer, width=myLayerW))
            # Right line
            x1 = A + ((L - A) / 2) + myLayerD
            y1 = 0
            x2 = x1
            y2 = B
            fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer=myLayer,width=myLayerW))
            # Bottom right arc
            fp.append(Arc(center=[round(A, 2), round(B, 2)], start=[round(x2, 2), round(y2, 2)], angle=90.0, layer=myLayer, width=myLayerW))
            # Bottom line
            x1 = A
            y1 = B + ((W - B) / 2) + myLayerD
            x2 = 0
            y2 = y1
            fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer=myLayer,width=myLayerW))
            # Bottom left arc
            fp.append(Arc(center=[round(0, 2), round(B, 2)], start=[round(x2, 2), round(y2, 2)], angle=90.0, layer=myLayer, width=myLayerW))
            # Left line
            if (i == 0):
                x1 = 0 - (((L - A) / 2) + myLayerD)
                y1 = B
                x2 = x1
                y2 = 2
                fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer=myLayer,width=myLayerW))
                x1 = x2;
                y1 = y2
                x2 = x1 + 1
                y2 = 1
                fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer=myLayer,width=myLayerW))
                x1 = x2;
                y1 = y2
                x2 = x1 - 1
                y2 = 0
            else:
                x1 = 0 - (((L - A) / 2) + myLayerD)
                y1 = B
                x2 = x1
                y2 = 0
            fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer=myLayer,width=myLayerW))
            # Top left arc
            fp.append(Arc(center=[round(0, 2), round(0, 2)], start=[round(x2, 2), round(y2, 2)], angle=90.0, layer=myLayer, width=myLayerW))
            
            Pin1x1 = 0 - (((L - A) / 2) + 0.25)
            Pin1y1 = 0 - (((W - B) / 2) + 0.25)
            Pin1dx = 3.0
        
    elif Type == 1:
        #
        # This have the shape of a box with rounded top and bottom side
        #
        #
        # Add the component outline
        #
        # Calculate the arc
        #
        Points = []
        Layer = ['F.Fab', 'F.SilkS', 'F.CrtYd']
        LayerW = [0.1, 0.12, 0.05]
        LayerD = [0, 0.12, 0.25]
        #
        k = 0.0
        m = 0.0
        dx = round(L / 3, 2)
        dy = round(((W - B) / 2), 2)
        for i in range(0, 3):
            myLayer = Layer[i]
            myLayerW = LayerW[i]
            myLayerD = LayerD[i]
            #
            if (i == 0):
                #
                # Top arc
                #
                Fabh = dy
                angleD = 30.0
                Fabalpha = math.radians(angleD)
                x1 = round(cx, 2)
                y1 = round(0, 2)
                tdy = Fabh * math.cos(Fabalpha)
                tdx = Fabh * math.sin(Fabalpha)
                x2 = round(x1 - tdx, 2)
                y2 = round(0 - tdy, 2)
                p1 = [x1, y1, x2, y2]
                Points.append(p1)
                fp.append(Arc(center=[x1, y1], start=[x2, y2], angle=2*angleD, layer=myLayer, width=myLayerW))

                #
                # Top left line
                #
                x1 = round(cx - (L / 2), 2)
                y1 = round(0 - (PadSize / 2), 2)
                stx1 = x1
                sty1 = y1
                x2 = x2
                y2 = y2
                p1 = [x1, y1, x2, y2]
                Points.append(p1)
                fp.append(Line(start=[x1, y1],end=[x2, y2], layer=myLayer, width=myLayerW))
                #
                # Top right line
                #
                x1 = round(cx + tdx, 2)
                y1 = y2
                x2 = round(cx + (L / 2), 2)
                y2 = round(0 - (PadSize / 2), 2)
                p1 = [x1, y1, x2, y2]
                Points.append(p1)
                fp.append(Line(start=[x1, y1], end=[x2, y2], layer=myLayer, width=myLayerW))
                #
                # Right line
                #
                x1 = x2
                y1 = y2
                x2 = x1
                y2 = round(B + (PadSize / 2), 2)
                tty4 = y2;
                p1 = [x1, y1, x2, y2]
                Points.append(p1)
                fp.append(Line(start=[x1, y1], end=[x2, y2], layer=myLayer, width=myLayerW))
                #
                #
                # Bottom arc
                #
                Fabh = dy
                angleD = 30.0
                Fabalpha = math.radians(angleD)
                x1 = round(cx, 2)
                y1 = round(B, 2)
                tdy = Fabh * math.cos(Fabalpha)
                tdx = Fabh * math.sin(Fabalpha)
                x3 = round(cx + tdx, 2)
                y3 = round(B + tdy, 2)
                p1 = [x1, y1, x3, y3]
                Points.append(p1)
                fp.append(Arc(center=[x1, y1], start=[x3, y3], angle=2*angleD, layer=myLayer, width=myLayerW))
                #
                # Bottom right line
                #
                x1 = x2
                y1 = y2
                x2 = x3
                y2 = y3
                p1 = [x1, y1, x2, y2]
                Points.append(p1)
                fp.append(Line(start=[x1, y1], end=[x2, y2], layer=myLayer, width=myLayerW))
                #
                x1 = round(cx - tdx, 2)
                y1 = y3
                x2 = round(cx - (L / 2), 2)
                y2 = tty4
                p1 = [x1, y1, x2, y2]
                Points.append(p1)
                fp.append(Line(start=[x1, y1], end=[x2, y2], layer=myLayer, width=myLayerW))
                #
                # Left line including pin 1 chamfer
                #
                x1 = x2
                y1 = y2
                x2 = x1
                y2 = sty1
                p1 = [x1, y1, x2, y2]
                Points.append(p1)
                y2 = 0.5
                fp.append(Line(start=[x1, y1], end=[x2, y2], layer=myLayer, width=myLayerW))
                #
                x1 = x2
                y1 = y2
                x2 = x2 + 0.5
                y2 = 0;
                fp.append(Line(start=[x1, y1], end=[x2, y2], layer=myLayer, width=myLayerW))
                #
                x1 = x2
                y1 = y2
                x2 = x2 - 0.5
                y2 = -0.5;
                fp.append(Line(start=[x1, y1], end=[x2, y2], layer=myLayer, width=myLayerW))
                #
                x1 = x2
                y1 = y2
                x2 = x2
                y2 = sty1
                fp.append(Line(start=[x1, y1], end=[x2, y2], layer=myLayer, width=myLayerW))
                #
                Fabx1 = x2;
                Faby1 = y2;
                
            else:
                #
                # Y delta
                #
                point = Points[1]
                k = (point[3] - point[1]) / (point[2] - point[0])
                m = (point[1] - k * point[0]) - myLayerD - 0.02
                x1 = point[0] - myLayerD
                y1 = k * x1 + m
                ddy = math.fabs(math.sqrt(math.pow(point[1], 2)) - math.sqrt(math.pow(y1, 2)))
                # Top arc
                point = Points[0]
                Fabh = dy
                x1 = point[0]
                cx1 = x1
                y1 = round(point[1] - myLayerD, 2)
                tdy = Fabh * math.cos(Fabalpha)
                tdx = Fabh * math.sin(Fabalpha)
                x2 = round(point[2], 2)
                cx2 = x2
                y2 = round(point[3] - myLayerD - 0.02, 2)
                fp.append(Arc(center=[x1, y1], start=[x2, y2], angle=2*angleD, layer=myLayer, width=myLayerW))
                #
                # Top left line
                #
                point = Points[1]
                x1 = round(point[0] - myLayerD, 2)
                stx1 = x1
                y1 = round(k * x1 + m, 2)
                sty1 = y1
                x2 = round(point[2], 2)
                y2 = round((k * x2 + m), 2)
                fp.append(Line(start=[x1, y1], end=[x2, y2], layer=myLayer, width=myLayerW))
                # Top right line
                point = Points[2]
                x1 = round(cx1 + (cx1 - cx2), 2)
                y1 = y2
                x2 = round(point[2] + myLayerD, 2)
                y2 = sty1
                fp.append(Line(start=[x1, y1], end=[x2, y2], layer=myLayer, width=myLayerW))
                #
                # Right line
                #
                point = Points[3]
                x1 = x2
                y1 = y2
                x2 = x1
                tx2 = x2
                y2 = round(point[3] + ddy, 2)
                ty2 = y2
                fp.append(Line(start=[x1, y1], end=[x2, y2], layer=myLayer, width=myLayerW))
                #
                # Bottom arc
                #
                point = Points[4]
                Fabh = dy
                x1 = point[0]
                cx1 = x1
                y1 = round(point[1] + myLayerD, 2)
                tdy = Fabh * math.cos(Fabalpha)
                tdx = Fabh * math.sin(Fabalpha)
                x3 = round(point[2], 2)
                y3 = round(point[3] + myLayerD + 0.02, 2)
                fp.append(Arc(center=[x1, y1], start=[x3, y3], angle=2*angleD, layer=myLayer, width=myLayerW))
                #
                # Bottom right line
                #
                point = Points[5]
                x1 = tx2
                y1 = ty2
                x2 = x3
                y2 = y3
                fp.append(Line(start=[x1, y1], end=[x2, y2], layer=myLayer, width=myLayerW))
                # Bottom left line
                point = Points[6]
                x1 = round(cx1 - tdx, 2)
                y1 = y3
                x2 = stx1
                y2 = ty2
                fp.append(Line(start=[x1, y1], end=[x2, y2], layer=myLayer, width=myLayerW))
                #
                point = Points[7]
                x1 = x2
                y1 = y2
                x2 = x1
                y2 = sty1
                fp.append(Line(start=[x1, y1], end=[x2, y2], layer=myLayer, width=myLayerW))

                Pin1x1 = x2
                Pin1y1 = y2
                Pin1dx = 0.25
                RefX1 = 1.0
                RefY1 = -5

    elif Type == 2:
        #
        # This have the shape of a hexagon
        #
        Points = []
        # Add the component outline
        #
        ty = ((W - B) / 2)
        alpha = 30.0    # 70 degree
        alphar = ((2 * math.pi) / 360.0) * alpha
        tx = ty * (math.sin(alphar) / math.cos(alphar))
        x1 = 0 - ((L - A) / 2)
        y1 = 0
        x2 = x1 + tx
        y2 = y1 - ty
        k = (y1 - y2) / (x1 - x2)
        m = y1 - (k * x1)
        p1 = [x1, y1, x2, y2, k, m]
        Points.append(p1)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = x1 + (L - (2 * tx))
        y2 = y1
        k = (y1 - y2) / (x1 - x2)
        m = y1 - (k * x1)
        p1 = [x1, y1, x2, y2, k, m]
        Points.append(p1)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = x1 + tx
        y2 = y1 + ty
        k = (y1 - y2) / (x1 - x2)
        m = y1 - (k * x1)
        p1 = [x1, y1, x2, y2, k, m]
        Points.append(p1)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = x1
        y2 = y1 + B
        k = 0
        m = 0
        p1 = [x1, y1, x2, y2, k, m]
        Points.append(p1)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = x1 - tx
        y2 = y1 + ty
        k = (y1 - y2) / (x1 - x2)
        m = y1 - (k * x1)
        p1 = [x1, y1, x2, y2, k, m]
        Points.append(p1)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = x1 - (L - (2 * tx))
        y2 = y1
        k = (y1 - y2) / (x1 - x2)
        m = y1 - (k * x1)
        p1 = [x1, y1, x2, y2, k, m]
        Points.append(p1)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = x1 - tx
        y2 = y1 - ty
        k = (y1 - y2) / (x1 - x2)
        m = y1 - (k * x1)
        p1 = [x1, y1, x2, y2, k, m]
        Points.append(p1)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = 0 - ((L - A) / 2)
        tx2 = x2
        y2 = 2
        k = (y1 - y2) / (x1 - x2)
        m = y1 - (k * x1)
        p1 = [x1, y1, x2, y2, k, m]
        Points.append(p1)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = x2 + 1
        y2 = 1
        k = (y1 - y2) / (x1 - x2)
        m = y1 - (k * x1)
        p1 = [x1, y1, x2, y2, k, m]
        Points.append(p1)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = tx2
        y2 = 0
        k = (y1 - y2) / (x1 - x2)
        m = y1 - (k * x1)
        p1 = [x1, y1, x2, y2, k, m]
        Points.append(p1)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))

        #
        # Add the component outline
        #
        PadDistance = 0.75
        space=0.12
        p1 = Points[0]
        k =  p1[4]
        m = p1[5]
        y1 = (0 - ((PadSize / 2) + PadDistance))
        x1 = ((y1 - m) / k)
        y1 = y1 - (space * math.sin(alphar))
        x1 = x1 - (space * math.cos(alphar))
        y2 = p1[3] - space
        x2 = ((y2 - (m - (2 * space))) / k)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.SilkS',width=0.12))
        #
        # Top line
        #
        p1 = Points[1]
        x1 = x2
        y1 = y2
        x2 = p1[2] + (space * math.sin(alphar))
        y2 = y1
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.SilkS',width=0.12))
        #
        p1 = Points[2]
        k =  p1[4]
        m = p1[5]
        x1 = x2
        y1 = y2
        y2 = (0 - ((PadSize / 2) + PadDistance))
        x2 = ((y2 - m) / k)
        y2 = y2 - (space * math.sin(alphar))
        x2 = x2 + (space * math.cos(alphar))
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.SilkS',width=0.12))
        #
        # right side line
        #
        p1 = Points[3]
        k =  p1[4]
        m = p1[5]
        x1 = p1[0] + space
        y1 = ((PadSize / 2) + PadDistance)
        x2 = x1
        y2 = B - ((PadSize / 2) + 0.5)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.SilkS',width=0.12))
        #
        p1 = Points[4]
        k =  p1[4]
        m = p1[5]
        y1 = B + ((PadSize / 2) + PadDistance)
        x1 = ((y1 - m) / k)
        y1 = y1 + (space * math.sin(alphar))
        x1 = x1 + (space * math.cos(alphar))
        y2 = p1[3] + space
        x2 = ((y2 - (m + (2 * space))) / k)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.SilkS',width=0.12))
        #
        # Bottom line
        #
        p1 = Points[5]
        x1 = x2
        y1 = y2
        x2 = p1[2] - (space * math.sin(alphar))
        y2 = y1
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.SilkS',width=0.12))
        #
        p1 = Points[6]
        k =  p1[4]
        m = p1[5]
        x1 = x2
        y1 = y2
        y2 = B + ((PadSize / 2) + PadDistance)
        x2 = ((y2 - m) / k)
        y2 = y2 + (space * math.sin(alphar))
        x2 = x2 - (space * math.cos(alphar))
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.SilkS',width=0.12))
        #
        # Left side line
        #
        p1 = Points[7]
        k =  p1[4]
        m = p1[5]
        x1 = p1[0] - space
        y1 = B - ((PadSize / 2) + PadDistance)
        x2 = x1
        y2 = ((PadSize / 2) + PadDistance)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.SilkS',width=0.12))

        #
        # Add the component courtyard
        #
        PadDistance = 0.75
        space=0.25
        p1 = Points[0]
        k =  p1[4]
        m = p1[5]
        y1 = (0 - ((PadSize / 2) + PadDistance))
        x1 = ((y1 - m) / k)
        y1 = y1 - (space * math.sin(alphar))
        x1 = x1 - (space * math.cos(alphar))
        y2 = p1[3] - space
        x2 = ((y2 - (m - (2 * space))) / k)
        scx = x1
        scy = y1
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.CrtYd',width=0.05))
        #
        # Top line
        #
        p1 = Points[1]
        x1 = x2
        y1 = y2
        x2 = p1[2] + (space * math.sin(alphar))
        y2 = y1
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.CrtYd',width=0.05))
        #
        p1 = Points[2]
        k =  p1[4]
        m = p1[5]
        x1 = x2
        y1 = y2
        y2 = (0 - ((PadSize / 2) + PadDistance))
        x2 = ((y2 - m) / k)
        y2 = y2 - (space * math.sin(alphar))
        x2 = p1[2] + space
        y2 = p1[3]
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.CrtYd',width=0.05))
        #
        # Right side line
        #
        p1 = Points[3]
        k =  p1[4]
        m = p1[5]
        x1 = p1[0] + space
        y1 = p1[1]
        x2 = x1
        y2 = p1[3] + (space * math.sin(alphar))
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.CrtYd',width=0.05))
        #
        p1 = Points[4]
        k =  p1[4]
        m = p1[5]
        y1 = y2
        x1 = x2
        y2 = p1[3] + space
        x2 = ((y2 - (m + (2 * space))) / k)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.CrtYd',width=0.05))
        #
        # Bottom line
        #
        p1 = Points[5]
        x1 = x2
        y1 = y2
        x2 = p1[2] - (space * math.sin(alphar))
        y2 = y1
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.CrtYd',width=0.05))
        #
        p1 = Points[6]
        x1 = x2
        y1 = y2
        x2 = p1[2]
        y2 = p1[3]
        y2 = y2 + (space * math.sin(alphar))
        x2 = x2 - (space * math.cos(alphar))
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.CrtYd',width=0.05))
        #
        # Left side line
        #
        p1 = Points[7]
        x1 = x2
        y1 = y2
        x2 = x1
        y2 = scy 
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.CrtYd',width=0.05))
        x1 = x2
        y1 = y2
        x2 = scx
        y2 = scy
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.CrtYd',width=0.05))
        #
        Pin1x1 = x1
        Pin1y1 = scy

        RefX1 = 10.0
        
    elif Type == 3:
        #
        # This have the shape of a box
        #
        #
        # Add the component outline
        #
        x1 = 0 - ((L - A) / 2)
        y1 = 0 - ((W - B) / 2)
        x2 = x1 + L
        y2 = y1
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = x1
        y2 = y1 + W
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = x1 - L
        y2 = y1
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = x1
        y2 = 1
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = x1 + 1
        y2 = y1 - 1
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = 0 - ((L - A) / 2)
        y2 = -1
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = 0 - ((L - A) / 2)
        y2 = 0 - ((W - B) / 2)
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.Fab',width=0.1))

        #
        # Add the component outline
        #
        x1 = (0 - ((L - A) / 2)) - 0.12
        y1 = (0 - ((W - B) / 2)) - 0.12
        x2 = x1 + L + 0.24
        y2 = y1
        if (y1 > ((PadSize / 2) + 0.25)):
            x1 = ((PadSize / 2) + 0.5)
            x2 = A - (PadSize / 2) - 0.5
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.SilkS',width=0.12))
        #
        x1 = x1 + L + 0.24
        y1 = y2 
        x2 = x1
        y2 = y1 + W + 0.24
        if (x1 < (A + ((PadSize / 2) + 0.25))):
            y1 = (PadSize / 2) + 0.5
            y2 = B - (PadSize / 2) - 0.5
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.SilkS',width=0.12))
        #
        x1 = x1
        y1 = (0 - ((W - B) / 2)) + W + 0.12
        x2 = (0 - ((L - A) / 2)) - 0.12
        y2 = y1
        if (y2 < (B + ((PadSize / 2) + 0.25))):
            x1 = ((PadSize / 2) + 0.5)
            x2 = A - (PadSize / 2) - 0.5
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.SilkS',width=0.12))
        #
        x1 = x2
        y1 = y2 
        x2 = x1
        y2 = (0 - ((W - B) / 2)) - 0.12
        if (x1 > (0 - ((PadSize / 2) + 0.25))):
            y1 = (PadSize / 2) + 0.5
            y2 = B - (PadSize / 2) - 0.5
        fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.SilkS',width=0.12))

        #
        # Add the component courtyard
        #
        x1 = (0 - ((L - A) / 2)) - 0.25
        y1 = (0 - ((W - B) / 2)) - 0.25
        if (x1 > (0 - ((PadSize / 2) + 0.25))):
            x1 = 0 - ((PadSize / 2) + 0.25)
        if (y1 > (0 - ((PadSize / 2) + 0.25))):
            y1 = 0 - ((PadSize / 2) + 0.25)
        Pin1x1 = x1
        Pin1y1 = y1
        x2 = x1 + A - Pin1x1
        y2 = y1 + B - Pin1y1
        if (x2 < (A + ((L - A) / 2) + 0.25)):
            x2 = (A + ((L - A) / 2) + 0.25)
        if (y2 < (B + ((W - B) / 2) + 0.25)):
            y2 = (B + ((W - B) / 2) + 0.25)
        if (x2 < (A + (PadSize / 2) + 0.25)):
            x2 = (A + (PadSize / 2) + 0.25)
        if (y2 < (B + (PadSize / 2) + 0.25)):
            y2 = (B + (PadSize / 2) + 0.25)
        fp.append(RectLine(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.CrtYd',width=0.05))

        RefX1 = 0.0
        RefY1 = 0 - (((W - B) / 2) + 2)

    #
    # Add Pin 1 marker
    #
    x1 = Pin1x1 - 0.25
    y1 = Pin1y1 - 0.25
    x2 = x1 + Pin1dx
    y2 = y1
    fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.SilkS',width=0.12))
    x1 = x1
    y1 = y1
    x2 = x1
    y2 = y1 + 3.0
    fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer='F.SilkS',width=0.12))

    fp.setTags(tags)
    fp.setDescription(description)
    
    #
    # Set general values
    #
    fp.append(Text(type='reference', text='REF**', at=[RefX1, RefY1], layer='F.SilkS'))
    fp.append(Text(type='value', text=fp_name,     at=[round((A / 2), 2), round(((W - B) / 2) + B + 1.5,   2)], layer='F.Fab'))
    fp.append(Text(type='user', text="%R",         at=[round((A / 2), 2), round((B / 2), 2)], layer='F.Fab'))
    
    #
    # Add 3D model
    #
    fp.append(Model(filename="${KISYS3DMOD}/" + TargetDir + "/" + fp_name + ".wrl", at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))
    
    #
    # Add pads
    #
    fp.append(Pad(number=1,at=[0, 0], layers=Pad.LAYERS_THT, shape=Pad.SHAPE_RECT,   type=Pad.TYPE_THT,  size=[PadSize,PadSize], drill=round(PDiam + 0.1, 2)))
    fp.append(Pad(number=2,at=[A, 0], layers=Pad.LAYERS_THT, shape=Pad.SHAPE_CIRCLE, type=Pad.TYPE_THT,  size=[PadSize,PadSize], drill=round(PDiam + 0.1, 2)))
    fp.append(Pad(number=3,at=[0, B], layers=Pad.LAYERS_THT, shape=Pad.SHAPE_CIRCLE, type=Pad.TYPE_THT,  size=[PadSize,PadSize], drill=round(PDiam + 0.1, 2)))
    fp.append(Pad(number=4,at=[A, B], layers=Pad.LAYERS_THT, shape=Pad.SHAPE_CIRCLE, type=Pad.TYPE_THT,  size=[PadSize,PadSize], drill=round(PDiam + 0.1, 2)))

    #filename
    filename = output_dir + fp_name + ".kicad_mod"
    
    file_handler = KicadFileHandler(fp)
    file_handler.writeFile(filename)
