import yaml
import pprint


def footprint_name(package, variant, num_pins, add_tab, tab_number):
    tab_suffix = '_TabPin' if add_tab else ''
    pins = str(num_pins)
    tab = str(tab_number)
    return '{p:s}-{ps:s}Lead{ts:s}{tn:s}'.format(p=package, ps=pins, ts=tab_suffix, tn=tab)


for device in yaml.load_all(open('dpak-config.yaml')):
    print('PACKAGE: {p:s}'.format(p=device['package']))
    print('KEYWORDS: {w:s}'.format(w=device['keywords']))
    print('BASE:')
    pprint.pprint(device['base'])    
    for v in device['variants']:
        print('VARIANT: {np:1d} pins'.format(np=v['pins']))
        pprint.pprint(v)
        print('EXAMPLE FOOTPRINT NAME: {fn:s}'\
              .format(fn=footprint_name(device['package'], v, v['pins'], True, 1 + v['pins'] // 2)))
    print()
