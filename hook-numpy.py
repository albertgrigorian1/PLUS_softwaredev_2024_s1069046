# hook-numpy.py
from PyInstaller.utils.hooks import collect_data_files

# Sammle alle notwendigen Daten von numpy
datas = collect_data_files('numpy')
