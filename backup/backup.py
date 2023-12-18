import os
import sys
import json
from pathlib import Path
import configparser
import shutil

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    backupables = {}
    for section in config.sections():
        item = section
        source_path = config.get(section, "source")
        dest_paths = json.loads(config.get(section,"destinations"))
        backupables[item] = {
            "source_path":source_path,
            "destinations":dest_paths
        }
    return backupables

def main(backupables):
    fails = []
    for backup in backupables:
        backup = backupables[backup]
        source = backup["source_path"]
        if os.path.isfile(source):
            for dest in backup["destinations"]:
                if os.path.isdir(dest):
                    shutil.copy2(source, dest)
                else:
                    fails.append(f"Could not find dest: {dest} (source = {source})")
        else:
            fails.append(f"Could not find source: {source}")
    return fails

if __name__ == '__main__':
    config_path = Path(os.path.dirname(os.path.abspath(sys.argv[0]))).parent.absolute().joinpath("data/backup.ini")
    backupables = read_config(config_path)
    fails = main(backupables)
    if fails:
        for f in fails:
            print(f)

