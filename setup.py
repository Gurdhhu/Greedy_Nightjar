from cx_Freeze import setup, Executable
import sys

# to build an installer run command:
# python setup.py bdist_msi

base = None
if sys.platform == "win32":
    base = "Win32GUI"

files_to_include = ["./Sound/", "./Pics"]

executables = [Executable(script="Greedy_Nightjar.py", base=base, icon="icon.ico")]
build_exe_options = {"packages":["pygame", "random"],
                           "include_files":files_to_include}

setup(
    name="Greedy_Nightjar",
    version="2.0",
    description="A simple game: Greedy Nightjar is eating moths and escaping from the Owl's claws.",
    options={"build_exe": build_exe_options},
    executables=executables)