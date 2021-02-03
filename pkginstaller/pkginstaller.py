
from coolutils.json_plus import read_json

DEFAULT_CONFIG = {
    "metadata": {
        "name": "template", 
        "main_file": "main.py" 
    },
    "path": {
        "library_path": "../lib/",
        "bin_path": "../bin/",
        "dist_path": "../dist/"
    },
    "install": {
        "dir_pack": False, 
        "install_dir": ""
    },
    "data": {
        "files": [],
        "dirs": []
    }
}

read_json('cfg.json')