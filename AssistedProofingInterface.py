from fontTools.ttLib import TTFont
import os
from fontTools.designspaceLib import DesignSpaceDocument as dsp_doc
import fontTools.varLib as varLib
from fontTools.misc.fixedTools import otRound, strToFixedToFloat, floatToFixedToFloat
import fnmatch
from typing import Union
import re
import drawBot as bot
import drawBotGrid as grid
from drawBotGrid import textOverflowTestMode as overflow_mode
from defcon.tools.identifiers import makeRandomIdentifier

import getpass
import datetime

# API
# Assisted Proofing Interface

NOW  = datetime.datetime.now()
USER = getpass.getuser()
di   = os.path.split(__file__)[0]
PROOF_FOLDER = ""

CORE         = ()
RUNNING_TEXT = ()
OPENTYPE     = ()
GRADIENT     = ()
INSPECTOR    = ()

SECTION_TYPES = [CORE, RUNNING_TEXT, OPENTYPE, GRADIENT, INSPECTOR]

RUNNING_TEXT_TYPES = [
"spacing",
"figures",
"lowercaseCopy",
"uppercaseCopy",
"paragraph",
"kerning"
]

FONT_SIZE_DEFAULT = 28
FONT_SIZE_SMALL   = 9
FONT_SIZE_MED     = 12

PAGE_SIZES = bot.sizes()
PAGE_SIZE_DEFAULT = "LetterLandscape"


def find_proof_directory(start_location, target):
    start_location = os.path.abspath(start_location)
    closest_directory = save_path = None
    closest_distance = float('inf')  # Initialize to positive infinity
    current_path = start_location
    while current_path != os.path.sep:
        for filename in os.listdir(current_path):
            if target in filename:
                distance = len(os.path.relpath(current_path, start_location).split(os.path.sep))
                if distance < closest_distance:
                    closest_directory = current_path
                    closest_distance = distance
                    save_path = os.path.join(closest_directory, filename)
        current_path = os.path.dirname(current_path)
    return save_path


###################################
################################### taken from fontMake instancistator

def widthClass(wdth_user_value) -> int:
    WDTH_VALUE_TO_OS2_WIDTH_CLASS = { 50:1, 62.5:2, 75:3, 87.5:4, 100:5, 112.5:6, 125:7, 150:8, 200:9}
    width_user_value = min(max(wdth_user_value, 50), 200)
    width_user_value_mapped = varLib.models.piecewiseLinearMap(
        width_user_value, WDTH_VALUE_TO_OS2_WIDTH_CLASS
    )
    return otRound(width_user_value_mapped)

def weightClass(wght_user_value) -> int:
    weight_user_value = min(max(wght_user_value, 1), 1000)
    return otRound(weight_user_value)

def italicVal(slnt_user_value) -> Union[int, float]:
    slant_user_value = min(max(slnt_user_value, -90), 90)
    return slant_user_value

###################################

class proofLocation:

    def __init__(self):

        self._name = "unnamed location"
        self._location = None

        # DesignSpaceDocument or TTFont
        self._source_loca = "TTFont"
        self._in_crop = True

    def _get_in_crop(self):
        return self._in_crop

    def _set_in_crop(self, new_in_crop):
        self._in_crop = new_in_crop

    in_crop = property(_get_in_crop, _set_in_crop)

    def _get_source_loca(self):
        return self._source_loca

    def _set_source_loca(self, new_source_loca):
        self._source_loca = new_source_loca

    source = property(_get_source_loca, _set_source_loca)

    def _get_name(self):
        return self._name

    def _set_name(self, new_name):
        self._name = new_name

    name = property(_get_name, _set_name)

    def _get_location(self):
        return self._location

    def _set_location(self, new_location):
        self._location = new_location

    location = property(_get_location, _set_location)

    def generate_name(self, TTFont):
        f = TTFont
        best_name = f["name"].getBestFullName()
        if "fvar" in f:
            for i in f["fvar"].instances: 
                if i.coordinates == self._location:   
                    for name in f["name"].names:
                        if name.nameID == i.subfamilyNameID:
                            best_name = f'{f["name"].getBestFamilyName()} {name}'
        return best_name


