import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

from ec3 import __version__ as version

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "EC3 Python Wrapper"
copyright = "2024, Jared Friedman"
author = "Jared Friedman"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# Auto Create Api Reference
autoapi_dirs = ["../ec3"]
autoapi_add_toctree_entry = True
autoapi_options = [
    "members",
    "undoc-members",
    "private-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_logo = "ec3_wrapper_logo.svg"
html_theme_options = {
    'logo_only': True,
    'display_version': False
}

html_css_files = ["custom.css"]

# -- Options for EPUB output
epub_show_urls = "footnote"


################################
# CUSTOM
################################
napoleon_google_docstring = True
napoleon_include_init_with_doc = True
napoleon_attr_annotations = True


__version__ = version.split("-", 0)
__release__ = version
