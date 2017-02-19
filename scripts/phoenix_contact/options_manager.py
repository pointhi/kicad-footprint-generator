import os
import fnmatch

class OptionManager():
    helpstr = ["?", "--help", "-h"]

    model_filter = ".*" # default build all

    # try catch for flow controll because i'm to lazy to really think about it!
    @staticmethod
    def __num(s):
        try:
            return int(s)
        except ValueError:
            return float(s) # What if an invalid value is given? Answer: shut up and use it correctly ;)

    def _useconfig_KLCv1_0(self):
        self.lib_name="Connectors_Phoenix"
        self.out_dir=self.lib_name+".pretty"+os.sep
        self.packages_3d=self.lib_name+".3dshapes"+os.sep

        self.courtyard_distance = 0.5
        self.silk_body_offset = 0.08
        self.fab_line_width = 0.15
        self.silk_line_width = 0.15

        self.with_fab_layer = False
        self.inner_details_on_fab = False
        self.use_second_ref = False
        self.main_ref_on_silk = True

        self.value_fontsize = [1,1]
        self.value_fontwidth=0.15
        self.value_inside = False

        self.main_ref_fontsize=[1,1]
        self.main_ref_fontwidth=0.15

        self.second_ref_fontsize=[1,1]
        self.second_ref_fontwidth=0.15

    def _useconfig_KLCv1_1(self):
        self.lib_name="Connectors_Phoenix"
        self.out_dir=self.lib_name+".pretty"+os.sep
        self.packages_3d=self.lib_name+".3dshapes"+os.sep

        self.courtyard_distance = 0.5
        self.silk_body_offset = 0.08
        self.fab_line_width = 0.1
        self.silk_line_width = 0.12

        self.with_fab_layer = False
        self.inner_details_on_fab = False
        self.use_second_ref = False
        self.main_ref_on_silk = False

        self.value_fontsize = [1,1]
        self.value_fontwidth=0.15
        self.value_inside = False

        self.main_ref_fontsize=[2,2]
        self.main_ref_fontwidth=0.2

        self.second_ref_fontsize=[1,1]
        self.second_ref_fontwidth=0.15

    def _useconfig_KLCv1_2(self):
        self.lib_name="Connectors_Phoenix"
        self.out_dir=self.lib_name+".pretty"+os.sep
        self.packages_3d=self.lib_name+".3dshapes"+os.sep

        self.courtyard_distance = 0.5
        self.silk_body_offset = 0.08
        self.fab_line_width = 0.1
        self.silk_line_width = 0.12

        self.with_fab_layer = True
        self.inner_details_on_fab = False
        self.use_second_ref = True
        self.main_ref_on_silk = True

        self.value_fontsize = [1,1]
        self.value_fontwidth=0.15
        self.value_inside = False

        self.main_ref_fontsize=[1,1]
        self.main_ref_fontwidth=0.15

        self.second_ref_fontsize=[1,1]
        self.second_ref_fontwidth=0.15

    def _useconfig_TERA(self):
        self.lib_name="tera_Connectors_Phoenix"
        self.out_dir=self.lib_name+".pretty"+os.sep
        self.packages_3d=self.lib_name+".3dshapes"+os.sep

        self.courtyard_distance = 0.5
        self.silk_body_offset = 0.08
        self.fab_line_width = 0.05
        self.silk_line_width = 0.15

        self.with_fab_layer = True
        self.inner_details_on_fab = False
        self.use_second_ref = True
        self.main_ref_on_silk = False

        self.value_fontsize = [0.6,0.6]
        self.value_fontwidth=0.1
        self.value_inside = True

        self.main_ref_fontsize=[1,1]
        self.main_ref_fontwidth=0.15

        self.second_ref_fontsize=[1,1]
        self.second_ref_fontwidth=0.15

    def __init__(self):
        self._useconfig_KLCv1_2()

    def parse_commands(self, cmd_line_args):
        if len(cmd_line_args) >=1 and (cmd_line_args[0] in self.helpstr):
            self.printHelp()
            return 0
        need_help = False
        new_outdir = None
        for arg in cmd_line_args:
            if arg.startswith("--useconfig="):
                config = arg[len("--useconfig="):]
                if config == "KLCv1.2":
                    self._useconfig_KLCv1_2()
                elif config == "KLCv1.1":
                    self._useconfig_KLCv1_1()
                elif config == "KLCv1.0":
                    self._useconfig_KLCv1_0()
                elif config == "TERA":
                    self._useconfig_TERA()
                else:
                    self._useconfig_KLCv1_2()
            elif arg.startswith("--lib_name="):
                self.set_lib_name(arg[len("--lib_name="):])
            elif arg.startswith("--out_dir="):
                new_outdir = arg[len("--out_dir="):]
            elif arg.startswith("--model_filter="):
                self.model_filter = fnmatch.translate(arg[len("--model_filter="):])
            else:
                print ("I did not unterstand: \"" + arg + "\" Ignored.")
                need_help = True
        if need_help:
            self.printHelp()
        if new_outdir is not None:
            # Ensure outdir is set after lib name (otherwise it would be overwritten.)
            self.set_outdir(new_outdir)
        return 1

    def printHelp(self):
        print("The following options can be used to configurate the generated footprints:\n"+
            "\t"+' or '.join(self.helpstr) + " prints this help message and stops. (only if first parameter)\n"+
            "\t --useconfig=[KLCv1.2 | KLCv1.1 | KLCv1.0 | TERA] without any option KLCv1.2 will be used"
            "\t--lib_name=<Name of Library> Used for output dir name and 3dshapes name.\n"+
            "\t--out_dir=<path> output will be put here.\n"+
            "\t--model_filter=<filter string> Unix filename filter syntax.\n"
        )

    def set_lib_name(self, new_name):
        if new_name.endswith(".pretty"):
            new_name=new_name[:-len(".pretty")]
        self.lib_name=new_name
        self.out_dir=self.lib_name+".pretty"+os.sep
        self.packages_3d=self.lib_name+".3dshapes"+os.sep

    def set_outdir(self, new_dir):
        self.out_dir=new_dir + ("" if new_dir.endswith(os.sep) else os.sep)

    def create_marker_poly(self, bottom_y, center_x=0):
        marker_width=0.6
        marker_height=0.6

        marker_top=bottom_y-marker_height
        marker_poly=[
            {'x':center_x, 'y':bottom_y},
            {'x':center_x+marker_width/2, 'y':marker_top},
            {'x':center_x-marker_width/2, 'y':marker_top},
            {'x':center_x, 'y':bottom_y}
        ]

        return marker_poly
