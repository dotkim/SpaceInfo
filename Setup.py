from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == 'win32':
    base = None


executables = [Executable("SpaceInfo.py", base=base)]

packages = ["wmi"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "SpaceInfo",
    options = options,
    version = "1",
    description = 'test',
    executables = executables
)
