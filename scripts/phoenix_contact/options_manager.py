import os
import fnmatch

class OptionManager():
    helpstr = ["?", "--help", "-h"]

    model_filter = ".*" # default build all

    lib_name="Connectors_Phoenix"
    out_dir=lib_name+".pretty"+os.sep
    packages_3d=lib_name+".3dshapes"+os.sep

    courtyard_distance = 0.5
    silk_body_offset = 0.08
    fab_line_width = 0.05

    with_fab_layer = False
    inner_details_on_fab = False
    reference_on_fab_layer = False


    # try catch for flow controll because i'm to lazy to really think about it!
    @staticmethod
    def __num(s):
        try:
            return int(s)
        except ValueError:
            return float(s) # What if an invalid value is given? Answer: shut up and use it correctly ;)

    def parse_commands(self, cmd_line_args):
        if len(cmd_line_args) >=1 and (cmd_line_args[0] in self.helpstr):
            self.printHelp()
            return 0
        need_help = False
        new_outdir = None
        for arg in cmd_line_args:
            if arg.startswith("--lib_name="):
                self.set_lib_name(arg[len("--lib_name="):])
            elif arg.startswith("--out_dir="):
                new_outdir = arg[len("--out_dir="):]
            elif arg.startswith("--model_filter="):
                self.model_filter = fnmatch.translate(arg[len("--model_filter="):])
            elif arg.startswith("--crty_offset="):
                self.courtyard_distance = self.__num(arg[len("--crty_offset="):])
            elif arg.startswith("--silk_offset="):
                self.silk_body_offset = self.__num(arg[len("--silk_offset="):])
            elif arg.startswith("--fab_line_width="):
                self.fab_line_width = self.__num(arg[len("--fab_line_width="):])
            elif arg == "--enable_fab":
                self.with_fab_layer = 1
            elif arg == "--enable_detailed_fab":
                self.inner_details_on_fab = 1
                self.with_fab_layer = 1
            elif arg == "--enable_ref_on_fab":
                self.reference_on_fab_layer = 1
                self.with_fab_layer = 1
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
            "\t--lib_name=<Name of Library> Used for output dir name and 3dshapes name.\n"+
            "\t--out_dir=<path> output will be put here.\n"+
            "\t--model_filter=<filter string> Unix filename filter syntax.\n"+
            "\t--crty_offset=<int or float>\n"+
            "\t--silk_offset=<int or float>\n"+
            "\t--fab_line_width=<int or float>\n"+
            "\t--enable_fab\n"+
            "\t--enable_detailed_fab\n"+
            "\t--enable_ref_on_fab\n"
        )

    def set_lib_name(self, new_name):
        if new_name.endswith(".pretty"):
            new_name=new_name[:-len(".pretty")]
        self.lib_name=new_name
        self.out_dir=self.lib_name+".pretty"+os.sep
        self.packages_3d=self.lib_name+".3dshapes"+os.sep

    def set_outdir(self, new_dir):
        self.out_dir=new_dir + ("" if new_dir.endswith(os.sep) else os.sep)
