
font Proofing Development Kit
=============================

<p align="center">
<img src="assets/images/fpdk_logo_light.png" alt="fPDK Logo" width="300">
</p>

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Support](#support)
- [Contributing](#contributing)

## Installation

Download to your project directory, add `README.md`, and commit:


## Usage

```python
from fPDK import proofDocument

doc = proofDocument()

doc.load("path/to/old.proof") # load old settings

"""
add a font or designspace, only accepts path strings
    should it accept designspace objects? ufos?
"""
doc.add_object("path/to/project.designspace")

"""
crop design-space to be proofed
using the varLib instantiator syntax
values are in user-values
can also user `doc.crop = ` syntax
"""
doc.crop_space("wght=300:700 slnt=0")

"""
test [in]valid sizes
doc.size = (100,100,20)
doc.size = "big paper size"
"""
doc.size = "LetterLandscape"

"""
we can see the loaded fonts and their locations
"""
for font in doc.fonts:
    print(font)
    for s in font.locations[2:5]:
        print(s.name)
        print(s.is_source)
        print(s.in_crop)

"""
set font used in captions
"""
doc.caption_font = "Menlo-Regular"

"""
auto will use some %s but can accept 1 int which will apply
to all or a tuple of 4 values in top, left, bottom, right order
"""
doc.margin = "auto"
doc.margin = (40,30,30,50)

"""
we can turn this on and off any setter between new sections
"""

"""
the fPDK will use not use instances in .designspace projects
unless turned on. If a dsp is given, it will use the sources to 
proof (we need to proof sources more than instances, right?) 
"""
doc.use_instances = True

doc.setup_proof() # setup newDrawing() and make a cover page

doc.new_section("core") # there are several custom presets for proof pages
doc.new_section(
                "paragraph",
                # can be one value or a list of multiple ints
                # if there are multiple values with `multi_size_page` == False
                # there will be one page for each point size
                point_size=[12,20],

                multi_size_page=True # if True and multiple point sizes, adds multi-column page with no overflow
               )

doc.open_automatically = False
"""
kwargs inside of save/write overwrite whatever the doc says.
path = compiles name for current file, will override if declared
open = by default is `False`, open in Preview
overwrite = save over older proofs, default is `True`. `False` will append + "1" until path is unique
"""
doc.save(open=True)

doc.write(overwrite=False) # save current project as custom `.proof` file for later use


```

## Support

Please [open an issue](https://github.com/connordavenport/fPDK/issues/new) for support.
This is a personal project and I have limited time so there are no promises that updates will be made in a timely manner.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/fraction/readme-boilerplate/compare/).


