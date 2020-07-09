import os
from pyprobar.utils import rm

rm('dist')
os.system("yapf -i -r ./pyprobar")
os.system("pip uninstall pyprobar -y && python setup.py install")
rm('pyprobar.egg-info')
rm('build')
