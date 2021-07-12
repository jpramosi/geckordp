# pylint: skip-file
# todo ugly
import sys
import subprocess
import os
import shutil
from pathlib import Path
import sphinx_rtd_theme


# generation parameters
project = "geckordp"
copyright = "2021, reapler"
author = "reapler"
PROJECT_PATH = Path().absolute().parent.parent
#raise RuntimeError(PROJECT_PATH)
PROJECT_NAME = str(PROJECT_PATH.stem)
SOURCE_PATH = PROJECT_PATH.joinpath(PROJECT_NAME)
DOCUMENTATION_HTML = PROJECT_PATH.joinpath("docs")
DOCUMENTATION_SOURCE = PROJECT_PATH.joinpath("docs").joinpath("src")
DOCUMENTATION_BUILD = PROJECT_PATH.joinpath("docs").joinpath("build")


# exclude documentation files
exclude_source = [
    "actor.rst",
    "actors.rst",
    "actors.addon.rst",
    "actors.descriptors.rst",
    "actors.targets.rst",
    "addon.rst",
    "descriptors.rst",
    "targets.rst",
    "modules.rst",
]


# element mapping:
# (documentation path, source path)
doc_from_source = [
    ("", SOURCE_PATH),
    ("actors", SOURCE_PATH.joinpath("actors")),
    ("actors", SOURCE_PATH.joinpath("actors").joinpath("addon")),
    ("actors", SOURCE_PATH.joinpath("actors").joinpath("descriptors")),
    ("actors", SOURCE_PATH.joinpath("actors").joinpath("targets")),
]


# add python source to path and generate
# documentation for the specified directory
sys.path.insert(0, str(PROJECT_PATH))
for ds in doc_from_source:
    sys.path.insert(0, str(ds[1]))
    popen = subprocess.Popen([
        "sphinx-apidoc",
        "--separate",
        "--force",
        "-o",
        str(DOCUMENTATION_BUILD.joinpath(ds[0])),
        str(ds[1])
    ],
        universal_newlines=True,
        shell=False)
    popen.wait()


# set template for actor index
ACTORS_MODULES_RST = """actors
======

.. toctree::
   :maxdepth: 4

"""
# find all actors in documentation and append to actor index buffer
actor_list = []
for subdir, _dirs, files in os.walk(DOCUMENTATION_BUILD.joinpath("actors")):
    for file in files:
        if (file in exclude_source or not file.startswith("actors.")):
            continue
        actor_list.append(f"   {Path(file).stem}\n")
actor_list.sort()
for a in actor_list:
    ACTORS_MODULES_RST += a
# append diagram
ACTORS_MODULES_RST += f"\n.. image:: /../actor-hierarchy.png\n"
# write buffer to file
with open(DOCUMENTATION_BUILD.joinpath("actors").joinpath("modules.rst"), "w") as f:
    f.write(ACTORS_MODULES_RST)


# set template for index
INDEX = """
## Modules
```{eval-rst}
============================
```

```{eval-rst}

.. toctree::
   :maxdepth: 2

   geckordp.rdp_client.rst
   geckordp.profile.rst
   geckordp.firefox.rst
   geckordp.settings.rst
   geckordp.utils.rst
   actors/modules.rst

.. toctree::
   :maxdepth: 2
   :hidden:

   examples/modules.rst
```
"""
# set template separator line
SEPARATOR_LINE = """```{eval-rst}
============================
```
"""
# replace tags with templates
INDEX_MD = ""
with open(PROJECT_PATH.joinpath("README.md"), "r") as f:
    INDEX_MD = f.read()
    INDEX_MD = (INDEX_MD
                .replace("<!-- CLASS_INDEX -->", INDEX)
                .replace("<!-- SEPARATOR -->", SEPARATOR_LINE))
# write index buffer to file
with open(DOCUMENTATION_BUILD.joinpath("index.md"), "w") as f:
    f.write(INDEX_MD)


# set template for examples index
EXAMPLES_MODULES_RST = """examples
============================

.. toctree::
   :maxdepth: 4

"""
# set template for single example files
EXAMPLE = """
{}.py
============================

.. code-block:: python
   :caption: {}.py

{}
"""
# create example directory in documentation
Path(DOCUMENTATION_BUILD.joinpath("examples")).mkdir(exist_ok=True)
# foreach example create a file and append to example index
for subdir, _dirs, files in os.walk(PROJECT_PATH.joinpath("examples")):
    for file in files:
        if ("__init__" in str(file)):
            continue

        # read and format code
        code = ""
        with open(os.path.join(subdir, file), "r") as f:
            code = f.read()
        code = "   " + code.replace("\n", "\n   ")

        # append example file to index
        name = Path(file).stem
        EXAMPLES_MODULES_RST += f"   {name}\n"

        # write example file as documentation .rst
        with open(DOCUMENTATION_BUILD.joinpath("examples").joinpath(name+".rst"), "w") as f:
            f.write(EXAMPLE.format(name, name, code))
# write example index buffer to file
with open(DOCUMENTATION_BUILD.joinpath("examples").joinpath("modules.rst"), "w") as f:
    f.write(EXAMPLES_MODULES_RST)


extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = "sphinx_rtd_theme"


def setup(app):
    # copy css
    try:
        src = DOCUMENTATION_SOURCE.joinpath("default.css")
        dest = DOCUMENTATION_HTML.joinpath(
            "_static").joinpath("default.css")
        dest.parent.mkdir(exist_ok=True)
        shutil.copyfile(src, dest)
    except Exception as ex:
        print(ex)
    # copy diagram
    try:
        src = PROJECT_PATH.joinpath("actor-hierarchy-t.png")
        dest = DOCUMENTATION_HTML.joinpath("actor-hierarchy.png")
        shutil.copyfile(src, dest)
    except Exception as ex:
        print(ex)
    app.add_css_file("default.css")
