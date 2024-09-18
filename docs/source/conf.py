# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Data Pipeline'
copyright = '2024, Sacha Renault'
author = 'Sacha Renault'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import sphinx_rtd_theme

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.mathjax',   # If you need math support
]

# Use the Read the Docs theme
html_theme = 'sphinx_rtd_theme'

# Include the RTD theme path (this shouldn't be necessary, but it's a safeguard)
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

templates_path = ['_templates']
exclude_patterns = []

autodoc_default_options = {
    'members': True,
    'special-members': '__call__, __getitem__',
    'undoc-members': True,
    'private-members': True,
    'inherited-members': True,
    'show-inheritance': True,
}



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']
html_css_files = ['custom.css']
