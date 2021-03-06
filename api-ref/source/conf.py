# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# designer_family-api-ref documentation build configuration file, created by
# sphinx-quickstart on Sat May  1 15:17:47 2010.
#
# This file is execfile()d with the current directory set to
# its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import os
import sys

import pbr.version

version_info = pbr.version.VersionInfo('designer_family')

sys.path.insert(0, os.path.abspath('../'))

extensions = [
    'openstackdocstheme',
    'os_api_ref',
    'ext.validator',
]

# -- General configuration ----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Placement API Reference'
copyright = u'2010-present, OpenStack Foundation'

# openstackdocstheme options
repository_name = 'openstack/designer_family'
use_storyboard = True

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The full version, including alpha/beta/rc tags.
release = version_info.release_string()
# The short X.Y version.
version = version_info.version_string()

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = 'openstackdocs'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "sidebar_mode": "toc",
}

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%Y-%m-%d %H:%M'

# -- Options for LaTeX output -------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
latex_documents = [
    ('index', 'Placement.tex', u'OpenStack Placement API Documentation',
     u'OpenStack Foundation', 'manual'),
]

# -- Options for openstackdocstheme -------------------------------------------

openstack_projects = [
    'designer_family',
]
