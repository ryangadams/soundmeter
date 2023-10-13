from setuptools import setup

APP = ["app.py"]  # main file of your app
DATA_FILES = []
OPTIONS = {
    "argv_emulation": True,
    "site_packages": True,
    "iconfile": "icon.icns",  # if you want to add some ico
    "plist": {
        "CFBundleName": "Sound Monitor",
        "CFBundleShortVersionString": "1.0.0",  # must be in X.X.X format
        "CFBundleVersion": "1.0.0",
        "CFBundleIdentifier": "uk.me.rga.soundmonitor",  # optional
        "NSHumanReadableCopyright": "@ Ryan Adams 2021",  # optional
        "CFBundleDevelopmentRegion": "English",  # optional - English is default
    },
}
setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