class proofSource(proofLocation):

    def __init__(self, location):
        self.location = location

    def __repr__(self):
        return f"<proofSource @ {self.name}>"


class proofInstance(proofLocation):

    def __init__(self, location):
        self.location = location

    def __repr__(self):
        return f"<proofInstance @ {self.name}>"
    

class proofFont:

    def __repr__(self):
        return f"<proofFont @ {self.name}>"

    def __init__(self, path):

        self.path               = path
        self.font_object        = None
        self.load_font()
        self.is_variable        = False
        self.instances          = []
        self.sources            = []
        self.locations          = []
        self.operator_reference = None
        self._name              = self._compile_name()

        self.load_locations()

    def load_font(self):
        if self.path:
            self.font_object = TTFont(self.path)

    # get font objects best possible name
    def _compile_name(self):
        f = self.font_object
        best_name = f["name"].getBestFullName()
        return best_name

    def _get_name(self):
        return self._name

    def _set_name(self, new_name=None):
        self._name = new_name

    name = property(_get_name, _set_name)


    def _sort_locations(self, instances):
        return sorted(instances, key=lambda d: (-widthClass(d.location.get("wdth",0)), -italicVal(d.location.get("slnt",0)), weightClass(d.location.get("wght",0))))

    def _reformat_locations(self,designspace,instance,axisMap,renamer):
        parsed = {}
        instance = designspace.map_backward(instance.location)
        for axis,val in instance.items():
            a = renamer.get(axis)
            if a in axisMap.keys():
                parsed[a]=val
        return parsed

    def load_locations(self):
        source   = self.font_object
        operator = self.operator_reference

        _instances = []  

        for inst in [instance.coordinates for instance in source["fvar"].instances]:
            built = proofInstance(inst)
            n = built.generate_name(source)
            built.name = n
            built._source_loca = "TTFont"
            _instances.append(built)

        self.instances = self._sort_locations(_instances)

        if operator:
            RENAME  = {a.name:a.tag for a in operator.axes}
            axisMap = {a.axisTag:(a.minValue,a.maxValue) for a in source["fvar"].axes}            

            _sources = []

            for _master in [master for master in operator.sources if not master.layerName]:
                src = self._reformat_locations(operator,_master,axisMap,RENAME)
                built = proofSource(src)
                n = f"{_master.familyName} {_master.styleName}"
                built.name = n
                built._source_loca = "DesignSpaceDocument"
                _sources.append(built)

            self.sources = self._sort_locations(_sources)

        self.locations = []
        self.locations.extend(self.sources)
        self.locations.extend(self.instances)



