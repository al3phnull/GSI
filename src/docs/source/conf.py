# -*- coding: utf-8 -*-
#
# Django RPC documentation build configuration file, created by
# sphinx-quickstart on Mon Aug  6 13:02:10 2012.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os

# documentation root, use os.path.abspath to make it absolute, like shown here

sys.path.append(sys.path.insert(0, os.path.abspath('../../')))

sys.path.insert(0, os.path.abspath('../../../eggs/django_solo-1.1.2-py2.7.egg'))
sys.path.insert(0, os.path.abspath('../../../eggs/python_magic-0.4.11-py2.7.egg'))
sys.path.insert(0, os.path.abspath('../../../eggs/Django-1.8-py2.7.egg/django/core/management'))
sys.path.insert(0, os.path.abspath('../../../eggs/django_annoying-0.10.3-py2.7.egg'))

from django.conf import settings
settings.configure()

from gsi import settings
# from gsi.settings import BASE_DIR

os.environ['DJANGO_SETTINGS_MODULE'] = 'gsi.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gsi.settings')


# sys.path.append(sys.path.insert(0, os.path.abspath('../../')))
# sys.path.append(sys.path.insert(0, os.path.abspath('../../../eggs/')))

# sys.path.append(sys.path.insert(0, os.path.abspath('.')))
# sys.path.append(sys.path.insert(0, os.path.abspath('../')))
# sys.path.append(sys.path.insert(0, os.path.abspath('../../')))
# sys.path.append(sys.path.insert(0, os.path.abspath('../../../src/')))

# sys.path.insert(0, os.path.abspath("../../"))
# sys.path.append(sys.path.insert(0, os.path.abspath('../../../eggs/')))





# sys.path.insert(0, os.path.abspath('../../../eggs/django_solo-1.1.2-py2.7.egg'))
# sys.path.insert(0, os.path.abspath('../../../eggs/python_magic-0.4.11-py2.7.egg'))
# sys.path.insert(0, os.path.abspath('../../../eggs/Django-1.8-py2.7.egg/django/core/management'))
# sys.path.insert(0, os.path.abspath('../../../eggs/django_annoying-0.10.3-py2.7.egg'))




# sys.path.insert(0, os.path.abspath('../../core'))
# sys.path.insert(0, os.path.abspath('../../../eggs/python_magic-0.4.11-py2.7.egg'))
# sys.path.insert(0, os.path.abspath('../../../eggs/Django-1.8-py2.7.egg/django/core/management'))
# sys.path.insert(0, os.path.abspath('../../../eggs/django_annoying-0.10.3-py2.7.egg'))

# sys.path.insert(0, '/data/work/virtualenvs/gsi/src/GSI/eggs/django_solo-1.1.2-py2.7.egg')
# sys.path.insert(0, '/data/work/virtualenvs/gsi/src/GSI/eggs/python_magic-0.4.11-py2.7.egg')
# sys.path.insert(0, '/data/work/virtualenvs/gsi/src/GSI/eggs/Django-1.8-py2.7.egg/django/core/management')
# sys.path.insert(0, '/data/work/virtualenvs/gsi/src/GSI/eggs/django_annoying-0.10.3-py2.7.egg')

# from django.conf import settings
# settings.configure()
#
# from gsi.settings import BASE_DIR
#
# os.environ['DJANGO_SETTINGS_MODULE'] = 'gsi.settings'
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gsi.settings")



# print 'path =================== ',  os.path.abspath('../../../eggs/')




# setup Django
# import gsi.settings
# from django.core.management import setup_environ
# setup_environ(gsi.settings)

# -------------------------------------------------------------------------------------------



# def rel(*x):
#     path = os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
#     return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
#
# # sys.path.insert(0, rel('/../../../eggs/Django-1.8-py2.7.egg/django'))
# sys.path.insert(0, rel('/../../gsi/'))
# # sys.path.insert(0, rel('/../../core/'))
# sys.path.insert(0, rel('../../'))
# # sys.path.insert(0, rel('../../../GSI'))
#
#
# # sys.path.insert(0, '/data/work/virtualenvs/gsi')
# # sys.path.insert(0, '/data/work/virtualenvs/gsi/src/GSI/src')
# #
# # sys.path.insert(0, '/data/work/virtualenvs/gsi/src/GSI/eggs/django_solo-1.1.2-py2.7.egg')
# #
# #
# # sys.path.insert(0, '/data/work/virtualenvs/gsi/src/GSI/eggs/Django-1.8-py2.7.egg/django/')
# #
# # sys.path.insert(0, '/data/work/virtualenvs/gsi/lib/python2.7/site-packages/django')
# # sys.path.insert(0, '/data/work/virtualenvs/gsi/lib/python2.7/site-packages/django/contrib/')
# sys.path.insert(0, '/data/work/virtualenvs/gsi/src/GSI/src/gsi/')
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gsi.settings")
#
#
#
#
# sys.path.append('/data/work/virtualenvs/gsi/src/GSI/eggs/django_solo-1.1.2-py2.7.egg')
# sys.path.append('/data/work/virtualenvs/gsi/src/GSI/eggs/python_magic-0.4.11-py2.7.egg')
# sys.path.append('/data/work/virtualenvs/gsi/src/GSI/eggs/django_annoying-0.10.3-py2.7.egg')
# sys.path.append('/data/work/virtualenvs/gsi/src/GSI/eggs/Django-1.8-py2.7.egg/django/contrib/contenttypes/')
#
# # added new path
#
# # sys.path.append('/data/work/virtualenvs/gsi')
# # sys.path.append('/data/work/virtualenvs/gsi/src/GSI/src')
#
# # sys.path.append('/data/work/virtualenvs/gsi/src/GSI/eggs/django_solo-1.1.2-py2.7.egg')
# # sys.path.append('/data/work/virtualenvs/gsi/src/GSI/eggs/python_magic-0.4.11-py2.7.egg')
# # sys.path.append('/data/work/virtualenvs/gsi/src/GSI/eggs/django_annoying-0.10.3-py2.7.egg')
# # sys.path.append('/data/work/virtualenvs/gsi/src/GSI/eggs/Django-1.8-py2.7.egg/django/')
#
# sys.path.append('/data/work/virtualenvs/gsi/lib/python2.7/site-packages/django')
# sys.path.append('/data/work/virtualenvs/gsi/lib/python2.7/site-packages/django/contrib/')
# sys.path.append('/data/work/virtualenvs/gsi/lib/python2.7/site-packages/django/contrib/auth/')
#
# print 'path =================== ',  sys.path


# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------
# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.intersphinx', 'sphinx.ext.todo', 'sphinx.ext.coverage', 'sphinx.ext.viewcode']

# extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.intersphinx', 'sphinx.ext.todo', 'sphinx.ext.coverage', 'sphinx.ext.imgmath', 'sphinx.ext.viewcode']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'GSi'
copyright = u'2016, GSi'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '1.0'
# The full version, including alpha/beta/rc tags.
release = '1.0'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'nature'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'DjangoRPCdoc'


# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'GSi.tex', u'GSi Documentation',
   u'GSi', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'djangorpc', u'Django RPC Documentation',
     [u'Dmitriy Kostochko'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'DjangoRPC', u'Django RPC Documentation',
   u'Dmitriy Kostochko', 'DjangoRPC', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

autoclass_content = 'init'
