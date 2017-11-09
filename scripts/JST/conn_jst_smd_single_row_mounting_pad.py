# Generator for jst smd connectors (single row with two mounting pads)

def generate_one_footprint(pinrange, series_definition, configuration):
    jst_name = series_definition['mpn_format_string'].format(pincount=pincount)

    pad_pos_y = -series_definition['rel_pad_y_outside_edge']/2 +
        series_definition['pad_size'][1]/2
    mount_pad_y_pos = series_definition['rel_pad_y_outside_edge']/2 -
        series_definition['mount_pad_size'][1]/2
    mount_pad_center_x_to_pin = series_definition['center_pad_to_mounting_pad_edge'] +
        series_definition['mount_pad_size'][0]/2.0

    body_def = {}
    if series_definition['pad1_position'] == 'bottom-left':
        pad_pos_y *= -1
        mount_pad_y_pos *= -1
        body_def['top'] = mount_pad_y_pos - series_definition['rel_body_edge']
    else:


    # SMT type shrouded header, Side entry type (normal type)
    footprint_name = configuration['fp_name_format_string'].format(series=series,
        mpn=jst_name, num_rows=number_of_rows,
        pins_per_row=pincount, pitch=pad_spacing, orientation=orientation)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("JST {:s} series connector, {:s} ({:s})".format(series_definition['series'],
        jst_name, series_definition['datasheet']))
    kicad_mod.setAttribute('smd')
    kicad_mod.setTags(series_definition['tags'])


    ############################# Pads ##################################
    kicad_mod.append(Pad(number ='""', type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        at=[x_left_mount_pad, mount_pad_y_pos],
                        size=series_definition['mounting_pad_size'],
                        layers=Pad.LAYERS_SMT))
    kicad_mod.append(Pad(number ='""', type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        at=[-x_left_mount_pad, mount_pad_y_pos],
                        size=series_definition['mounting_pad_size'],
                        layers=Pad.LAYERS_SMT))

    ######################### Text Fields ###############################

    text_center = series_definition['ref_text_inside_pos']
    reference_fields = configuration['references']
    kicad_mod.append(Text(type='reference', text='REF**',
        **getTextFieldDetails(reference_fields[0], cy1, cy2, text_center)))

    for additional_ref in reference_fields[1:]:
        kicad_mod.append(Text(type='user', text='%R',
        **getTextFieldDetails(additional_ref, cy1, cy2, text_center)))

    value_fields = configuration['values']
    kicad_mod.append(Text(type='value', text=footprint_name,
        **getTextFieldDetails(value_fields[0], cy1, cy2, text_center)))

    for additional_value in value_fields[1:]:
        kicad_mod.append(Text(type='user', text='%V',
            **getTextFieldDetails(additional_value, cy1, cy2, text_center)))


    ########################### file names ###############################
    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}')

    lib_name = configuration['lib_name_format_string'].format(series=series)
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=footprint_name)
    kicad_mod.append(Model(filename=model_name))

    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)

def generate_series(configuration, series_definition, id):
    pinrange_def_type, pinrange_def = series_definition['pinrange']
    if pinrange_def_type == 'range':
        pinrange = range(**pinrange_def)
    elif pinrange_def_type == 'list':
        pinrange = pinrange_def
    else:
        print("Pinrange definition error in part {:s}".format(id))
        return

    for pincount in pinrange:
        generate_one_footprint(pinrange, series_definition, configuration)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='list of files holding information about what devices should be created.')
    parser.add_argument('-c', '--config', type=str, nargs='?', help='the config file defining how the footprint will look like.', default='config_KLCv3.0.yaml')
    args = parser.parse_args()

    with open(args.config, 'r') as config_stream:
        try:
            configuration = yaml.load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    for filepath in args.files:
        with open(filepath, 'r') as series_stream:
            try:
                series_definitions = yaml.load(series_stream)
            except yaml.YAMLError as exc:
                print(exc)
        for series_definition_id in series_definitions:
            def generate_series(configuration, series_definitions[series_definition_id], series_definition_id)
