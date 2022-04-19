from setuptools import setup

APP = ['main.py']
DATA_FILES = ['icon.png', 'spotify.png', 'music.png']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleShortVersionString': '0.1.0',
        'LSUIElement': True,
    },
    'packages': ['rumps','requests', 'json', 'pypresence', 'subprocess'],
}

setup(
    app=APP,
    name='Glance',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], 
install_requires=['rumps','requests', 'pypresence',]
)
