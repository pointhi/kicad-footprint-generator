# create empty kicad footprint
#obj = KicadMod("")

#hole ={'number':1, 'type':'thru_hole', 'shape':'circle', 'pos':{'x':0, 'y':0, 'orientation':0}, 'size':{'x':2, 'y':2}, 'drill': {'size':{'x':0.8}, 'shape':'circle', 'offset':None}, 'layers':['*.Cu','*.Mask','F.SilkS'], 'die_length':None, 'rect_delta':None, 'clearance':None, 'solder_mask_margin':None, 'solder_paste_margin':None, 'solder_paste_margin_ratio':None, 'zone_connect':None, 'thermal_width':None, 'thermal_gap':None}

#obj._addPads([hole])
#
#obj.save('test')

class KicadMod(object):
    def __init__(self, name):
        self.setModuleName(name)
        self.text_array = []
        self.line_array = []
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
        
        for line in self.line_array:
            output += self._saveLine(line)
        
        for pad in self.pad_array:
            output += self._savePad(pad)
        
        output = output + ')'
        
        print(output)