class proofDocument:

    def __repr__(self):
        return f"<proofDocument @ {self.identifier} : {len(self.fonts)}>"

    def __init__(self):

        self._identifier = None
        self.fonts = []
        # size can either be a tuple of ints or a DrawBot
        # compatible paper size name string
        
        self.operator = None
        self.crop = ""
        self._expand_instances = False

        self._path = None
        self._name = None

        # proof UI settings
        self._size = "LetterLandscape"
        self._margin = 10
        self._margin_left   = self._margin
        self._margin_right  = self._margin
        self._margin_top    = self._margin
        self._margin_bottom = self._margin


        self._auto_open = False

        self._caption_font = "SFMono-Regular"


    # do we even need ids??-----------------------
    def _get_identifier(self):
        if not self._identifier:
            self._identifier = self.generate_identifier()
        return self._identifier

    def _set_identifier(self, new_id):
        self._identifier = new_id

    identifier = property(_get_identifier, _set_identifier)

    def generate_identifier(self):
        return makeRandomIdentifier(existing=[])
    # ----------------------------------------------


    def _get_page_size(self):
        if isinstance(self._size, str):
            size = PAGE_SIZES[self._size]
        else:
            size = self._size
        return size

    def _set_page_size(self, new_page_size):
        if isinstance(new_page_size, str):
            if new_page_size in list(PAGE_SIZES.keys()):
                self._size = new_page_size
            else:
                self._size = PAGE_SIZE_DEFAULT
                print(f"""ERROR: {new_page_size} is not a valid page size, defaulting to {PAGE_SIZE_DEFAULT}""")
        if isinstance(new_page_size, tuple):
            ll = len(new_page_size)
            if ll == 2:
                self._size = new_page_size
            elif ll == 1:
                self._size = (new_page_size, new_page_size)
            else:
                self._size = PAGE_SIZE_DEFAULT
                print(f"""ERROR: {new_page_size} is not a valid page size, defaulting to {PAGE_SIZES[PAGE_SIZE_DEFAULT]}""")

        if self._margin == "auto":
            self.margin = "auto"

    size = property(_get_page_size, _set_page_size)

    def _set_caption_font(self, new_font):
        import errno
        if new_font in bot.installedFonts():
            self._caption_font = new_font
        else:
            raise FileNotFoundError(
                        errno.ENOENT,
                        os.strerror(errno.ENOENT),
                        new_font
                        )

    def _get_caption_font(self):
        return self._caption_font

    caption_font = property(_get_caption_font, _set_caption_font)


    def _set_auto_open(self, bool):
        self._auto_open = bool

    def _get_auto_open(self):
        return self._auto_open

    # open pdf immediately after saving to disk
    open_automatically = property(_get_auto_open, _set_auto_open)

    def _set_path(self, new_path):
        self._path = new_path

    def _get_path(self):
        if not self._path:
            self._path = self.generate_path_base()
        return self._path

    path = property(_get_path, _set_path)

    def _set_name(self, new_name):
        self._name = new_name

    def _get_name(self):
        if not self._name and self.fonts:
            # return family name for top level font
            self._name = self.fonts[0].font_object["name"].getBestFamilyName().replace(" ","")
        return self._name

    name = property(_get_name, _set_name)

    def uniquify(self, path):
        # https://stackoverflow.com/a/57896232
        filename, extension = os.path.splitext(path)
        counter = 1
        while os.path.exists(path):
            path = filename + "-" + str(counter) + extension
            counter += 1
        return path

    def generate_path_base(self):
        cd = os.path.split(self.fonts[0].path)[0]
        directory = find_proof_directory(cd, "proofs") 
        if not directory:
            directory = cd
        # make sure file names are always unique!
        path = self.uniquify(f'{directory}/{NOW:%Y-%m%d}-{self.name}-Proof.pdf')
        return path

    def save(self, path=None):
        pass

    def new_section(self,
                    proof_type=None,
                    point_size=FONT_SIZE_DEFAULT, # can accept list to generate section at different sizes
                    sources=True,
                    instances=False,
                    restrict_page=False # if set to False the overflow will add new pages
                    ):

        pass

    def _get_margin(self):
        return (
                self._margin_top,
                self._margin_left, 
                self._margin_bottom,
                self._margin_right,
                )

    def _set_margin(self, new_margin):
        # we can accept a tuple of 4 to set individual 
        # or 1 value to apply across the board
        if isinstance(new_margin, tuple):
            if len(new_margin) == 4:
                # counter clockwise from top
                T,L,B,R = new_margin
            else:
                # if length isnt 4 we just use the first value
                T = L = B = R = new_margin[0]
        elif str(new_margin).lower() == "auto":
            # this is a biased margin spacing based on page size
            w,h = self.size
            T = int(h * 0.09)
            L = R = int(w * 0.085)
            B = int(h * 0.12)

        else:
            # if we set the main margin, we also reset all margins
            T = L = B = R = new_margin
        self._margin        = new_margin
        self._margin_left   = L
        self._margin_right  = R
        self._margin_top    = T
        self._margin_bottom = B

    margin = property(_get_margin, _set_margin)



    def find_close(self, root_dir, target_filename):
        closest_file = None
        closest_mtime = float('inf')

        for foldername, subfolders, filenames in os.walk(root_dir):
            for filename in fnmatch.filter(filenames, target_filename):
                file_path = os.path.join(foldername, filename)
                mtime = os.path.getmtime(file_path)
                
                if mtime < closest_mtime:
                    closest_mtime = mtime
                    closest_file = file_path

        return closest_file


    def get_variable_fonts_from_op(self):
        d = self.operator
        var = d.variableFonts
        di,fi = os.path.split(os.path.abspath(d.path))
        allVFs = []
        if var:
            for vf in var:
                name = vf.name
                file_name = vf.filename
                if file_name:
                    if os.path.isabs(file_name):
                        p = file_name
                    else:
                        if "variable_ttf/" in file_name:
                            pass
                        else:
                            file_name = f"variable_ttf/{file_name}"
                        p = os.path.join(di,file_name)
                        if not os.path.exists(p):
                            continue 
                else:
                    if name:
                        p = self.find_close(di,f"{name}.ttf")

                te = proofFont(p)
                te.is_variable = True
                te.operator_reference = self.operator
                te.load_locations()

                allVFs.append(te)

        return allVFs


    def add_object(self, path=None):
        suffixes = ".ttf .otf .woff .woff2"
        suff = os.path.splitext(path)[-1]
        if suff in suffixes.split(" "):
            o = proofFont(path)        
            self.fonts.append(o)
        elif suff == ".designspace":
            self.operator = dsp_doc.fromfile(path)
            vfs = self.get_variable_fonts_from_op()
            self.fonts.extend(vfs)

    #convience function to add multiple paths at once
    def add_objects(self, paths=[]):
        for path in paths:
            self.add_object(path)


    def reformat_limits(self, limits):
        '''
        use fontTools.varLib model for extracting the CLI data into a dictionary item
        taken from the source code ^
        '''
        result = {}
        for limitString in [limits]:
            match = re.match(r"^(\w{1,4})=(?:(drop)|(?:([^:]+)(?:[:](.+))?))$", limitString)
            if not match:
                raise ValueError("invalid location format: %r" % limitString)
                sys.exit()
            tag = match.group(1).ljust(4)
            if match.group(2):  # 'drop'
                lbound = None
            else:
                lbound = strToFixedToFloat(match.group(3), precisionBits=16)
            ubound = lbound
            if match.group(4):
                ubound = []
                for v in match.group(4).split(":"):
                    ubound.append(strToFixedToFloat(v, precisionBits=16))
            if lbound != ubound:
                result[tag] = tuple((lbound, *ubound))
            else:
                result[tag] = lbound
        return result


    def crop_space(self, zone):
        zone = self.reformat_limits(zone)
        for font in self.fonts:
            cropped = []
            instances = font.instances
            instances.extend(font.sources)
            if isinstance(zone, dict):
                for inst in instances:

                    check = []
                    for axis,value in zone.items():
                        a = inst.location.get(axis)
                        if a:
                            if isinstance(value, float):
                                if a == value:
                                    check.append(1)
                                else:
                                    check.append(0)
                            if isinstance(value, tuple):
                                mn,mx = value[0],value[-1]
                                if a:
                                    if mn <= a <= mx:
                                        check.append(1)
                                    else:
                                        check.append(0)
                    if 0 not in check:
                        inst.in_crop = True
                    else:
                        inst.in_crop = False


    def _get_expand_instances(self):
        return self._expand_instances

    def _set_expand_instances(self, bool):
        self._expand_instances = bool

    expandInstances = property(_get_expand_instances, _set_expand_instances)



doc = proofDocument()

doc.add_object("/Users/connordavenport/Dropbox/Clients/Dinamo/03_DifferentTimes/Sources/Different-Times-v10.designspace")
doc.crop_space("wght=0:320:600")

for font in doc.fonts:

    print(font)
    # for s in font.instances[-5:-1]:
        # print(s.name)
        # print(s.location)
        # print(s.in_crop)

doc.new_section()


doc.caption_font = "ABCGaisyrMonoUnlicensedTrial-Regular"
doc.margin = "auto"

print(doc.path)
print(doc.margin)

# test invalid sizes
# doc.size = (100,100,20)
# doc.size = "big paper size"

# test valid size
doc.size = "A4Landscape"



