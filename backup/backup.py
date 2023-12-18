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
        source_path = config.get(section, "source")
        item_type = config.get(section, "type")
        dest_paths = json.loads(config.get(section, "destinations"))
        backupables[section] = {
            "source_path": source_path,
            "destinations": dest_paths,
            "item_type": item_type
        }
    return backupables

def backup_item(source, dest, item_type):
    if os.path.isdir(dest):
        if item_type == "file":
            shutil.copy2(source, dest)
        elif item_type == "folder":
            shutil.copytree(source, dest)
    else:
        return f"Could not find dest: {dest} (source = {source})"

def main(backupables):
    fails = []
    for name, backup in backupables.items():
        source = backup["source_path"]
        item_type = backup["item_type"]
        if os.path.exists(source):
            for dest in backup["destinations"]:
                fail_message = backup_item(source, dest, item_type)
                if fail_message:
                    fails.append(fail_message)
        else:
            fails.append(f"Could not find source: {source}")
    return fails

if __name__ == '__main__':
    script_dir = Path(__file__).resolve().parent
    config_path = script_dir.joinpath("data/backup.ini")
    backupables = read_config(config_path)
    fails = main(backupables)
    for fail in fails:
        print(fail)
