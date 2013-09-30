from distutils.core import setup
import py2exe

py2exe_options = {
        "includes":["sip",],
        }

setup(windows=["md.pyw"], options={'py2exe':py2exe_options})
