
from setuptools import setup

setup( 
    name = "Panda Game",
    options = {
        "build_apps": {
            "include_patterns": [
                "**/*.png",
                "**/*.ogg",
                "**/*.txt",
                "**/*.egg",
                "fonts/*"
            ],
            "gui_apps": {
                "Panda Game": "Game.py",
            },
            "plugins": [
                "pandagl",
                "p3openal_audio",
            ],
            "platforms": [
                "manylinux1_x86_64",
                "macosx_10_6_x86_64",
                "win_amd64",
            ],
            "log_filename": "$USER_APPDATA/PandaGame/output.log",
            "log_append": False,
        }
    }
)


