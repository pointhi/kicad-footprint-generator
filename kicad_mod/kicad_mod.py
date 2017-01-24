'''
kicad-footprint-generator is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

kicad-footprint-generator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.

(C) 2015-2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>
'''

import time

def getFormatedFloat(val):
    return ('%f' % val).rstrip('0').rstrip('.')


class KicadMod(object):
    def __init__(self, name):
        self.setModuleName(name)
        self.text_array = []
        self.line_array = []
        self.circle_array = []
        self.pad_array = []
        self.description = None
        self.tags = None
        self.attribute = None
        self.center_pos = {'x':0, 'y':0}


    def setModuleName(self, name):
        self.module_name = name


    def setDescription(self, description):
        self.description = description


    def setTags(self, tags):
        self.tags = tags


    def setAttribute(self, value):
        self.attribute = value


    def setCenterPos(self, position):
        self.center_pos = position


    def addRawText(self, data):
        self.text_array.append(data)    


    def addText(self, which_text, text, position, layer='F.SilkS'):
        self.addRawText({'which_text':which_text
                        ,'text':text
                        ,'layer':layer
                        ,'position':position})

    def addReference(self, text, position, layer='F.SilkS'):
        self.addText('reference', text, position, layer)


    def addValue(self, text, position, layer='F.Fab'):
        self.addText('value', text, position, layer)


    def addRawLine(self, data):
        self.line_array.append(data)


    def addLine(self, start_pos, end_pos, layer='F.SilkS', width=0.15):
        self.addRawLine({'start':{'position':start_pos}
                        ,'end':{'position':end_pos}
                        ,'layer':layer
                        ,'width':width})


    def addPolygoneLine(self, polygone_line, layer='F.SilkS', width=0.15):
        for line_start, line_end in zip(polygone_line, polygone_line[1:]):
            self.addLine(line_start, line_end, layer, width)


    def addRectLine(self, start_pos, end_pos, layer='F.SilkS', width=0.15):
        self.addPolygoneLine([{'x':start_pos['x'], 'y':start_pos['y']}
                             ,{'x':start_pos['x'], 'y':end_pos['y']}
                             ,{'x':end_pos['x'], 'y':end_pos['y']}
                             ,{'x':end_pos['x'], 'y':start_pos['y']}
                             ,{'x':start_pos['x'], 'y':start_pos['y']}]
                            ,layer
                            ,width)


    def addRawCircle(self, data):
        self.circle_array.append(data)


    def addCircle(self, position, dimensions, layer='F.SilkS', width=0.15):
        self.addRawCircle({'position':position
                          ,'dimensions':dimensions
                          ,'layer':layer
                          ,'width':width})


    def addRawPad(self, data):
        self.pad_array.append(data)


    def addPad(self, number, type, form, position, size, drill, layers=['*.Cu', '*.Mask', 'F.SilkS']):
        self.addRawPad({'number':number, 'type':type, 'form':form, 'position':position, 'size':size, 'drill':drill, 'layers':layers})


    def _savePosition(self, position, keyword='at'):
        if position.get('orientation', 0) != 0:
            return '({keyword} {x} {y} {orientation})'.format(keyword=keyword
                                                             ,x=getFormatedFloat(position['x']-self.center_pos['x'])
                                                             ,y=getFormatedFloat(position['y']-self.center_pos['y'])
                                                             ,orientation=getFormatedFloat((position['orientation']+360)%360))
        else:
            return '({keyword} {x} {y})'.format(keyword=keyword
                                               ,x=getFormatedFloat(position['x']-self.center_pos['x'])
                                               ,y=getFormatedFloat(position['y']-self.center_pos['y']))


    def _saveSize(self, size, keyword='at'):
        return '({keyword} {x} {y})'.format(keyword=keyword
                                           ,x=getFormatedFloat(size['x'])
                                           ,y=getFormatedFloat(size['y']))


    def _saveText(self, data):
        output = '  (fp_text {which_text} {text} '.format(which_text=data['which_text']
                                                         ,text=data['text'])
        output += self._savePosition(data['position'], 'at')
        output += ' (layer {layer})\r\n'.format(layer=data['layer'])
        output += '    (effects (font (size 1 1) (thickness 0.15)))\r\n'
        output += '  )\r\n'
        
        return output


    def _saveLine(self, data):
        output = '  (fp_line '
        output += self._savePosition(data['start']['position'], 'start')
        output += ' '
        output += self._savePosition(data['end']['position'], 'end')
        output += ' (layer {layer}) (width {width}))\r\n'.format(layer=data['layer']
                                                                ,width=data['width'])
        return output


    def _saveCircle(self, data):
        output = '  (fp_circle '
        output += self._savePosition(data['position'], 'center')
        output += ' '
        
        dimensions = []
        dimensions = {'x':data['position']['x']+data['dimensions']['x']
                     ,'y':data['position']['y']+data['dimensions']['y']}
        
        output += self._savePosition(dimensions, 'end')
        output += ' (layer {layer}) (width {width}))\r\n'.format(layer=data['layer']
                                                                ,width=data['width'])
        return output


    def _savePad(self, data):
        output = '  (pad {number} {type} {form} '.format(number=data['number']
                                                        ,type=data['type']
                                                        ,form=data['form'])
        output += self._savePosition(data['position'], 'at')
        output += ' '
        output += self._saveSize(data['size'], 'size')
        output += ' (drill {drill}) '.format(drill=data['drill'])
        output += '(layers ' + ' '.join(data['layers']) + '))\r\n'
        return output


    def __str__(self):
        '''
        generate kicad_mod content
        '''
        output = '(module {name} (layer F.Cu) (tedit {timestamp:X})\r\n'.format(name=self.module_name, timestamp=int(time.time()))

        if self.description:
            output += '  (descr "{description}")\r\n'.format(description=self.description)

        if self.tags:
            output += '  (tags "{tags}")\r\n'.format(tags=self.tags)

        if self.attribute:
            output += '  (attr {attr})\r\n'.format(attr=self.attribute)

        for text in self.text_array:
            output += self._saveText(text)

        for circle in self.circle_array:
            output += self._saveCircle(circle)

        for line in self.line_array:
            output += self._saveLine(line)

        for pad in self.pad_array:
            output += self._savePad(pad)

        output = output + ')'

        return output


def createNumberedPadsTHT(kicad_mod, pincount, pad_spacing, pad_diameter, pad_size):
    for pad_number in range(1, pincount+1):
        pad_pos_x = (pad_number-1)*pad_spacing
        if pad_number == 1:
            kicad_mod.addPad(pad_number, 'thru_hole', 'rect', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask', 'F.SilkS'])
        elif pad_size['x'] == pad_size['y']:
            kicad_mod.addPad(pad_number, 'thru_hole', 'circle', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask', 'F.SilkS'])
        else:
            kicad_mod.addPad(pad_number, 'thru_hole', 'oval', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask', 'F.SilkS'])


def createNumberedPadsSMD(kicad_mod, pincount, pad_spacing, pad_size, pad_pos_y, pad_number_offset=0, pad_number_multiplier=1):
    start_pos_x = -(pincount-1)*pad_spacing/2.
    for pad_number in range(1, pincount+1):
        pad_pos_x = start_pos_x+(pad_number-1)*pad_spacing
        real_pad_number = pad_number * pad_number_multiplier + pad_number_offset - 1
        kicad_mod.addPad(real_pad_number, 'smd', 'rect', {'x':pad_pos_x, 'y':pad_pos_y}, pad_size, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
