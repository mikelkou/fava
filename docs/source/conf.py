# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "extensions"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "favapy"
copyright = "2023, Mikaela Koutrouli"
author = "Mikaela Koutrouli"
version = "0.3.9"
release = "0.3.9.4"

source_suffix = {
    ".rst": "restructuredtext",
    ".ipynb": "myst-nb",
    ".myst": "myst-nb",
}

# autodoc
autosummary_generate = True
autodoc_member_order = "groupwise"
default_role = "literal"
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_use_rtype = True  # having a separate entry generally helps readability
napoleon_use_param = True
# myst
myst_heading_anchors = 3  # create anchors for h1-h6
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "dollarmath",
]
myst_url_schemes = ("http", "https", "mailto")
nb_output_stderr = "remove"
nb_execution_mode = "off"
nb_merge_streams = True
pygments_style = "default"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = [
#    "sphinx.ext.autodoc",
#    "sphinx.ext.napoleon",
#    "nbsphinx",
# ]

extensions = [
    "sphinx.ext.napoleon",
    "myst_nb",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinxcontrib.bibtex",
    "sphinx_autodoc_typehints",
    "sphinx.ext.mathjax",
    *[p.stem for p in (HERE / "extensions").glob("*.py")],
]


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_logo = "_static/Fava_logo.png"
html_title = project + " version " + release
html_theme_options = {
    "navigation_with_keys": True,
    "collapse_navigation": False,
}
