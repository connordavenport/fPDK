from fontTools.ttLib import TTFont
import os
from fontTools.designspaceLib import DesignSpaceDocument as dsp_doc
import fontTools.varLib as varLib
from fontTools.misc.fixedTools import otRound, strToFixedToFloat, floatToFixedToFloat
import fnmatch
from typing import Union
import re

# API
# Assisted Proofing Interface


PROOF_SECTION_TYPES = [
"core",
"spacing",
"figures",
"lowercaseCopy",
"uppercaseCopy",
"paragraph",
"kerning"
]


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

        self.identifier = 1234567898
        self.fonts = []
        # size can either be a tuple of ints or a DrawBot
        # compatible paper size name string
        self.size = "LetterLandscape"
        self.operator = None
        self.crop = ""
        self._expand_instances = False

        self._path = None

        # proof UI settings
        self._margin = 10

        self._margin_left   = self._margin
        self._margin_right  = self._margin
        self._margin_top    = self._margin
        self._margin_bottom = self._margin


    def _set_path(self, new_path):
        self._path = new_path

    def _get_path(self):
        return self._path

    path = property(_get_path, _set_path)

    def save(self, path=None):
        pass

    def new_section(self,
                    proof_type=None,
                    sources=True,
                    instances=False,
                    ):
        pass

    def _get_margin_left(self):
        return self._margin_left

    def _set_margin_left(self, new_margin_left):
        self._margin_left = new_margin_left

    margin_left = property(_get_margin_left, _set_margin_left)

    def _get_margin_right(self):
        return self._margin_right

    def _set_margin_right(self, new_margin_right):
        self._margin_right = new_margin_right

    margin_right = property(_get_margin_right, _set_margin_right)

    def _get_margin_top(self):
        return self._margin_top

    def _set_margin_top(self, new_margin_top):
        self._margin_top = new_margin_top

    margin_top = property(_get_margin_top, _set_margin_top)

    def _get_margin_bottom(self):
        return self._margin_bottom

    def _set_margin_bottom(self, new_margin_bottom):
        self._margin_bottom = new_margin_bottom

    margin_bottom = property(_get_margin_bottom, _set_margin_bottom)


    def _get_margin(self):
        return self._margin

    def _set_margin(self, new_margin):
        # if we set the main margin, we also reset all margins
        self._margin        = new_margin
        self._margin_left   = new_margin
        self._margin_right  = new_margin
        self._margin_top    = new_margin
        self._margin_bottom = new_margin

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

#allows you to crop the 
doc.crop_space("wght=0:320:600")


for font in doc.fonts:
    for s in font.instances[-5:-1]:
        print(s.name)
        print(s.location)
        print(s.in_crop)

doc.new_section()



