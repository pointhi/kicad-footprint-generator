# library to create kicad footprints

class KicadMod(object):
    def __init__(self, name):
        self.setModuleName(name)
        self.text_array = []
        self.line_array = []
        self.circle_array = []
        self.pad_array = []
        self.description = None
        self.tags = None
    
    def setModuleName(self, name):
        self.module_name = name

    def setDescription(self, description):
        self.description = description
        
    def setTags(self, tags):
        self.tags = tags

    def addRawText(self, data):
        self.text_array.append(data)
    
    def addText(self, which_text, text, position, layer='F.SilkS'):
        self.addRawText({'which_text':which_text
                        ,'text':text
                        ,'layer':layer
                        ,'position':position})
    
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
            return '({keyword} {x} {y} {orientation})'.format(keyword=keyword, x=position['x'], y=position['y'], orientation=(position['orientation']+360)%360)
        else:
            return '({keyword} {x} {y})'.format(keyword=keyword, x=position['x'], y=position['y'])
    
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
        #(fp_circle (center -12.5 0.25) (end -12.25 0.25) (layer F.SilkS) (width 0.15))

        

    def _savePad(self, data):
        output = '  (pad {number} {type} {form} '.format(number=data['number']
                                                        ,type=data['type']
                                                        ,form=data['form'])
        output += self._savePosition(data['position'], 'at')
        output += ' '
        output += self._savePosition(data['size'], 'size')
        output += ' (drill {drill}) '.format(drill=data['drill'])
        output += '(layers ' + ' '.join(data['layers']) + '))\r\n'
        return output

    def save(self, filename):
        output = '(module {name} (layer F.Cu) (tedit 55D37D85)\r\n'.format(name=self.module_name)
        
        if self.description:
            output += '  (descr "{description}")\r\n'.format(description=self.description)

        if self.tags:
            output += '  (tags "{tags}")\r\n'.format(tags=self.tags)
        
        for text in self.text_array:
            output += self._saveText(text)
        
        for circle in self.circle_array:
            output += self._saveCircle(circle)
        
        for line in self.line_array:
            output += self._saveLine(line)
        
        for pad in self.pad_array:
            output += self._savePad(pad)
        
        output = output + ')'
        
        print(output)

def createNumberedPadsTHT(kicad_mod, pincount, pad_spacing, pad_diameter, pad_size):
    for pad_number in range(1, pincount+1):
        pad_pos_x = (pad_number-1)*pad_spacing
        if pad_number == 1:
            kicad_mod.addPad(pad_number, 'thru_hole', 'rect', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask', 'F.SilkS'])
        elif pad_size['x'] == pad_size['y']:
            kicad_mod.addPad(pad_number, 'thru_hole', 'circle', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask', 'F.SilkS'])
        else:
            kicad_mod.addPad(pad_number, 'thru_hole', 'oval', {'x':pad_pos_x, 'y':0}, pad_size, pad_diameter, ['*.Cu', '*.Mask', 'F.SilkS'])

def createNumberedPadsSMD(kicad_mod, pincount, pad_spacing, pad_size, pad_pos_y):
    start_pos_x = -(pincount-1)*pad_spacing/2
    for pad_number in range(1, pincount+1):
        pad_pos_x = start_pos_x+(pad_number-1)*pad_spacing
        kicad_mod.addPad(pad_number, 'smd', 'rect', {'x':pad_pos_x, 'y':pad_pos_y}, pad_size, 0, ['F.Cu', 'F.Paste', 'F.Mask'])
