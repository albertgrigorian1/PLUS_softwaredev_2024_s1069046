from setuptools import setup

APP = ['bewerber_pdfs.py']  # Name des Hauptskripts
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,  # Ermöglicht das Übergeben von Befehlszeilenargumenten
    'packages': ['img2pdf', 'pandas', 'openpyxl'],  # Benötigte Pakete
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)