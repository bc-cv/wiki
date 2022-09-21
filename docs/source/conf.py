import datetime
import sphinx_rtd_theme
import doctest

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx_rtd_theme',
]

source_suffix = '.rst'
master_doc = 'index'

author = 'BCCV, Boston College'
project = 'Intern-Wiki'
copyright = '{}, {}'.format(datetime.datetime.now().year, author)

#version = 'master (2019.04.06)'
#release = 'master'

html_theme = 'sphinx_rtd_theme'
# html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

doctest_default_flags = doctest.NORMALIZE_WHITESPACE
intersphinx_mapping = {'python': ('https://docs.python.org/', None)}

html_theme_options = {
    'collapse_navigation': False,
    'display_version': True,
    'logo_only': True,
}

html_logo = '_static/img/vcg-logo_100.jpg'
html_static_path = ['_static']

add_module_names = False


def setup(app):
    def skip(app, what, name, obj, skip, options):
        members = [
            '__init__',
            '__repr__',
            '__weakref__',
            '__dict__',
            '__module__',
        ]
        return True if name in members else skip

    app.add_css_file('_static/css/custom.css')
    app.connect('autodoc-skip-member', skip)
